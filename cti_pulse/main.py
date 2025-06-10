import streamlit as st
import time
from datetime import datetime
from components.ui_components import UIComponents
from components.ai_assistant import AIAssistant
from components.visualizations import ThreatVisualizations
from components.threat_analysis import ThreatAnalysis
from utils.threat_processor import ThreatProcessor
from utils.api_client import APIClient
from utils.nltk_setup import initialize_nltk
from config.settings import CYBER_THREATS
from assets.styles import load_custom_css

# Configure page
st.set_page_config(
    page_title="CyberPulse - Real-Time Threat Intelligence",
    page_icon="🔒",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load custom CSS
load_custom_css()

# Initialize NLTK
initialize_nltk()

# Initialize components
ui = UIComponents()
ai_assistant = AIAssistant()
visualizations = ThreatVisualizations()
threat_analysis = ThreatAnalysis()
threat_processor = ThreatProcessor()
api_client = APIClient()


def main():
    # Render header
    ui.render_header()

    # AI Assistant Section
    ai_results = ai_assistant.render_chat_interface()

    # Sidebar controls
    sidebar_config = ui.render_sidebar()

    # Process AI query if provided
    if ai_results['should_process']:
        process_ai_query(ai_results)

    # Manual dashboard processing
    elif sidebar_config['should_process']:
        process_manual_query(sidebar_config)

    # Display results if available
    if hasattr(st.session_state, 'threat_data'):
        query_info = f" (from query: '{st.session_state.query_used}')" if hasattr(st.session_state,
                                                                                  'query_used') else ""
        st.info(f"📊 Showing cached data from {st.session_state.last_update.strftime('%H:%M:%S')}{query_info}")
        display_dashboard()
    else:
        ui.render_welcome_screen()


def process_ai_query(ai_results):
    """Process AI assistant query"""
    with st.spinner("🧠 Analyzing your query..."):
        matched_threats = threat_processor.extract_cybersecurity_terms(ai_results['query'])

        if matched_threats:
            ui.display_ai_response(matched_threats, ai_results['settings'])
            if fetch_threat_intelligence(matched_threats, ai_results['settings']):
                st.session_state.query_used = f"{ai_results['query']} (AI: severity≥{ai_results['settings']['severity_filter']}, {ai_results['settings']['articles_per_threat']} articles)"
                st.success(
                    f"🎉 Analysis complete! Found intelligence for {len(st.session_state.threat_data)} threat types.")
        else:
            ui.display_no_threats_message()


def process_manual_query(config):
    """Process manual dashboard query"""
    if not config['selected_threats']:
        st.warning("⚠️ Please select at least one threat type to monitor or use the AI assistant above.")
        return

    if fetch_threat_intelligence(config['selected_threats'], config):
        st.session_state.query_used = "Manual Selection"
        st.success(f"🎉 Successfully gathered intelligence for {len(st.session_state.threat_data)} threat types!")


def fetch_threat_intelligence(threats, settings):
    """Fetch and process threat intelligence data with progress tracking"""
    st.write("🚀 Starting threat intelligence gathering...")
    all_threat_data = {}

    # Create columns for live updates
    col1, col2 = st.columns([3, 1])

    with col1:
        progress_bar = st.progress(0)
        status_container = st.container()

    # Process each threat
    for i, threat in enumerate(threats[:5]):  # Limit to top 5
        with status_container:
            st.write(f"🔍 Processing: **{threat}**")

        # Add small delay between requests
        if i > 0:
            time.sleep(1)

        data = api_client.get_threat_data(threat, settings['articles_per_threat'])

        if data and 'results' in data:
            analysis = threat_processor.analyze_threat_sentiment(data, threat)
            filtered_analysis = [a for a in analysis if a['threat_score'] >= settings['severity_filter']]

            all_threat_data[threat] = {
                'raw_data': data,
                'analysis': filtered_analysis,
                'article_count': len(filtered_analysis)
            }

            with status_container:
                st.success(
                    f"✅ **{threat}**: Found {len(filtered_analysis)} articles (severity >= {settings['severity_filter']})")
        else:
            with status_container:
                st.error(f"❌ **{threat}**: No data found")

        progress_bar.progress((i + 1) / len(threats[:5]))

    # Clear status
    status_container.empty()
    progress_bar.empty()

    if all_threat_data:
        st.session_state.threat_data = all_threat_data
        st.session_state.last_update = datetime.now()
        return True
    else:
        st.error("❌ No threat data could be retrieved. Please check API connection.")
        return False


def display_dashboard():
    """Display the main dashboard with all components"""
    if not hasattr(st.session_state, 'threat_data'):
        return

    all_threat_data = st.session_state.threat_data

    # Executive Summary
    ui.render_executive_summary(all_threat_data)

    # Key Metrics
    ui.render_key_metrics(all_threat_data)

    # Visualizations
    visualizations.render_threat_charts(all_threat_data)

    # Critical Alerts
    ui.render_critical_alerts(all_threat_data)

    # Detailed Analysis
    threat_analysis.render_detailed_analysis(all_threat_data)


if __name__ == "__main__":
    main()
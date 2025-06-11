import streamlit as st
import numpy as np
from datetime import datetime
from assets.templates import *
from assets.styles import get_severity_color_class, get_severity_emoji
from config.settings import CYBER_THREATS
from utils.data_processor import generate_executive_summary

class UIComponents:
    """UI Components for the CyberPulse application"""

    def render_header(self):
        """Render the main application header"""
        st.markdown(get_header_template(), unsafe_allow_html=True)

    def render_sidebar(self):
        """Render sidebar controls and return configuration"""
        st.sidebar.header("⚙️ Dashboard Controls")
        st.sidebar.markdown("*Configure your threat monitoring:*")

        # Manual threat selection
        selected_threats = st.sidebar.multiselect(
            "🎯 Monitor Threats:",
            list(CYBER_THREATS.keys()),
            default=[]
        )

        # Settings
        severity_filter = st.sidebar.slider("🚨 Minimum Severity", 1, 10, 3)
        articles_per_threat = st.sidebar.slider("📄 Articles per threat", 5, 100, 15)

        # Buttons
        fetch_button = st.sidebar.button("🔍 Fetch Intelligence", type="primary")
        test_api_button = st.sidebar.button("🔧 Test API Connection")

        # Handle API test
        if test_api_button:
            self._test_api_connection()

        return {
            'selected_threats': selected_threats,
            'severity_filter': severity_filter,
            'articles_per_threat': articles_per_threat,
            'should_process': fetch_button
        }

    def _test_api_connection(self):
        """Test API connection"""
        from utils.api_client import APIClient

        st.sidebar.write("Testing API connection...")
        api_client = APIClient()
        test_data = api_client.get_threat_data("cyber attack", 5)

        if test_data:
            st.sidebar.success("✅ API connection successful!")
            st.sidebar.write(f"Found {len(test_data.get('results', []))} results")
        else:
            st.sidebar.error("❌ API connection failed")

    def render_executive_summary(self, all_threat_data):
        """Render executive summary"""
        summary_data = generate_executive_summary(all_threat_data)

        threat_level_emoji = "🔴 CRITICAL" if summary_data['high_severity'] > 5 else \
            "🟡 ELEVATED" if summary_data['high_severity'] > 0 else "🟢 NORMAL"

        st.markdown(get_executive_summary_template(
            threat_level_emoji,
            summary_data['total_threats'],
            summary_data['high_severity'],
            summary_data['top_threat'],
            summary_data['avg_sentiment']
        ), unsafe_allow_html=True)

    def render_key_metrics(self, all_threat_data):
        """Render key metrics cards"""
        all_articles = [article for data in all_threat_data.values() for article in data['analysis']]

        total_articles = sum(data['article_count'] for data in all_threat_data.values())
        high_severity_count = sum(1 for article in all_articles if article['threat_score'] >= 7)
        avg_score = np.mean([a['threat_score'] for a in all_articles]) if all_articles else 0

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.markdown(get_metric_card_template(total_articles, "Total Threats", "📊"), unsafe_allow_html=True)
        with col2:
            st.markdown(get_metric_card_template(high_severity_count, "Critical Alerts", "🔴"), unsafe_allow_html=True)
        with col3:
            st.markdown(get_metric_card_template(f"{avg_score:.1f}/10", "Avg Severity", "📈"), unsafe_allow_html=True)
        with col4:
            if hasattr(st.session_state, 'last_update'):
                time_str = st.session_state.last_update.strftime("%H:%M:%S")
                st.markdown(get_metric_card_template(time_str, "Last Updated", "🕐"), unsafe_allow_html=True)

    def render_critical_alerts(self, all_threat_data):
        """Render critical threat alerts"""
        st.header("🚨 Critical Threat Alerts")

        all_articles = [article for data in all_threat_data.values() for article in data['analysis']]
        critical_threats = [a for a in all_articles if a['threat_score'] >= 7]

        if critical_threats:
            for threat in critical_threats[:5]:  # Show top 5 critical
                severity_class = get_severity_color_class(threat['threat_score'])
                emoji = get_severity_emoji(threat['threat_score'])

                # Format date
                formatted_date = self._format_date(threat['published_date'])

                st.markdown(get_alert_card_template(
                    threat['title'],
                    f"{threat['threat_score']:.1f}",
                    threat['category'],
                    threat['source'],
                    threat['summary'],
                    formatted_date,
                    severity_class,
                    emoji
                ), unsafe_allow_html=True)
        else:
            st.info("🟢 No critical threats detected at current severity threshold.")

    def render_welcome_screen(self):
        """Render welcome screen when no data is available"""
        st.markdown(get_welcome_screen_template(), unsafe_allow_html=True)

    def display_ai_response(self, matched_threats, settings):
        """Display AI assistant response"""
        threat_list = ", ".join([threat.title() for threat in matched_threats[:3]])

        st.markdown(get_ai_response_template(
            len(matched_threats),
            threat_list,
            settings
        ), unsafe_allow_html=True)

    def display_no_threats_message(self):
        """Display message when no threats are found"""
        st.markdown(get_no_threats_message_template(), unsafe_allow_html=True)

    def _format_date(self, date_str):
        """Format date string for display"""
        if date_str == 'Date not available':
            return date_str

        try:
            if 'T' in date_str:  # ISO format
                pub_date = datetime.fromisoformat(date_str.replace('Z', '+00:00'))
                return pub_date.strftime('%B %d, %Y at %I:%M %p UTC')
            else:
                pub_date = datetime.strptime(date_str[:10], '%Y-%m-%d')
                return pub_date.strftime('%B %d, %Y')
        except:
            return date_str
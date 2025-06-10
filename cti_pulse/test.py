import streamlit as st
import requests
import json
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import nltk
import re
from datetime import datetime, timedelta
import time
import numpy as np
from collections import Counter
import hashlib

# Configure page
st.set_page_config(
    page_title="CyberPulse - Real-Time Threat Intelligence",
    page_icon="🔒",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Download NLTK data if not present
@st.cache_resource
def download_nltk_data():
    try:
        nltk.data.find('vader_lexicon')
    except LookupError:
        nltk.download('vader_lexicon')

download_nltk_data()

# API setup
API_URL = "https://zfgp45ih7i.execute-api.eu-west-1.amazonaws.com/sandbox/api/search"
API_KEY = "LKM38746G38B7RB46GBER"

headers = {
    "Content-Type": "application/json",
    "x-api-key": API_KEY
}

# Enhanced cyber threat keywords with severity ratings
cyber_threats = {
    "ransomware attack": {"severity": 5, "category": "Malware"},
    "data breach": {"severity": 4, "category": "Data Security"},
    "cyber attack": {"severity": 4, "category": "General Attack"},
    "phishing campaign": {"severity": 3, "category": "Social Engineering"},
    "malware outbreak": {"severity": 4, "category": "Malware"},
    "zero day vulnerability": {"severity": 5, "category": "Vulnerability"},
    "supply chain attack": {"severity": 5, "category": "Advanced Threat"},
    "ddos attack": {"severity": 3, "category": "Infrastructure"},
    "insider threat": {"severity": 4, "category": "Insider Risk"},
    "apt group": {"severity": 5, "category": "Advanced Persistent Threat"}
}

def get_threat_data(threat_keyword, num_results=20):
    """Get threat intelligence data for a specific keyword - simplified version"""
    payload = {
        "query_text": threat_keyword,
        "result_size": min(num_results, 100),  # Respect API limit
        "include_highlights": True,
        "include_smart_tags": True
    }
    
    try:
        st.write(f"🔍 Fetching data for: {threat_keyword}")
        response = requests.post(API_URL, headers=headers, data=json.dumps(payload), timeout=30)
        
        st.write(f"Status code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            st.write(f"✅ Successfully fetched data for {threat_keyword}")
            return data
        else:
            st.error(f"❌ API Error for {threat_keyword}: {response.status_code}")
            st.write(f"Response: {response.text}")
            return None
            
    except requests.exceptions.Timeout:
        st.error(f"⏳ Timeout for {threat_keyword}")
        return None
    except requests.exceptions.RequestException as e:
        st.error(f"❌ Network error for {threat_keyword}: {str(e)}")
        return None

def calculate_threat_score(article, threat_keyword):
    """Calculate threat severity score based on multiple factors"""
    base_severity = cyber_threats.get(threat_keyword, {}).get("severity", 3)
    
    # Sentiment factor (more negative = higher threat)
    sentiment_factor = max(0, -article['sentiment_compound'] + 0.5)
    
    # Recency factor (newer = higher threat)
    try:
        pub_date = datetime.strptime(article['published_date'][:10], '%Y-%m-%d')
        days_old = (datetime.now() - pub_date).days
        recency_factor = max(0.1, 1 - (days_old / 30))  # Decay over 30 days
    except:
        recency_factor = 0.5
    
    # Keywords that increase severity
    high_impact_keywords = ['critical', 'widespread', 'global', 'massive', 'unprecedented']
    keyword_boost = sum(1 for keyword in high_impact_keywords if keyword in article['clean_summary'])
    
    final_score = (base_severity + sentiment_factor + keyword_boost) * recency_factor
    return min(10, max(1, final_score))  # Clamp between 1-10

def analyze_threat_sentiment(threat_data, threat_keyword):
    """Enhanced threat analysis with scoring"""
    if not threat_data or 'results' not in threat_data:
        return []
    
    sia = SentimentIntensityAnalyzer()
    threat_analysis = []
    
    for article in threat_data['results']:
        summary = article.get('summary', '')
        title = article.get('title', '')
        
        # Clean the text
        clean_summary = re.sub(r"http\S+|www\.\S+", "", summary.lower())
        clean_summary = re.sub(r"[^a-z\s]", " ", clean_summary)
        clean_summary = re.sub(r"\s+", " ", clean_summary).strip()
        
        # Get sentiment
        sentiment = sia.polarity_scores(clean_summary)
        
        analysis_item = {
            'title': title,
            'summary': summary,
            'clean_summary': clean_summary,
            'sentiment_compound': sentiment['compound'],
            'sentiment_neg': sentiment['neg'],
            'published_date': article.get('published_date', ''),
            'source': article.get('source', ''),
            'highlights': article.get('highlights', []),
            'threat_keyword': threat_keyword,
            'category': cyber_threats.get(threat_keyword, {}).get("category", "Unknown")
        }
        
        # Calculate threat score
        analysis_item['threat_score'] = calculate_threat_score(analysis_item, threat_keyword)
        
        threat_analysis.append(analysis_item)
    
    return sorted(threat_analysis, key=lambda x: x['threat_score'], reverse=True)

def get_severity_color(score):
    """Get color based on threat severity score"""
    if score >= 8:
        return "🔴", "#ff4444"
    elif score >= 6:
        return "🟠", "#ff8800"
    elif score >= 4:
        return "🟡", "#ffaa00"
    else:
        return "🟢", "#44ff44"

def generate_executive_summary(all_threat_data):
    """Generate AI-powered executive summary"""
    total_threats = sum(len(data['analysis']) for data in all_threat_data.values())
    high_severity = sum(1 for data in all_threat_data.values() 
                       for article in data['analysis'] if article['threat_score'] >= 7)
    
    # Find trending threats
    threat_counts = {threat: len(data['analysis']) for threat, data in all_threat_data.items()}
    top_threat = max(threat_counts, key=threat_counts.get) if threat_counts else "None"
    
    # Average sentiment
    all_articles = [article for data in all_threat_data.values() for article in data['analysis']]
    avg_sentiment = np.mean([a['sentiment_compound'] for a in all_articles]) if all_articles else 0
    
    summary = f"""
    ## 📊 Executive Threat Summary
    
    **Current Threat Landscape:** {"🔴 CRITICAL" if high_severity > 5 else "🟡 ELEVATED" if high_severity > 0 else "🟢 NORMAL"}
    
    - **Total Threats Monitored:** {total_threats}
    - **High Severity Alerts:** {high_severity}
    - **Top Trending Threat:** {top_threat.title()}
    - **Overall Sentiment:** {"Negative" if avg_sentiment < -0.1 else "Neutral" if avg_sentiment < 0.1 else "Positive"}
    
    **Key Recommendations:**
    - {"Immediate attention required for high-severity threats" if high_severity > 3 else "Continue monitoring current threat levels"}
    - {"Focus on " + top_threat + " mitigation strategies" if top_threat != "None" else "Maintain current security posture"}
    """
    
    return summary

# Streamlit Dashboard
def main():
    st.title("🔒 CyberPulse - Real-Time Threat Intelligence Platform")
    st.markdown("*Automated threat detection and prioritization for modern security teams*")
    
    # Sidebar controls
    st.sidebar.header("⚙️ Dashboard Controls")
    
    selected_threats = st.sidebar.multiselect(
        "🎯 Monitor Threats:", 
        list(cyber_threats.keys()), 
        default=["ransomware attack", "data breach", "cyber attack"]  # Start with 3 threats
    )
    
    severity_filter = st.sidebar.slider("🚨 Minimum Severity Level", 1, 10, 3)
    articles_per_threat = st.sidebar.slider("📄 Articles per threat", 5, 30, 10)
    
    # Test API Connection
    if st.sidebar.button("🔧 Test API Connection"):
        st.sidebar.write("Testing API connection...")
        test_data = get_threat_data("cyber attack", 5)
        if test_data:
            st.sidebar.success("✅ API connection successful!")
            st.sidebar.write(f"Found {len(test_data.get('results', []))} results")
        else:
            st.sidebar.error("❌ API connection failed")
    
    # Main dashboard
    if st.button("🔍 Fetch Latest Intelligence", type="primary"):
        if not selected_threats:
            st.warning("⚠️ Please select at least one threat type to monitor.")
            return
        
        st.write("🚀 Starting threat intelligence gathering...")
        all_threat_data = {}
        
        # Create columns for live updates
        col1, col2 = st.columns([3, 1])
        
        with col1:
            progress_bar = st.progress(0)
            status_container = st.container()
        
        # Process each threat
        for i, threat in enumerate(selected_threats):
            with status_container:
                st.write(f"🔍 Processing: **{threat}**")
            
            # Add small delay between requests
            if i > 0:
                time.sleep(1)
            
            data = get_threat_data(threat, articles_per_threat)
            
            if data and 'results' in data:
                analysis = analyze_threat_sentiment(data, threat)
                # Filter by severity
                filtered_analysis = [a for a in analysis if a['threat_score'] >= severity_filter]
                all_threat_data[threat] = {
                    'raw_data': data,
                    'analysis': filtered_analysis,
                    'article_count': len(filtered_analysis)
                }
                
                with status_container:
                    st.success(f"✅ **{threat}**: Found {len(filtered_analysis)} articles (severity >= {severity_filter})")
            else:
                with status_container:
                    st.error(f"❌ **{threat}**: No data found")
            
            progress_bar.progress((i + 1) / len(selected_threats))
        
        # Clear status
        status_container.empty()
        progress_bar.empty()
        
        # Store results and display
        if all_threat_data:
            st.session_state.threat_data = all_threat_data
            st.session_state.last_update = datetime.now()
            st.success(f"🎉 Successfully gathered intelligence for {len(all_threat_data)} threat types!")
            display_dashboard_results()
        else:
            st.error("❌ No threat data could be retrieved. Please check API connection.")
    
    elif hasattr(st.session_state, 'threat_data'):
        st.info(f"📊 Showing cached data from {st.session_state.last_update.strftime('%H:%M:%S')}")
        display_dashboard_results()
    else:
        # Show welcome screen
        st.markdown("""
        ## 🎯 Welcome to CyberPulse
        
        **Real-time cyber threat intelligence dashboard** that monitors and analyzes threats across multiple categories.
        
        ### 🚀 Getting Started:
        1. Select threat types to monitor from the sidebar
        2. Adjust severity filter and article count
        3. Click "Fetch Latest Intelligence" to start
        
        ### 📊 Features:
        - **Real-time threat scoring** based on sentiment and impact
        - **Interactive visualizations** for threat analysis
        - **Executive summaries** for quick decision making
        - **Category-based filtering** and monitoring
        """)

def display_dashboard_results():
    """Display the dashboard results from session state"""
    if not hasattr(st.session_state, 'threat_data'):
        return
    
    all_threat_data = st.session_state.threat_data
    
    if not all_threat_data:
        st.warning("⚠️ No threat data available.")
        return
    
    # Executive Summary
    st.markdown(generate_executive_summary(all_threat_data))
    
    # Key Metrics Row
    col1, col2, col3, col4 = st.columns(4)
    
    total_articles = sum(data['article_count'] for data in all_threat_data.values())
    all_articles = [article for data in all_threat_data.values() for article in data['analysis']]
    high_severity_count = sum(1 for article in all_articles if article['threat_score'] >= 8)
    avg_score = np.mean([a['threat_score'] for a in all_articles]) if all_articles else 0
    
    with col1:
        st.metric("📊 Total Threats", total_articles)
    with col2:
        st.metric("🔴 Critical Alerts", high_severity_count)
    with col3:
        st.metric("📈 Avg Severity", f"{avg_score:.1f}/10")
    with col4:
        if hasattr(st.session_state, 'last_update'):
            st.metric("🕐 Last Updated", st.session_state.last_update.strftime("%H:%M:%S"))
    
    if not all_articles:
        st.warning("📭 No articles found matching your severity filter. Try lowering the minimum severity level.")
        return
    
    # Visualization Section
    st.header("📈 Threat Intelligence Visualizations")
    
    # Create visualizations
    viz_col1, viz_col2 = st.columns(2)
    
    with viz_col1:
        # Threat distribution by category
        categories = [article['category'] for article in all_articles]
        category_counts = Counter(categories)
        
        if category_counts:
            fig_pie = px.pie(
                values=list(category_counts.values()),
                names=list(category_counts.keys()),
                title="🎯 Threats by Category"
            )
            st.plotly_chart(fig_pie, use_container_width=True)
    
    with viz_col2:
        # Severity distribution
        severity_ranges = ['Low (1-3)', 'Medium (4-6)', 'High (7-8)', 'Critical (9-10)']
        severity_counts = [
            sum(1 for a in all_articles if 1 <= a['threat_score'] <= 3),
            sum(1 for a in all_articles if 4 <= a['threat_score'] <= 6),
            sum(1 for a in all_articles if 7 <= a['threat_score'] <= 8),
            sum(1 for a in all_articles if 9 <= a['threat_score'] <= 10)
        ]
        
        fig_bar = px.bar(
            x=severity_ranges,
            y=severity_counts,
            title="🚨 Threat Severity Distribution",
            color=severity_counts,
            color_continuous_scale="Reds"
        )
        st.plotly_chart(fig_bar, use_container_width=True)
    
    # Critical Alerts Section
    st.header("🚨 Critical Threat Alerts")
    
    critical_threats = [a for a in all_articles if a['threat_score'] >= 8]
    
    if critical_threats:
        for threat in critical_threats[:5]:  # Show top 5 critical
            emoji, color = get_severity_color(threat['threat_score'])
            
            with st.container():
                st.markdown(f"""
                <div style="border-left: 4px solid {color}; padding: 10px; margin: 10px 0; background-color: #f8f9fa;">
                    <h4>{emoji} {threat['title']}</h4>
                    <p><strong>Severity:</strong> {threat['threat_score']:.1f}/10 | 
                       <strong>Category:</strong> {threat['category']} | 
                       <strong>Source:</strong> {threat['source']}</p>
                    <p>{threat['summary'][:200]}...</p>
                    <small>📅 {threat['published_date']}</small>
                </div>
                """, unsafe_allow_html=True)
    else:
        st.info("🟢 No critical threats detected at current severity threshold.")
    
    # Detailed Threat Analysis
    st.header("🔍 Detailed Threat Analysis")
    
    for threat_name, data in all_threat_data.items():
        if data['analysis']:
            with st.expander(f"📋 {threat_name.title()} ({len(data['analysis'])} articles)"):
                
                # Threat-specific metrics
                threat_articles = data['analysis']
                avg_sentiment = np.mean([a['sentiment_compound'] for a in threat_articles])
                avg_severity = np.mean([a['threat_score'] for a in threat_articles])
                
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Articles", len(threat_articles))
                with col2:
                    st.metric("Avg Severity", f"{avg_severity:.1f}")
                with col3:
                    sentiment_label = "Negative" if avg_sentiment < -0.1 else "Neutral" if avg_sentiment < 0.1 else "Positive"
                    st.metric("Sentiment", sentiment_label)
                
                # Top articles for this threat
                st.subheader("Top Articles:")
                for article in threat_articles[:3]:
                    emoji, _ = get_severity_color(article['threat_score'])
                    st.write(f"{emoji} **{article['title']}** (Score: {article['threat_score']:.1f})")
                    st.write(f"*{article['summary'][:150]}...*")
                    st.write(f"Source: {article['source']} | Date: {article['published_date']}")
                    st.markdown("---")

if __name__ == "__main__":
    main()
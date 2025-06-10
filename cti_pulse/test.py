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
        nltk.data.find('punkt_tab')
        nltk.data.find('stopwords')
    except LookupError:
        nltk.download('vader_lexicon')
        nltk.download('punkt_tab')
        nltk.download('punkt')  # Fallback
        nltk.download('stopwords')

download_nltk_data()

# API setup
API_URL = "https://zfgp45ih7i.execute-api.eu-west-1.amazonaws.com/sandbox/api/search"
API_KEY = "LKM38746G38B7RB46GBER"

headers = {
    "Content-Type": "application/json",
    "x-api-key": API_KEY
}

# Enhanced cyber threat keywords with severity ratings and synonyms
cyber_threats = {
    "ransomware attack": {"severity": 5, "category": "Malware", "synonyms": ["ransomware", "crypto locker", "ransom malware", "encryption attack"]},
    "data breach": {"severity": 4, "category": "Data Security", "synonyms": ["data leak", "information breach", "data compromise", "data theft", "breach"]},
    "cyber attack": {"severity": 4, "category": "General Attack", "synonyms": ["cyberattack", "cyber incident", "security breach", "hack", "attack"]},
    "phishing campaign": {"severity": 3, "category": "Social Engineering", "synonyms": ["phishing", "email scam", "social engineering", "spear phishing", "business email compromise"]},
    "malware outbreak": {"severity": 4, "category": "Malware", "synonyms": ["malware", "virus", "trojan", "worm", "malicious software"]},
    "zero day vulnerability": {"severity": 5, "category": "Vulnerability", "synonyms": ["zero-day", "0day", "vulnerability", "exploit", "security flaw"]},
    "supply chain attack": {"severity": 5, "category": "Advanced Threat", "synonyms": ["supply chain", "third party attack", "vendor compromise"]},
    "ddos attack": {"severity": 3, "category": "Infrastructure", "synonyms": ["ddos", "denial of service", "dos attack", "botnet attack"]},
    "insider threat": {"severity": 4, "category": "Insider Risk", "synonyms": ["insider attack", "internal threat", "rogue employee", "privilege abuse"]},
    "apt group": {"severity": 5, "category": "Advanced Persistent Threat", "synonyms": ["apt", "advanced persistent threat", "nation state", "state sponsored"]}
}

# Cybersecurity keyword patterns for NLP extraction
cyber_keywords = {
    'attacks': ['attack', 'exploit', 'breach', 'hack', 'compromise', 'intrusion', 'incident'],
    'malware': ['malware', 'virus', 'trojan', 'ransomware', 'spyware', 'adware', 'rootkit', 'worm'],
    'techniques': ['phishing', 'spoofing', 'social engineering', 'brute force', 'sql injection', 'xss'],
    'vulnerabilities': ['vulnerability', 'exploit', 'zero-day', '0day', 'cve', 'patch', 'flaw'],
    'threats': ['threat', 'risk', 'apt', 'insider', 'nation state', 'cybercriminal'],
    'infrastructure': ['ddos', 'botnet', 'c2', 'command and control', 'infrastructure'],
    'data': ['data', 'information', 'credentials', 'personal', 'sensitive', 'confidential']
}

def extract_cybersecurity_terms(user_query):
    """Extract cybersecurity-related terms from natural language query using NLP"""
    query_lower = user_query.lower()
    
    # Simple tokenization fallback if NLTK fails
    try:
        from nltk.corpus import stopwords
        from nltk.tokenize import word_tokenize
        
        stop_words = set(stopwords.words('english'))
        tokens = word_tokenize(query_lower)
        tokens = [token for token in tokens if token.isalpha() and token not in stop_words]
    except Exception as e:
        # Fallback to simple tokenization if NLTK fails
        st.warning(f"Using simple tokenization: {str(e)}")
        simple_stop_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by', 'is', 'are', 'was', 'were', 'be', 'been', 'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could', 'should', 'may', 'might', 'can', 'what', 'how', 'when', 'where', 'why', 'who', 'this', 'that', 'these', 'those'}
        # Simple regex-based tokenization
        import re
        tokens = re.findall(r'\b[a-zA-Z]+\b', query_lower)
        tokens = [token for token in tokens if token not in simple_stop_words and len(token) > 2]
    
    # Find matching cybersecurity terms
    confidence_scores = {}
    
    # Check for direct matches with threat keywords and synonyms
    for threat_name, threat_info in cyber_threats.items():
        score = 0
        
        # Check main threat name - give high priority to complete matches
        threat_words = threat_name.split()
        if all(word in query_lower for word in threat_words):
            score += 15  # Higher score for complete threat name match
        elif any(word in query_lower for word in threat_words):
            # Only add points if it's a specific word, not generic "attack"
            specific_words = [word for word in threat_words if word not in ['attack', 'campaign', 'outbreak', 'group']]
            if any(word in query_lower for word in specific_words):
                score += 8
            else:
                score += 2  # Lower score for generic words like "attack"
        
        # Check synonyms - prioritize specific synonyms
        for synonym in threat_info.get('synonyms', []):
            if synonym in query_lower:
                if synonym in ['ransomware', 'phishing', 'ddos', 'apt']:  # Specific cybersecurity terms
                    score += 12
                else:
                    score += 6
            elif any(word in synonym.split() for word in tokens):
                score += 2
        
        if score > 0:
            confidence_scores[threat_name] = score
    
    # Check for general cybersecurity keywords - but with lower priority
    for category, keywords in cyber_keywords.items():
        for keyword in keywords:
            if keyword in query_lower:
                # Only boost if we haven't already found a strong specific match
                max_existing_score = max(confidence_scores.values()) if confidence_scores else 0
                
                # If we already have a strong match (>10), don't add generic boosts
                if max_existing_score > 10:
                    continue
                
                # Map keywords to threat types with conservative scoring
                if category == 'malware' and keyword == 'ransomware':
                    confidence_scores['ransomware attack'] = confidence_scores.get('ransomware attack', 0) + 10
                elif category == 'malware' and keyword in ['virus', 'trojan', 'worm']:
                    confidence_scores['malware outbreak'] = confidence_scores.get('malware outbreak', 0) + 4
                elif category == 'attacks' and keyword == 'breach':
                    confidence_scores['data breach'] = confidence_scores.get('data breach', 0) + 8
                elif category == 'techniques' and keyword == 'phishing':
                    confidence_scores['phishing campaign'] = confidence_scores.get('phishing campaign', 0) + 10
                elif category == 'vulnerabilities' and keyword in ['zero-day', '0day']:
                    confidence_scores['zero day vulnerability'] = confidence_scores.get('zero day vulnerability', 0) + 8
                elif category == 'infrastructure' and keyword == 'ddos':
                    confidence_scores['ddos attack'] = confidence_scores.get('ddos attack', 0) + 10
                elif category == 'attacks' and keyword == 'attack':
                    # Only add minimal points for generic "attack" if no specific match found
                    if not any(score > 8 for score in confidence_scores.values()):
                        confidence_scores['cyber attack'] = confidence_scores.get('cyber attack', 0) + 3
    
    # Sort by confidence and return top matches
    sorted_threats = sorted(confidence_scores.items(), key=lambda x: x[1], reverse=True)
    
    # Be more selective - only return the top match if it's significantly higher than others
    if sorted_threats:
        top_score = sorted_threats[0][1]
        # If the top match is much stronger (>= 10 points), only return it
        if top_score >= 10:
            return [sorted_threats[0][0]]
        # Otherwise, return threats with confidence > 5 and within 3 points of the top score
        else:
            return [threat for threat, score in sorted_threats if score > 5 and (top_score - score) <= 3]
    
    return []

def generate_chatbot_response(matched_threats, user_query):
    """Generate a conversational response based on matched threats"""
    if not matched_threats:
        return """
        🤖 I didn't find any specific cybersecurity threats in your query. 
        
        Try asking about topics like:
        - "What ransomware attacks happened recently?"
        - "Show me data breaches this week"
        - "Any phishing campaigns targeting banks?"
        - "Latest zero-day vulnerabilities"
        """
    
    threat_list = ", ".join([threat.title() for threat in matched_threats[:3]])
    
    response = f"""
    🤖 **I found {len(matched_threats)} relevant cybersecurity topic(s) based on your query:**
    
    **Searching for:** {threat_list}
    
    I'll fetch the latest threat intelligence for these topics. This may take a moment...
    """
    
    return response

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
    
    # Add chatbot section at the top
    st.header("🤖 AI Threat Intelligence Assistant")
    
    # AI Controls
    ai_col1, ai_col2, ai_col3 = st.columns([2, 1, 1])
    with ai_col2:
        ai_severity_filter = st.slider("🚨 AI Severity Filter", 1, 10, 3, key="ai_severity")
    with ai_col3:
        ai_articles_per_threat = st.slider("📄 AI Articles per threat", 5, 100, 15, key="ai_articles")
    
    # Chat interface
    with st.container():
        col1, col2 = st.columns([4, 1])
        
        with col1:
            user_query = st.text_input(
                "Ask me about cybersecurity threats in natural language:",
                placeholder="e.g., 'What ransomware attacks happened this week?' or 'Show me recent data breaches'"
            )
        
        with col2:
            search_button = st.button("🔍 Ask AI", type="primary")
    
    # Process chatbot query
    if search_button and user_query:
        with st.spinner("🧠 Analyzing your query..."):
            matched_threats = extract_cybersecurity_terms(user_query)
            
            # Display chatbot response with current settings
            if matched_threats:
                threat_list = ", ".join([threat.title() for threat in matched_threats[:3]])
                response = f"""
                🤖 **I found {len(matched_threats)} relevant cybersecurity topic(s) based on your query:**
                
                **Searching for:** {threat_list}
                **Settings:** Severity ≥{ai_severity_filter}, {ai_articles_per_threat} articles per threat
                
                I'll fetch the latest threat intelligence for these topics. This may take a moment...
                """
                st.markdown(response)
                
                # Automatically fetch data for matched threats
                st.write("---")
                st.write("🚀 Fetching threat intelligence...")
                
                all_threat_data = {}
                progress_bar = st.progress(0)
                
                for i, threat in enumerate(matched_threats[:5]):  # Limit to top 5
                    data = get_threat_data(threat, ai_articles_per_threat)
                    
                    if data and 'results' in data:
                        analysis = analyze_threat_sentiment(data, threat)
                        # Use AI severity filter
                        filtered_analysis = [a for a in analysis if a['threat_score'] >= ai_severity_filter]
                        all_threat_data[threat] = {
                            'raw_data': data,
                            'analysis': filtered_analysis,
                            'article_count': len(filtered_analysis)
                        }
                        st.success(f"✅ Found {len(filtered_analysis)} articles for {threat} (severity ≥{ai_severity_filter})")
                    else:
                        st.warning(f"⚠️ No data found for {threat}")
                    
                    progress_bar.progress((i + 1) / len(matched_threats[:5]))
                
                progress_bar.empty()
                
                if all_threat_data:
                    st.session_state.threat_data = all_threat_data
                    st.session_state.last_update = datetime.now()
                    st.session_state.query_used = f"{user_query} (AI: severity≥{ai_severity_filter}, {ai_articles_per_threat} articles)"
                    st.success(f"🎉 Analysis complete! Found intelligence for {len(all_threat_data)} threat types.")
                    display_dashboard_results()
            else:
                response = """
                🤖 I didn't find any specific cybersecurity threats in your query. 
                
                Try asking about topics like:
                - "What ransomware attacks happened recently?"
                - "Show me data breaches this week"
                - "Any phishing campaigns targeting banks?"
                - "Latest zero-day vulnerabilities"
                """
                st.markdown(response)
    
    # Sidebar controls (existing functionality)
    st.sidebar.header("⚙️ Manual Dashboard Controls")
    st.sidebar.markdown("*Or use manual controls below:*")
    
    selected_threats = st.sidebar.multiselect(
        "🎯 Monitor Threats:", 
        list(cyber_threats.keys()), 
        default=[]  # Empty by default since we have chatbot
    )
    
    severity_filter = st.sidebar.slider("🚨 Manual Severity Level", 1, 10, 3, key="manual_severity")
    articles_per_threat = st.sidebar.slider("📄 Manual Articles per threat", 5, 100, 15, key="manual_articles")
    
    # Test API Connection
    if st.sidebar.button("🔧 Test API Connection"):
        st.sidebar.write("Testing API connection...")
        test_data = get_threat_data("cyber attack", 5)
        if test_data:
            st.sidebar.success("✅ API connection successful!")
            st.sidebar.write(f"Found {len(test_data.get('results', []))} results")
        else:
            st.sidebar.error("❌ API connection failed")
    
    # Manual dashboard (existing functionality)
    if st.sidebar.button("🔍 Fetch Latest Intelligence"):
        if not selected_threats:
            st.warning("⚠️ Please select at least one threat type to monitor or use the AI assistant above.")
            return
        
        st.write("🚀 Starting manual threat intelligence gathering...")
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
            st.session_state.query_used = "Manual Selection"
            st.success(f"🎉 Successfully gathered intelligence for {len(all_threat_data)} threat types!")
            display_dashboard_results()
        else:
            st.error("❌ No threat data could be retrieved. Please check API connection.")
    
    elif hasattr(st.session_state, 'threat_data'):
        query_info = f" (from query: '{st.session_state.query_used}')" if hasattr(st.session_state, 'query_used') else ""
        st.info(f"📊 Showing cached data from {st.session_state.last_update.strftime('%H:%M:%S')}{query_info}")
        display_dashboard_results()
    else:
        # Show welcome screen with chatbot examples
        st.markdown("""
        ## 🎯 Welcome to CyberPulse AI
        
        **Real-time cyber threat intelligence dashboard** with AI-powered natural language queries.
        
        ### 🤖 Try the AI Assistant:
        Ask questions like:
        - *"What ransomware attacks happened this week?"*
        - *"Show me recent data breaches in healthcare"*
        - *"Any phishing campaigns targeting banks?"*
        - *"Latest zero-day vulnerabilities affecting Windows"*
        - *"Supply chain attacks on software companies"*
        
        ### 📊 Features:
        - **Natural language queries** - Ask in plain English
        - **Smart threat extraction** - AI identifies relevant cybersecurity terms
        - **Real-time threat scoring** based on sentiment and impact
        - **Interactive visualizations** for threat analysis
        - **Executive summaries** for quick decision making
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
    
    # Create unique keys based on current time to avoid duplicates
    timestamp = int(time.time() * 1000)  # Millisecond timestamp for uniqueness
    
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
            st.plotly_chart(fig_pie, use_container_width=True, key=f"category_pie_{timestamp}")
    
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
        st.plotly_chart(fig_bar, use_container_width=True, key=f"severity_bar_{timestamp}")
    
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
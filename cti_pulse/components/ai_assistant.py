import streamlit as st
from assets.templates import get_ai_container_template


class AIAssistant:
    """AI Assistant component for natural language threat queries"""

    def render_chat_interface(self):
        """Render the AI chat interface"""
        st.markdown(get_ai_container_template(), unsafe_allow_html=True)

        # AI Controls
        ai_col1, ai_col2, ai_col3 = st.columns([2, 1, 1])

        with ai_col2:
            ai_severity_filter = st.slider("🚨 AI Severity Filter", 1, 10, 3, key="ai_severity")
        with ai_col3:
            ai_articles_per_threat = st.slider("📄 AI Articles per threat", 5, 100, 15, key="ai_articles")

        # Chat interface
        col1, col2 = st.columns([4, 1])

        with col1:
            user_query = st.text_input(
                "Ask me about cybersecurity threats in natural language:",
                placeholder="e.g., 'What ransomware attacks happened this week?' or 'Show me recent data breaches'",
                key="ai_query_input"
            )

        with col2:
            search_button = st.button("🔍 Ask AI", type="primary", key="ai_search_btn")

        # Add some example queries as buttons
        st.markdown("**Quick Examples:**")
        example_col1, example_col2, example_col3 = st.columns(3)

        example_query = None

        with example_col1:
            if st.button("🔐 Ransomware", key="example_1"):
                example_query = "What ransomware attacks happened this week?"

        with example_col2:
            if st.button("💾 Data Breaches", key="example_2"):
                example_query = "Show me recent data breaches"

        with example_col3:
            if st.button("🎣 Phishing Campaigns", key="example_3"):
                example_query = "Any phishing campaigns targeting banks?"

        # Use example query if button was clicked
        if example_query:
            user_query = example_query
            search_button = True

        return {
            'query': user_query,
            'should_process': search_button and user_query,
            'settings': {
                'severity_filter': ai_severity_filter,
                'articles_per_threat': ai_articles_per_threat
            }
        }
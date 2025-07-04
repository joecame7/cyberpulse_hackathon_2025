import streamlit as st
from assets.templates import get_ai_container_template


class AIAssistant:
    """AI Assistant component for natural language threat queries"""

    def render_chat_interface(self):
        """Render the AI chat interface"""
        st.markdown(get_ai_container_template(), unsafe_allow_html=True)

        # AI Controls - aligned to the left like the chat input
        ai_col1, ai_col2 = st.columns([1, 1])

        with ai_col1:
            ai_severity_filter = st.slider("🚨 AI Severity Filter", 1, 10, 3, key="ai_severity")
        with ai_col2:
            ai_articles_per_threat = st.slider("📄 AI Articles per threat", 5, 100, 15, key="ai_articles")

        # Chat interface with proper alignment
        col1, col2 = st.columns([5, 1])

        with col1:
            user_query = st.text_input(
                "Ask me about cybersecurity threats in natural language:",
                placeholder="e.g., 'What ransomware attacks and data breaches happened this week?' or 'Show me phishing and malware threats'",
                key="ai_query_input",
                label_visibility="visible"
            )

        with col2:
            # Add empty space to align button with input field
            st.markdown("<div style='height: 25px;'></div>", unsafe_allow_html=True)
            search_button = st.button("🔍 Ask AI", type="primary", key="ai_search_btn", use_container_width=True)

        # Add some example queries as buttons
        st.markdown("**Quick Examples:**")
        example_col1, example_col2, example_col3, example_col4 = st.columns([1, 1, 1, 2])

        example_query = None

        with example_col1:
            if st.button("🔐 Ransomware", key="example_1"):
                example_query = "What ransomware attacks happened this week?"

        with example_col2:
            if st.button("💾 Data Breaches", key="example_2"):
                example_query = "Show me recent data breaches and phishing campaigns"

        with example_col3:
            if st.button("🎣 Multiple Threats", key="example_3"):
                example_query = "Any malware, ransomware, or zero-day vulnerabilities this month?"

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
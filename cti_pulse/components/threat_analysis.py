import streamlit as st
import numpy as np
from datetime import datetime
from assets.templates import get_threat_article_template
from assets.styles import get_severity_color_class, get_severity_emoji


class ThreatAnalysis:
    """Detailed threat analysis component"""

    def render_detailed_analysis(self, all_threat_data):
        """Render detailed threat analysis for each threat type"""
        st.header("🔍 Detailed Threat Analysis")

        # Use tabs instead of nested expanders
        if all_threat_data:
            threat_names = list(all_threat_data.keys())
            tabs = st.tabs([f"📋 {name.title()} ({len(all_threat_data[name]['analysis'])})" for name in threat_names])

            for tab, (threat_name, data) in zip(tabs, all_threat_data.items()):
                with tab:
                    if data['analysis']:
                        self._render_threat_content(threat_name, data)

    def _render_threat_content(self, threat_name, data):
        """Render content for a specific threat"""
        threat_articles = data['analysis']

        # Threat-specific metrics
        self._render_threat_metrics(threat_articles)

        # Article list with details
        st.subheader(f"📄 All {len(threat_articles)} Articles:")

        # Use session state to track which articles have expanded details
        if 'expanded_articles' not in st.session_state:
            st.session_state.expanded_articles = set()

        for i, article in enumerate(threat_articles, 1):
            self._render_article_with_details(article, i, threat_name)

    def _render_threat_metrics(self, threat_articles):
        """Render metrics for a specific threat type"""
        avg_sentiment = np.mean([a['sentiment_compound'] for a in threat_articles])
        avg_severity = np.mean([a['threat_score'] for a in threat_articles])
        recent_count = sum(1 for a in threat_articles if self._is_recent(a['published_date']))

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric("📊 Articles", len(threat_articles))

        with col2:
            st.metric("🎯 Avg Severity", f"{avg_severity:.1f}/10")

        with col3:
            sentiment_label = self._get_sentiment_label(avg_sentiment)
            sentiment_color = self._get_sentiment_color(avg_sentiment)
            st.metric("😐 Sentiment", sentiment_label)

        with col4:
            st.metric("🆕 Recent (7d)", recent_count)

        # Sentiment analysis bar
        self._render_sentiment_bar(avg_sentiment)

    def _render_sentiment_bar(self, avg_sentiment):
        """Render sentiment analysis bar"""
        sentiment_percentage = ((avg_sentiment + 1) / 2) * 100  # Convert -1,1 to 0,100

        if avg_sentiment < -0.3:
            color = "#e74c3c"
            label = "Very Negative"
        elif avg_sentiment < -0.1:
            color = "#f39c12"
            label = "Negative"
        elif avg_sentiment < 0.1:
            color = "#95a5a6"
            label = "Neutral"
        elif avg_sentiment < 0.3:
            color = "#27ae60"
            label = "Positive"
        else:
            color = "#2ecc71"
            label = "Very Positive"

        st.markdown(f"""
        <div style="margin: 1rem 0;">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.5rem;">
                <span><strong>Overall Sentiment:</strong> {label}</span>
                <span><strong>{avg_sentiment:.2f}</strong></span>
            </div>
            <div style="background-color: #ecf0f1; border-radius: 10px; height: 20px; overflow: hidden;">
                <div style="background-color: {color}; height: 100%; width: {sentiment_percentage:.1f}%; 
                            border-radius: 10px; transition: width 0.3s ease;"></div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    def _render_article_with_details(self, article, index, threat_name):
        """Render article with expandable details"""
        severity_class = get_severity_color_class(article['threat_score'])
        emoji = get_severity_emoji(article['threat_score'])
        formatted_date = self._format_date(article['published_date'])

        # Unique key for this article
        article_key = f"{threat_name}_{index}_{hash(article['title'])}"

        # Main article display
        st.markdown(get_threat_article_template(
            index,
            article['title'],
            f"{article['threat_score']:.1f}",
            formatted_date,
            article['source'],
            article['summary'],
            severity_class,
            emoji
        ), unsafe_allow_html=True)

        # Toggle button for details
        col1, col2 = st.columns([2, 3])
        with col1:
            if st.button(
                    "🔍 Show Details" if article_key not in st.session_state.expanded_articles else "🔽 Hide Details",
                    key=f"toggle_{article_key}",
                    use_container_width=True
            ):
                if article_key in st.session_state.expanded_articles:
                    st.session_state.expanded_articles.remove(article_key)
                else:
                    st.session_state.expanded_articles.add(article_key)
                st.rerun()

        # Show details if expanded
        if article_key in st.session_state.expanded_articles:
            with st.container():
                st.markdown("---")
                self._render_article_details(article)
                st.markdown("---")

    def _render_article_details(self, article):
        """Render detailed information for a single article"""
        col1, col2 = st.columns(2)

        with col1:
            st.markdown("**📊 Sentiment Analysis:**")
            st.write(f"• Compound Score: {article['sentiment_compound']:.3f}")
            st.write(f"• Negative: {article['sentiment_neg']:.3f}")
            st.write(f"• Category: {article['category']}")

        with col2:
            st.markdown("**📈 Threat Scoring:**")
            st.write(f"• Final Score: {article['threat_score']:.1f}/10")
            st.write(f"• Threat Type: {article['threat_keyword']}")

        # Highlights if available
        if article.get('highlights'):
            st.markdown("**🔍 Key Highlights:**")
            for highlight in article['highlights'][:3]:  # Show top 3 highlights
                st.markdown(f"• *{highlight}*")

        # Raw summary for debugging
        if st.checkbox(f"Show raw data", key=f"raw_{hash(article['title'])}"):
            st.json({
                'clean_summary': article['clean_summary'][:200] + "..." if len(article['clean_summary']) > 200 else
                article['clean_summary'],
                'sentiment_scores': {
                    'compound': article['sentiment_compound'],
                    'negative': article['sentiment_neg']
                },
                'metadata': {
                    'source': article['source'],
                    'published_date': article['published_date'],
                    'threat_keyword': article['threat_keyword']
                }
            })

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

    def _is_recent(self, date_str, days=7):
        """Check if date is within specified days"""
        if date_str == 'Date not available':
            return False

        try:
            if 'T' in date_str:
                pub_date = datetime.fromisoformat(date_str.replace('Z', '+00:00'))
            else:
                pub_date = datetime.strptime(date_str[:10], '%Y-%m-%d')

            days_old = (datetime.now(pub_date.tzinfo) - pub_date).days
            return days_old <= days
        except:
            return False

    def _get_sentiment_label(self, sentiment):
        """Get sentiment label from score"""
        if sentiment < -0.3:
            return "Very Negative"
        elif sentiment < -0.1:
            return "Negative"
        elif sentiment < 0.1:
            return "Neutral"
        elif sentiment < 0.3:
            return "Positive"
        else:
            return "Very Positive"

    def _get_sentiment_color(self, sentiment):
        """Get color for sentiment display"""
        if sentiment < -0.1:
            return "#e74c3c"
        elif sentiment < 0.1:
            return "#f39c12"
        else:
            return "#27ae60"
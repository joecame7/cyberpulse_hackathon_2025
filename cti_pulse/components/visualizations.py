import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from collections import Counter
import pandas as pd
import time


class ThreatVisualizations:
    """Threat visualization components"""

    def render_threat_charts(self, all_threat_data):
        """Render all threat visualization charts"""
        st.header("📈 Threat Intelligence Visualizations")

        all_articles = [article for data in all_threat_data.values() for article in data['analysis']]

        if not all_articles:
            st.warning("📭 No articles found matching your severity filter. Try lowering the minimum severity level.")
            return

        # Create unique timestamp for chart keys
        timestamp = int(time.time() * 1000)

        # Render severity distribution chart
        self._render_severity_distribution(all_articles, timestamp)

        # Full width charts
        self._render_timeline_chart(all_articles, timestamp)
        self._render_source_analysis(all_articles, timestamp)

    def _render_severity_distribution(self, all_articles, timestamp):
        """Render severity distribution bar chart"""
        severity_ranges = ['Low (1-3)', 'Medium (4-6)', 'High (7-8)', 'Critical (9-10)']
        severity_counts = [
            sum(1 for a in all_articles if 1 <= a['threat_score'] <= 3),
            sum(1 for a in all_articles if 4 <= a['threat_score'] <= 6),
            sum(1 for a in all_articles if 7 <= a['threat_score'] <= 8),
            sum(1 for a in all_articles if 9 <= a['threat_score'] <= 10)
        ]

        # Custom colors for severity levels
        colors = ['#2ECC71', '#F39C12', '#E67E22', '#E74C3C']

        fig_bar = go.Figure(data=[
            go.Bar(
                x=severity_ranges,
                y=severity_counts,
                marker_color=colors,
                text=severity_counts,
                textposition='auto',
                hovertemplate='<b>%{x}</b><br>Count: %{y}<extra></extra>'
            )
        ])

        fig_bar.update_layout(
            title="🚨 Threat Severity Distribution",
            xaxis_title="Severity Level",
            yaxis_title="Number of Threats",
            height=400,
            showlegend=False,
            title_font_size=16
        )

        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.plotly_chart(fig_bar, use_container_width=True, key=f"severity_bar_{timestamp}")
        st.markdown('</div>', unsafe_allow_html=True)

    def _render_timeline_chart(self, all_articles, timestamp):
        """Render threat timeline chart"""
        st.subheader("📅 Threat Timeline Analysis")

        # Process dates and create timeline data
        timeline_data = []
        for article in all_articles:
            if article['published_date'] != 'Date not available':
                try:
                    from datetime import datetime
                    if 'T' in article['published_date']:
                        date = datetime.fromisoformat(article['published_date'].replace('Z', '+00:00')).date()
                    else:
                        date = datetime.strptime(article['published_date'][:10], '%Y-%m-%d').date()

                    timeline_data.append({
                        'date': date,
                        'severity': article['threat_score'],
                        'category': article['category'],
                        'title': article['title'][:50] + "..." if len(article['title']) > 50 else article['title']
                    })
                except:
                    continue

        if timeline_data:
            df = pd.DataFrame(timeline_data)

            # Create scatter plot with severity over time
            fig_timeline = px.scatter(
                df,
                x='date',
                y='severity',
                color='category',
                size='severity',
                hover_data=['title'],
                title="🕐 Threat Severity Over Time",
                labels={'severity': 'Threat Score', 'date': 'Publication Date'},
                color_discrete_sequence=['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7', '#DDA0DD']
            )

            fig_timeline.update_layout(
                height=400,
                title_font_size=16,
                xaxis_title="Publication Date",
                yaxis_title="Threat Score",
                showlegend=True
            )

            fig_timeline.update_traces(
                marker=dict(line=dict(width=1, color='DarkSlateGrey')),
                selector=dict(mode='markers')
            )

            st.markdown('<div class="chart-container">', unsafe_allow_html=True)
            st.plotly_chart(fig_timeline, use_container_width=True, key=f"timeline_{timestamp}")
            st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.info("📅 No timeline data available - dates not properly formatted in source data.")

    def _render_source_analysis(self, all_articles, timestamp):
        """Render source analysis chart"""
        st.subheader("📰 Top Threat Intelligence Sources")

        # Count articles by source
        sources = [article['source'] for article in all_articles if article['source'] != 'Source not available']
        source_counts = Counter(sources)

        # Get top 10 sources
        top_sources = dict(source_counts.most_common(10))

        if top_sources:
            # Create horizontal bar chart
            fig_sources = go.Figure(data=[
                go.Bar(
                    y=list(reversed(list(top_sources.keys()))),  # Reverse for better display
                    x=list(reversed(list(top_sources.values()))),
                    orientation='h',
                    marker_color='#667eea',
                    text=list(reversed(list(top_sources.values()))),
                    textposition='auto',
                    hovertemplate='<b>%{y}</b><br>Articles: %{x}<extra></extra>'
                )
            ])

            fig_sources.update_layout(
                title="📊 Articles by Source",
                xaxis_title="Number of Articles",
                yaxis_title="Source",
                height=400,
                title_font_size=16,
                margin=dict(l=150)  # Add left margin for long source names
            )

            st.markdown('<div class="chart-container">', unsafe_allow_html=True)
            st.plotly_chart(fig_sources, use_container_width=True, key=f"sources_{timestamp}")
            st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.info("📰 No source data available for analysis.")
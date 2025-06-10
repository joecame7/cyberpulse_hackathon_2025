import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import json
from datetime import datetime, timedelta
import requests
from collections import Counter
import time
import matplotlib.pyplot as plt
import matplotlib.backends.backend_pdf as pdf_backend
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
import io
import base64

# Import your main CTI class
# from cti_pulse_main import CyberThreatIntelligence

st.set_page_config(
    page_title="🚨 Cyber Threat Intelligence Pulse",
    page_icon="🛡️",
    layout="wide"
)

# Custom CSS for dark theme
st.markdown("""
<style>
.main-header {
    background: linear-gradient(90deg, #1e3c72 0%, #2a5298 100%);
    padding: 20px;
    border-radius: 10px;
    margin-bottom: 20px;
}
.threat-card {
    background: #f8f9fa;
    padding: 15px;
    border-radius: 8px;
    border-left: 4px solid #dc3545;
    margin: 10px 0;
}
.metric-card {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    padding: 20px;
    border-radius: 10px;
    color: white;
    text-align: center;
}
</style>
""", unsafe_allow_html=True)

# Sidebar for controls
st.sidebar.title("🛡️ CTI Control Panel")
refresh_data = st.sidebar.button("🔄 Refresh Intelligence", type="primary")
auto_refresh = st.sidebar.checkbox("Auto-refresh (30s)")

# Main header
st.markdown("""
<div class="main-header">
    <h1 style="color: white; margin: 0;">🚨 Cyber Threat Intelligence Pulse</h1>
    <p style="color: #ccc; margin: 5px 0 0 0;">Real-time cybersecurity threat monitoring and analysis</p>
</div>
""", unsafe_allow_html=True)

# Initialize session state
if 'threat_data' not in st.session_state:
    st.session_state.threat_data = None
    st.session_state.last_update = None

# Load or refresh data
@st.cache_data(ttl=1800)  # Cache for 30 minutes
def load_threat_data():
    """Load threat intelligence data"""
    API_KEY = "LKM38746G38B7RB46GBER"
    
    # Mock data for demo purposes - replace with actual API calls
    mock_data = {
        'threat_categories': {
            'ransomware': 24,
            'data_breach': 18,
            'malware': 15,
            'phishing': 12,
            'apt_groups': 10,
            'zero_day': 8,
            'supply_chain': 6,
            'vulnerability': 20
        },
        'severity_counts': {
            'critical': 8,
            'high': 23,
            'medium': 35,
            'low': 12,
            'unknown': 5
        },
        'avg_threat_score': 0.67,
        'total_threats': 83,
        'sources_monitored': 15,
        'high_priority_threats': [
            {
                'title': 'New Ransomware Group Targets Healthcare Infrastructure',
                'threat_score': 0.89,
                'categories': ['ransomware', 'apt_groups'],
                'severity': 'critical',
                'source': 'SecurityWeek'
            },
            {
                'title': 'Zero-Day Exploit Discovered in Popular Enterprise Software',
                'threat_score': 0.85,
                'categories': ['zero_day', 'vulnerability'],
                'severity': 'high',
                'source': 'Bleeping Computer'
            },
            {
                'title': 'Supply Chain Attack Affects Multiple Fortune 500 Companies',
                'threat_score': 0.82,
                'categories': ['supply_chain', 'apt_groups'],
                'severity': 'high',
                'source': 'ThreatPost'
            }
        ],
        'trending_threats': [
            'AI-powered phishing attacks',
            'Cloud infrastructure targeting',
            'Cryptocurrency exchange breaches',
            'IoT botnet campaigns'
        ]
    }
    
    return mock_data

# Load data
if refresh_data or st.session_state.threat_data is None:
    with st.spinner("🔍 Collecting latest threat intelligence..."):
        st.session_state.threat_data = load_threat_data()
        st.session_state.last_update = datetime.now()
        time.sleep(2)  # Simulate processing time

data = st.session_state.threat_data

# Auto-refresh functionality
if auto_refresh:
    time.sleep(30)
    st.rerun()

# Display last update time
if st.session_state.last_update:
    st.info(f"🕒 Last updated: {st.session_state.last_update.strftime('%Y-%m-%d %H:%M:%S')}")

# Key Metrics Row
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        label="🎯 Total Threats",
        value=data['total_threats'],
        delta="+12 (24h)"
    )

with col2:
    st.metric(
        label="⚠️ Avg Threat Score",
        value=f"{data['avg_threat_score']:.2f}",
        delta="+0.08 (↑ High)"
    )

with col3:
    st.metric(
        label="📊 Sources Monitored",
        value=data['sources_monitored'],
        delta="+2 (New)"
    )

with col4:
    st.metric(
        label="🔥 Critical Alerts",
        value=data['severity_counts']['critical'],
        delta="+3 (24h)"
    )

# Main dashboard content
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("📊 Threat Landscape Overview")
    
    # Threat Categories Chart
    fig_categories = px.bar(
        x=list(data['threat_categories'].keys()),
        y=list(data['threat_categories'].values()),
        title="Threat Categories Distribution",
        color=list(data['threat_categories'].values()),
        color_continuous_scale="Reds"
    )
    fig_categories.update_layout(
        xaxis_title="Threat Category",
        yaxis_title="Number of Incidents",
        showlegend=False
    )
    st.plotly_chart(fig_categories, use_container_width=True)
    
    # Severity Distribution
    fig_severity = px.pie(
        values=list(data['severity_counts'].values()),
        names=list(data['severity_counts'].keys()),
        title="Threat Severity Distribution",
        color_discrete_map={
            'critical': '#dc3545',
            'high': '#fd7e14',
            'medium': '#ffc107',
            'low': '#28a745',
            'unknown': '#6c757d'
        }
    )
    st.plotly_chart(fig_severity, use_container_width=True)

with col2:
    st.subheader("🚨 High Priority Alerts")
    
    for threat in data['high_priority_threats']:
        severity_color = {
            'critical': '#dc3545',
            'high': '#fd7e14',
            'medium': '#ffc107',
            'low': '#28a745'
        }.get(threat['severity'], '#6c757d')
        
        st.markdown(f"""
        <div style="border-left: 4px solid {severity_color}; padding: 10px; margin: 10px 0; background: #f8f9fa; border-radius: 5px;">
            <h5 style="margin: 0; color: #333;">{threat['title'][:60]}...</h5>
            <p style="margin: 5px 0; color: #666; font-size: 0.9em;">
                <strong>Threat Score:</strong> {threat['threat_score']:.2f}<br>
                <strong>Categories:</strong> {', '.join(threat['categories'])}<br>
                <strong>Source:</strong> {threat['source']}
            </p>
        </div>
        """, unsafe_allow_html=True)

# Trending Threats Section
st.subheader("📈 Trending Threats")
trending_cols = st.columns(2)

with trending_cols[0]:
    st.write("**Emerging Threat Patterns:**")
    for i, threat in enumerate(data['trending_threats'][:2], 1):
        st.write(f"{i}. {threat}")

with trending_cols[1]:
    st.write("**Watch List:**")
    for i, threat in enumerate(data['trending_threats'][2:], 3):
        st.write(f"{i}. {threat}")

# Geographic Threat Map (Mock data for demo)
st.subheader("🌍 Geographic Threat Distribution")

# Mock geographic data
geo_data = pd.DataFrame({
    'country': ['United States', 'China', 'Russia', 'Germany', 'United Kingdom', 'France', 'Japan', 'Canada'],
    'threats': [45, 32, 28, 18, 15, 12, 10, 8],
    'lat': [39.8283, 35.8617, 61.5240, 51.1657, 55.3781, 46.6032, 36.2048, 56.1304],
    'lon': [-98.5795, 104.1954, 105.3188, 10.4515, -3.4360, 2.1301, 138.2529, -106.3468]
})

fig_map = px.scatter_geo(
    geo_data,
    lat='lat',
    lon='lon',
    size='threats',
    hover_name='country',
    hover_data={'threats': True},
    title="Global Threat Activity Hotspots",
    size_max=20
)
fig_map.update_layout(geo=dict(projection_type='natural earth'))
st.plotly_chart(fig_map, use_container_width=True)

# Actionable Insights Section
st.subheader("💡 Actionable Intelligence")

insights_col1, insights_col2 = st.columns(2)

with insights_col1:
    st.info("""
    **🎯 Immediate Actions Required:**
    - Patch critical vulnerabilities in enterprise software
    - Enhance email security filters for AI-powered phishing
    - Review and update incident response plans
    - Conduct tabletop exercises for ransomware scenarios
    """)

with insights_col2:
    st.warning("""
    **⚠️ Threat Landscape Trends:**
    - 34% increase in supply chain attacks
    - AI-enhanced social engineering campaigns
    - Targeting of cloud infrastructure accelerating
    - Cryptocurrency-related cyber crime surging
    """)

def generate_pdf_report(data):
    """Generate a comprehensive PDF report"""
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4)
    styles = getSampleStyleSheet()
    story = []
    
    # Title
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        spaceAfter=30,
        textColor=colors.darkblue,
        alignment=1  # Center alignment
    )
    story.append(Paragraph("🚨 Cyber Threat Intelligence Report", title_style))
    story.append(Spacer(1, 20))
    
    # Summary section
    story.append(Paragraph("Executive Summary", styles['Heading2']))
    summary_text = f"""
    <b>Report Generated:</b> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}<br/>
    <b>Total Threats Identified:</b> {data['total_threats']}<br/>
    <b>Average Threat Score:</b> {data['avg_threat_score']:.2f}/1.0<br/>
    <b>Critical Alerts:</b> {data['severity_counts']['critical']}<br/>
    <b>Sources Monitored:</b> {data['sources_monitored']}
    """
    story.append(Paragraph(summary_text, styles['Normal']))
    story.append(Spacer(1, 20))
    
    # High Priority Threats
    story.append(Paragraph("High Priority Threats", styles['Heading2']))
    for i, threat in enumerate(data['high_priority_threats'], 1):
        threat_text = f"""
        <b>{i}. {threat['title']}</b><br/>
        Threat Score: {threat['threat_score']:.2f}<br/>
        Categories: {', '.join(threat['categories'])}<br/>
        Severity: {threat['severity'].upper()}<br/>
        Source: {threat['source']}
        """
        story.append(Paragraph(threat_text, styles['Normal']))
        story.append(Spacer(1, 10))
    
    # Threat Categories Table
    story.append(Paragraph("Threat Categories Breakdown", styles['Heading2']))
    table_data = [['Category', 'Count']]
    for category, count in data['threat_categories'].items():
        table_data.append([category.replace('_', ' ').title(), str(count)])
    
    table = Table(table_data)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 14),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    story.append(table)
    story.append(Spacer(1, 20))
    
    # Trending Threats
    story.append(Paragraph("Trending Threats", styles['Heading2']))
    for i, trend in enumerate(data['trending_threats'], 1):
        story.append(Paragraph(f"{i}. {trend}", styles['Normal']))
    
    doc.build(story)
    buffer.seek(0)
    return buffer

def create_threat_chart_for_pdf(data):
    """Create a chart image for PDF inclusion"""
    plt.figure(figsize=(10, 6))
    categories = list(data['threat_categories'].keys())
    counts = list(data['threat_categories'].values())
    
    plt.bar(categories, counts, color='#dc3545', alpha=0.7)
    plt.title('Threat Categories Distribution', fontsize=16, fontweight='bold')
    plt.xlabel('Threat Category')
    plt.ylabel('Number of Incidents')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    
    # Save to bytes
    img_buffer = io.BytesIO()
    plt.savefig(img_buffer, format='png', dpi=300, bbox_inches='tight')
    img_buffer.seek(0)
    plt.close()
    return img_buffer

# Export functionality
st.subheader("📋 Export & Sharing")
export_col1, export_col2, export_col3 = st.columns(3)

with export_col1:
    if st.button("📊 Export Dashboard"):
        try:
            with st.spinner("Generating PDF report..."):
                pdf_buffer = generate_pdf_report(data)
                
                # Create download button
                st.download_button(
                    label="📄 Download PDF Report",
                    data=pdf_buffer.getvalue(),
                    file_name=f"threat_intelligence_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf",
                    mime="application/pdf"
                )
                st.success("PDF report generated successfully!")
        except Exception as e:
            st.error(f"Error generating PDF: {str(e)}")

with export_col2:
    if st.button("📧 Email Briefing"):
        # Generate a text summary for email
        email_content = f"""
        CYBER THREAT INTELLIGENCE BRIEFING
        Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
        
        SUMMARY:
        - Total Threats: {data['total_threats']}
        - Average Threat Score: {data['avg_threat_score']:.2f}
        - Critical Alerts: {data['severity_counts']['critical']}
        
        TOP THREATS:
        """
        for i, threat in enumerate(data['high_priority_threats'][:3], 1):
            email_content += f"{i}. {threat['title'][:60]}...\n"
        
        st.text_area("Email Content (Copy & Send):", email_content, height=200)
        st.success("Email briefing prepared!")

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; padding: 20px;">
    <p>🛡️ Cyber Threat Intelligence Pulse | Cardiff NLP Hackathon 2025</p>
    <p>Powered by AMPLYFI API & Advanced NLP Analytics</p>
</div>
""", unsafe_allow_html=True)
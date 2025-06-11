"""
HTML Templates for CyberPulse Application
Centralized HTML content for better maintainability
"""


def get_header_template():
    """Main application header template"""
    return """
    <div style="text-align: center; padding: 1rem 0; margin-bottom: 2rem;">
        <img src="data:image/png;base64,{logo_base64}" alt="CyberPulse Logo" style="height: 150px; width: auto;">
    </div>
    """


def get_ai_container_template():
    """AI Assistant container template"""
    return """
    <div class="ai-container">
        <h2>🤖 AI Threat Intelligence Assistant</h2>
        <p style="margin-bottom: 1rem; opacity: 0.9;">
            Ask me about cybersecurity threats in natural language
        </p>
    </div>
    """


def get_executive_summary_template(threat_level, total_threats, high_severity, top_threat, sentiment):
    """Executive summary template"""
    return f"""
    <div class="exec-summary">
        <h2>📊 Executive Threat Summary</h2>
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 1rem; margin-top: 1rem;">
            <div>
                <strong>Current Threat Level:</strong><br>
                {threat_level}
            </div>
            <div>
                <strong>Total Threats:</strong><br>
                {total_threats}
            </div>
            <div>
                <strong>High Severity:</strong><br>
                {high_severity}
            </div>
            <div>
                <strong>Top Threat:</strong><br>
                {top_threat}
            </div>
        </div>
        <div style="margin-top: 1.5rem; padding-top: 1rem; border-top: 1px solid rgba(255,255,255,0.3);">
            <strong>Key Recommendations:</strong>
            <ul style="margin-top: 0.5rem;">
                <li>{"Immediate attention required for high-severity threats" if high_severity > 3 else "Continue monitoring current threat levels"}</li>
                <li>{"Focus on " + top_threat + " mitigation strategies" if top_threat != "None" else "Maintain current security posture"}</li>
            </ul>
        </div>
    </div>
    """


def get_metric_card_template(value, label, icon="📊"):
    """Metric card template"""
    return f"""
    <div class="metric-card">
        <div class="metric-value">{icon} {value}</div>
        <div class="metric-label">{label}</div>
    </div>
    """


def get_alert_card_template(title, severity, category, source, summary, date, severity_class, emoji):
    """Alert card template"""
    return f"""
    <div class="alert-card {severity_class}">
        <h4 style="margin: 0 0 0.5rem 0; color: #2d3748;">
            {emoji} {title}
        </h4>
        <div style="display: flex; gap: 1rem; margin-bottom: 0.75rem; flex-wrap: wrap;">
            <span><strong>Severity:</strong> {severity}/10</span>
            <span><strong>Category:</strong> {category}</span>
            <span><strong>Source:</strong> {source}</span>
        </div>
        <p style="margin: 0.5rem 0; color: #4a5568; line-height: 1.5;">
            {summary[:300]}{"..." if len(summary) > 300 else ""}
        </p>
        <small style="color: #718096;">📅 {date}</small>
    </div>
    """


def get_welcome_screen_template():
    """Welcome screen template"""
    return """
    <div class="welcome-container">
        <h2>🎯 Welcome to CyberPulse AI</h2>
        <p style="font-size: 1.1rem; color: #4a5568; margin-bottom: 2rem;">
            Real-time cyber threat intelligence dashboard with AI-powered natural language queries
        </p>

        <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                    color: white; padding: 1.5rem; border-radius: 15px; margin-bottom: 2rem;">
            <h3 style="margin-top: 0;">🤖 Try the AI Assistant</h3>
            <p>Ask questions like:</p>
            <ul style="text-align: left; display: inline-block;">
                <li><em>"What ransomware attacks happened this week?"</em></li>
                <li><em>"Show me recent data breaches in healthcare"</em></li>
                <li><em>"Any phishing campaigns targeting banks?"</em></li>
                <li><em>"Latest zero-day vulnerabilities affecting Windows"</em></li>
                <li><em>"Supply chain attacks on software companies"</em></li>
            </ul>
        </div>

        <div class="feature-grid">
            <div class="feature-card">
                <h4>🧠 Natural Language Queries</h4>
                <p>Ask in plain English and get intelligent threat analysis</p>
            </div>
            <div class="feature-card">
                <h4>🔍 Smart Threat Extraction</h4>
                <p>AI identifies relevant cybersecurity terms automatically</p>
            </div>
            <div class="feature-card">
                <h4>📊 Real-time Scoring</h4>
                <p>Dynamic threat scoring based on sentiment and impact</p>
            </div>
            <div class="feature-card">
                <h4>📈 Interactive Visualizations</h4>
                <p>Rich charts and graphs for threat analysis</p>
            </div>
            <div class="feature-card">
                <h4>📋 Executive Summaries</h4>
                <p>Quick decision-making insights for leadership</p>
            </div>
            <div class="feature-card">
                <h4>🚨 Critical Alerts</h4>
                <p>Prioritized threat notifications for immediate action</p>
            </div>
        </div>
    </div>
    """


def get_threat_article_template(index, title, severity, date, source, summary, severity_class, emoji):
    """Individual threat article template"""
    return f"""
    <div class="alert-card {severity_class}">
        <h5 style="margin: 0 0 0.5rem 0; color: #2d3748;">
            {emoji} <strong>Article {index}: {title}</strong>
        </h5>
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); 
                    gap: 0.5rem; margin-bottom: 0.75rem;">
            <span><strong>Severity:</strong> {severity}/10</span>
            <span><strong>📅 Published:</strong> {date}</span>
            <span><strong>📰 Source:</strong> {source}</span>
        </div>
        <div style="margin-top: 1rem; padding-top: 0.75rem; border-top: 1px solid #e2e8f0;">
            <strong>Summary:</strong>
            <p style="margin: 0.5rem 0 0 0; color: #4a5568; line-height: 1.6;">
                {summary}
            </p>
        </div>
    </div>
    """


def get_no_threats_message_template():
    """No threats found message template"""
    return """
    <div style="background: linear-gradient(135deg, #ffeaa7 0%, #fab1a0 100%); 
                color: #2d3436; padding: 2rem; border-radius: 15px; text-align: center; margin: 1rem 0;">
        <h3>🤖 I didn't find any specific cybersecurity threats in your query</h3>
        <p style="margin-bottom: 1rem;">Try asking about topics like:</p>
        <ul style="list-style: none; padding: 0;">
            <li>💼 "What ransomware attacks happened recently?"</li>
            <li>🏥 "Show me data breaches this week"</li>
            <li>🏦 "Any phishing campaigns targeting banks?"</li>
            <li>🛡️ "Latest zero-day vulnerabilities"</li>
        </ul>
    </div>
    """


def get_ai_response_template(threat_count, threat_list, settings):
    """AI response template"""
    return f"""
    <div style="background: linear-gradient(135deg, #00b894 0%, #00cec9 100%); 
                color: white; padding: 1.5rem; border-radius: 15px; margin: 1rem 0;">
        <h4 style="margin: 0 0 1rem 0;">
            🤖 I found {threat_count} relevant cybersecurity topic{'s' if threat_count != 1 else ''} based on your query:
        </h4>
        <p><strong>Searching for:</strong> {threat_list}</p>
        <p><strong>Settings:</strong> Severity ≥{settings['severity_filter']}, {settings['articles_per_threat']} articles per threat</p>
        <p style="margin-bottom: 0; opacity: 0.9;">
            I'll fetch the latest threat intelligence for {'these topics' if threat_count > 1 else 'this topic'}. This may take a moment...
        </p>
    </div>
    """
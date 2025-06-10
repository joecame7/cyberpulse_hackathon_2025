import streamlit as st


def load_custom_css():
    """Load custom CSS styles for the application"""
    st.markdown("""
    <style>
        /* Import Google Fonts */
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');

        /* Global Styles */
        .main {
            font-family: 'Inter', sans-serif;
            background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
            min-height: 100vh;
        }

        /* Hide Streamlit default elements */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}

        /* Main Content Container */
        .block-container {
            padding-top: 1rem;
            padding-bottom: 2rem;
        }

        /* Header Styles */
        .main-header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 3rem 2rem;
            border-radius: 20px;
            margin-bottom: 2rem;
            color: white;
            text-align: center;
            box-shadow: 0 20px 60px rgba(102, 126, 234, 0.3);
            position: relative;
            overflow: hidden;
        }

        .main-header::before {
            content: '';
            position: absolute;
            top: -50%;
            right: -50%;
            width: 100%;
            height: 100%;
            background: radial-gradient(circle, rgba(255,255,255,0.1) 0%, transparent 70%);
            pointer-events: none;
        }

        .main-header h1 {
            font-size: 3rem;
            margin-bottom: 0.5rem;
            font-weight: 700;
            text-shadow: 0 2px 10px rgba(0,0,0,0.2);
            position: relative;
            z-index: 1;
        }

        .main-header p {
            font-size: 1.2rem;
            opacity: 0.95;
            margin: 0;
            position: relative;
            z-index: 1;
        }

        /* AI Assistant Container */
        .ai-container {
            background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
            padding: 2rem;
            border-radius: 20px;
            margin-bottom: 2rem;
            color: white;
            box-shadow: 0 15px 50px rgba(240, 147, 251, 0.3);
            position: relative;
            overflow: hidden;
        }

        .ai-container::before {
            content: '';
            position: absolute;
            top: -50%;
            left: -50%;
            width: 200%;
            height: 200%;
            background: radial-gradient(circle, rgba(255,255,255,0.1) 0%, transparent 70%);
            pointer-events: none;
            animation: float 6s ease-in-out infinite;
        }

        @keyframes float {
            0%, 100% { transform: translateY(0px) rotate(0deg); }
            50% { transform: translateY(-20px) rotate(180deg); }
        }

        .ai-container h2 {
            margin-top: 0;
            font-weight: 600;
            font-size: 1.8rem;
            position: relative;
            z-index: 1;
        }

        /* Metric Cards */
        .metric-card {
            background: rgba(255, 255, 255, 0.95);
            backdrop-filter: blur(10px);
            padding: 2rem;
            border-radius: 15px;
            border: 1px solid rgba(255, 255, 255, 0.2);
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
            transition: all 0.3s ease;
            text-align: center;
            position: relative;
            overflow: hidden;
        }

        .metric-card::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 4px;
            background: linear-gradient(90deg, #667eea, #764ba2);
        }

        .metric-card:hover {
            transform: translateY(-8px);
            box-shadow: 0 20px 60px rgba(0, 0, 0, 0.2);
        }

        .metric-value {
            font-size: 2.5rem;
            font-weight: 700;
            color: #2d3748;
            margin-bottom: 0.5rem;
        }

        .metric-label {
            font-size: 0.9rem;
            color: #718096;
            font-weight: 500;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }

        /* Alert Cards */
        .alert-card {
            background: rgba(255, 255, 255, 0.95);
            backdrop-filter: blur(10px);
            padding: 1.5rem;
            margin: 1rem 0;
            border-radius: 15px;
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
            transition: all 0.3s ease;
            border-left: 5px solid;
            position: relative;
            overflow: hidden;
        }

        .alert-card:hover {
            transform: translateX(8px);
            box-shadow: 0 8px 30px rgba(0, 0, 0, 0.15);
        }

        .alert-critical {
            border-left-color: #e53e3e;
            background: linear-gradient(135deg, rgba(229, 62, 62, 0.05) 0%, rgba(255, 255, 255, 0.95) 100%);
        }

        .alert-high {
            border-left-color: #ff8800;
            background: linear-gradient(135deg, rgba(255, 136, 0, 0.05) 0%, rgba(255, 255, 255, 0.95) 100%);
        }

        .alert-medium {
            border-left-color: #ffaa00;
            background: linear-gradient(135deg, rgba(255, 170, 0, 0.05) 0%, rgba(255, 255, 255, 0.95) 100%);
        }

        .alert-low {
            border-left-color: #38a169;
            background: linear-gradient(135deg, rgba(56, 161, 105, 0.05) 0%, rgba(255, 255, 255, 0.95) 100%);
        }

        /* Executive Summary */
        .exec-summary {
            background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
            color: white;
            padding: 2rem;
            border-radius: 20px;
            margin-bottom: 2rem;
            box-shadow: 0 15px 50px rgba(79, 172, 254, 0.3);
        }

        .exec-summary h2 {
            margin-top: 0;
            font-size: 1.8rem;
            font-weight: 600;
        }

        /* Welcome Screen */
        .welcome-container {
            text-align: center;
            padding: 4rem 2rem;
            background: rgba(255, 255, 255, 0.9);
            backdrop-filter: blur(10px);
            border-radius: 20px;
            margin: 2rem 0;
            box-shadow: 0 10px 40px rgba(0, 0, 0, 0.1);
        }

        .welcome-container h2 {
            color: #2d3748;
            font-size: 2.2rem;
            margin-bottom: 1rem;
        }

        .feature-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 1.5rem;
            margin-top: 2rem;
        }

        .feature-card {
            background: rgba(255, 255, 255, 0.8);
            padding: 1.5rem;
            border-radius: 15px;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
            transition: transform 0.3s ease;
        }

        .feature-card:hover {
            transform: translateY(-5px);
        }

        /* Custom Button Styles */
        .stButton > button {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            border-radius: 10px;
            padding: 0.5rem 2rem;
            font-weight: 600;
            transition: all 0.3s ease;
            box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
        }

        .stButton > button:hover {
            transform: translateY(-2px);
            box-shadow: 0 8px 25px rgba(102, 126, 234, 0.4);
        }

        /* Input Styles */
        .stTextInput > div > div > input {
            border-radius: 10px;
            border: 2px solid #e2e8f0;
            padding: 0.75rem 1rem;
            font-size: 1rem;
            transition: all 0.3s ease;
        }

        .stTextInput > div > div > input:focus {
            border-color: #667eea;
            box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
        }

        /* Sidebar Styles */
        .css-1d391kg {
            background: linear-gradient(180deg, #f8fafc 0%, #e2e8f0 100%);
        }

        /* Expandable Sections */
        .streamlit-expanderHeader {
            background: rgba(255, 255, 255, 0.9);
            border-radius: 10px;
            padding: 1rem;
            margin-bottom: 0.5rem;
            font-weight: 600;
        }

        /* Charts Container */
        .chart-container {
            background: rgba(255, 255, 255, 0.95);
            backdrop-filter: blur(10px);
            border-radius: 15px;
            padding: 1.5rem;
            margin: 1rem 0;
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
        }

        /* Loading Animations */
        @keyframes pulse {
            0%, 100% { opacity: 1; }
            50% { opacity: 0.5; }
        }

        .loading {
            animation: pulse 2s infinite;
        }

        /* Responsive Design */
        @media (max-width: 768px) {
            .main-header h1 {
                font-size: 2rem;
            }

            .main-header p {
                font-size: 1rem;
            }

            .metric-card {
                padding: 1rem;
            }

            .metric-value {
                font-size: 2rem;
            }
        }
    </style>
    """, unsafe_allow_html=True)


def get_severity_color_class(score):
    """Get CSS class based on threat severity score"""
    if score >= 8:
        return "alert-critical"
    elif score >= 6:
        return "alert-high"
    elif score >= 4:
        return "alert-medium"
    else:
        return "alert-low"


def get_severity_emoji(score):
    """Get emoji based on threat severity score"""
    if score >= 8:
        return "🔴"
    elif score >= 6:
        return "🟠"
    elif score >= 4:
        return "🟡"
    else:
        return "🟢"
# CyberPulse - Real-Time Threat Intelligence Platform

A sophisticated cybersecurity threat intelligence dashboard with AI-powered natural language queries, built with Streamlit.

## Table of Contents
- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [Running the Application](#running-the-application)
- [Usage Guide](#usage-guide)
- [Project Structure](#project-structure)
- [API Configuration](#api-configuration)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)

## Features

- **AI-Powered Natural Language Queries**: Ask questions in plain English about cybersecurity threats
- **Real-Time Threat Intelligence**: Fetch and analyse live threat data from external APIs
- **Smart Threat Extraction**: Automatically identifies relevant cybersecurity terms from user queries
- **Interactive Visualisations**: Rich charts and graphs for threat analysis using Plotly
- **Critical Alert System**: Prioritised threat notifications for immediate action
- **Executive Summaries**: Quick decision-making insights for leadership
- **Detailed Analysis**: In-depth threat analysis with sentiment scoring using NLTK
- **Configurable Dashboard**: Customisable severity filters and data sources
- **Responsive Design**: Modern UI with custom CSS styling and animations

## Prerequisites

Before running CyberPulse, ensure you have the following installed:

- **Python 3.8 or higher**
- **pip** (Python package installer)
- **Internet connection** (for API calls and NLTK data downloads)

## Installation

### 1. Clone the Repository

```bash
git clone <your-repository-url>
cd team3/cti_pulse
```

### 2. Create a Virtual Environment (Recommended)

```bash
# Create virtual environment
python -m venv cyberpulse_env

# Activate virtual environment
# On Windows:
cyberpulse_env\Scripts\activate

# On macOS/Linux:
source cyberpulse_env/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Verify Installation

```bash
python -c "import streamlit; print('Streamlit version:', streamlit.__version__)"
```

## Configuration

### API Configuration

The application uses an external threat intelligence API. The configuration is located in `config/settings.py`:

```python
API_CONFIG = {
    'url': "https://zfgp45ih7i.execute-api.eu-west-1.amazonaws.com/sandbox/api/search",
    'key': "LKM38746G38B7RB46GBER",
    'timeout': 30,
    'max_results': 100
}
```

**Note**: Update the API key and URL if you have different credentials.

### Logo Setup (Optional)

Place your logo file as `logo.png` in the main directory (`cti_pulse/logo.png`). If no logo is found, the application will use a text-based header as fallback.

### Threat Types Configuration

The application monitors various threat types defined in `config/settings.py`:

- Ransomware attacks
- Data breaches
- Cyber attacks
- Phishing campaigns
- Malware outbreaks
- Zero-day vulnerabilities
- Supply chain attacks
- DDoS attacks
- Insider threats
- APT groups

## Running the Application

### Standard Method

```bash
# Navigate to the cti_pulse directory
cd cti_pulse

# Run the application
streamlit run main.py
```

### Custom Port

```bash
# Run on a specific port
streamlit run main.py --server.port 8502
```

### Network Access

```bash
# Allow external access
streamlit run main.py --server.address 0.0.0.0
```

The application will open automatically in your default web browser at `http://localhost:8501`.

## Usage Guide

### 1. AI Assistant Interface

**Natural Language Queries**: Type questions like:
- "What ransomware attacks happened this week?"
- "Show me recent data breaches and phishing campaigns"
- "Any malware, ransomware, or zero-day vulnerabilities this month?"

**Quick Examples**: Use the provided buttons for common queries:
- Ransomware
- Data Breaches
- Multiple Threats

**AI Settings**: Adjust severity filter (1-10) and articles per threat (5-100)

### 2. Manual Dashboard

**Sidebar Controls**: 
- Select specific threat types to monitor
- Configure severity threshold
- Set number of articles per threat
- Test API connection

**Fetch Intelligence**: Click to retrieve data for selected threats

### 3. Dashboard Features

**Executive Summary**: High-level threat overview with current threat level and recommendations

**Key Metrics**: 
- Total threats detected
- Critical alerts count
- Average severity score
- Last update timestamp

**Visualisations**: 
- Threat severity distribution (bar chart)
- Timeline analysis (scatter plot)
- Source analysis (horizontal bar chart)

**Critical Alerts**: High-priority threats requiring immediate attention

**Detailed Analysis**: In-depth examination with:
- Sentiment analysis using NLTK VADER
- Threat scoring algorithm
- Article details with expandable views
- Source credibility assessment

## Project Structure

```
cti_pulse/
├── main.py                          # Main application entry point
├── requirements.txt                 # Python dependencies
├── logo.png                        # Application logo (optional)
├── assets/                         # UI assets and templates
│   ├── __init__.py
│   ├── styles.py                   # CSS styling and themes
│   └── templates.py                # HTML templates
├── components/                     # UI components
│   ├── __init__.py
│   ├── ai_assistant.py            # AI chat interface
│   ├── threat_analysis.py         # Detailed threat analysis
│   ├── ui_components.py           # General UI components
│   └── visualisations.py          # Charts and graphs (Plotly)
├── config/                        # Configuration files
│   ├── __init__.py
│   └── settings.py                # Application settings and threat types
└── utils/                         # Utility functions
    ├── __init__.py
    ├── api_client.py              # API communication
    ├── chatbot_utils.py           # AI response generation
    ├── data_processor.py          # Data processing utilities
    ├── nltk_setup.py              # NLTK initialisation
    └── threat_processor.py        # Threat analysis logic
```

## API Configuration

### Testing API Connection

1. Use the sidebar "Test API Connection" button
2. Check the status messages for connection verification
3. Ensure your internet connection is stable

### Modifying API Settings

Edit `config/settings.py` to update:

- **API URL**: Change the endpoint
- **API Key**: Update authentication credentials
- **Timeout**: Adjust request timeout (default: 30 seconds)
- **Max Results**: Set maximum results per query (default: 100)

### Threat Scoring Algorithm

The application uses a sophisticated threat scoring system that considers:

- **Base Severity**: Predefined threat type severity (1-5)
- **Sentiment Analysis**: NLTK VADER compound score
- **Recency Factor**: Age of the article (bonus for recent threats)
- **Keyword Impact**: Presence of high-impact security keywords
- **Source Credibility**: Boost for major security sources

## Troubleshooting

### Common Issues

1. **NLTK Download Errors**
   ```bash
   # Manual NLTK data download
   python -c "import nltk; nltk.download('vader_lexicon'); nltk.download('punkt'); nltk.download('stopwords')"
   ```

2. **Port Already in Use**
   ```bash
   # Use a different port
   streamlit run main.py --server.port 8502
   ```

3. **API Connection Issues**
   - Check internet connection
   - Verify API credentials in `config/settings.py`
   - Test API connection using the sidebar button
   - Check if the API endpoint is accessible

4. **Missing Dependencies**
   ```bash
   # Reinstall requirements
   pip install -r requirements.txt --upgrade
   ```

5. **Logo Not Displaying**
   - Ensure `logo.png` exists in the `cti_pulse` directory
   - Check file permissions
   - Application will fall back to text header if logo is missing

6. **Visualisation Issues**
   - Clear browser cache
   - Check if Plotly is properly installed
   - Ensure data is being fetched correctly

### Performance Optimisation

- **Reduce Articles per Threat**: Lower the number for faster processing
- **Increase Severity Filter**: Higher threshold filters out low-priority threats
- **Clear Browser Cache**: Refresh if visualisations aren't updating
- **Monitor API Rate Limits**: Be mindful of API request frequency

## Security Notes

- The application includes API credentials in the configuration file
- In production, consider using environment variables for sensitive data
- The API endpoint is external - ensure your network allows outbound HTTPS connections
- All data processing occurs locally - no sensitive data is stored externally

## Development

### Adding New Threat Types

Edit `config/settings.py` and add to `CYBER_THREATS`:

```python
"new_threat_type": {
    "severity": 4,
    "category": "Category Name",
    "synonyms": ["synonym1", "synonym2"]
}
```

### Customising UI

- **Styles**: Modify `assets/styles.py` - includes dark/light themes
- **Templates**: Update `assets/templates.py` for HTML components
- **Colours**: Adjust `COLOR_SCHEMES` in `config/settings.py`
- **Visualisations**: Modify chart configurations in `components/visualisations.py`

### Extending AI Capabilities

- **Threat Processing**: Enhance `utils/threat_processor.py` for better term extraction
- **Sentiment Analysis**: Customise sentiment thresholds in `config/settings.py`
- **Response Generation**: Improve AI responses in `utils/chatbot_utils.py`

## Dependencies

```txt
streamlit>=1.28.0       # Web application framework
requests>=2.31.0        # HTTP library for API calls
pandas>=2.0.0          # Data manipulation and analysis
matplotlib>=3.7.0       # Basic plotting capabilities
plotly>=5.15.0         # Interactive visualisations
nltk>=3.8.0            # Natural language processing
numpy>=1.24.0          # Numerical computing
```

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Test thoroughly with different query types
5. Commit your changes (`git commit -m 'Add amazing feature'`)
6. Push to the branch (`git push origin feature/amazing-feature`)
7. Submit a pull request

### Development Guidelines

- Follow PEP 8 style guidelines
- Add docstrings to new functions
- Test with various threat intelligence queries
- Ensure cross-platform compatibility
- Update documentation for new features

## Licence

This project is developed for educational purposes. Please ensure compliance with your organisation's security policies when using with real threat intelligence data.

## Support

For issues and questions:
1. Check the troubleshooting section
2. Review the API connection status
3. Ensure all dependencies are properly installed
4. Test with simple queries first

---

**Ready to monitor cyber threats? Run `streamlit run main.py` and start protecting your organisation!**

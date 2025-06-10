"""
Configuration settings for CyberPulse application
"""

# API Configuration
API_CONFIG = {
    'url': "https://zfgp45ih7i.execute-api.eu-west-1.amazonaws.com/sandbox/api/search",
    'key': "LKM38746G38B7RB46GBER",
    'timeout': 30,
    'max_results': 100
}

# Enhanced cyber threat keywords with severity ratings and synonyms
CYBER_THREATS = {
    "ransomware attack": {
        "severity": 5,
        "category": "Malware",
        "synonyms": ["ransomware", "crypto locker", "ransom malware", "encryption attack"]
    },
    "data breach": {
        "severity": 4,
        "category": "Data Security",
        "synonyms": ["data leak", "information breach", "data compromise", "data theft", "breach"]
    },
    "cyber attack": {
        "severity": 4,
        "category": "General Attack",
        "synonyms": ["cyberattack", "cyber incident", "security breach", "hack", "attack"]
    },
    "phishing campaign": {
        "severity": 3,
        "category": "Social Engineering",
        "synonyms": ["phishing", "email scam", "social engineering", "spear phishing", "business email compromise"]
    },
    "malware outbreak": {
        "severity": 4,
        "category": "Malware",
        "synonyms": ["malware", "virus", "trojan", "worm", "malicious software"]
    },
    "zero day vulnerability": {
        "severity": 5,
        "category": "Vulnerability",
        "synonyms": ["zero-day", "0day", "vulnerability", "exploit", "security flaw"]
    },
    "supply chain attack": {
        "severity": 5,
        "category": "Advanced Threat",
        "synonyms": ["supply chain", "third party attack", "vendor compromise"]
    },
    "ddos attack": {
        "severity": 3,
        "category": "Infrastructure",
        "synonyms": ["ddos", "denial of service", "dos attack", "botnet attack"]
    },
    "insider threat": {
        "severity": 4,
        "category": "Insider Risk",
        "synonyms": ["insider attack", "internal threat", "rogue employee", "privilege abuse"]
    },
    "apt group": {
        "severity": 5,
        "category": "Advanced Persistent Threat",
        "synonyms": ["apt", "advanced persistent threat", "nation state", "state sponsored"]
    }
}

# Cybersecurity keyword patterns for NLP extraction
CYBER_KEYWORDS = {
    'attacks': ['attack', 'exploit', 'breach', 'hack', 'compromise', 'intrusion', 'incident'],
    'malware': ['malware', 'virus', 'trojan', 'ransomware', 'spyware', 'adware', 'rootkit', 'worm'],
    'techniques': ['phishing', 'spoofing', 'social engineering', 'brute force', 'sql injection', 'xss'],
    'vulnerabilities': ['vulnerability', 'exploit', 'zero-day', '0day', 'cve', 'patch', 'flaw'],
    'threats': ['threat', 'risk', 'apt', 'insider', 'nation state', 'cybercriminal'],
    'infrastructure': ['ddos', 'botnet', 'c2', 'command and control', 'infrastructure'],
    'data': ['data', 'information', 'credentials', 'personal', 'sensitive', 'confidential']
}

# Threat scoring configuration
THREAT_SCORING = {
    'base_severity_weight': 1.0,
    'sentiment_weight': 2.0,
    'recency_weight': 1.5,
    'keyword_weight': 1.0,
    'source_weight': 0.5,
    'max_score': 10,
    'min_score': 1
}

# Sentiment thresholds
SENTIMENT_THRESHOLDS = {
    'very_negative': -0.5,
    'negative': -0.1,
    'neutral_low': -0.1,
    'neutral_high': 0.1,
    'positive': 0.1
}

# Recency scoring (in days)
RECENCY_SCORING = {
    'very_recent': 7,    # Last week - score 2
    'recent': 30,        # Last month - score 1
    'moderate': 90,      # Last 3 months - score 0.5
    'old': float('inf') # Older - score 0
}

# High impact keywords for threat scoring
HIGH_IMPACT_KEYWORDS = [
    'critical', 'widespread', 'global', 'massive', 'unprecedented',
    'emergency', 'urgent', 'severe', 'major', 'significant',
    'exploit', 'vulnerability', 'breach', 'compromise', 'attack'
]

# Major security sources for credibility boost
MAJOR_SECURITY_SOURCES = [
    'krebs', 'bleeping', 'dark reading', 'threatpost',
    'security', 'cyber', 'infosec', 'sans'
]

# UI Configuration
UI_CONFIG = {
    'max_critical_alerts': 5,
    'max_articles_display': 10,
    'chart_height': 400,
    'default_severity_filter': 3,
    'default_articles_per_threat': 15
}

# Color schemes
COLOR_SCHEMES = {
    'severity': {
        'critical': '#e53e3e',
        'high': '#ff8800',
        'medium': '#ffaa00',
        'low': '#38a169'
    },
    'categories': [
        '#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4',
        '#FFEAA7', '#DDA0DD', '#98D8C8', '#F093FB'
    ],
    'gradients': {
        'primary': 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
        'ai': 'linear-gradient(135deg, #f093fb 0%, #f5576c 100%)',
        'success': 'linear-gradient(135deg, #00b894 0%, #00cec9 100%)',
        'warning': 'linear-gradient(135deg, #ffeaa7 0%, #fab1a0 100%)',
        'executive': 'linear-gradient(135deg, #4facfe 0%, #00f2fe 100%)'
    }
}

# Application metadata
APP_METADATA = {
    'name': 'CyberPulse',
    'version': '2.0.0',
    'description': 'Real-Time Threat Intelligence Platform',
    'author': 'Security Team',
    'last_updated': '2024-12-10'
}
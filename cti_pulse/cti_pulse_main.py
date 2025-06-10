# -*- coding: utf-8 -*-
"""
Cyber Threat Intelligence Pulse
Cardiff NLP Hackathon 2025
Real-time cybersecurity threat monitoring and analysis
"""

import requests
import json
import pandas as pd
import nltk
import re
from collections import Counter
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import seaborn as sns
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from wordcloud import WordCloud
import numpy as np

# Download required NLTK data
nltk.download('vader_lexicon', quiet=True)
nltk.download('punkt', quiet=True)
nltk.download('stopwords', quiet=True)

class CyberThreatIntelligence:
    def __init__(self, api_key):
        self.api_url = "https://zfgp45ih7i.execute-api.eu-west-1.amazonaws.com/sandbox/api/search"
        self.api_key = api_key
        self.headers = {
            "Content-Type": "application/json",
            "x-api-key": self.api_key
        }
        self.sia = SentimentIntensityAnalyzer()
        
        # Define threat categories and keywords
        self.threat_categories = {
            'ransomware': ['ransomware', 'ransom attack', 'encryption malware', 'lockbit', 'conti', 'ryuk'],
            'apt_groups': ['APT', 'advanced persistent threat', 'nation state', 'state sponsored', 'lazarus', 'fancy bear'],
            'zero_day': ['zero-day', 'zero day', '0-day', 'unknown vulnerability', 'exploit in wild'],
            'supply_chain': ['supply chain attack', 'software supply chain', 'dependency attack', 'third party breach'],
            'data_breach': ['data breach', 'data leak', 'personal information', 'customer data', 'breach notification'],
            'malware': ['malware', 'trojan', 'botnet', 'backdoor', 'banking malware', 'stealer'],
            'phishing': ['phishing', 'spear phishing', 'business email compromise', 'BEC', 'social engineering'],
            'vulnerability': ['critical vulnerability', 'security flaw', 'patch', 'CVE-', 'remote code execution']
        }
        
        # Threat severity keywords
        self.severity_keywords = {
            'critical': ['critical', 'severe', 'urgent', 'immediate', 'emergency'],
            'high': ['high risk', 'significant', 'major', 'serious', 'widespread'],
            'medium': ['moderate', 'medium', 'notable', 'concerning'],
            'low': ['minor', 'low risk', 'limited', 'minimal']
        }
        
    def query_api(self, query_text, result_size=50, include_highlights=True, include_smart_tags=True):
        """Query the AMPLYFI API following official requirements"""
        # Ensure result_size doesn't exceed API limit
        if result_size > 100:
            result_size = 100
            print(f"Warning: result_size reduced to 100 (API limit)")
        
        payload = {
            "query_text": query_text,
            "result_size": result_size,
            "include_highlights": include_highlights,
            "include_smart_tags": include_smart_tags,
            "ai_answer": "basic"  # Only "basic" is allowed
        }
        
        try:
            response = requests.post(self.api_url, headers=self.headers, data=json.dumps(payload))
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"API Error: {e}")
            return None
    
    def clean_text(self, text):
        """Clean and normalize text for analysis"""
        if not isinstance(text, str):
            return ""
        
        # Remove URLs
        text = re.sub(r"http\S+|www\.\S+", "", text)
        # Convert to lowercase
        text = text.lower()
        # Keep only letters, numbers, and spaces
        text = re.sub(r"[^a-z0-9\s]", " ", text)
        # Collapse multiple spaces
        text = re.sub(r"\s+", " ", text).strip()
        return text
    
    def analyze_sentiment(self, text):
        """Analyze sentiment with cybersecurity context"""
        scores = self.sia.polarity_scores(text)
        
        # In cybersecurity, negative sentiment often indicates higher threat severity
        # Reverse the interpretation for threat analysis
        threat_score = abs(scores['compound'])  # Use absolute value for threat intensity
        
        if scores['compound'] <= -0.5:
            threat_level = 'High'
        elif scores['compound'] <= -0.1:
            threat_level = 'Medium'
        elif scores['compound'] >= 0.1:
            threat_level = 'Low'
        else:
            threat_level = 'Medium'
            
        return {
            'sentiment_scores': scores,
            'threat_score': threat_score,
            'threat_level': threat_level
        }
    
    def categorize_threat(self, text):
        """Categorize the threat based on keywords"""
        text_lower = text.lower()
        categories = []
        
        for category, keywords in self.threat_categories.items():
            if any(keyword in text_lower for keyword in keywords):
                categories.append(category)
        
        return categories if categories else ['unknown']
    
    def assess_severity(self, text):
        """Assess threat severity based on keywords"""
        text_lower = text.lower()
        
        for severity, keywords in self.severity_keywords.items():
            if any(keyword in text_lower for keyword in keywords):
                return severity
        
        return 'unknown'
    
    def collect_threat_intelligence(self, days_lookback=7):
        """Collect comprehensive threat intelligence"""
        print("🔍 Collecting Cyber Threat Intelligence...")
        
        all_data = []
        queries = [
            "ransomware attack 2025",
            "data breach notification", 
            "APT group campaign",
            "zero-day vulnerability",
            "malware campaign",
            "cybersecurity incident",
            "supply chain attack",
            "phishing campaign"
        ]
        
        for query in queries:
            print(f"   Querying: {query}")
            try:
                # Use API compliant parameters: result_size <=100, include_smart_tags=True
                response = self.query_api(
                    query_text=query, 
                    result_size=25,  # Well under 100 limit
                    include_highlights=True,
                    include_smart_tags=True
                )
                
                if response and 'results' in response:
                    for item in response['results']:
                        # Extract and clean data
                        summary = item.get('summary', '')
                        title = item.get('title', '')
                        
                        if not summary and not title:  # Skip empty items
                            continue
                            
                        clean_summary = self.clean_text(summary)
                        clean_title = self.clean_text(title)
                        
                        # Analyze the content
                        sentiment_analysis = self.analyze_sentiment(summary)
                        threat_categories = self.categorize_threat(summary + " " + title)
                        severity = self.assess_severity(summary + " " + title)
                        
                        # Extract metadata including smart_tags if available
                        smart_tags = item.get('smart_tags', {})
                        highlights = item.get('highlights', [])
                        
                        data_point = {
                            'query': query,
                            'title': title,
                            'summary': summary,
                            'clean_summary': clean_summary,
                            'clean_title': clean_title,
                            'url': item.get('url', ''),
                            'date': item.get('date', ''),
                            'source': item.get('source', 'Unknown'),
                            'smart_tags': smart_tags,  # AMPLYFI smart tags
                            'highlights': highlights,  # AMPLYFI highlights
                            'threat_categories': threat_categories,
                            'severity': severity,
                            'threat_score': sentiment_analysis['threat_score'],
                            'threat_level': sentiment_analysis['threat_level'],
                            'sentiment_compound': sentiment_analysis['sentiment_scores']['compound'],
                            'sentiment_pos': sentiment_analysis['sentiment_scores']['pos'],
                            'sentiment_neg': sentiment_analysis['sentiment_scores']['neg'],
                            'sentiment_neu': sentiment_analysis['sentiment_scores']['neu']
                        }
                        
                        all_data.append(data_point)
                        
            except Exception as e:
                print(f"   Error with query '{query}': {e}")
                continue
        
        df = pd.DataFrame(all_data)
        print(f"✅ Collected {len(df)} threat intelligence items")
        
        # Remove duplicates based on title similarity
        if not df.empty:
            df = df.drop_duplicates(subset=['title'], keep='first')
            print(f"✅ After deduplication: {len(df)} unique items")
            
        return df
    
    def generate_threat_briefing(self, df):
        """Generate automated threat briefing"""
        print("\n🚨 CYBER THREAT INTELLIGENCE BRIEFING")
        print("=" * 50)
        
        # Top threats by category
        threat_counts = Counter()
        for categories in df['threat_categories']:
            for category in categories:
                threat_counts[category] += 1
        
        print(f"\n📊 TOP THREAT CATEGORIES:")
        for threat, count in threat_counts.most_common(5):
            print(f"   • {threat.replace('_', ' ').title()}: {count} mentions")
        
        # Severity distribution
        severity_counts = df['severity'].value_counts()
        print(f"\n⚠️  THREAT SEVERITY BREAKDOWN:")
        for severity, count in severity_counts.items():
            print(f"   • {severity.title()}: {count} incidents")
        
        # High-threat items
        high_threats = df[df['threat_level'] == 'High'].head(3)
        print(f"\n🔥 TOP HIGH-THREAT ITEMS:")
        for idx, threat in high_threats.iterrows():
            print(f"   • {threat['title'][:80]}...")
            print(f"     Threat Score: {threat['threat_score']:.2f}")
            print(f"     Categories: {', '.join(threat['threat_categories'])}")
            print()
        
        # Recent trends
        print(f"\n📈 THREAT LANDSCAPE SUMMARY:")
        avg_threat_score = df['threat_score'].mean()
        print(f"   • Average Threat Intensity: {avg_threat_score:.2f}/1.0")
        print(f"   • Total Sources Monitored: {df['source'].nunique()}")
        print(f"   • Most Active Threat: {threat_counts.most_common(1)[0][0].replace('_', ' ').title()}")
        
        return {
            'threat_counts': threat_counts,
            'severity_counts': severity_counts,
            'avg_threat_score': avg_threat_score,
            'high_threats': high_threats
        }
    
    def create_visualizations(self, df):
        """Create threat intelligence visualizations"""
        plt.style.use('dark_background')
        fig, axes = plt.subplots(2, 2, figsize=(15, 12))
        fig.suptitle('Cyber Threat Intelligence Dashboard', fontsize=16, color='white')
        
        # 1. Threat Categories Distribution
        threat_counts = Counter()
        for categories in df['threat_categories']:
            for category in categories:
                threat_counts[category] += 1
        
        categories, counts = zip(*threat_counts.most_common(8))
        axes[0, 0].bar(categories, counts, color='#ff6b6b')
        axes[0, 0].set_title('Threat Categories', color='white')
        axes[0, 0].tick_params(axis='x', rotation=45, colors='white')
        axes[0, 0].tick_params(axis='y', colors='white')
        
        # 2. Threat Score Distribution
        axes[0, 1].hist(df['threat_score'], bins=20, color='#4ecdc4', alpha=0.7)
        axes[0, 1].set_title('Threat Score Distribution', color='white')
        axes[0, 1].set_xlabel('Threat Score', color='white')
        axes[0, 1].set_ylabel('Frequency', color='white')
        axes[0, 1].tick_params(colors='white')
        
        # 3. Severity Levels
        severity_counts = df['severity'].value_counts()
        colors = {'critical': '#ff4757', 'high': '#ff6348', 'medium': '#ffa502', 'low': '#26de81', 'unknown': '#778ca3'}
        severity_colors = [colors.get(sev, '#778ca3') for sev in severity_counts.index]
        
        axes[1, 0].pie(severity_counts.values, labels=severity_counts.index, autopct='%1.1f%%', 
                       colors=severity_colors, startangle=90)
        axes[1, 0].set_title('Threat Severity Distribution', color='white')
        
        # 4. Top Sources
        top_sources = df['source'].value_counts().head(10)
        axes[1, 1].barh(range(len(top_sources)), top_sources.values, color='#a55eea')
        axes[1, 1].set_yticks(range(len(top_sources)))
        axes[1, 1].set_yticklabels(top_sources.index, color='white')
        axes[1, 1].set_title('Top Information Sources', color='white')
        axes[1, 1].tick_params(colors='white')
        
        plt.tight_layout()
        return fig
    
    def export_threat_report(self, df, briefing_data, filename="threat_intelligence_report.json"):
        """Export comprehensive threat report"""
        report = {
            'generated_at': datetime.now().isoformat(),
            'summary': {
                'total_threats': len(df),
                'avg_threat_score': briefing_data['avg_threat_score'],
                'top_threat_category': list(briefing_data['threat_counts'].keys())[0],
                'sources_monitored': df['source'].nunique()
            },
            'threat_categories': dict(briefing_data['threat_counts']),
            'severity_breakdown': briefing_data['severity_counts'].to_dict(),
            'high_priority_threats': [
                {
                    'title': row['title'],
                    'threat_score': row['threat_score'],
                    'categories': row['threat_categories'],
                    'url': row['url']
                }
                for _, row in briefing_data['high_threats'].iterrows()
            ]
        }
        
        with open(filename, 'w') as f:
            json.dump(report, f, indent=2)
        
        print(f"📋 Threat report exported to {filename}")
        return report

# Main execution
if __name__ == "__main__":
    # Initialize the CTI system
    API_KEY = "LKM38746G38B7RB46GBER"
    cti = CyberThreatIntelligence(API_KEY)
    
    # Collect threat intelligence
    threat_data = cti.collect_threat_intelligence()
    
    # Generate briefing
    briefing = cti.generate_threat_briefing(threat_data)
    
    # Create visualizations
    fig = cti.create_visualizations(threat_data)
    plt.show()
    
    # Export report
    report = cti.export_threat_report(threat_data, briefing)
    
    print("\n🎯 Cyber Threat Intelligence Pulse Complete!")
    print("Ready for live demo and presentation!")
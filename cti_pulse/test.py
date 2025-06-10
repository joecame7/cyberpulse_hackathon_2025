import requests
import json
import pandas as pd
import matplotlib.pyplot as plt
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import nltk
import re
from datetime import datetime

nltk.download('vader_lexicon')

# API setup
API_URL = "https://zfgp45ih7i.execute-api.eu-west-1.amazonaws.com/sandbox/api/search"
API_KEY = "LKM38746G38B7RB46GBER"

headers = {
    "Content-Type": "application/json",
    "x-api-key": API_KEY
}

# Define cyber threat keywords to monitor
cyber_threats = [
    "ransomware attack",
    "data breach",
    "cyber attack",
    "phishing campaign", 
    "malware outbreak",
    "zero day vulnerability"
]

def get_threat_data(threat_keyword, num_results=20):
    """Get threat intelligence data for a specific keyword"""
    payload = {
        "query_text": threat_keyword,
        "result_size": num_results,
        "include_highlights": True,
        "include_smart_tags": True
    }
    
    response = requests.post(API_URL, headers=headers, data=json.dumps(payload))
    
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error fetching data for {threat_keyword}: {response.status_code}")
        return None

def analyze_threat_sentiment(threat_data):
    """Analyze sentiment of threat reports"""
    if not threat_data or 'results' not in threat_data:
        return []
    
    sia = SentimentIntensityAnalyzer()
    
    threat_analysis = []
    for article in threat_data['results']:
        summary = article.get('summary', '')
        title = article.get('title', '')
        
        # Clean the text
        clean_summary = re.sub(r"http\S+|www\.\S+", "", summary.lower())
        clean_summary = re.sub(r"[^a-z\s]", " ", clean_summary)
        clean_summary = re.sub(r"\s+", " ", clean_summary).strip()
        
        # Get sentiment
        sentiment = sia.polarity_scores(clean_summary)
        
        threat_analysis.append({
            'title': title,
            'summary': summary,
            'clean_summary': clean_summary,
            'sentiment_compound': sentiment['compound'],
            'sentiment_neg': sentiment['neg'],
            'published_date': article.get('published_date', ''),
            'source': article.get('source', ''),
            'highlights': article.get('highlights', [])
        })
    
    return threat_analysis

# Main execution
if __name__ == "__main__":
    print("🔍 Cyber Threat Intelligence Dashboard")
    print("=" * 50)
    
    all_threat_data = {}
    
    # Collect data for each threat type
    for threat in cyber_threats:
        print(f"Searching for: {threat}")
        data = get_threat_data(threat)
        if data:
            analysis = analyze_threat_sentiment(data)
            all_threat_data[threat] = {
                'raw_data': data,
                'analysis': analysis,
                'article_count': len(analysis)
            }
            print(f"  Found {len(analysis)} articles")
        else:
            print(f"  No data found")
    
    print("\n📊 Threat Intelligence Summary:")
    print("-" * 30)
    
    # Display summary statistics
    for threat, data in all_threat_data.items():
        if data['analysis']:
            avg_sentiment = sum(a['sentiment_compound'] for a in data['analysis']) / len(data['analysis'])
            negative_articles = sum(1 for a in data['analysis'] if a['sentiment_compound'] < -0.1)
            
            print(f"\n🚨 {threat.upper()}:")
            print(f"   Articles found: {data['article_count']}")
            print(f"   Average sentiment: {avg_sentiment:.3f}")
            print(f"   Negative reports: {negative_articles}")
            
            # Show most concerning article
            if data['analysis']:
                most_negative = min(data['analysis'], key=lambda x: x['sentiment_compound'])
                print(f"   Most concerning: {most_negative['title'][:60]}...")
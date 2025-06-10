import numpy as np
from collections import Counter


def generate_executive_summary(all_threat_data):
    """Generate executive summary data"""
    total_threats = sum(len(data['analysis']) for data in all_threat_data.values())
    high_severity = sum(1 for data in all_threat_data.values()
                        for article in data['analysis'] if article['threat_score'] >= 6)

    # Find trending threats
    threat_counts = {threat: len(data['analysis']) for threat, data in all_threat_data.items()}
    top_threat = max(threat_counts, key=threat_counts.get) if threat_counts else "None"

    # Average sentiment
    all_articles = [article for data in all_threat_data.values() for article in data['analysis']]
    avg_sentiment = np.mean([a['sentiment_compound'] for a in all_articles]) if all_articles else 0

    return {
        'total_threats': total_threats,
        'high_severity': high_severity,
        'top_threat': top_threat,
        'avg_sentiment': avg_sentiment
    }


def process_timeline_data(all_articles):
    """Process articles for timeline visualization"""
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
                    'title': article['title']
                })
            except:
                continue

    return timeline_data


def get_category_distribution(all_articles):
    """Get threat category distribution"""
    categories = [article['category'] for article in all_articles]
    return Counter(categories)


def get_severity_distribution(all_articles):
    """Get severity level distribution"""
    return {
        'Low (1-3)': sum(1 for a in all_articles if 1 <= a['threat_score'] <= 3),
        'Medium (4-6)': sum(1 for a in all_articles if 4 <= a['threat_score'] <= 6),
        'High (7-8)': sum(1 for a in all_articles if 7 <= a['threat_score'] <= 8),
        'Critical (9-10)': sum(1 for a in all_articles if 9 <= a['threat_score'] <= 10)
    }


def get_source_analysis(all_articles, top_n=10):
    """Get top sources analysis"""
    sources = [article['source'] for article in all_articles]
    source_counts = Counter(sources)
    return dict(source_counts.most_common(top_n))
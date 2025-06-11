import re
import streamlit as st
from datetime import datetime
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from config.settings import CYBER_THREATS, CYBER_KEYWORDS, THREAT_SCORING, HIGH_IMPACT_KEYWORDS, MAJOR_SECURITY_SOURCES


class ThreatProcessor:
    """Process and analyze threat intelligence data"""

    def __init__(self):
        self.sia = SentimentIntensityAnalyzer()

    def extract_cybersecurity_terms(self, user_query):
        """Extract cybersecurity-related terms from natural language query using NLP"""
        query_lower = user_query.lower()

        # Simple tokenization with fallback
        try:
            from nltk.corpus import stopwords
            from nltk.tokenize import word_tokenize

            stop_words = set(stopwords.words('english'))
            tokens = word_tokenize(query_lower)
            tokens = [token for token in tokens if token.isalpha() and token not in stop_words]
        except Exception as e:
            st.warning(f"Using simple tokenization: {str(e)}")
            simple_stop_words = {
                'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to',
                'for', 'of', 'with', 'by', 'is', 'are', 'was', 'were', 'be',
                'been', 'have', 'has', 'had', 'do', 'does', 'did', 'will',
                'would', 'could', 'should', 'may', 'might', 'can', 'what',
                'how', 'when', 'where', 'why', 'who', 'this', 'that', 'these', 'those'
            }
            tokens = re.findall(r'\b[a-zA-Z]+\b', query_lower)
            tokens = [token for token in tokens if token not in simple_stop_words and len(token) > 2]

        # Find matching cybersecurity terms
        confidence_scores = {}

        # Check for direct matches with threat keywords and synonyms
        for threat_name, threat_info in CYBER_THREATS.items():
            score = 0

            # Check main threat name
            threat_words = threat_name.split()
            if all(word in query_lower for word in threat_words):
                score += 15
            elif any(word in query_lower for word in threat_words):
                specific_words = [word for word in threat_words if
                                  word not in ['attack', 'campaign', 'outbreak', 'group']]
                if any(word in query_lower for word in specific_words):
                    score += 8
                else:
                    score += 2

            # Check synonyms
            for synonym in threat_info.get('synonyms', []):
                if synonym in query_lower:
                    if synonym in ['ransomware', 'phishing', 'ddos', 'apt']:
                        score += 12
                    else:
                        score += 6
                elif any(word in synonym.split() for word in tokens):
                    score += 2

            if score > 0:
                confidence_scores[threat_name] = score

        # Check for general cybersecurity keywords
        for category, keywords in CYBER_KEYWORDS.items():
            for keyword in keywords:
                if keyword in query_lower:
                    # Don't skip if there are existing high scores - allow multiple threats
                    self._map_keyword_to_threat(keyword, category, confidence_scores)

        # Sort and return multiple matches (changed logic)
        sorted_threats = sorted(confidence_scores.items(), key=lambda x: x[1], reverse=True)

        if sorted_threats:
            # Return multiple threats based on relevance
            relevant_threats = []
            
            # Always include high confidence matches (score >= 8)
            high_confidence = [threat for threat, score in sorted_threats if score >= 8]
            relevant_threats.extend(high_confidence)
            
            # If we have high confidence matches, also include medium confidence ones
            if high_confidence:
                medium_confidence = [threat for threat, score in sorted_threats 
                                   if 5 <= score < 8 and threat not in relevant_threats]
                relevant_threats.extend(medium_confidence[:2])  # Add up to 2 medium confidence
            else:
                # If no high confidence, take top medium confidence matches
                medium_confidence = [threat for threat, score in sorted_threats if score >= 5]
                relevant_threats.extend(medium_confidence[:3])  # Take top 3
            
            # Remove duplicates while preserving order
            seen = set()
            final_threats = []
            for threat in relevant_threats:
                if threat not in seen:
                    seen.add(threat)
                    final_threats.append(threat)
            
            return final_threats[:5]  # Limit to top 5 threats max

        return []

    def _map_keyword_to_threat(self, keyword, category, confidence_scores):
        """Map keywords to specific threat types"""
        if category == 'malware' and keyword == 'ransomware':
            confidence_scores['ransomware attack'] = confidence_scores.get('ransomware attack', 0) + 10
        elif category == 'malware' and keyword in ['virus', 'trojan', 'worm']:
            confidence_scores['malware outbreak'] = confidence_scores.get('malware outbreak', 0) + 4
        elif category == 'attacks' and keyword == 'breach':
            confidence_scores['data breach'] = confidence_scores.get('data breach', 0) + 8
        elif category == 'techniques' and keyword == 'phishing':
            confidence_scores['phishing campaign'] = confidence_scores.get('phishing campaign', 0) + 10
        elif category == 'vulnerabilities' and keyword in ['zero-day', '0day']:
            confidence_scores['zero day vulnerability'] = confidence_scores.get('zero day vulnerability', 0) + 8
        elif category == 'infrastructure' and keyword == 'ddos':
            confidence_scores['ddos attack'] = confidence_scores.get('ddos attack', 0) + 10
        elif category == 'attacks' and keyword == 'attack':
            if not any(score > 8 for score in confidence_scores.values()):
                confidence_scores['cyber attack'] = confidence_scores.get('cyber attack', 0) + 3

    def analyze_threat_sentiment(self, threat_data, threat_keyword):
        """Enhanced threat analysis with scoring"""
        if not threat_data or 'results' not in threat_data:
            return []

        threat_analysis = []

        for article in threat_data['results']:
            summary = article.get('summary', '')
            title = article.get('title', '')

            # Clean the text
            clean_summary = re.sub(r"http\S+|www\.\S+", "", summary.lower())
            clean_summary = re.sub(r"[^a-z\s]", " ", clean_summary)
            clean_summary = re.sub(r"\s+", " ", clean_summary).strip()

            # Get sentiment
            sentiment = self.sia.polarity_scores(clean_summary)

            # Get date and source
            published_date = article.get('timestamp', 'Date not available')
            source = self._extract_source(article.get('url', ''))

            analysis_item = {
                'title': title,
                'summary': summary,
                'clean_summary': clean_summary,
                'sentiment_compound': sentiment['compound'],
                'sentiment_neg': sentiment['neg'],
                'published_date': published_date,
                'source': source,
                'highlights': article.get('highlights', []),
                'threat_keyword': threat_keyword,
                'category': CYBER_THREATS.get(threat_keyword, {}).get("category", "Unknown"),
                'raw_article': article
            }

            # Calculate threat score
            analysis_item['threat_score'] = self._calculate_threat_score(analysis_item, threat_keyword)

            threat_analysis.append(analysis_item)

        return sorted(threat_analysis, key=lambda x: x['threat_score'], reverse=True)

    def _extract_source(self, url):
        """Extract source from URL"""
        if not url:
            return 'Source not available'

        try:
            import urllib.parse
            parsed_url = urllib.parse.urlparse(url)
            return parsed_url.netloc.replace('www.', '')
        except:
            return url

    def _calculate_threat_score(self, article, threat_keyword):
        """Calculate threat severity score based on multiple factors"""
        base_severity = CYBER_THREATS.get(threat_keyword, {}).get("severity", 3)

        # Sentiment factor
        sentiment_score = 0
        if article['sentiment_compound'] < -0.5:
            sentiment_score = 3
        elif article['sentiment_compound'] < -0.1:
            sentiment_score = 2
        elif article['sentiment_compound'] < 0.1:
            sentiment_score = 1
        else:
            sentiment_score = 0

        # Recency factor
        recency_score = self._calculate_recency_score(article['published_date'])

        # High impact keywords
        keyword_score = 0
        for keyword in HIGH_IMPACT_KEYWORDS:
            if keyword in article['clean_summary']:
                keyword_score += 0.5
        keyword_score = min(keyword_score, 3)

        # Source credibility boost
        source_boost = 0
        source_lower = article['source'].lower()
        if any(source in source_lower for source in MAJOR_SECURITY_SOURCES):
            source_boost = 1

        # Calculate final score
        final_score = base_severity + sentiment_score + recency_score + keyword_score + source_boost

        # Normalize to 1-10 scale
        final_score = min(10, max(1, final_score))

        return final_score

    def _calculate_recency_score(self, published_date):
        """Calculate recency score based on publication date"""
        recency_score = 0
        try:
            if published_date != 'Date not available':
                if 'T' in published_date:
                    pub_date = datetime.fromisoformat(published_date.replace('Z', '+00:00'))
                else:
                    pub_date = datetime.strptime(published_date[:10], '%Y-%m-%d')

                days_old = (datetime.now(pub_date.tzinfo) - pub_date).days
                if days_old <= 7:
                    recency_score = 2
                elif days_old <= 30:
                    recency_score = 1
                elif days_old <= 90:
                    recency_score = 0.5
                else:
                    recency_score = 0
            else:
                recency_score = 0.5
        except:
            recency_score = 0.5

        return recency_score
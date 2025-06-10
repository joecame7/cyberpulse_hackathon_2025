import requests
import json
import streamlit as st
from config.settings import API_CONFIG


class APIClient:
    """API client for threat intelligence data"""

    def __init__(self):
        self.api_url = API_CONFIG['url']
        self.api_key = API_CONFIG['key']
        self.timeout = API_CONFIG['timeout']
        self.max_results = API_CONFIG['max_results']

        self.headers = {
            "Content-Type": "application/json",
            "x-api-key": self.api_key
        }

    def get_threat_data(self, threat_keyword, num_results=20):
        """Get threat intelligence data for a specific keyword - with proper error handling"""
        payload = {
            "query_text": threat_keyword,
            "result_size": min(num_results, self.max_results),
            "include_highlights": True,
            "include_smart_tags": True
        }

        try:
            st.write(f"🔍 Fetching data for: {threat_keyword}")
            response = requests.post(
                self.api_url,
                headers=self.headers,
                data=json.dumps(payload),
                timeout=self.timeout
            )

            st.write(f"Status code: {response.status_code}")

            if response.status_code == 200:
                data = response.json()
                st.write(f"✅ Successfully fetched data for {threat_keyword}")
                return data
            else:
                st.error(f"❌ API Error for {threat_keyword}: {response.status_code}")
                st.write(f"Response: {response.text}")
                return None

        except requests.exceptions.Timeout:
            st.error(f"⏳ Timeout for {threat_keyword}")
            return None
        except requests.exceptions.RequestException as e:
            st.error(f"❌ Network error for {threat_keyword}: {str(e)}")
            return None

    def test_connection(self):
        """Test API connection"""
        try:
            test_data = self.get_threat_data("cyber attack", 5)
            return test_data is not None
        except Exception as e:
            st.error(f"API connection test failed: {str(e)}")
            return False
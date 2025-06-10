"""
Simple API Test for AMPLYFI
Run this first to check if the API is working
"""

import requests
import json
import time

API_URL = "https://zfgp45ih7i.execute-api.eu-west-1.amazonaws.com/sandbox/api/search"
API_KEY = "LKM38746G38B7RB46GBER"

headers = {
    "Content-Type": "application/json",
    "x-api-key": API_KEY
}

def test_simple_query():
    """Test a simple query to check API status"""
    payload = {
        "query_text": "cybersecurity",
        "result_size": 5,
        "include_highlights": True,
        "include_smart_tags": True,
        "ai_answer": "basic"
    }
    
    print("🧪 Testing AMPLYFI API connection...")
    print(f"📡 Query: {payload['query_text']}")
    
    start_time = time.time()
    
    try:
        response = requests.post(API_URL, headers=headers, data=json.dumps(payload), timeout=10)
        elapsed = time.time() - start_time
        
        print(f"⏱️  Response time: {elapsed:.2f}s")
        print(f"📊 Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            if 'results' in data:
                print(f"✅ Success! Retrieved {len(data['results'])} results")
                if data['results']:
                    print(f"📝 Sample title: {data['results'][0].get('title', 'No title')[:80]}...")
                return True
            else:
                print("❌ No results in response")
                return False
        else:
            print(f"❌ HTTP Error: {response.status_code}")
            print(f"Response: {response.text[:200]}...")
            return False
            
    except requests.exceptions.Timeout:
        elapsed = time.time() - start_time
        print(f"⏰ Timeout after {elapsed:.2f}s")
        return False
    except Exception as e:
        elapsed = time.time() - start_time
        print(f"❌ Error after {elapsed:.2f}s: {e}")
        return False

if __name__ == "__main__":
    print("=" * 50)
    print("AMPLYFI API Test")
    print("=" * 50)
    
    success = test_simple_query()
    
    print("\n" + "=" * 50)
    if success:
        print("✅ API is working! You can run the dashboard.")
    else:
        print("❌ API issues detected. Dashboard will use demo data.")
    print("=" * 50)

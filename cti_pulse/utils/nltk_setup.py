import streamlit as st
import nltk

@st.cache_resource
def download_nltk_data():
    """Download required NLTK data if not present"""
    try:
        nltk.data.find('vader_lexicon')
        nltk.data.find('punkt_tab')
        nltk.data.find('stopwords')
    except LookupError:
        try:
            nltk.download('vader_lexicon', quiet=True)
            nltk.download('punkt_tab', quiet=True)
            nltk.download('punkt', quiet=True)  # Fallback
            nltk.download('stopwords', quiet=True)
            st.success("✅ NLTK data downloaded successfully")
        except Exception as e:
            st.warning(f"⚠️ Could not download NLTK data: {str(e)}")
            st.info("The application will use fallback text processing methods.")

def initialize_nltk():
    """Initialize NLTK with error handling"""
    try:
        download_nltk_data()
        return True
    except Exception as e:
        st.error(f"❌ NLTK initialization failed: {str(e)}")
        return False
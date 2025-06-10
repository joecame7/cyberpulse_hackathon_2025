def generate_chatbot_response(matched_threats, user_query):
    """Generate a conversational response based on matched threats"""
    if not matched_threats:
        return """
        🤖 I didn't find any specific cybersecurity threats in your query. 

        Try asking about topics like:
        - "What ransomware attacks happened recently?"
        - "Show me data breaches this week"
        - "Any phishing campaigns targeting banks?"
        - "Latest zero-day vulnerabilities"
        """

    threat_list = ", ".join([threat.title() for threat in matched_threats[:3]])

    response = f"""
    🤖 **I found {len(matched_threats)} relevant cybersecurity topic(s) based on your query:**

    **Searching for:** {threat_list}

    I'll fetch the latest threat intelligence for these topics. This may take a moment...
    """

    return response
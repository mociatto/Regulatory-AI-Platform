import google.generativeai as genai

def analyze_article_with_ai(article_text, model):
    """
    Analyze an article using Google Generative AI to determine if it's relevant to pharmaceutical regulatory activities.
    
    Args:
        article_text (str): The full text content of the article
        model: The configured Google Generative AI model object
    
    Returns:
        str: AI analysis of the article's relevance to pharmaceutical regulatory activities
    """
    prompt = f"""
    Analyze the following article and determine if it's relevant to pharmaceutical regulatory activities, 
    particularly focusing on drug approvals, safety concerns, regulatory decisions, or policy changes 
    related to pharmaceutical products.
    
    Article text:
    {article_text}
    
    Please provide a clear "Yes" or "No" answer followed by a brief explanation of why this article 
    is or isn't relevant to pharmaceutical regulatory activities. Focus on regulatory aspects, 
    not general health news.
    """
    
    try:
        response = model.generate_content(prompt).text
        return response
    except Exception as e:
        return f"Error during AI analysis: {e}" 
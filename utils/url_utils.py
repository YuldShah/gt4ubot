import urllib.parse

def create_google_search_url(query: str) -> str:
    """
    Create a Google search URL from a text query.
    Encodes the query properly for URLs.
    
    Args:
        query: The search query text
        
    Returns:
        str: A properly formatted Google search URL
    """
    base_url = "https://www.google.com/search?q="
    encoded_query = urllib.parse.quote_plus(query)
    return base_url + encoded_query
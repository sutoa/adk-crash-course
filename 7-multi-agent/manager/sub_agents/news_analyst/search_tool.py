import os
import requests
from google.adk.tools.tool_context import ToolContext


def search_news(query: str, tool_context: ToolContext) -> dict:
    """Search for news articles using Serper API.
    
    Args:
        query: The search query for news articles
        tool_context: Context for accessing session state
        
    Returns:
        Dictionary containing search results
    """
    serper_api_key = os.getenv("SERPER_API_KEY")
    
    if not serper_api_key:
        return {
            "status": "error",
            "message": "SERPER_API_KEY not found in environment variables"
        }
    
    url = "https://google.serper.dev/search"
    headers = {
        "X-API-KEY": serper_api_key,
        "Content-Type": "application/json"
    }
    
    payload = {
        "q": query,
        "type": "news",
        "num": 5
    }
    
    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        
        data = response.json()
        
        # Extract relevant information
        results = []
        if "news" in data:
            for item in data["news"]:
                results.append({
                    "title": item.get("title", ""),
                    "snippet": item.get("snippet", ""),
                    "link": item.get("link", ""),
                    "date": item.get("date", ""),
                    "source": item.get("source", "")
                })
        
        return {
            "status": "success",
            "query": query,
            "results": results,
            "total_results": len(results)
        }
        
    except requests.exceptions.RequestException as e:
        return {
            "status": "error",
            "message": f"Search request failed: {str(e)}"
        }
    except Exception as e:
        return {
            "status": "error",
            "message": f"Unexpected error: {str(e)}"
        } 
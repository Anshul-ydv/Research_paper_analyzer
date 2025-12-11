import requests
import xml.etree.ElementTree as ET
from typing import List, Dict, Any
from dataclasses import dataclass
from google.adk.tools import Tool

@dataclass
class ArxivDocument:
    id: str
    title: str
    summary: str
    url: str
    authors: List[str]
    published: str

class ArxivMCPTool:
    """MCP-compliant tool for querying the arXiv API."""
    
    def __init__(self):
        self.base_url = "http://export.arxiv.org/api/query"
        self.user_agent = "Research-Agent-ADK/1.0"

    async def execute(self, query: str, max_results: int = 3) -> List[Dict[str, Any]]:
        """Execute a search query against arXiv and return structured results."""
        if not query.strip():
            return []

        # Construct arXiv API query
        params = {
            'search_query': f'all:{query}',
            'start': 0,
            'max_results': max_results
        }
        headers = {'User-Agent': self.user_agent}

        try:
            response = requests.get(self.base_url, params=params, headers=headers)
            response.raise_for_status()
            
            # Parse XML response
            root = ET.fromstring(response.text)
            namespace = {'atom': 'http://www.w3.org/2005/Atom'}
            
            results = []
            for entry in root.findall('atom:entry', namespace):
                doc = ArxivDocument(
                    id=entry.find('atom:id', namespace).text,
                    title=entry.find('atom:title', namespace).text.strip(),
                    summary=entry.find('atom:summary', namespace).text.strip(),
                    url=entry.find('atom:id', namespace).text,
                    authors=[author.find('atom:name', namespace).text 
                            for author in entry.findall('atom:author', namespace)],
                    published=entry.find('atom:published', namespace).text
                )
                
                results.append({
                    'id': doc.id,
                    'title': doc.title,
                    'summary': doc.summary,
                    'url': doc.url,
                    'authors': doc.authors,
                    'published': doc.published
                })
            
            return results
            
        except Exception as e:
            print(f"Error querying arXiv: {e}")
            return []

def create_arxiv_tool() -> Tool:
    """Create an ADK Tool instance for arXiv search."""
    arxiv = ArxivMCPTool()
    return Tool(
        name="search_papers",
        description="Search academic papers on arXiv",
        function=arxiv.execute
    )
"""
Document Processing Service
- Fetches API documentation from URLs
- Parses HTML/Markdown
- Chunks documentation for analysis
"""

import aiohttp
from bs4 import BeautifulSoup
import re
from typing import List, Dict


async def fetch_documentation(url: str) -> str:
    """
    Fetch documentation from URL
    
    Args:
        url: URL to API documentation
        
    Returns:
        Raw HTML content
    """
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                      "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.9",
        "Cache-Control": "no-cache",
    }

    last_error = None
    timeout = aiohttp.ClientTimeout(total=30)

    try:
        async with aiohttp.ClientSession(headers=headers) as session:
            for _ in range(2):
                try:
                    async with session.get(url, timeout=timeout, allow_redirects=True) as response:
                        if response.status == 200:
                            return await response.text()
                        last_error = f"Failed to fetch: HTTP {response.status}"
                except Exception as e:
                    last_error = str(e)
        raise Exception(last_error or "Unknown fetch error")
    except Exception as e:
        raise Exception(f"Error fetching documentation: {str(e)}")


def parse_html_docs(html: str) -> str:
    """
    Parse HTML documentation and extract text
    
    Args:
        html: Raw HTML content
        
    Returns:
        Cleaned text content
    """
    soup = BeautifulSoup(html, 'html.parser')
    
    # Remove script and style tags
    for script in soup(["script", "style"]):
        script.decompose()
    
    # Get text
    text = soup.get_text()
    
    # Clean up whitespace
    lines = (line.strip() for line in text.splitlines())
    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
    text = '\n'.join(chunk for chunk in chunks if chunk)
    
    return text


def chunk_documentation(text: str, chunk_size: int = 2000) -> List[str]:
    """
    Split documentation into chunks
    
    Args:
        text: Full documentation text
        chunk_size: Size of each chunk
        
    Returns:
        List of text chunks
    """
    chunks = []
    
    # Split by newlines first
    lines = text.split('\n')
    current_chunk = ""
    
    for line in lines:
        if len(current_chunk) + len(line) < chunk_size:
            current_chunk += line + "\n"
        else:
            if current_chunk:
                chunks.append(current_chunk)
            current_chunk = line + "\n"
    
    if current_chunk:
        chunks.append(current_chunk)
    
    return chunks


def extract_headers(text: str) -> List[Dict]:
    """
    Extract headers from documentation
    
    Args:
        text: Documentation text
        
    Returns:
        List of headers with hierarchy
    """
    headers = []
    lines = text.split('\n')
    
    for line in lines:
        # Markdown headers
        if line.startswith('#'):
            level = len(line) - len(line.lstrip('#'))
            title = line.lstrip('#').strip()
            headers.append({
                'level': level,
                'title': title,
                'type': 'markdown'
            })
        # HTML headers
        elif re.match(r'^<h[1-6]', line):
            match = re.search(r'<h([1-6])>(.+?)</h\1>', line)
            if match:
                headers.append({
                    'level': int(match.group(1)),
                    'title': match.group(2),
                    'type': 'html'
                })
    
    return headers


def extract_code_blocks(text: str) -> List[Dict]:
    """
    Extract code blocks from documentation
    
    Args:
        text: Documentation text
        
    Returns:
        List of code blocks with language
    """
    code_blocks = []
    
    # Markdown code blocks
    pattern = r'```(\w*)\n(.*?)\n```'
    for match in re.finditer(pattern, text, re.DOTALL):
        language = match.group(1) or 'unknown'
        code = match.group(2)
        code_blocks.append({
            'language': language,
            'code': code,
            'format': 'markdown'
        })
    
    return code_blocks

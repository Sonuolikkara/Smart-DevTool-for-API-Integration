"""
API Analysis Service
- Extracts endpoints from documentation
- Detects authentication methods
- Identifies request/response formats
"""

import re
from typing import List, Dict, Optional


def extract_endpoints(text: str) -> List[Dict]:
    """
    Extract API endpoints from documentation text
    
    Args:
        text: API documentation text
        
    Returns:
        List of endpoints with method, path, description
    """
    endpoints = []
    
    # Pattern 1: REST endpoints (GET /path, POST /path, etc)
    pattern1 = r'(GET|POST|PUT|DELETE|PATCH|HEAD|OPTIONS)\s+([/\w\-{}_:\.]+)'
    
    for match in re.finditer(pattern1, text, re.IGNORECASE):
        method = match.group(1).upper()
        path = match.group(2)
        
        # Get next line as description
        start_pos = match.end()
        next_newline = text.find('\n', start_pos)
        description = text[start_pos:next_newline].strip() if next_newline > 0 else ""
        
        endpoints.append({
            'method': method,
            'path': path,
            'description': description[:100],  # First 100 chars
            'source': 'rest_pattern'
        })
    
    # Pattern 2: Endpoint descriptions like "List users", "Create user", etc
    pattern2 = r'(List|Get|Create|Update|Delete|Fetch|Search|Query)\s+([A-Za-z\s]+)\s*(?:Endpoint|API)?'
    
    for match in re.finditer(pattern2, text, re.IGNORECASE):
        action = match.group(1)
        resource = match.group(2).strip()
        
        # Guess method based on action
        method_map = {
            'list': 'GET',
            'get': 'GET',
            'fetch': 'GET',
            'search': 'GET',
            'query': 'GET',
            'create': 'POST',
            'update': 'PUT',
            'delete': 'DELETE'
        }
        
        method = method_map.get(action.lower(), 'GET')
        
        # Generate path
        path = f"/{resource.lower().replace(' ', '_')}"
        
        endpoints.append({
            'method': method,
            'path': path,
            'description': f"{action} {resource}",
            'source': 'description_pattern'
        })
    
    # Remove duplicates
    unique_endpoints = []
    seen = set()
    
    for ep in endpoints:
        key = (ep['method'], ep['path'])
        if key not in seen:
            seen.add(key)
            unique_endpoints.append(ep)
    
    return unique_endpoints


def extract_parameters(text: str, endpoint_path: str = "") -> List[Dict]:
    """
    Extract parameters from documentation
    
    Args:
        text: Documentation text around endpoint
        endpoint_path: The endpoint path for context
        
    Returns:
        List of parameters with name, type, required flag
    """
    parameters = []
    
    # Pattern: param_name (type, required)
    pattern = r'(\w+)\s*(?:\(|:)\s*(?:(string|integer|number|boolean|array|object)[,\)])'
    
    for match in re.finditer(pattern, text, re.IGNORECASE):
        param_name = match.group(1)
        param_type = match.group(2).lower()
        
        # Check if marked as required
        required = 'required' in text[max(0, match.start()-50):match.end()+50]
        
        parameters.append({
            'name': param_name,
            'type': param_type,
            'required': required
        })
    
    return parameters


def detect_auth_method(text: str) -> Dict:
    """
    Detect authentication method from documentation
    
    Args:
        text: API documentation text
        
    Returns:
        Authentication method details
    """
    text_lower = text.lower()
    
    # Check for different auth methods
    auth_types = {
        'bearer': r'bearer\s+token',
        'api_key': r'api[_\s]?key|x-api-key',
        'oauth': r'oauth\s*2|authorization.*code',
        'basic': r'basic\s+auth|username.*password',
        'jwt': r'jwt|json\s+web\s+token',
        'aws': r'aws\s+signature|aws4-hmac',
        'none': r'no\s+auth|public|anonymous'
    }
    
    detected = []
    
    for auth_type, pattern in auth_types.items():
        if re.search(pattern, text_lower):
            detected.append(auth_type)
    
    # Determine primary auth method
    if detected:
        return {
            'primary': detected[0],
            'methods': detected,
            'confidence': len(detected)
        }
    else:
        return {
            'primary': 'unknown',
            'methods': [],
            'confidence': 0
        }


def extract_response_format(text: str) -> Dict:
    """
    Identify response format (JSON, XML, etc)
    
    Args:
        text: Documentation text
        
    Returns:
        Response format details
    """
    text_lower = text.lower()
    
    formats = {
        'json': r'json|application/json',
        'xml': r'xml|application/xml',
        'html': r'html|text/html',
        'plain': r'plain\s+text|text/plain',
        'csv': r'csv|text/csv'
    }
    
    detected = []
    
    for fmt, pattern in formats.items():
        if re.search(pattern, text_lower):
            detected.append(fmt)
    
    # JSON is most common
    primary = 'json' if 'json' in detected else (detected[0] if detected else 'unknown')
    
    return {
        'primary': primary,
        'formats': detected,
        'content_types': [f"application/{fmt}" if fmt != 'unknown' else 'unknown' for fmt in detected]
    }


def analyze_endpoint_security(text: str) -> Dict:
    """
    Analyze security aspects of endpoints
    
    Args:
        text: Documentation text
        
    Returns:
        Security information
    """
    security_info = {
        'rate_limited': bool(re.search(r'rate\s+limit|requests?\s+per', text, re.IGNORECASE)),
        'requires_https': bool(re.search(r'https|ssl|tls|secure', text, re.IGNORECASE)),
        'requires_auth': bool(re.search(r'auth|token|api.?key|credential', text, re.IGNORECASE)),
        'cors_enabled': bool(re.search(r'cors|cross.?origin', text, re.IGNORECASE))
    }
    
    return security_info


def generate_endpoint_summary(endpoints: List[Dict]) -> Dict:
    """
    Generate summary statistics about extracted endpoints
    
    Args:
        endpoints: List of extracted endpoints
        
    Returns:
        Summary statistics
    """
    methods = {}
    resources = {}
    
    for ep in endpoints:
        # Count by method
        method = ep['method']
        methods[method] = methods.get(method, 0) + 1
        
        # Extract resource from path
        resource = ep['path'].split('/')[1] if '/' in ep['path'] else 'root'
        resources[resource] = resources.get(resource, 0) + 1
    
    return {
        'total_endpoints': len(endpoints),
        'methods': methods,
        'resources': resources,
        'method_breakdown': {
            'GET': methods.get('GET', 0),
            'POST': methods.get('POST', 0),
            'PUT': methods.get('PUT', 0),
            'DELETE': methods.get('DELETE', 0),
            'PATCH': methods.get('PATCH', 0)
        }
    }

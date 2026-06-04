"""SDK Code Generation Service - Generates wrapper code from API analysis."""
import json
from typing import List, Dict, Any
from datetime import datetime


class SDKGenerator:
    """Generate SDK wrapper code in multiple languages from API analysis."""

    def __init__(self):
        self.templates = {
            'python': self._generate_python_sdk,
            'javascript': self._generate_javascript_sdk,
            'typescript': self._generate_typescript_sdk,
            'go': self._generate_go_sdk,
            'java': self._generate_java_sdk,
        }

    def generate_sdk(self, language: str, endpoints: List[Dict], api_name: str = "API") -> str:
        """Generate SDK code in specified language."""
        if language not in self.templates:
            raise ValueError(f"Unsupported language: {language}")
        return self.templates[language](endpoints, api_name)

    def _generate_python_sdk(self, endpoints: List[Dict], api_name: str) -> str:
        """Generate Python SDK wrapper."""
        code = f'''"""
{api_name} SDK - Auto-generated wrapper
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""
import requests
from typing import Dict, Optional, List, Any
from dataclasses import dataclass


@dataclass
class APIResponse:
    """Standardized API response wrapper."""
    status_code: int
    data: Any
    headers: Dict
    error: Optional[str] = None


class {api_name.replace(' ', '')}Client:
    """Main client for {api_name} API."""
    
    def __init__(self, base_url: str, api_key: Optional[str] = None):
        """Initialize {api_name} client.
        
        Args:
            base_url: Base URL for the API
            api_key: Optional API key for authentication
        """
        self.base_url = base_url.rstrip('/')
        self.api_key = api_key
        self.session = requests.Session()
        self._setup_headers()
    
    def _setup_headers(self) -> None:
        """Setup default headers."""
        self.session.headers.update({{
            'Content-Type': 'application/json',
            'User-Agent': '{api_name}-SDK-Python/1.0',
        }})
        if self.api_key:
            self.session.headers.update({{
                'Authorization': f'Bearer {{self.api_key}}'
            }})
    
    def _make_request(self, method: str, endpoint: str, **kwargs) -> APIResponse:
        """Make HTTP request to API.
        
        Args:
            method: HTTP method (GET, POST, PUT, DELETE, PATCH)
            endpoint: API endpoint path
            **kwargs: Additional arguments for requests
            
        Returns:
            APIResponse object with status, data, and headers
        """
        url = f"{{self.base_url}}{{endpoint}}"
        try:
            response = self.session.request(method, url, **kwargs)
            return APIResponse(
                status_code=response.status_code,
                data=response.json() if response.text else None,
                headers=dict(response.headers),
                error=None if response.ok else response.text
            )
        except Exception as e:
            return APIResponse(
                status_code=0,
                data=None,
                headers={{}},
                error=str(e)
            )

'''
        # Add endpoint methods
        for endpoint in endpoints[:10]:  # Limit to 10 endpoints for SDK
            method = endpoint.get('method', 'GET').lower()
            path = endpoint.get('path', '/')
            func_name = self._generate_function_name(method, path)
            code += f'''
    def {func_name}(self, **kwargs) -> APIResponse:
        """Call {method.upper()} {path}"""
        return self._make_request('{method.upper()}', '{path}', **kwargs)
'''
        
        code += f'''


# Example usage:
if __name__ == "__main__":
    client = {api_name.replace(' ', '')}Client(
        base_url="https://api.example.com",
        api_key="your-api-key"
    )
    
    # Make API calls
    # response = client.get_list()
    # print(response.data)
'''
        return code

    def _generate_javascript_sdk(self, endpoints: List[Dict], api_name: str) -> str:
        """Generate JavaScript SDK wrapper."""
        code = f'''/**
 * {api_name} SDK - Auto-generated wrapper
 * Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
 */

class {api_name.replace(' ', '')}Client {{
    constructor(baseUrl, apiKey = null) {{
        this.baseUrl = baseUrl.replace(/\\/$/, '');
        this.apiKey = apiKey;
        this.headers = {{
            'Content-Type': 'application/json',
            'User-Agent': '{api_name}-SDK-JavaScript/1.0',
        }};
        if (apiKey) {{
            this.headers['Authorization'] = `Bearer ${{apiKey}}`;
        }}
    }}

    async _makeRequest(method, endpoint, data = null) {{
        const url = `${{this.baseUrl}}${{endpoint}}`;
        const options = {{
            method,
            headers: this.headers,
        }};
        
        if (data) {{
            options.body = JSON.stringify(data);
        }}
        
        try {{
            const response = await fetch(url, options);
            const responseData = await response.json().catch(() => null);
            return {{
                statusCode: response.status,
                data: responseData,
                headers: Object.fromEntries(response.headers),
                error: null,
            }};
        }} catch (error) {{
            return {{
                statusCode: 0,
                data: null,
                headers: {{}},
                error: error.message,
            }};
        }}
    }}

'''
        # Add endpoint methods
        for endpoint in endpoints[:10]:
            method = endpoint.get('method', 'GET').lower()
            path = endpoint.get('path', '/')
            func_name = self._generate_function_name(method, path)
            code += f'''
    async {func_name}(params = null) {{
        return this._makeRequest('{method.upper()}', '{path}', params);
    }}

'''
        
        code += f'''
}}

// Example usage:
const client = new {api_name.replace(' ', '')}Client(
    'https://api.example.com',
    'your-api-key'
);

// Make API calls
// const response = await client.getList();
// console.log(response.data);

module.exports = {api_name.replace(' ', '')}Client;
'''
        return code

    def _generate_typescript_sdk(self, endpoints: List[Dict], api_name: str) -> str:
        """Generate TypeScript SDK wrapper."""
        code = f'''/**
 * {api_name} SDK - Auto-generated TypeScript wrapper
 * Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
 */

interface APIResponse<T> {{
    statusCode: number;
    data: T | null;
    headers: Record<string, string>;
    error: string | null;
}}

interface RequestOptions {{
    headers?: Record<string, string>;
    params?: Record<string, any>;
    data?: Record<string, any>;
}}

export class {api_name.replace(' ', '')}Client {{
    private baseUrl: string;
    private apiKey: string | null;
    private headers: Record<string, string>;

    constructor(baseUrl: string, apiKey: string | null = null) {{
        this.baseUrl = baseUrl.replace(/\\/$/, '');
        this.apiKey = apiKey;
        this.headers = {{
            'Content-Type': 'application/json',
            'User-Agent': '{api_name}-SDK-TypeScript/1.0',
        }};
        if (apiKey) {{
            this.headers['Authorization'] = `Bearer ${{apiKey}}`;
        }}
    }}

    private async _makeRequest<T>(
        method: string,
        endpoint: string,
        data?: any
    ): Promise<APIResponse<T>> {{
        const url = `${{this.baseUrl}}${{endpoint}}`;
        
        try {{
            const response = await fetch(url, {{
                method,
                headers: this.headers,
                body: data ? JSON.stringify(data) : undefined,
            }});
            
            const responseData = await response.json().catch(() => null);
            
            return {{
                statusCode: response.status,
                data: responseData as T,
                headers: Object.fromEntries(response.headers),
                error: null,
            }};
        }} catch (error) {{
            return {{
                statusCode: 0,
                data: null,
                headers: {{}},
                error: error instanceof Error ? error.message : 'Unknown error',
            }};
        }}
    }}

'''
        # Add endpoint methods
        for endpoint in endpoints[:10]:
            method = endpoint.get('method', 'GET').lower()
            path = endpoint.get('path', '/')
            func_name = self._generate_function_name(method, path)
            code += f'''
    async {func_name}(params?: any): Promise<APIResponse<any>> {{
        return this._makeRequest('{method.upper()}', '{path}', params);
    }}

'''
        code += f'''
}}

export default {api_name.replace(' ', '')}Client;
'''
        return code

    def _generate_go_sdk(self, endpoints: List[Dict], api_name: str) -> str:
        """Generate Go SDK wrapper."""
        code = f'''package {api_name.lower().replace(' ', '')}

import (
    "bytes"
    "encoding/json"
    "fmt"
    "io"
    "net/http"
    "time"
)

// APIResponse represents a standardized API response
type APIResponse struct {{
    StatusCode int               `json:"status_code"`
    Data       interface{{}}       `json:"data"`
    Headers    map[string]string `json:"headers"`
    Error      *string           `json:"error"`
}}

// Client is the main {api_name} API client
type Client struct {{
    BaseURL   string
    APIKey    string
    HTTPClient *http.Client
}}

// NewClient creates a new {api_name} client
func NewClient(baseURL, apiKey string) *Client {{
    return &Client{{
        BaseURL:    baseURL,
        APIKey:     apiKey,
        HTTPClient: &http.Client{{Timeout: 30 * time.Second}},
    }}
}}

// makeRequest makes an HTTP request to the API
func (c *Client) makeRequest(method, endpoint string, body interface{{}}) (*APIResponse, error) {{
    url := fmt.Sprintf("%s%s", c.BaseURL, endpoint)
    
    var bodyReader io.Reader
    if body != nil {{
        bodyBytes, err := json.Marshal(body)
        if err != nil {{
            return nil, err
        }}
        bodyReader = bytes.NewReader(bodyBytes)
    }}
    
    req, err := http.NewRequest(method, url, bodyReader)
    if err != nil {{
        return nil, err
    }}
    
    req.Header.Set("Content-Type", "application/json")
    req.Header.Set("User-Agent", "{api_name}-SDK-Go/1.0")
    if c.APIKey != "" {{
        req.Header.Set("Authorization", fmt.Sprintf("Bearer %s", c.APIKey))
    }}
    
    resp, err := c.HTTPClient.Do(req)
    if err != nil {{
        return nil, err
    }}
    defer resp.Body.Close()
    
    var data interface{{}}
    json.NewDecoder(resp.Body).Decode(&data)
    
    return &APIResponse{{
        StatusCode: resp.StatusCode,
        Data:       data,
        Headers:    headerToMap(resp.Header),
    }}, nil
}}

func headerToMap(h http.Header) map[string]string {{
    m := make(map[string]string)
    for k, v := range h {{
        if len(v) > 0 {{
            m[k] = v[0]
        }}
    }}
    return m
}}

'''
        # Add endpoint methods
        for endpoint in endpoints[:10]:
            method = endpoint.get('method', 'GET').lower()
            path = endpoint.get('path', '/')
            func_name = self._generate_function_name(method, path, capitalize=True)
            code += f'''
// {func_name} calls {method.upper()} {path}
func (c *Client) {func_name}(body interface{{}}) (*APIResponse, error) {{
    return c.makeRequest("{method.upper()}", "{path}", body)
}}

'''
        return code

    def _generate_java_sdk(self, endpoints: List[Dict], api_name: str) -> str:
        """Generate Java SDK wrapper."""
        code = f'''/**
 * {api_name} SDK - Auto-generated wrapper
 * Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
 */

import com.google.gson.Gson;
import com.google.gson.JsonObject;
import java.io.IOException;
import java.net.URI;
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;
import java.util.HashMap;
import java.util.Map;
import java.util.Optional;

public class {api_name.replace(' ', '')}Client {{
    private final String baseUrl;
    private final Optional<String> apiKey;
    private final HttpClient httpClient;
    private final Gson gson;

    public {api_name.replace(' ', '')}Client(String baseUrl) {{
        this(baseUrl, null);
    }}

    public {api_name.replace(' ', '')}Client(String baseUrl, String apiKey) {{
        this.baseUrl = baseUrl.replaceAll("/$", "");
        this.apiKey = Optional.ofNullable(apiKey);
        this.httpClient = HttpClient.newHttpClient();
        this.gson = new Gson();
    }}

    public static class APIResponse {{
        public int statusCode;
        public Object data;
        public Map<String, String> headers;
        public String error;

        public APIResponse(int statusCode, Object data, Map<String, String> headers) {{
            this.statusCode = statusCode;
            this.data = data;
            this.headers = headers;
        }}
    }}

    private APIResponse makeRequest(String method, String endpoint, Object body) {{
        try {{
            String url = baseUrl + endpoint;
            HttpRequest.Builder requestBuilder = HttpRequest.newBuilder()
                    .uri(URI.create(url))
                    .method(method, body != null ? 
                        HttpRequest.BodyPublishers.ofString(gson.toJson(body)) :
                        HttpRequest.BodyPublishers.noBody())
                    .header("Content-Type", "application/json")
                    .header("User-Agent", "{api_name}-SDK-Java/1.0");

            if (apiKey.isPresent()) {{
                requestBuilder.header("Authorization", "Bearer " + apiKey.get());
            }}

            HttpResponse<String> response = httpClient.send(
                requestBuilder.build(),
                HttpResponse.BodyHandlers.ofString()
            );

            Map<String, String> headerMap = new HashMap<>();
            response.headers().map().forEach((k, v) -> 
                headerMap.put(k, v.isEmpty() ? "" : v.get(0))
            );

            Object data = response.body() != null && !response.body().isEmpty() ?
                gson.fromJson(response.body(), JsonObject.class) : null;

            return new APIResponse(response.statusCode(), data, headerMap);
        }} catch (IOException | InterruptedException e) {{
            return new APIResponse(0, null, new HashMap<>());
        }}
    }}

'''
        # Add endpoint methods
        for endpoint in endpoints[:10]:
            method = endpoint.get('method', 'GET').lower()
            path = endpoint.get('path', '/')
            func_name = self._generate_function_name(method, path)
            code += f'''
    public APIResponse {func_name}() {{
        return makeRequest("{method.upper()}", "{path}", null);
    }}

'''
        code += f'''
}}
'''
        return code

    def _generate_function_name(self, method: str, path: str, capitalize: bool = False) -> str:
        """Generate a function name from HTTP method and path."""
        # Remove leading slashes and split by /
        parts = [p for p in path.split('/') if p]
        
        if not parts:
            func_name = method.lower()
        else:
            func_name = method.lower() + '_' + '_'.join(parts)
        
        # Remove special characters
        func_name = ''.join(c if c.isalnum() or c == '_' else '' for c in func_name)
        
        if capitalize:
            func_name = ''.join(word.capitalize() for word in func_name.split('_'))
        
        return func_name or 'request'

    def generate_test_suite(self, language: str, endpoints: List[Dict], api_name: str) -> str:
        """Generate test suite for SDK."""
        if language == 'python':
            return self._generate_python_tests(endpoints, api_name)
        elif language == 'javascript':
            return self._generate_javascript_tests(endpoints, api_name)
        return ""

    def _generate_python_tests(self, endpoints: List[Dict], api_name: str) -> str:
        """Generate Python unit tests."""
        code = f'''"""
Test suite for {api_name} SDK
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""
import unittest
from unittest.mock import Mock, patch, MagicMock
from {api_name.lower().replace(' ', '_')} import {api_name.replace(' ', '')}Client, APIResponse


class Test{api_name.replace(' ', '')}Client(unittest.TestCase):
    
    def setUp(self):
        self.client = {api_name.replace(' ', '')}Client(
            base_url="https://api.example.com",
            api_key="test-key"
        )
    
    @patch('requests.Session.request')
    def test_client_initialization(self, mock_request):
        """Test client initializes with correct headers."""
        self.assertIsNotNone(self.client.session)
        self.assertEqual(self.client.base_url, "https://api.example.com")
        self.assertEqual(self.client.api_key, "test-key")
    
    @patch('requests.Session.request')
    def test_make_request_success(self, mock_request):
        """Test successful API request."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {{"data": "test"}}
        mock_response.text = '{{"data": "test"}}'
        mock_response.ok = True
        mock_response.headers = {{}}\
        mock_request.return_value = mock_response
        
        response = self.client._make_request("GET", "/test")
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, {{"data": "test"}})
        self.assertIsNone(response.error)
    
    @patch('requests.Session.request')
    def test_make_request_failure(self, mock_request):
        """Test failed API request."""
        mock_request.side_effect = Exception("Connection error")
        
        response = self.client._make_request("GET", "/test")
        
        self.assertEqual(response.status_code, 0)
        self.assertIsNotNone(response.error)


if __name__ == "__main__":
    unittest.main()
'''
        return code

    def _generate_javascript_tests(self, endpoints: List[Dict], api_name: str) -> str:
        """Generate JavaScript tests."""
        code = f'''/**
 * Test suite for {api_name} SDK
 * Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
 */

const {api_name.replace(' ', '')}Client = require('./{api_name.lower().replace(' ', '_')}');

describe('{api_name}Client', () => {{
    let client;

    beforeEach(() => {{
        client = new {api_name.replace(' ', '')}Client(
            'https://api.example.com',
            'test-key'
        );
    }});

    test('should initialize with correct properties', () => {{
        expect(client.baseUrl).toBe('https://api.example.com');
        expect(client.apiKey).toBe('test-key');
        expect(client.headers['Authorization']).toBe('Bearer test-key');
    }});

    test('should make successful request', async () => {{
        global.fetch = jest.fn(() =>
            Promise.resolve({{
                ok: true,
                status: 200,
                json: () => Promise.resolve({{ data: 'test' }}),
                headers: new Map(),
            }})
        );

        const response = await client._makeRequest('GET', '/test');

        expect(response.statusCode).toBe(200);
        expect(response.data.data).toBe('test');
        expect(response.error).toBeNull();
    }});

    test('should handle request failure', async () => {{
        global.fetch = jest.fn(() =>
            Promise.reject(new Error('Network error'))
        );

        const response = await client._makeRequest('GET', '/test');

        expect(response.statusCode).toBe(0);
        expect(response.error).toBeDefined();
    }});
}});
'''
        return code

"""
LLM prompts for various tasks
"""


ENDPOINT_EXTRACTION_PROMPT = """
Extract all API endpoints from the following documentation.
For each endpoint, identify:
1. HTTP method (GET, POST, PUT, DELETE, PATCH)
2. Path/URL
3. Required and optional parameters
4. Request body format (if applicable)
5. Response format
6. Authentication requirements

Return as a structured list.

Documentation:
{documentation}
"""


AUTH_DETECTION_PROMPT = """
Analyze the following API documentation and identify the authentication method(s).

For each authentication method found, provide:
1. Type (Bearer Token, API Key, Basic Auth, OAuth 2.0, etc.)
2. Location (Header, Query Parameter, Body)
3. Header/Parameter name
4. How to obtain credentials
5. Example of authenticated request

Documentation:
{documentation}
"""


CODE_GENERATION_PROMPT = """
Generate a production-ready {language} wrapper class for the following API.

API Name: {api_name}
Endpoints: {endpoints}
Authentication: {auth_method}

Requirements:
- Type hints (if applicable to language)
- Error handling with retry logic
- Docstrings for every method and class
- Proper async/await handling (if language supports)
- Input validation
- Example usage in docstring
- Logging statements
- Rate limiting awareness if mentioned
- Follow {language} best practices

Generate the complete, copy-paste ready code:
"""


SDK_RECOMMENDATION_PROMPT = """
For the API "{api_name}" in {language}, should we:
1. Use the official SDK (if available)
2. Use a REST-based wrapper

Analyze and provide:
- Recommendation with reasoning
- Installation command for recommended approach
- Pros and cons of each approach
- Any caveats or considerations

API Documentation:
{documentation}
"""


TEST_GENERATION_PROMPT = """
Generate comprehensive unit tests for the following {language} code.

The tests should cover:
1. Successful API calls
2. Error handling
3. Parameter validation
4. Authentication
5. Edge cases

Use appropriate testing framework for {language}.

Code to test:
{code}
"""


PARAMETER_EXTRACTION_PROMPT = """
From the following endpoint documentation, extract all parameters:

{endpoint_docs}

For each parameter, identify:
1. Name
2. Type (string, integer, boolean, array, object, etc.)
3. Required (yes/no)
4. Description
5. Location (query, path, body, header)
6. Default value (if any)
7. Constraints/validation (if any)
"""

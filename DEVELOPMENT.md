# Development Guide

## Project Structure

```
aem-admin-pyclient/
├── src/                       # Source code directory
│   └── aem_admin_client/      # Main package
│       ├── __init__.py        # Package exports
│       ├── base.py            # Base HTTP client with debug logging
│       ├── client.py          # Main AEMAdminClient class
│       ├── exceptions.py      # Custom exceptions
│       ├── models.py          # Pydantic data models with RFC 2822 datetime parsing
│       └── operations/        # API operation modules
│           ├── __init__.py
│           ├── cache.py       # Cache operations
│           ├── code.py        # Code operations
│           ├── config.py      # Configuration operations (with .json extensions)
│           ├── index.py       # Index operations
│           ├── job.py         # Job operations
│           ├── log.py         # Log operations
│           ├── preview.py     # Preview operations
│           ├── publish.py     # Publish operations
│           ├── snapshot.py    # Snapshot operations
│           └── status.py      # Status operations
├── tests/                     # Unit tests
│   ├── __init__.py
│   └── test_client.py
├── examples/                  # Usage examples
│   └── basic_usage.py
├── docs/                      # Documentation
│   └── API_REFERENCE.md
├── cli.py                     # Command-line interface
├── setup.py                   # Package setup
├── requirements.txt           # Dependencies
├── pytest.ini               # Test configuration
├── README.md                 # Main documentation
├── DEVELOPMENT.md            # This file
├── aem-admin-api-spec.json   # OpenAPI specification
└── .gitignore               # Git ignore rules
```

## Development Setup

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd aem-admin-pyclient
   ```

2. **Set up virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   pip install pytest pytest-cov  # For testing
   ```

4. **Install in development mode:**
   ```bash
   pip install -e .
   ```

## Environment Configuration

The client supports environment variables for configuration:

```bash
# Authentication
export AEM_ADMIN_AUTH_TOKEN="your_auth_token"
export AEM_ADMIN_AUTH_COOKIE="your_auth_cookie"

# Base URL
export AEM_ADMIN_BASE_URL="https://admin.hlx.page"

# Logging
export AEM_ADMIN_LOG_LEVEL="DEBUG"  # DEBUG, INFO, WARNING, ERROR, CRITICAL
export LOG_LEVEL="INFO"             # General log level fallback
export PYTHON_LOG_LEVEL="WARNING"   # Python-specific log level fallback
```

## Running Tests

```bash
# Run all tests
pytest

# Run with verbose output
pytest -v

# Run with coverage
pytest --cov=src/aem_admin_client --cov-report=html --cov-report=term

# Run specific test file
pytest tests/test_client.py

# Run specific test method
pytest tests/test_client.py::TestAEMAdminClient::test_status_operation

# Run tests with markers
pytest -m unit          # Unit tests only
pytest -m integration   # Integration tests only
pytest -m "not slow"    # Skip slow tests

# Run tests with live logging
pytest -s --log-cli-level=DEBUG

# Stop on first failure
pytest -x
```

## Code Style

The project follows Python best practices:

- **Type hints**: All functions have proper type annotations
- **Docstrings**: All public methods have comprehensive docstrings
- **Error handling**: Specific exceptions for different error conditions
- **Modular design**: Organized into logical operation modules
- **Environment configuration**: Support for environment variables
- **Debug logging**: Comprehensive HTTP request/response logging

## Authentication

The client now uses **cookie-based authentication** exclusively:

- **Auth Token**: Stored as `auth_token` cookie (not Authorization header)
- **Auth Cookie**: Direct cookie value
- **Environment Variables**: `AEM_ADMIN_AUTH_TOKEN` or `AEM_ADMIN_AUTH_COOKIE`

```python
# All these methods set the auth_token cookie
client = AEMAdminClient(auth_token="token")
client = AEMAdminClient(auth_cookie="cookie")
# Or via environment variables
```

## Debug Logging

Enhanced logging capabilities:

- **Environment Control**: Set log level via `AEM_ADMIN_LOG_LEVEL`
- **HTTP Logging**: Detailed request/response logging at DEBUG level
- **Security**: Sensitive headers (Authorization, Cookie) are masked
- **Performance**: Logging checks are optimized with `isEnabledFor()`

```python
# Enable debug logging
client = AEMAdminClient(auth_token="token", debug=True)

# Or via environment
export AEM_ADMIN_LOG_LEVEL=DEBUG
```

## Data Models & Parsing

Enhanced Pydantic models with:

- **RFC 2822 DateTime Parsing**: Handles API datetime formats like `"Tue, 08 Apr 2025 13:40:43 GMT"`
- **Flexible Field Handling**: Optional fields for incomplete API responses
- **Fallback Parsing**: ISO format fallback for datetime fields
- **Validation Fixes**: Proper handling of empty objects and missing fields

## API Endpoint Compliance

All configuration endpoints now include required `.json` extensions:

- `GET /config/{org}.json` (not `/config/{org}`)
- `GET /config/{org}/sites/{site}.json`
- `GET /config/{org}/profiles/{profile}.json`

This matches the [AEM Admin API](https://www.aem.live/docs/admin.html) specification requirements.

## Adding New Operations

To add a new operation module:

1. Create a new file in `aem_admin_client/operations/`
2. Follow the pattern of existing modules
3. Add the new class to `operations/__init__.py`
4. Add the operation to the main client in `client.py`
5. Add tests for the new functionality
6. Ensure proper `.json` extensions for config endpoints
7. Handle empty POST requests with `data={}` if needed

## Testing

The project includes:

- **Unit tests**: Mock-based tests for all major functionality
- **Mocking**: Proper mock objects with headers, status codes, and responses
- **Authentication tests**: Updated for cookie-based auth
- **Error handling tests**: All exception types covered
- **Coverage reporting**: HTML and terminal coverage reports

Current test coverage: **61%** (751 statements, 295 missed)

## Building and Distribution

### Building the Package
```bash
# Clean previous builds
rm -rf dist/*

# Build the package
python -m build
```

### Distribution Methods

1. **Install from Local Build**:
   ```bash
   pip install dist/aem-admin-client-12.74.3-py3-none-any.whl
   ```

2. **Install from GitHub**:
   ```bash
   # Latest version
   pip install git+https://github.com/adobe-rnd/aem-admin-pyclient.git

   # Specific version
   pip install git+https://github.com/adobe-rnd/aem-admin-pyclient.git@v12.74.3
   ```

3. **Add to Requirements File**:
   ```
   aem-admin-client @ git+https://github.com/adobe-rnd/aem-admin-pyclient.git@v12.74.3
   ```

4. **Add to pyproject.toml**:
   ```toml
   dependencies = [
       "aem-admin-client @ git+https://github.com/adobe-rnd/aem-admin-pyclient.git@v12.74.3",
   ]
   ```

### Version Management

1. **Update Version**:
   - Edit `src/aem_admin_client/__init__.py`
   - Update `__version__` variable

2. **Create Release**:
   ```bash
   # Commit version change
   git add src/aem_admin_client/__init__.py
   git commit -m "chore: Update version to X.Y.Z"

   # Create and push tag
   git tag -a vX.Y.Z -m "Release version X.Y.Z"
   git push origin main
   git push origin vX.Y.Z
   ```

## API Coverage

The client covers all major [AEM Admin API](https://www.aem.live/docs/admin.html) endpoints:

- ✅ Status operations (get status, bulk status)
- ✅ Publish operations (publish, unpublish, bulk operations)
- ✅ Preview operations (preview, delete, bulk operations)
- ✅ Code operations (get status, update, delete)
- ✅ Cache operations (get status, purge)
- ✅ Index operations (get status, update, delete)
- ✅ Job operations (get, list, delete)
- ✅ Log operations (get logs with filtering)
- ✅ Snapshot operations (list, create, get, delete, review)
- ✅ Configuration operations (org, site, profile configs with .json extensions)

## Error Handling

The client provides comprehensive error handling:

- `AEMAdminError`: Base exception class
- `AuthenticationError`: 401 errors
- `AuthorizationError`: 403 errors
- `NotFoundError`: 404 errors
- `ConflictError`: 409 errors
- `RateLimitError`: 429 errors
- `ServerError`: 5xx errors
- `ValidationError`: 400 errors

## Recent Improvements

### Authentication Changes
- ✅ Switched from Bearer token headers to cookie-based authentication
- ✅ Environment variable support for all configuration options

### Logging Enhancements
- ✅ Environment-controlled log levels
- ✅ Detailed HTTP request/response logging
- ✅ Security-conscious header masking
- ✅ Performance-optimized logging checks

### Data Model Fixes
- ✅ RFC 2822 datetime parsing for API responses
- ✅ Optional field handling for incomplete responses
- ✅ Flexible LogResponse model with extra field support

### API Compliance
- ✅ Added required `.json` extensions to config endpoints
- ✅ Fixed empty POST request handling
- ✅ Proper content-type management

### Testing Updates
- ✅ Fixed authentication tests for cookie-based auth
- ✅ Improved mock objects with proper headers
- ✅ All tests passing with comprehensive coverage reporting

### Distribution Updates
- ✅ GitHub-based installation support
- ✅ Version-specific installation options
- ✅ Modern Python packaging with pyproject.toml
- ✅ Simplified development installation

## Future Enhancements

Potential improvements:

- [ ] Async client support using `aiohttp`
- [ ] Response caching
- [ ] Retry with exponential backoff
- [ ] Webhook support
- [ ] Batch operations optimization
- [ ] Configuration validation
- [ ] Integration tests with real API
- [ ] Performance benchmarking
- [ ] Additional operation modules
- [ ] PyPI distribution
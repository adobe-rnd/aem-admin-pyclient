# AEM Admin Python Client

A comprehensive Python client library for the [AEM Admin API](https://www.aem.live/docs/admin.html), providing easy-to-use interfaces for managing AEM content and code lifecycle operations.

## Features

- **Modular Design**: Well-organized modules for different API operations
- **Type Safety**: Full type hints and Pydantic models for request/response validation
- **Authentication Support**: Cookie-based and Bearer token authentication
- **Comprehensive Coverage**: Support for all major [AEM Admin API](https://www.aem.live/docs/admin.html) endpoints
- **Error Handling**: Robust error handling with custom exceptions
- **Async Support**: Optional async client for high-performance applications

## Installation

```bash
pip install aem-admin-client
```

For development:
```bash
pip install aem-admin-client[dev]
```

## Quick Start

```python
from aem_admin_client import AEMAdminClient

# Initialize client with authentication
client = AEMAdminClient(
    base_url="https://admin.hlx.page",
    auth_token="your-auth-token"  # or use auth_cookie
)

# Get status of a resource
status = client.status.get_status(
    org="your-org",
    site="your-site",
    ref="main",
    path="index"
)

# Publish a resource
result = client.publish.publish_resource(
    org="your-org",
    site="your-site",
    ref="main",
    path="index"
)

# Preview a resource
preview = client.preview.preview_resource(
    org="your-org",
    site="your-site",
    ref="main",
    path="index"
)
```

## Authentication

The client supports multiple authentication methods:

### Bearer Token
```python
client = AEMAdminClient(
    base_url="https://admin.hlx.page",
    auth_token="your-api-key"
)
```

### Auth Cookie
```python
client = AEMAdminClient(
    base_url="https://admin.hlx.page",
    auth_cookie="your-auth-cookie"
)
```

## API Coverage

- **Status Operations**: Get resource status and bulk status operations
- **Publish Operations**: Publish resources and manage live content
- **Preview Operations**: Preview resources and manage preview content
- **Code Operations**: Manage code bus operations
- **Cache Operations**: Cache management and purging
- **Index Operations**: Search index management
- **Job Operations**: Asynchronous job management
- **Log Operations**: Access and manage logs
- **Snapshot Operations**: Create and manage snapshots
- **Configuration Management**: Org, site, and profile configurations
- **Sitemap Operations**: Manage sitemaps

## Error Handling

```python
from aem_admin_client.exceptions import AEMAdminError, AuthenticationError

try:
    status = client.status.get_status("org", "site", "main", "path")
except AuthenticationError:
    print("Authentication failed")
except AEMAdminError as e:
    print(f"API error: {e}")
```

## Development

```bash
# Clone the repository
git clone <repository-url>
cd aem-admin-pyclient

# Install development dependencies
pip install -e .[dev]

# Run tests
pytest

# Format code
black .

# Type checking
mypy aem_admin_client
```

## License

This project is licensed under the Apache License 2.0 - see the [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

## Acknowledgments

- Built for the [AEM Admin API](https://www.aem.live/docs/admin.html)
- Compatible with Adobe Experience Manager and Helix services
# AEM Admin Python Client - API Reference

## Overview

The AEM Admin Python Client provides a comprehensive interface to the [AEM Admin API](https://www.aem.live/docs/admin.html), organized into logical operation modules for easy use.

## Client Initialization

```python
from aem_admin_client import AEMAdminClient

# Using Bearer Token
client = AEMAdminClient(
    base_url="https://admin.hlx.page",
    auth_token="your-api-key",
    timeout=30,
    max_retries=3
)

# Using Auth Cookie
client = AEMAdminClient(
    base_url="https://admin.hlx.page",
    auth_cookie="your-auth-cookie",
    timeout=30,
    max_retries=3
)
```

## Operation Modules

### Status Operations (`client.status`)

#### `get_status(org, site, ref, path, edit_url=None)`
Get the overall status of a resource.

**Parameters:**
- `org` (str): Organization name
- `site` (str): Site ID
- `ref` (str): Repository reference (branch)
- `path` (str): Relative path of the resource
- `edit_url` (str, optional): URL of the edit document or 'auto'

**Returns:** `StatusResponse`

#### `bulk_status(org, site, ref, request)`
Start a bulk status job for multiple resources.

**Parameters:**
- `org` (str): Organization name
- `site` (str): Site ID
- `ref` (str): Repository reference (branch)
- `request` (BulkStatusRequest): Bulk status request

**Returns:** `JobResponse`

### Publish Operations (`client.publish`)

#### `get_publish_status(org, site, ref, path)`
Get the publish status of a resource.

**Returns:** `LiveInfo`

#### `publish_resource(org, site, ref, path, force_update_redirects=None, disable_notifications=None)`
Publish a single resource.

**Parameters:**
- `force_update_redirects` (bool, optional): Force update of redirects
- `disable_notifications` (bool, optional): Disable notifications

**Returns:** `Dict[str, Any]`

#### `unpublish_resource(org, site, ref, path)`
Unpublish a resource.

**Returns:** `Dict[str, Any]`

#### `bulk_publish(org, site, ref, request)`
Start a bulk publish job.

**Parameters:**
- `request` (PublishRequest): Bulk publish request

**Returns:** `JobResponse`

#### `bulk_unpublish(org, site, ref, paths)`
Start a bulk unpublish job.

**Parameters:**
- `paths` (List[str]): List of paths to unpublish

**Returns:** `JobResponse`

### Preview Operations (`client.preview`)

#### `get_preview_status(org, site, ref, path)`
Get the preview status of a resource.

**Returns:** `PreviewInfo`

#### `preview_resource(org, site, ref, path, word2md_version=None, gdocs2md_version=None, html2md_version=None)`
Preview a single resource.

**Parameters:**
- `word2md_version` (str, optional): Version for word2md service
- `gdocs2md_version` (str, optional): Version for gdocs2md service
- `html2md_version` (str, optional): Version for html2md service

**Returns:** `Dict[str, Any]`

#### `delete_preview(org, site, ref, path)`
Delete a preview resource.

**Returns:** `Dict[str, Any]`

#### `bulk_preview(org, site, ref, request)`
Start a bulk preview job.

**Parameters:**
- `request` (PreviewRequest): Bulk preview request

**Returns:** `JobResponse`

#### `bulk_delete_preview(org, site, ref, paths)`
Start a bulk preview deletion job.

**Parameters:**
- `paths` (List[str]): List of paths to delete from preview

**Returns:** `JobResponse`

### Code Operations (`client.code`)

#### `get_code_status(org, site, ref, path)`
Get the code status of a resource.

**Returns:** `CodeInfo`

#### `update_code(org, site, ref, path)`
Update code for a resource.

**Returns:** `Dict[str, Any]`

#### `delete_code(org, site, ref, path)`
Delete code for a resource.

**Returns:** `Dict[str, Any]`

### Cache Operations (`client.cache`)

#### `get_cache_status(org, site, ref, path)`
Get the cache status of a resource.

**Returns:** `CacheInfo`

#### `purge_cache(org, site, ref, path)`
Purge cache for a resource.

**Returns:** `Dict[str, Any]`

### Index Operations (`client.index`)

#### `get_index_status(org, site, ref, path)`
Get the index status of a resource.

**Returns:** `IndexInfo`

#### `update_index(org, site, ref, path)`
Update index for a resource.

**Returns:** `Dict[str, Any]`

#### `delete_from_index(org, site, ref, path)`
Delete a resource from index.

**Returns:** `Dict[str, Any]`

### Job Operations (`client.job`)

#### `get_job(org, site, ref, topic, job_name)`
Get information about a specific job.

**Parameters:**
- `topic` (str): Job topic
- `job_name` (str): Job name

**Returns:** `JobInfo`

#### `list_jobs(org, site, ref, topic)`
List jobs for a specific topic.

**Parameters:**
- `topic` (str): Job topic

**Returns:** `List[JobInfo]`

#### `delete_job(org, site, ref, topic, job_name)`
Delete a specific job.

**Parameters:**
- `topic` (str): Job topic
- `job_name` (str): Job name

**Returns:** `Dict[str, Any]`

### Log Operations (`client.log`)

#### `get_logs(org, site, ref, from_time=None, to_time=None, since=None, next_token=None)`
Get logs for a site.

**Parameters:**
- `from_time` (str, optional): Starting date to get logs from
- `to_time` (str, optional): Ending date to get logs from
- `since` (str, optional): Time span to retrieve logs for (e.g., '5m', '1h', '1d')
- `next_token` (str, optional): Token from previous call to continue

**Returns:** `LogResponse`

### Snapshot Operations (`client.snapshot`)

#### `list_snapshots(org, site, ref)`
List all snapshots for a site.

**Returns:** `List[SnapshotInfo]`

#### `create_snapshot(org, site, ref, request, filter_type=None, publish=None)`
Create a new snapshot.

**Parameters:**
- `request` (SnapshotRequest): Snapshot creation request
- `filter_type` (str, optional): Filter type ('all' or 'modified')
- `publish` (bool, optional): Whether to publish the snapshot

**Returns:** `SnapshotInfo`

#### `get_snapshot(org, site, ref, snapshot_id)`
Get information about a specific snapshot.

**Parameters:**
- `snapshot_id` (str): Snapshot ID

**Returns:** `SnapshotInfo`

#### `delete_snapshot(org, site, ref, snapshot_id)`
Delete a snapshot.

**Parameters:**
- `snapshot_id` (str): Snapshot ID

**Returns:** `Dict[str, Any]`

#### `review_snapshot(org, site, ref, snapshot_id, review_action, message=None)`
Review a snapshot (request, approve, or reject).

**Parameters:**
- `snapshot_id` (str): Snapshot ID
- `review_action` (str): Review action ('request', 'approve', 'reject')
- `message` (str, optional): Optional review message

**Returns:** `Dict[str, Any]`

### Configuration Operations (`client.config`)

#### Organization Configuration

- `get_org_config(org)` → `OrgConfig`
- `update_org_config(org, config)` → `OrgConfig`

#### Site Configuration

- `get_site_config(org, site)` → `SiteConfig`
- `update_site_config(org, site, config)` → `SiteConfig`
- `delete_site_config(org, site)` → `Dict[str, Any]`

#### Profile Configuration

- `get_profile_config(org, profile)` → `ProfileConfig`
- `update_profile_config(org, profile, config)` → `ProfileConfig`
- `delete_profile_config(org, profile)` → `Dict[str, Any]`

#### Generic Configuration

- `get_config(path)` → `ConfigResponse`
- `update_config(path, data)` → `ConfigResponse`
- `delete_config(path)` → `Dict[str, Any]`

## Data Models

### Core Models

- `StatusResponse`: Complete status information
- `LiveInfo`: Live/published resource information
- `PreviewInfo`: Preview resource information
- `EditInfo`: Edit/source resource information
- `CodeInfo`: Code resource information
- `CacheInfo`: Cache information
- `IndexInfo`: Index information

### Request Models

- `BulkStatusRequest`: Bulk status request
- `PublishRequest`: Publish request
- `PreviewRequest`: Preview request
- `SnapshotRequest`: Snapshot creation request

### Job Models

- `JobInfo`: Job information
- `JobResponse`: Job response with links
- `JobCreated`: Job creation response

### Configuration Models

- `SiteConfig`: Site configuration
- `OrgConfig`: Organization configuration
- `ProfileConfig`: Profile configuration
- `ConfigResponse`: Generic configuration response

## Error Handling

The client provides specific exception types for different error conditions:

```python
from aem_admin_client.exceptions import (
    AEMAdminError,           # Base exception
    AuthenticationError,     # 401 errors
    AuthorizationError,      # 403 errors
    NotFoundError,          # 404 errors
    ConflictError,          # 409 errors
    RateLimitError,         # 429 errors
    ServerError,            # 5xx errors
    ValidationError,        # 400 errors
)

try:
    status = client.status.get_status("org", "site", "main", "path")
except AuthenticationError:
    print("Authentication failed")
except NotFoundError:
    print("Resource not found")
except AEMAdminError as e:
    print(f"API error: {e}")
```

## Context Manager Usage

The client supports context manager usage for automatic cleanup:

```python
with AEMAdminClient(auth_token="your-token") as client:
    status = client.status.get_status("org", "site", "main", "index")
    # Session is automatically closed when exiting the context
```
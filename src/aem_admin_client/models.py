"""Pydantic models for AEM Admin API data structures."""

from datetime import datetime
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field, field_validator


class ResourceInfo(BaseModel):
    """Basic resource information."""

    web_path: str = Field(alias="webPath")
    resource_path: str = Field(alias="resourcePath")


class LiveInfo(BaseModel):
    """Live/published resource information."""

    status: int
    url: Optional[str] = None
    last_modified: Optional[datetime] = Field(None, alias="lastModified")
    last_modified_by: Optional[str] = Field(None, alias="lastModifiedBy")
    content_bus_id: Optional[str] = Field(None, alias="contentBusId")
    permissions: List[str] = []

    @field_validator("last_modified", mode="before")
    @classmethod
    def parse_datetime(cls, v: Any) -> Optional[datetime]:
        """Parse RFC 2822 datetime format."""
        if isinstance(v, str):
            try:
                from email.utils import parsedate_to_datetime
                return parsedate_to_datetime(v)
            except (ValueError, TypeError):
                # Fallback to ISO format parsing
                from datetime import datetime
                return datetime.fromisoformat(v.replace("Z", "+00:00"))
        return None if v is None else v


class PreviewInfo(BaseModel):
    """Preview resource information."""

    status: int
    url: Optional[str] = None
    last_modified: Optional[datetime] = Field(None, alias="lastModified")
    last_modified_by: Optional[str] = Field(None, alias="lastModifiedBy")
    content_bus_id: Optional[str] = Field(None, alias="contentBusId")
    permissions: List[str] = []

    @field_validator("last_modified", mode="before")
    @classmethod
    def parse_datetime(cls, v: Any) -> Optional[datetime]:
        """Parse RFC 2822 datetime format."""
        if isinstance(v, str):
            try:
                from email.utils import parsedate_to_datetime
                return parsedate_to_datetime(v)
            except (ValueError, TypeError):
                # Fallback to ISO format parsing
                from datetime import datetime
                return datetime.fromisoformat(v.replace("Z", "+00:00"))
        return None if v is None else v


class EditInfo(BaseModel):
    """Edit/source resource information."""

    status: Optional[int] = None  # Make status optional to handle empty edit objects
    url: Optional[str] = None
    source_location: Optional[str] = Field(None, alias="sourceLocation")
    last_modified: Optional[datetime] = Field(None, alias="lastModified")

    @field_validator("last_modified", mode="before")
    @classmethod
    def parse_datetime(cls, v: Any) -> Optional[datetime]:
        """Parse RFC 2822 datetime format."""
        if isinstance(v, str):
            try:
                from email.utils import parsedate_to_datetime
                return parsedate_to_datetime(v)
            except (ValueError, TypeError):
                # Fallback to ISO format parsing
                from datetime import datetime
                return datetime.fromisoformat(v.replace("Z", "+00:00"))
        return None if v is None else v


class CodeInfo(BaseModel):
    """Code resource information."""

    status: int
    code_bus_id: Optional[str] = Field(None, alias="codeBusId")
    permissions: List[str] = []


class ResourceLinksInfo(BaseModel):
    """Resource links information."""

    status: Optional[str] = None
    preview: Optional[str] = None
    live: Optional[str] = None
    code: Optional[str] = None


class ProfileInfo(BaseModel):
    """Profile information."""

    name: Optional[str] = None


class StatusResponse(ResourceInfo):
    """Complete status response."""

    live: Optional[LiveInfo] = None
    preview: Optional[PreviewInfo] = None
    edit: Optional[EditInfo] = None
    code: Optional[CodeInfo] = None
    links: Optional[ResourceLinksInfo] = None
    profile: Optional[ProfileInfo] = None


class BulkStatusPath(BaseModel):
    """Model representing a path for bulk status operations."""

    path: str = Field(..., description="Path to check status for")
    type: str = Field(..., description="Type of status check")


class BulkStatusRequest(BaseModel):
    """Model representing a bulk status request."""

    paths: List[BulkStatusPath] = Field(
        ...,
        description="List of paths to check status for"
    )


class JobInfo(BaseModel):
    """Job information."""

    topic: str
    name: str
    state: str
    start_time: Optional[datetime] = Field(None, alias="startTime")
    end_time: Optional[datetime] = Field(None, alias="endTime")
    data: Optional[Dict[str, Any]] = None
    progress: Optional[Dict[str, Any]] = None
    result: Optional[Dict[str, Any]] = None

    @field_validator("start_time", "end_time", mode="before")
    @classmethod
    def parse_datetime(cls, v: Any) -> Optional[datetime]:
        """Parse RFC 2822 datetime format."""
        if isinstance(v, str):
            try:
                from email.utils import parsedate_to_datetime
                return parsedate_to_datetime(v)
            except (ValueError, TypeError):
                # Fallback to ISO format parsing
                from datetime import datetime
                return datetime.fromisoformat(v.replace("Z", "+00:00"))
        return None if v is None else v


class JobCreated(BaseModel):
    """Job creation response."""

    status: int
    message_id: str = Field(alias="messageId")
    job: JobInfo


class JobLinksInfo(BaseModel):
    """Job links information."""

    self: Optional[str] = None
    list: Optional[str] = None


class JobResponse(JobCreated):
    """Complete job response."""

    links: Optional[JobLinksInfo] = None


class PublishRequest(BaseModel):
    """Model representing a publish request."""

    paths: List[str] = Field(..., description="List of paths to publish")
    type: str = Field(..., description="Type of publish operation")


class PreviewRequest(BaseModel):
    """Request body for preview operations."""

    paths: Optional[List[str]] = None
    word2md_version: Optional[str] = Field(None, alias="hlx-word2md-version")
    gdocs2md_version: Optional[str] = Field(None, alias="hlx-gdocs2md-version")
    html2md_version: Optional[str] = Field(None, alias="hlx-html2md-version")


class CacheInfo(BaseModel):
    """Model representing cache information."""

    class Config:
        """Pydantic configuration for the CacheInfo model.

        Defines example data and schema customization.
        """

        json_schema_extra = {
            "example": {
                "path": "/content/example",
                "status": "cleared",
                "timestamp": "2023-01-01T00:00:00Z",
            }
        }

    path: str = Field(..., description="Path of the cached content")
    status: str = Field(..., description="Status of the cache operation")
    timestamp: datetime = Field(..., description="Timestamp of the cache operation")


class IndexInfo(BaseModel):
    """Index information."""

    status: int
    url: Optional[str] = None
    last_modified: Optional[datetime] = Field(None, alias="lastModified")

    @field_validator("last_modified", mode="before")
    @classmethod
    def parse_datetime(cls, v: Any) -> Optional[datetime]:
        """Parse RFC 2822 datetime format."""
        if isinstance(v, str):
            try:
                from email.utils import parsedate_to_datetime
                return parsedate_to_datetime(v)
            except (ValueError, TypeError):
                # Fallback to ISO format parsing
                from datetime import datetime
                return datetime.fromisoformat(v.replace("Z", "+00:00"))
        return None if v is None else v


class LogEntry(BaseModel):
    """Log entry."""

    timestamp: datetime
    level: str
    message: str
    source: Optional[str] = None
    request_id: Optional[str] = Field(None, alias="requestId")

    @field_validator("timestamp", mode="before")
    @classmethod
    def parse_datetime(cls, v: Any) -> Optional[datetime]:
        """Parse RFC 2822 datetime format."""
        if isinstance(v, str):
            try:
                from email.utils import parsedate_to_datetime
                return parsedate_to_datetime(v)
            except (ValueError, TypeError):
                # Fallback to ISO format parsing
                from datetime import datetime
                return datetime.fromisoformat(v.replace("Z", "+00:00"))
        return None if v is None else v


class LogResponse(BaseModel):
    """Log response."""

    logs: List[LogEntry] = Field(default_factory=list)  # Always a list, never None
    next_token: Optional[str] = Field(None, alias="nextToken")
    from_time: Optional[str] = Field(
        None,
        alias="from"
    )  # Add fields that appear in actual response
    to_time: Optional[str] = Field(None, alias="to")
    blocks: Optional[str] = None
    ref: Optional[str] = None

    class Config:
        """Pydantic configuration for the LogResponse model.

        Allows extra fields in the response data.
        """
        extra = "allow"


class SnapshotInfo(BaseModel):
    """Snapshot information."""

    id: str
    name: Optional[str] = None
    description: Optional[str] = None
    created: datetime
    created_by: str = Field(alias="createdBy")
    state: str
    filter: Optional[str] = None
    paths: List[str] = []

    @field_validator("created", mode="before")
    @classmethod
    def parse_datetime(cls, v: Any) -> Optional[datetime]:
        """Parse RFC 2822 datetime format."""
        if isinstance(v, str):
            try:
                from email.utils import parsedate_to_datetime
                return parsedate_to_datetime(v)
            except (ValueError, TypeError):
                # Fallback to ISO format parsing
                from datetime import datetime
                return datetime.fromisoformat(v.replace("Z", "+00:00"))
        return None if v is None else v


class SnapshotRequest(BaseModel):
    """Request body for snapshot operations."""

    name: Optional[str] = None
    description: Optional[str] = None
    paths: Optional[List[str]] = None
    filter: Optional[str] = None


class ConfigResponse(BaseModel):
    """Generic configuration response."""

    data: Dict[str, Any]
    last_modified: Optional[datetime] = Field(None, alias="lastModified")

    @field_validator("last_modified", mode="before")
    @classmethod
    def parse_datetime(cls, v: Any) -> Optional[datetime]:
        """Parse RFC 2822 datetime format."""
        if isinstance(v, str):
            try:
                from email.utils import parsedate_to_datetime
                return parsedate_to_datetime(v)
            except (ValueError, TypeError):
                # Fallback to ISO format parsing
                from datetime import datetime
                return datetime.fromisoformat(v.replace("Z", "+00:00"))
        return None if v is None else v


class SiteConfig(BaseModel):
    """Site configuration."""

    host: Optional[str] = None
    content: Optional[Dict[str, Any]] = None
    code: Optional[Dict[str, Any]] = None
    access: Optional[Dict[str, Any]] = None


class OrgConfig(BaseModel):
    """Organization configuration."""

    name: str
    sites: Optional[List[str]] = None
    groups: Optional[Dict[str, Any]] = None


class ProfileConfig(BaseModel):
    """Profile configuration."""

    name: str
    content: Optional[Dict[str, Any]] = None
    code: Optional[Dict[str, Any]] = None

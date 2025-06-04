#!/usr/bin/env python3
# Copyright 2024 AEM Admin Python Client Contributors
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Simple CLI tool for AEM Admin Python Client."""

import argparse
import json
import os
import sys
from typing import Optional

from aem_admin_client import AEMAdminClient, Config, get_client_from_env
from aem_admin_client.exceptions import AEMAdminError


def get_client(args) -> AEMAdminClient:
    """Create and return an AEM Admin client."""
    auth_token = args.token or os.getenv("AEM_AUTH_TOKEN")
    auth_cookie = args.cookie or os.getenv("AEM_AUTH_COOKIE")

    if not auth_token and not auth_cookie:
        print(
            "Error: Either --token or --cookie must be provided, or set AEM_AUTH_TOKEN/AEM_AUTH_COOKIE environment variable"
        )
        sys.exit(1)

    return AEMAdminClient(
        base_url=args.base_url,
        auth_token=auth_token,
        auth_cookie=auth_cookie,
        timeout=args.timeout,
    )


def cmd_status(args):
    """Get status of a resource."""
    client = get_client(args)
    try:
        status = client.status.get_status(args.org, args.site, args.ref, args.path)
        print(json.dumps(status.dict(), indent=2, default=str))
    except AEMAdminError as e:
        print(f"Error: {e}")
        sys.exit(1)
    finally:
        client.close()


def cmd_publish(args):
    """Publish a resource."""
    client = get_client(args)
    try:
        result = client.publish.publish_resource(
            args.org, args.site, args.ref, args.path
        )
        print(json.dumps(result, indent=2, default=str))
    except AEMAdminError as e:
        print(f"Error: {e}")
        sys.exit(1)
    finally:
        client.close()


def cmd_preview(args):
    """Preview a resource."""
    client = get_client(args)
    try:
        result = client.preview.preview_resource(
            args.org, args.site, args.ref, args.path
        )
        print(json.dumps(result, indent=2, default=str))
    except AEMAdminError as e:
        print(f"Error: {e}")
        sys.exit(1)
    finally:
        client.close()


def cmd_logs(args):
    """Get logs."""
    client = get_client(args)
    try:
        logs = client.log.get_logs(args.org, args.site, args.ref, since=args.since)
        print(json.dumps(logs.dict(), indent=2, default=str))
    except AEMAdminError as e:
        print(f"Error: {e}")
        sys.exit(1)
    finally:
        client.close()


def cmd_jobs(args):
    """List jobs."""
    client = get_client(args)
    try:
        jobs = client.job.list_jobs(args.org, args.site, args.ref, args.topic)
        print(json.dumps([job.dict() for job in jobs], indent=2, default=str))
    except AEMAdminError as e:
        print(f"Error: {e}")
        sys.exit(1)
    finally:
        client.close()


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(description="AEM Admin CLI Tool")

    # Global arguments
    parser.add_argument(
        "--base-url", default=Config.get_base_url(), help="Base URL for AEM Admin API"
    )
    parser.add_argument("--token", help="Bearer token for authentication")
    parser.add_argument("--cookie", help="Auth cookie for authentication")
    parser.add_argument(
        "--timeout",
        type=int,
        default=Config.get_timeout(),
        help="Request timeout in seconds",
    )

    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Status command
    status_parser = subparsers.add_parser("status", help="Get resource status")
    status_parser.add_argument("org", help="Organization name")
    status_parser.add_argument("site", help="Site ID")
    status_parser.add_argument("ref", help="Repository reference")
    status_parser.add_argument("path", help="Resource path")
    status_parser.set_defaults(func=cmd_status)

    # Publish command
    publish_parser = subparsers.add_parser("publish", help="Publish a resource")
    publish_parser.add_argument("org", help="Organization name")
    publish_parser.add_argument("site", help="Site ID")
    publish_parser.add_argument("ref", help="Repository reference")
    publish_parser.add_argument("path", help="Resource path")
    publish_parser.set_defaults(func=cmd_publish)

    # Preview command
    preview_parser = subparsers.add_parser("preview", help="Preview a resource")
    preview_parser.add_argument("org", help="Organization name")
    preview_parser.add_argument("site", help="Site ID")
    preview_parser.add_argument("ref", help="Repository reference")
    preview_parser.add_argument("path", help="Resource path")
    preview_parser.set_defaults(func=cmd_preview)

    # Logs command
    logs_parser = subparsers.add_parser("logs", help="Get logs")
    logs_parser.add_argument("org", help="Organization name")
    logs_parser.add_argument("site", help="Site ID")
    logs_parser.add_argument("ref", help="Repository reference")
    logs_parser.add_argument(
        "--since", default="1h", help="Time span (e.g., 5m, 1h, 1d)"
    )
    logs_parser.set_defaults(func=cmd_logs)

    # Jobs command
    jobs_parser = subparsers.add_parser("jobs", help="List jobs")
    jobs_parser.add_argument("org", help="Organization name")
    jobs_parser.add_argument("site", help="Site ID")
    jobs_parser.add_argument("ref", help="Repository reference")
    jobs_parser.add_argument("topic", help="Job topic")
    jobs_parser.set_defaults(func=cmd_jobs)

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    args.func(args)


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Example script demonstrating basic usage of the AEM Admin Client."""

import os

from aem_admin_client import AEMAdminClient


def main():
    """Run the example script."""
    # Create client instance
    client = AEMAdminClient(
        base_url=os.getenv("AEM_ADMIN_BASE_URL"),
        auth_token=os.getenv("AEM_ADMIN_AUTH_TOKEN"),
    )

    # Example organization, site, and reference
    org = os.getenv("AEM_DEFAULT_ORG")
    site = os.getenv("AEM_DEFAULT_SITE")
    ref = os.getenv("AEM_DEFAULT_REF")

    try:
        # 1. Get status of a resource
        print("Getting status of index page...")
        status = client.status.get_status(org, site, ref, "index")
        print(f"Status: {status.live.status if status.live else 'N/A'}")
        print(f"Preview URL: {status.preview.url if status.preview else 'N/A'}")
        print(f"Live URL: {status.live.url if status.live else 'N/A'}")

        # 2. Preview a resource
        print("\nPreviewing a resource...")
        preview_result = client.preview.preview_resource(org, site, ref, "index")
        print(f"Preview result: {preview_result}")

        # 3. Publish a resource
        print("\nPublishing a resource...")
        publish_result = client.publish.publish_resource(org, site, ref, "index")
        print(f"Publish result: {publish_result}")

        # # 4. Bulk status check
        # print("\nPerforming bulk status check...")
        # bulk_request = BulkStatusRequest(
        #     paths=[
        #         BulkStatusPath(path="index"),
        #         BulkStatusPath(prefix="/blog/"),
        #     ],
        #     select=["preview", "live"]
        # )
        # bulk_job = client.status.bulk_status(org, site, ref, bulk_request)
        # print(f"Bulk status job created: {bulk_job.job.name}")

        # # 5. Get job status
        # print("\nChecking job status...")
        # job_info = client.job.get_job(org, site, ref, "status", bulk_job.job.name)
        # print(f"Job state: {job_info.state}")

        # 6. Get logs
        print("\nGetting recent logs...")
        logs = client.log.get_logs(org, site, ref, since="1h")
        print(f"Found {len(logs.logs)} log entries")

        # 7. Cache operations
        print("\nPurging cache...")
        cache_result = client.cache.purge_cache(org, site, ref, "index")
        print(f"Cache purge result: {cache_result}")

        # 8. Configuration management
        print("\nGetting site configuration...")
        try:
            site_config = client.config.get_site_config(org, site)
            print(f"Site host: {site_config.host}")
        except Exception as e:
            print(f"Could not get site config: {e}")

    except Exception as e:
        print(f"Error: {e}")

    finally:
        # Clean up
        client.close()


if __name__ == "__main__":
    main()

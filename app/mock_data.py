import random
import time
from app.failure_scenarios import FAILURE_SCENARIOS, DEGRADED_DESCRIPTIONS

REGIONS = ["nz-hlz-1", "nz-por-1", "nz-wlg-1"]
SERVICES = ["nova", "neutron", "cinder", "keystone", "glance"]


def get_mock_region_health(region: str, force_failure: bool = False) -> dict:
    """
    Returns simulated health data for a given OpenStack region.
    
    force_failure=True triggers the region's specific failure scenario
    from failure_scenarios.py — using real OpenStack error strings.
    
    In production: replace this with real OpenStack SDK calls.
    The interface stays identical — only the data source changes.
    """
    health = {}
    scenario = FAILURE_SCENARIOS.get(region, {})

    for service in SERVICES:
        if force_failure and scenario.get("service") == service:
            # Use the real error string from failure_scenarios.py
            health[service] = {
                "status": scenario["status"],
                "latency_ms": scenario["latency_ms"],
                "error": scenario["error_string"],
                "last_checked": int(time.time())
            }
        else:
            rand = random.random()
            if rand > 0.90:
                status = "degraded"
                error = DEGRADED_DESCRIPTIONS.get(service, "")
            else:
                status = "healthy"
                error = None

            health[service] = {
                "status": status,
                "latency_ms": round(random.uniform(10, 200), 2),
                "error": error,
                "last_checked": int(time.time())
            }

    return health


def get_all_regions(force_failure_region: str = None) -> dict:
    """
    Returns health data for all NZ regions.
    Optionally force one region into its specific failure scenario.
    """
    result = {}
    for region in REGIONS:
        force = (region == force_failure_region)
        result[region] = get_mock_region_health(region, force_failure=force)
    return result

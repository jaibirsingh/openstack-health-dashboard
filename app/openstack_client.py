import os
from app.mock_data import get_all_regions
from app.failure_scenarios import FAILURE_SCENARIOS

# DEMO_MODE=true uses mock data
# DEMO_MODE=false uses real OpenStack SDK (production path)
DEMO_MODE = os.environ.get("DEMO_MODE", "true").lower() == "true"

# Tracks which region is currently in simulated failure
_forced_failure_region = None


def set_failure_region(region: str):
    global _forced_failure_region
    _forced_failure_region = region


def clear_failure_region():
    global _forced_failure_region
    _forced_failure_region = None


def get_forced_failure_region():
    return _forced_failure_region


def get_cluster_health() -> dict:
    """
    Main entry point. Returns health of all OpenStack regions.
    
    Demo mode: returns realistic mock data with real error strings.
    Production mode: replace with real OpenStack SDK calls below.
    
    The interface is identical in both modes — swapping is one config change.
    """
    if DEMO_MODE:
        return get_all_regions(force_failure_region=_forced_failure_region)

    # --- Production path (real OpenStack SDK) ---
    # Uncomment and configure when connecting to a real cluster:
    #
    # import openstack
    # conn = openstack.connect(cloud='catalyst')
    #
    # result = {}
    # for region in ['nz-hlz-1', 'nz-por-1', 'nz-wlg-1']:
    #     services = {}
    #     try:
    #         conn.compute.servers()
    #         services['nova'] = {'status': 'healthy', 'latency_ms': 50}
    #     except Exception as e:
    #         services['nova'] = {'status': 'down', 'error': str(e)}
    #     result[region] = services
    # return result
    pass


def get_active_failure_scenario() -> dict:
    """
    Returns the active failure scenario details if one is running.
    Used by the LLM advisor to get the real error string.
    """
    if _forced_failure_region:
        return FAILURE_SCENARIOS.get(_forced_failure_region, {})
    return {}

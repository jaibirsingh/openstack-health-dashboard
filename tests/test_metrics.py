from app.mock_data import get_mock_region_health, get_all_regions
from app.openstack_client import (
    get_cluster_health, set_failure_region, clear_failure_region
)


def test_region_health_returns_all_services():
    health = get_mock_region_health("nz-hlz-1")
    assert "nova" in health
    assert "neutron" in health
    assert "cinder" in health
    assert "keystone" in health
    assert "glance" in health


def test_service_status_is_valid():
    health = get_mock_region_health("nz-hlz-1")
    for service, info in health.items():
        assert info["status"] in ["healthy", "degraded", "down"]


def test_forced_failure_sets_nova_down_in_hlz():
    health = get_mock_region_health("nz-hlz-1", force_failure=True)
    assert health["nova"]["status"] == "down"


def test_forced_failure_sets_neutron_degraded_in_por():
    health = get_mock_region_health("nz-por-1", force_failure=True)
    assert health["neutron"]["status"] == "degraded"


def test_all_regions_returned():
    data = get_all_regions()
    assert "nz-hlz-1" in data
    assert "nz-por-1" in data
    assert "nz-wlg-1" in data


def test_failure_region_propagates_through_client():
    set_failure_region("nz-hlz-1")
    data = get_cluster_health()
    assert data["nz-hlz-1"]["nova"]["status"] == "down"
    clear_failure_region()


def test_clear_failure_removes_forced_state():
    set_failure_region("nz-hlz-1")
    clear_failure_region()
    data = get_cluster_health()
    assert data is not None

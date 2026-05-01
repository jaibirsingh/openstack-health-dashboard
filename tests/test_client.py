from app.openstack_client import (
    get_cluster_health,
    set_failure_region,
    clear_failure_region,
    get_active_failure_scenario
)


def test_cluster_health_returns_all_regions():
    data = get_cluster_health()
    assert "nz-hlz-1" in data
    assert "nz-por-1" in data
    assert "nz-wlg-1" in data


def test_set_failure_region_returns_scenario():
    set_failure_region("nz-hlz-1")
    scenario = get_active_failure_scenario()
    assert scenario["service"] == "nova"
    clear_failure_region()


def test_clear_failure_returns_none():
    set_failure_region("nz-hlz-1")
    clear_failure_region()
    scenario = get_active_failure_scenario()
    assert scenario == {}
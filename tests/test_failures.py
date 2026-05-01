from app.failure_scenarios import FAILURE_SCENARIOS
from app.mock_data import get_mock_region_health
from app.llm_advisor import build_prompt


def test_failure_scenarios_have_required_keys():
    for region, scenario in FAILURE_SCENARIOS.items():
        assert "service" in scenario
        assert "error_string" in scenario
        assert "status" in scenario
        assert "latency_ms" in scenario


def test_failure_error_string_is_not_empty():
    for region, scenario in FAILURE_SCENARIOS.items():
        assert len(scenario["error_string"]) > 20


def test_forced_failure_includes_error_string():
    health = get_mock_region_health("nz-hlz-1", force_failure=True)
    assert health["nova"]["error"] is not None
    assert len(health["nova"]["error"]) > 10


def test_llm_prompt_includes_error_string_when_provided():
    prompt = build_prompt("nova", "RabbitMQ connection timeout")
    assert "RabbitMQ connection timeout" in prompt


def test_llm_prompt_works_without_error_string():
    prompt = build_prompt("nova", None)
    assert "nova" in prompt.lower()


def test_cinder_failure_has_iscsi_error():
    scenario = FAILURE_SCENARIOS["nz-wlg-1"]
    assert "iSCSI" in scenario["error_string"]
    assert scenario["service"] == "cinder"


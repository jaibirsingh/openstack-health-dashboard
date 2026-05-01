from flask import Flask, jsonify, render_template, request
from app.openstack_client import (
    get_cluster_health,
    set_failure_region,
    clear_failure_region,
    get_active_failure_scenario
)
from app.llm_advisor import get_diagnosis

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('dashboard.html')


@app.route('/api/health')
def health():
    return jsonify(get_cluster_health())


@app.route('/api/diagnose', methods=['POST'])
def diagnose():
    """
    Accepts service name and optional real error string.
    Passes both to the LLM for specific diagnosis.
    This is AIOps — AI interpreting real infrastructure errors.
    """
    body = request.get_json()
    service = body.get('service', 'unknown')
    error_string = body.get('error_string', None)

    diagnosis = get_diagnosis(service, error_string)

    # Tell the UI whether we used Ollama or fallback
    try:
        import requests as req
        test = req.get("http://localhost:11434", timeout=2)
        model_used = "Ollama/Llama3 (local — NZ sovereign)"
    except Exception:
        model_used = "Built-in expert fallback"

    return jsonify({
        "service": service,
        "diagnosis": diagnosis,
        "model_used": model_used
    })


@app.route('/api/simulate-failure/<region>', methods=['POST'])
def simulate_failure(region):
    set_failure_region(region)
    scenario = get_active_failure_scenario()
    return jsonify({
        "status": "failure simulated",
        "region": region,
        "affected_service": scenario.get("service"),
        "error": scenario.get("error_string")
    })


@app.route('/api/clear-failure', methods=['POST'])
def clear_failure():
    clear_failure_region()
    return jsonify({"status": "cleared", "regions": "all healthy"})


@app.route('/metrics')
def metrics():
    """
    Prometheus-compatible metrics endpoint.
    Catalyst Cloud runs monitoring infrastructure — 
    this shows understanding of observability standards.
    """
    health = get_cluster_health()
    lines = []
    lines.append("# HELP openstack_service_up Service health (1=healthy, 0=down)")
    lines.append("# TYPE openstack_service_up gauge")

    for region, services in health.items():
        for service, info in services.items():
            val = 1 if info['status'] == 'healthy' else 0
            lines.append(
                f'openstack_service_up{{region="{region}",'
                f'service="{service}"}} {val}'
            )

    lines.append("")
    lines.append("# HELP openstack_service_latency_ms Service latency in ms")
    lines.append("# TYPE openstack_service_latency_ms gauge")

    for region, services in health.items():
        for service, info in services.items():
            lines.append(
                f'openstack_service_latency_ms{{region="{region}",'
                f'service="{service}"}} {info["latency_ms"]}'
            )

    return '\n'.join(lines), 200, {'Content-Type': 'text/plain; version=0.0.4'}


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

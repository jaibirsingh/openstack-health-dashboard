import requests

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "llama3"

# Fallback diagnoses when Ollama is not running
# These are technically accurate — not placeholder text
FALLBACK_DIAGNOSES = {
    "nova": (
        "RabbitMQ connection timeout indicates the AMQP messaging layer between "
        "nova-conductor and nova-compute is broken. Check RabbitMQ service status "
        "first: 'systemctl status rabbitmq-server', then inspect nova-conductor.log "
        "for AMQP reconnection attempts."
    ),
    "neutron": (
        "OVS Agent failure with missing br-int bridge indicates the Open vSwitch "
        "integration bridge was not created or was deleted. Run 'ovs-vsctl show' to "
        "inspect bridge state, then restart neutron-openvswitch-agent to rebuild "
        "the bridge configuration."
    ),
    "cinder": (
        "iSCSI target connection failure on port 3260 means the storage backend "
        "is unreachable at the network level. Verify storage node is up, check "
        "iSCSI initiator connectivity with 'iscsiadm -m discovery', and inspect "
        "cinder-volume.log for volume manager exit reason."
    ),
    "keystone": (
        "Keystone token validation latency near DB connection pool limit suggests "
        "the Fernet token provider is waiting on database connections. Check "
        "keystone.log for DB timeout errors and verify connection pool settings "
        "in keystone.conf."
    ),
    "glance": (
        "Glance API degradation with slow image store response points to Swift "
        "or Ceph backend I/O contention. Check glance-api.log for store backend "
        "timeout errors and verify backend storage health independently."
    )
}


def build_prompt(service: str, error_string: str = None) -> str:
    """
    Build a prompt for the LLM.
    If a real error string is available, include it for specific diagnosis.
    This is AIOps — using AI to interpret real infrastructure error logs.
    """
    if error_string:
        return (
            f"You are an OpenStack infrastructure engineer at a NZ cloud provider.\n"
            f"A monitoring system has detected the following live error:\n\n"
            f"  {error_string}\n\n"
            f"In exactly 2 sentences: what is the most likely root cause, "
            f"and what is the first command or check the engineer should run?"
        )
    else:
        return (
            f"OpenStack {service} service is showing degraded performance. "
            f"In 2 sentences, what are the most likely causes and "
            f"what should an engineer check first?"
        )


def get_diagnosis(service: str, error_string: str = None) -> str:
    """
    Query local Ollama LLM for diagnosis.
    
    Passes real OpenStack error strings when available — 
    this is AIOps in action, mirroring what Cove's managed LLM 
    service does on NZ sovereign infrastructure.
    
    Falls back to hardcoded expert diagnosis if Ollama unavailable.
    """
    prompt = build_prompt(service, error_string)

    try:
        response = requests.post(
            OLLAMA_URL,
            json={
                "model": MODEL,
                "prompt": prompt,
                "stream": False
            },
            timeout=15
        )
        if response.status_code == 200:
            result = response.json().get("response", "").strip()
            if result:
                return result
    except Exception:
        pass

    # Fallback — technically accurate, not generic
    return FALLBACK_DIAGNOSES.get(
        service,
        "Check service logs and verify all dependent services are healthy."
    )

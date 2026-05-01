"""
Real OpenStack failure scenarios with actual error strings.
"""

FAILURE_SCENARIOS = {
    "nz-hlz-1": {
        "service": "nova",
        "error_string": (
            "NovaException: VolumeBackendAPIException: "
            "Failed to connect to hypervisor on host nz-hlz-1-compute-02. "
            "RabbitMQ connection timeout after 30s. "
            "nova-conductor log: AMQP server unreachable."
        ),
        "status": "down",
        "latency_ms": 9999
    },
    "nz-por-1": {
        "service": "neutron",
        "error_string": (
            "NeutronException: OVS Agent failed on nz-por-1-network-01. "
            "neutron.agent.common.ovs_lib: Bridge br-int not found. "
            "Network namespace corruption detected. "
            "L2 agent heartbeat timeout: 75s."
        ),
        "status": "degraded",
        "latency_ms": 4200
    },
    "nz-wlg-1": {
        "service": "cinder",
        "error_string": (
            "CinderException: VolumeBackendAPIException: "
            "Storage backend unreachable on nz-wlg-1-storage-01. "
            "iSCSI target connection failed: connection refused port 3260. "
            "Volume manager exited unexpectedly."
        ),
        "status": "down",
        "latency_ms": 8800
    }
}

# Maps each OpenStack service to a realistic degraded state description
# Used when random degradation occurs (not a full simulated failure)
DEGRADED_DESCRIPTIONS = {
    "nova": "nova-scheduler latency elevated — possible RabbitMQ queue backlog",
    "neutron": "neutron-server response degraded — OVS agent may be under load",
    "cinder": "cinder-volume response slow — storage backend I/O contention",
    "keystone": "keystone token validation latency elevated — DB connection pool near limit",
    "glance": "glance-api degraded — image store backend responding slowly"
}

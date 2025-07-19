from enum import Enum

class MetricName(str, Enum):
    bandwidth_usage = "bandwidth_usage"
    latency = "latency"
    packet_errors = "packet_errors"

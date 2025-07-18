CREATE TABLE IF NOT EXISTS metric (
    switch_id VARCHAR PRIMARY KEY,
    bandwidth_usage FLOAT,
    latency FLOAT,
    packet_errors INTEGER
);

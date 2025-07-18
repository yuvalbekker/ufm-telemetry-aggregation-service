CREATE TABLE IF NOT EXISTS metric (
    switch_id VARCHAR(255) PRIMARY KEY,
    bandwidth_usage FLOAT,
    latency FLOAT,
    packet_errors INTEGER,
    collection_time TIMESTAMP,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

import uuid
import random
import csv
from datetime import datetime, timezone

def generate_csv(filename="telemetry_sample.csv", num_rows=100):
    with open(filename, "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        # Write header
        writer.writerow(["switch_id", "bandwidth_usage", "latency", "packet_errors", "collection_time"])
        # Write rows of sample data
        for _ in range(num_rows):
            switch_id = str(uuid.uuid4())
            bandwidth_usage = round(random.uniform(10, 1000), 2)  # Mbps
            latency = round(random.uniform(0.1, 10.0), 2)         # ms
            packet_errors = random.randint(0, 100)
            collection_time = datetime.now(timezone.utc).isoformat()
            writer.writerow([switch_id, bandwidth_usage, latency, packet_errors, collection_time])
    print(f"Generated {num_rows} rows in {filename}")

if __name__ == "__main__":
    generate_csv()
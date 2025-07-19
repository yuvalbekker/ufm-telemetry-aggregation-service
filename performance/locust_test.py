from locust import HttpUser, task, between
import random


class APIUser(HttpUser):
    wait_time = between(1, 3)
    switch_ids = [
        "da1d600c-dfa5-4843-8252-58c3fda0e0f4", "b516d533-7e7c-4b3b-9774-796737d438d3",
        "73d719fe-079f-4e85-849e-88b35d54f9d5", "18575e48-d55f-4b81-8670-95aa4db3b3c9",
        "c602f1c1-7bdc-4eae-bae0-e68c7e5d4f95", "f1739bcc-bca4-43ac-a2db-75e2b3b73d3f",
        "9dce0e34-8c95-458f-b264-1c9912f7c6a3", "03c1b58c-c152-4f13-9363-b7af143819f1",
        "e4928b46-c759-46bb-8329-322aa8435fb2", "fdc00b1a-7932-4389-b649-5a3cd66d27a2",
        "cfddcca8-eb18-4db6-8e2b-e529b9c48be6", "3f9ae9e9-6136-45a4-948f-e3e86703c52a",
        "4bd1271e-b195-4afb-bb1f-d5f8bd235242", "54b0be10-a8da-452c-af84-e90fd5bbc1f6",
        "aa394cc4-a97d-4f37-b9f1-9c64ba494682", "c616dc23-1666-42df-a0c4-722a4dab5db7",
        "f5fd8ca1-fb84-4dd4-89a0-73503e99d3c5", "2883ace9-bd94-4eaa-a319-3af905164be9",
        "80c2318c-6084-451b-bbe2-37314b8e951b", "00848188-e568-4b59-a95a-9219c8573f03"
    ]
    metric_names = ["latency", "bandwidth_usage", "packet_errors"]

    @task(2)
    def get_latency(self):
        self.client.get("/telemetry/ListMetrics/latency")

    @task(2)
    def get_bandwidth_usage(self):
        self.client.get("/telemetry/ListMetrics/bandwidth_usage")

    @task(2)
    def get_packet_errors(self):
        self.client.get("/telemetry/ListMetrics/packet_errors")

    @task(1)
    def get_metric_for_switch(self):
        metric = random.choice(self.metric_names)
        switch_id = random.choice(self.switch_ids)
        self.client.get(f"/telemetry/GetMetric/{metric}/{switch_id}")

# UFM Telemetry Aggregation Service

A FastAPI-based service for aggregating and managing UFM (Unified Fabric Manager) telemetry data.

## Quick Start

### Prerequisites

- Docker
- Docker Compose

### Clone the Repository

```bash
git clone <repository-url>
cd ufm-telemetry-aggregation-service
```

### Local Development Setup

1. **Start the services:**
   ```bash
   cd local
   docker-compose up -d
   ```

2. **Check service status:**
   ```bash
   docker-compose ps
   ```

3. **View logs:**
   ```bash
   docker-compose logs -f api
   ```

4. **Stop the services:**
   ```bash
   docker-compose down
   ```

## API Examples

The service runs on `http://localhost:8080` and provides the following endpoints:

### Health Check

Check if the service is running and healthy:

```bash
curl -X GET "http://localhost:8080/telemetry/health"
```

**Response:**
```json
{
  "service": "ufm-telemetry-aggregation-service",
  "status": "OK",
  "version": "1.0.0"
}
```

### Get Metric

Retrieve a specific metric for a switch:

```bash
curl -X GET "http://localhost:8080/telemetry/GetMetric/{metric_name}/{switch_id}"
```

**Example:**
```bash
curl -X GET "http://localhost:8080/telemetry/GetMetric/cpu_utilization/switch_001"
```

**Response:**
```json
{
  "switch_id": "switch_001",
  "metric_name": "cpu_utilization",
  "value": 75.5,
  "timestamp": "2024-01-01T12:00:00Z"
}
```

### List Metrics

Retrieve multiple metrics with pagination:

```bash
curl -X GET "http://localhost:8080/telemetry/ListMetrics/{metric_name}?limit=10&offset=0"
```

**Example:**
```bash
curl -X GET "http://localhost:8080/telemetry/ListMetrics/cpu_utilization?limit=5&offset=0"
```

**Response:**
```json
{
  "metrics": [
    {
      "switch_id": "switch_001",
      "metric_name": "cpu_utilization",
      "value": 75.5,
      "timestamp": "2024-01-01T12:00:00Z"
    }
  ],
  "total": 100,
  "limit": 5,
  "offset": 0
}
```

### Interactive API Documentation

Once the service is running, you can access the interactive API documentation:

- **Swagger UI:** http://localhost:8080/docs
- **ReDoc:** http://localhost:8080/redoc

## System Architecture

![System Architecture](docs/architecture.png)

## System Overview

The UFM Telemetry Aggregation Service is designed as a robust, scalable, and highly available system for collecting, processing, and serving network switch telemetry data. The architecture follows modern microservices principles with clear separation of concerns across three main operational layers.

### 1. Telemetry Generation

**Source & Collection:**
Telemetry data originates from a dedicated REST API service running in the `telemetry-counters-api` container. This API exposes real-time switch metrics through a `/counters` endpoint at `http://localhost:9001/counters`, delivering the data in CSV format.

**Event Generation:**
The `telemetry-event-generator` container operates as a periodicic client, fetching fresh metrics from the `/counters` endpoint. This component transforms raw CSV data into structured telemetry objects and publishing the metrics in  batches of 10 messages every 10 seconds to an AWS SNS topic (emulated via LocalStack).

### 2. Data Handling

**Decoupled Message Architecture:**
The system implements a message-driven architecture that completely decouples metric ingestion from storage operations. SNS topics connect to SQS queues, creating a durable, fault-tolerant buffer that can handle traffic spikes and temporary service outages.

**Processing Pipeline:**
The `telemetry-aggregation-worker` container serves as the system's data processing engine, continuously consuming messages from the SQS queue. Each worker processes metric batches, performs data validation and transformation, then persists structured data to the PostgreSQL metrics table.

**Optimized Database Schema:**
The PostgreSQL metrics table is designed for high-performance queries and comprehensive monitoring capabilities. The schema includes an index on the `switch_id` column, enabling fast retrieval of metrics for specific switches ids by the `/GetMetric` endpoint.

The table employs a dual-timestamp approach:
- **Collection Time:** Records when the metric was originally calculated by the counters API
- **Insertion Timestamp:** Captures when the metric was persisted to the database

This design enables system health monitoring. The difference between collection time and insertion timestamp serves as a real-time indicator of processing latency. Large gaps can signal bottlenecks in the ingestion pipeline, network issues, or resource constraints. This latency differential can be leveraged to:
- Create automated alerts for processing delays
- Generate system health metrics and dashboards  
- Trigger auto-scaling events when latency thresholds are exceeded
- Provide operational insights for capacity planning

**Key Advantages:**
- **Fault Tolerance:** SQS message persistence ensures zero data loss during system maintenance or failures
- **Elastic Scalability:** Worker containers can be horizontally scaled based on queue depth, automatically adapting to load
- **Performance Optimization:** Batch processing minimizes database connections and transaction overhead
- **Operational Resilience:** Message replay capability enables recovery from processing errors
- **Load Distribution:** Multiple workers can process messages concurrently for maximum throughput

### 3. REST Server Integration

**API Layer:**
The `telemetry-aggregation-api` container provides a RESTful interface for accessing processed telemetry data. This FastAPI-based service executes queries directly against the PostgreSQL database and delivering real-time
insights.

**Enterprise-Ready Features:**
- **Real-Time Access:** Direct database queries ensure immediate access to the latest processed metrics
- **Comprehensive API:** Full CRUD operations with advanced filtering, pagination, and search capabilities  
- **Interactive Documentation:** Built-in Swagger UI and ReDoc for seamless API exploration and testing
- **Type Safety:** Pydantic models ensure data consistency and automatic API documentation

**Key Advantages:**
- **Low Latency:** Direct database access minimizes response times for analytical queries
- **Developer Experience:** OpenAPI specification enables automatic client generation and testing
- **Monitoring Ready:** Built-in health checks and metrics endpoints support operational monitoring
- **Scalable Architecture:** Stateless design allows horizontal scaling of API instances

**Container-Native Design:**
All system components are orchestrated using Docker Compose, providing:


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

## System Overview

The UFM Telemetry Aggregation Service is designed as a robust, scalable, and highly available system for collecting, processing, and serving network switch telemetry data. The architecture follows modern microservices principles with clear separation of concerns across three main operational layers.

### 1. Telemetry Generation

**Source & Collection:**
Telemetry data originates from a dedicated REST API service running in the `telemetry-counters-api` container. This API exposes real-time switch metrics through a `/counters` endpoint at `http://localhost:9001/counters`, delivering comprehensive performance data in efficient CSV format.

**Intelligent Event Generation:**
The `telemetry-event-generator` container operates as an intelligent periodic client, fetching fresh metrics every 10 seconds. This component transforms raw CSV data into structured telemetry objects and employs a sophisticated batching strategy—publishing metrics in optimized batches of 10 messages to an AWS SNS topic (emulated via LocalStack).

**Key Advantages:**
- **High Throughput:** Batched publishing maximizes message throughput while minimizing API overhead
- **Reliability:** Consistent 10-second intervals ensure no data gaps
- **Scalability:** Architecture supports monitoring hundreds of switches without performance degradation
- **Cloud-Native:** SNS integration provides enterprise-grade message delivery guarantees

### 2. Data Handling

**Decoupled Message Architecture:**
The system implements a sophisticated message-driven architecture that completely decouples metric ingestion from storage operations. SNS topics seamlessly connect to SQS queues, creating a durable, fault-tolerant buffer that can handle traffic spikes and temporary service outages.

**Intelligent Processing Pipeline:**
The `telemetry-aggregation-worker` container serves as the system's data processing engine, continuously consuming messages from the SQS queue. Each worker processes metric batches, performs data validation and transformation, then persists structured data to the PostgreSQL metrics table.

**Key Advantages:**
- **Fault Tolerance:** SQS message persistence ensures zero data loss during system maintenance or failures
- **Elastic Scalability:** Worker containers can be horizontally scaled based on queue depth, automatically adapting to load
- **Performance Optimization:** Batch processing minimizes database connections and transaction overhead
- **Operational Resilience:** Message replay capability enables recovery from processing errors
- **Load Distribution:** Multiple workers can process messages concurrently for maximum throughput

### 3. REST Server Integration

**High-Performance API Layer:**
The `telemetry-aggregation-api` container provides a powerful, RESTful interface for accessing processed telemetry data. This FastAPI-based service executes optimized queries directly against the PostgreSQL database, delivering real-time insights through well-documented endpoints.

**Enterprise-Ready Features:**
- **Real-Time Access:** Direct database queries ensure immediate access to the latest processed metrics
- **Comprehensive API:** Full CRUD operations with advanced filtering, pagination, and search capabilities  
- **Interactive Documentation:** Built-in Swagger UI and ReDoc for seamless API exploration and testing
- **Type Safety:** Pydantic models ensure data consistency and automatic API documentation

**Key Advantages:**
- **Low Latency:** Direct database access minimizes response times for analytical queries
- **Data Consistency:** All served data reflects successfully processed and validated metrics
- **Developer Experience:** OpenAPI specification enables automatic client generation and testing
- **Monitoring Ready:** Built-in health checks and metrics endpoints support operational monitoring
- **Scalable Architecture:** Stateless design allows horizontal scaling of API instances

### Orchestration & Deployment

**Container-Native Design:**
All system components are orchestrated using Docker Compose, providing:

- **Consistent Environments:** Identical deployment across development, staging, and production
- **Simplified Operations:** Single-command deployment with automatic dependency management
- **Service Discovery:** Built-in networking enables seamless inter-service communication
- **Resource Management:** Configurable resource limits and health monitoring
- **Development Velocity:** Hot-reload capabilities and integrated debugging support

This architecture delivers enterprise-grade reliability while maintaining the flexibility needed for rapid development and deployment cycles.

## Architecture

The service consists of:

- **API Service:** FastAPI application handling HTTP requests
- **Database:** PostgreSQL for storing telemetry data
- **Worker:** Background worker for data processing (optional)

## Environment Variables

Create a `.env` file in the `local` directory with the following variables:

```env
POSTGRES_USER=your_db_user
POSTGRES_PASSWORD=your_db_password
POSTGRES_DB=telemetry_db
```

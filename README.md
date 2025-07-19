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

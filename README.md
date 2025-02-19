# Quantile Calculation API

## Overview
This is a FastAPI-based service that provides quantile computation for dynamically stored numerical pools. It allows users to:
- Append values to a pool (creating one if it does not exist).
- Query a percentile from a pool.
- Handle concurrent access safely.

## Features
- Efficient quantile computation using **NumPy** for large pools.
- **Thread-safe** storage with an in-memory data structure.
- **Optimized insertion** using `bisect.insort()` for better query performance.
- **Asynchronous background processing** for appending data.

## Installation

1. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```

2. Run the FastAPI server:
   ```sh
   bash run.sh
   ```
   The service will start at `http://0.0.0.0:8000`.

## API Endpoints

### 1. Append Values to a Pool
**Endpoint:**
```
POST /append_pool
```
**Request Body:**
```json
{
  "poolId": 1,
  "poolValues": [10, 20, 30]
}
```
**Response:**
```json
{
  "status": "appended"
}
```

### 2. Query a Quantile
**Endpoint:**
```
POST /query_pool
```
**Request Body:**
```json
{
  "poolId": 1,
  "percentile": 50
}
```
**Response:**
```json
{
  "quantile": 20,
  "count": 3
}
```

## Testing
Run unit tests with:
```sh
pytest tests/
```



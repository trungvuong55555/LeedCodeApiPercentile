from fastapi import FastAPI, HTTPException, BackgroundTasks
from app.models import AppendPoolRequest, QueryPoolRequest
from app.services import compute_quantile
from app.storage import get_pool_values, append_to_pool
import uvicorn

appAPI = FastAPI()


@appAPI.post("/append_pool")
async def append_pool(request: AppendPoolRequest, background_tasks: BackgroundTasks):
    """Append values asynchronously to reduce request latency."""
    if not request.poolValues:
        raise HTTPException(status_code=400, detail="poolValues must not be empty")

    background_tasks.add_task(append_to_pool, request.poolId, request.poolValues)
    return {"status": "processing"}


@appAPI.post("/query_pool")
async def query_pool(request: QueryPoolRequest):
    """Retrieve the quantile from a pool (if exists)."""
    values = get_pool_values(request.poolId)
    if values is None:
        raise HTTPException(status_code=404, detail="Pool not found")

    try:
        result = compute_quantile(values, request.percentile)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    return {"quantile": result, "count": len(values)}


if __name__ == "__main__":
    uvicorn.run(appAPI, host="0.0.0.0", port=8000)

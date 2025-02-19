from pydantic import BaseModel, Field
from typing import List


class AppendPoolRequest(BaseModel):
    """Request model for appending values to a pool."""
    poolId: int = Field(..., gt=0, description="Pool ID must be a positive integer")
    poolValues: List[float] = Field(..., min_items=1, description="List of values must not be empty")


class QueryPoolRequest(BaseModel):
    """Request model for querying a quantile from a pool."""
    poolId: int = Field(..., gt=0, description="Pool ID must be a positive integer")
    percentile: float = Field(..., ge=0, le=100, description="Percentile must be between 0 and 100")

import sys
import os
from fastapi.testclient import TestClient

# Ensure the app folder is in sys.path
sys.path.insert(0, os.path.abspath(os.path.dirname(os.path.dirname(__file__))))
from app.main import appAPI
# Create a test client
client = TestClient(appAPI)

def test_append_pool():
    """Test appending values to a pool."""
    response = client.post("/append_pool", json={"poolId": 1, "poolValues": [10, 20, 30]})
    assert response.status_code == 200
    assert response.json() == {"status": "inserted"}

def test_query_pool():
    """Test querying a quantile from a pool."""
    response = client.post("/query_pool", json={"poolId": 1, "percentile": 50})
    assert response.status_code == 200
    assert "quantile" in response.json()
    assert "count" in response.json()

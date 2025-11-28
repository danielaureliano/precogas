import requests
import redis
from fastapi.testclient import TestClient
from unittest.mock import patch
from app.main import app

client = TestClient(app)

@patch("app.main.requests.head")
@patch("app.main.redis_client") # Alvo do mock é agora a referência em app.main
def test_health_check_ok(mock_redis_client, mock_requests_head):
    """
    Testa o endpoint /health quando a conexão com a internet e o Redis estão OK.
    """
    mock_requests_head.return_value.raise_for_status.return_value = None
    mock_redis_client.ping.return_value = True # Garante que ping retorne True

    response = client.get("/health")

    assert response.status_code == 200
    assert response.json()["status"] == "UP"
    assert response.json()["checks"]["internet_connection"] == "OK"
    assert response.json()["checks"]["redis_connection"] == "OK"

@patch("app.main.requests.head")
@patch("app.main.redis_client")
def test_health_check_fail_internet(mock_redis_client, mock_requests_head):
    """
    Testa o endpoint /health quando a conexão com a internet falha.
    """
    mock_requests_head.side_effect = requests.exceptions.RequestException("Internet down")
    mock_redis_client.ping.return_value = True # Garante que ping retorne True

    response = client.get("/health")

    assert response.status_code == 503
    assert response.json()["status"] == "DOWN"
    assert "FAIL" in response.json()["checks"]["internet_connection"]
    assert response.json()["checks"]["redis_connection"] == "OK"

@patch("app.main.requests.head")
@patch("app.main.redis_client")
def test_health_check_fail_redis(mock_redis_client, mock_requests_head):
    """
    Testa o endpoint /health quando a conexão com o Redis falha.
    """
    mock_requests_head.return_value.raise_for_status.return_value = None
    mock_redis_client.ping.side_effect = redis.exceptions.ConnectionError("Redis down")

    response = client.get("/health")

    assert response.status_code == 503
    assert response.json()["status"] == "DOWN"
    assert response.json()["checks"]["internet_connection"] == "OK"
    assert "FAIL" in response.json()["checks"]["redis_connection"]

@patch("app.main.requests.head")
@patch("app.main.redis_client", None) # Mocks app.main.redis_client para ser None
def test_health_check_redis_not_initialized(mock_requests_head):
    """
    Testa o endpoint /health quando o cliente Redis não foi inicializado (startup fail).
    """
    mock_requests_head.return_value.raise_for_status.return_value = None

    response = client.get("/health")

    assert response.status_code == 200
    assert response.json()["status"] == "UP"
    assert response.json()["checks"]["internet_connection"] == "OK"
    assert "WARNING" in response.json()["checks"]["redis_connection"]

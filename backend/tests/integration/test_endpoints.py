"""Integration tests for all API endpoints."""

import pytest
from fastapi.testclient import TestClient

from main import app

# Create test client
client = TestClient(app)


class TestCryptoEndpoints:
    """Test crypto/token endpoints."""

    def test_mint_token_success(self):
        """Test successful token minting."""
        response = client.post(
            "/api/v1/crypto/mint-token",
            json={
                "agent_id": "agent_test_001",
                "user_id": 1,
                "user_role": "analyst_l3",
                "ticket_id": 42,
            },
        )

        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert "token" in data["data"]
        assert "expires_at" in data["data"]
        assert "ttl_seconds" in data["data"]

    def test_mint_token_invalid_user_id(self):
        """Test token minting with invalid user ID."""
        response = client.post(
            "/api/v1/crypto/mint-token",
            json={
                "agent_id": "agent_test",
                "user_id": -1,  # Invalid
                "user_role": "analyst_l3",
            },
        )

        assert response.status_code == 422  # Validation error

    def test_verify_token_success(self):
        """Test successful token verification."""
        # First mint a token
        mint_response = client.post(
            "/api/v1/crypto/mint-token",
            json={
                "agent_id": "agent_verify",
                "user_id": 1,
                "user_role": "analyst_l3",
            },
        )
        token = mint_response.json()["data"]["token"]

        # Now verify it
        verify_response = client.post(
            "/api/v1/crypto/verify-token",
            json={
                "token": token,
                "expected_session_id": "agent_verify",
            },
        )

        assert verify_response.status_code == 200
        data = verify_response.json()
        assert data["success"] is True
        assert data["data"]["valid"] is True
        assert data["data"]["expired"] is False

    def test_verify_token_invalid_format(self):
        """Test verification of malformed token."""
        response = client.post(
            "/api/v1/crypto/verify-token",
            json={
                "token": "invalid_token_format",
            },
        )

        assert response.status_code == 200
        data = response.json()
        assert data["data"]["valid"] is False

    def test_get_key_status(self):
        """Test getting HSM key status."""
        response = client.get("/api/v1/crypto/key-status")

        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert "key_id" in data["data"]
        assert "key_age_minutes" in data["data"]
        assert "should_rotate" in data["data"]


class TestDatabaseEndpoints:
    """Test database query endpoints."""

    def test_execute_query_success(self):
        """Test successful query execution."""
        response = client.post(
            "/api/v1/database/query",
            json={
                "query": "SELECT * FROM users WHERE role = ?",
                "params": ["admin"],
                "limit": 100,
            },
        )

        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert "transaction_id" in data["data"]
        assert "rows" in data["data"]
        assert "execution_time_ms" in data["data"]

    def test_execute_query_invalid_limit(self):
        """Test query with invalid limit."""
        response = client.post(
            "/api/v1/database/query",
            json={
                "query": "SELECT * FROM users",
                "limit": 50000,  # Exceeds max
            },
        )

        assert response.status_code == 422

    def test_execute_query_dangerous_statement(self):
        """Test query with dangerous keyword."""
        response = client.post(
            "/api/v1/database/query",
            json={
                "query": "DROP TABLE users",
            },
        )

        # Pydantic validation returns 422, but our schema validator would return 400
        assert response.status_code in [400, 422]

    def test_execute_batch_queries(self):
        """Test batch query execution."""
        response = client.post(
            "/api/v1/database/batch",
            json=[
                {
                    "query": "SELECT * FROM users",
                    "params": [],
                    "limit": 100,
                },
                {
                    "query": "SELECT * FROM accounts WHERE user_id = ?",
                    "params": [1],
                    "limit": 50,
                },
            ],
        )

        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert "transaction_id" in data["data"]
        assert "results" in data["data"]
        assert len(data["data"]["results"]) == 2


class TestAgentEndpoints:
    """Test agent execution endpoints."""

    def test_validate_query_success(self):
        """Test successful query validation."""
        response = client.post(
            "/api/v1/agent/validate",
            json={
                "tool": "query_database",
                "arguments": {
                    "query": "SELECT * FROM users",
                    "limit": 100,
                },
            },
        )

        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert data["data"]["valid"] is True

    def test_validate_query_invalid_tool(self):
        """Test validation of unknown tool."""
        response = client.post(
            "/api/v1/agent/validate",
            json={
                "tool": "unknown_tool",
                "arguments": {},
            },
        )

        assert response.status_code == 200
        data = response.json()
        assert data["data"]["valid"] is False
        assert len(data["data"]["errors"]) > 0

    def test_execute_agent_query_success(self):
        """Test successful agent query execution."""
        response = client.post(
            "/api/v1/agent/execute",
            json={
                "tool": "query_database",
                "arguments": {
                    "query": "SELECT * FROM users",
                    "limit": 100,
                },
            },
        )

        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert "transaction_id" in data["data"]
        assert data["data"]["status"] == "executed"

    def test_get_agent_status(self):
        """Test getting agent status."""
        response = client.get("/api/v1/agent/status")

        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert "status" in data["data"]
        assert "active_queries" in data["data"]


class TestDashboardEndpoints:
    """Test dashboard endpoints."""

    def test_get_telemetry(self):
        """Test getting telemetry data."""
        response = client.get("/api/v1/dashboard/telemetry")

        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert "threats_blocked" in data["data"]
        assert "active_tokens" in data["data"]
        assert "security_score" in data["data"]
        assert "recent_logs" in data["data"]

    def test_get_logs_default_pagination(self):
        """Test getting logs with default pagination."""
        response = client.get("/api/v1/dashboard/logs")

        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert "logs" in data["data"]
        assert "pagination" in data["data"]
        assert data["data"]["pagination"]["page"] == 1

    def test_get_logs_invalid_page(self):
        """Test getting logs with invalid page number."""
        response = client.get("/api/v1/dashboard/logs?page=0")

        assert response.status_code == 400

    def test_refresh_telemetry(self):
        """Test refreshing telemetry."""
        response = client.post("/api/v1/dashboard/refresh")

        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert data["data"]["status"] == "refreshed"


class TestDeceptionEndpoints:
    """Test deception/honey table endpoints."""

    def test_honey_table_sweep(self):
        """Test honey table detection."""
        response = client.post(
            "/api/v1/deception/sweep",
            json={
                "query": "SELECT * FROM company_client_global_dump_2026",
                "params": [],
                "limit": 100,
            },
        )

        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert "detected" in data["data"]
        assert "sandbox_routed" in data["data"]

    def test_get_sandbox_records(self):
        """Test getting sandbox records."""
        response = client.get("/api/v1/deception/sandbox-records?limit=50")

        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert "records" in data["data"]
        assert "count" in data["data"]

    def test_get_sandbox_records_invalid_limit(self):
        """Test sandbox records with invalid limit."""
        response = client.get("/api/v1/deception/sandbox-records?limit=5000")

        assert response.status_code == 400

    def test_get_incidents(self):
        """Test getting incidents."""
        response = client.get("/api/v1/deception/incidents")

        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert "incidents" in data["data"]
        assert "pagination" in data["data"]

    def test_generate_honey_data(self):
        """Test generating honey data."""
        response = client.post(
            "/api/v1/deception/generate-honey-data?count=50"
        )

        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert "records_created" in data["data"]


class TestAnalyticsEndpoints:
    """Test analytics endpoints."""

    def test_get_threat_distribution_default(self):
        """Test getting threat distribution with defaults."""
        response = client.get("/api/v1/analytics/threat-distribution")

        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert "threats" in data["data"]
        assert "total_threats" in data["data"]

    def test_get_threat_distribution_custom_days(self):
        """Test getting threat distribution with custom days."""
        response = client.get("/api/v1/analytics/threat-distribution?days=14")

        assert response.status_code == 200
        data = response.json()
        assert data["data"]["period"] == "14d"

    def test_get_threat_distribution_invalid_days(self):
        """Test threat distribution with invalid days."""
        response = client.get("/api/v1/analytics/threat-distribution?days=100")

        assert response.status_code == 400

    def test_get_top_attacks(self):
        """Test getting top attacks."""
        response = client.get("/api/v1/analytics/top-attacks")

        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert "attacks" in data["data"]
        assert len(data["data"]["attacks"]) > 0

    def test_get_token_success_stats(self):
        """Test getting token success statistics."""
        response = client.get("/api/v1/analytics/token-success")

        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert "verified_and_executed" in data["data"]
        assert "expired_and_dropped" in data["data"]
        assert "success_rate_percent" in data["data"]

    def test_get_request_volume_default(self):
        """Test getting request volume with default period."""
        response = client.get("/api/v1/analytics/request-volume")

        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert "query_count" in data["data"]
        assert "average_latency_ms" in data["data"]
        assert data["data"]["period"] == "24h"

    def test_get_request_volume_custom_period(self):
        """Test getting request volume with custom period."""
        response = client.get("/api/v1/analytics/request-volume?period=7d")

        assert response.status_code == 200
        data = response.json()
        assert data["data"]["period"] == "7d"

    def test_get_request_volume_invalid_period(self):
        """Test request volume with invalid period."""
        response = client.get("/api/v1/analytics/request-volume?period=invalid")

        assert response.status_code == 400


class TestHealthAndRoot:
    """Test health and root endpoints."""

    def test_health_check(self):
        """Test health check endpoint."""
        response = client.get("/health")

        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert "version" in data

    def test_root_endpoint(self):
        """Test root endpoint."""
        response = client.get("/")

        assert response.status_code == 200
        data = response.json()
        assert "name" in data
        assert "version" in data
        assert "endpoints" in data

"""Unit tests for schema validator."""

import pytest

from app.services.schema_validator import SchemaValidator


@pytest.fixture
def schema_validator():
    """Create schema validator instance."""
    return SchemaValidator()


class TestSchemaValidator:
    """Test SchemaValidator class."""

    def test_validate_valid_query_database_tool(self, schema_validator):
        """Test validation of valid query_database tool call."""
        valid, errors = schema_validator.validate_tool_call(
            tool="query_database",
            arguments={
                "query": "SELECT * FROM users WHERE id = ?",
                "params": [123],
                "limit": 100,
            },
        )

        assert valid is True
        assert len(errors) == 0

    def test_validate_missing_required_field(self, schema_validator):
        """Test validation fails when required field is missing."""
        valid, errors = schema_validator.validate_tool_call(
            tool="query_database",
            arguments={
                "params": [123],
                "limit": 100,
            },
        )

        assert valid is False
        assert any("query" in error.lower() for error in errors)

    def test_validate_invalid_field_type(self, schema_validator):
        """Test validation fails with invalid field type."""
        valid, errors = schema_validator.validate_tool_call(
            tool="query_database",
            arguments={
                "query": "SELECT * FROM users",
                "params": [123],
                "limit": "100",  # Should be int
            },
        )

        assert valid is False
        assert any("type" in error.lower() for error in errors)

    def test_validate_limit_too_large(self, schema_validator):
        """Test validation fails when limit exceeds maximum."""
        valid, errors = schema_validator.validate_tool_call(
            tool="query_database",
            arguments={
                "query": "SELECT * FROM users",
                "limit": 50000,  # Max is 10000
            },
        )

        assert valid is False
        assert any("maximum" in error.lower() or "exceeds" in error.lower() for error in errors)

    def test_validate_unknown_tool(self, schema_validator):
        """Test validation fails for unknown tool."""
        valid, errors = schema_validator.validate_tool_call(
            tool="unknown_tool",
            arguments={},
        )

        assert valid is False
        assert any("unknown" in error.lower() for error in errors)

    def test_validate_sql_injection_attempt(self, schema_validator):
        """Test validation detects SQL injection patterns in database queries."""
        # Test using the database query validator which checks for dangerous keywords
        valid, errors = schema_validator.validate_database_query(
            query="SELECT * FROM users; DROP TABLE users;",
        )

        # Should fail because of multiple statements
        assert valid is False
        assert any("multiple" in error.lower() for error in errors)

    def test_validate_drop_injection(self, schema_validator):
        """Test validation detects DROP statement injection."""
        valid, errors = schema_validator.validate_tool_call(
            tool="query_database",
            arguments={
                "query": "SELECT * FROM users",
            },
        )

        # This should be valid - a simple SELECT
        assert valid is True

        # Now test with actual DROP
        valid, errors = schema_validator.validate_database_query(
            query="SELECT * FROM users; DROP TABLE users;"
        )

        assert valid is False
        assert any("multiple" in error.lower() or "statement" in error.lower() for error in errors)

    def test_validate_template_injection(self, schema_validator):
        """Test validation detects template injection."""
        valid, errors = schema_validator.validate_tool_call(
            tool="query_database",
            arguments={
                "query": "SELECT * FROM {{ table_name }}",
            },
        )

        assert valid is False
        assert any("injection" in error.lower() or "pattern" in error.lower() for error in errors)

    def test_validate_database_query_valid(self, schema_validator):
        """Test validation of valid database query."""
        valid, errors = schema_validator.validate_database_query(
            query="SELECT id, username FROM users WHERE role = ?",
            params=["admin"],
            limit=100,
        )

        assert valid is True
        assert len(errors) == 0

    def test_validate_database_query_empty(self, schema_validator):
        """Test validation fails for empty query."""
        valid, errors = schema_validator.validate_database_query(query="")

        assert valid is False
        assert any("empty" in error.lower() for error in errors)

    def test_validate_database_query_multiple_statements(self, schema_validator):
        """Test validation fails for multiple statements."""
        valid, errors = schema_validator.validate_database_query(
            query="SELECT * FROM users; SELECT * FROM accounts;"
        )

        assert valid is False
        assert any("multiple" in error.lower() for error in errors)

    def test_validate_database_query_drop_statement(self, schema_validator):
        """Test validation fails for DROP statement."""
        valid, errors = schema_validator.validate_database_query(
            query="DROP TABLE users"
        )

        assert valid is False
        assert any("drop" in error.lower() for error in errors)

    def test_validate_database_query_delete_with_where(self, schema_validator):
        """Test validation allows DELETE with WHERE clause."""
        valid, errors = schema_validator.validate_database_query(
            query="DELETE FROM audit_logs WHERE created_at < ?"
        )

        assert valid is True

    def test_validate_database_query_delete_without_where(self, schema_validator):
        """Test validation fails for DELETE without WHERE."""
        valid, errors = schema_validator.validate_database_query(
            query="DELETE FROM users"
        )

        assert valid is False
        assert any("where" in error.lower() for error in errors)

    def test_validate_database_query_invalid_limit_type(self, schema_validator):
        """Test validation fails for non-integer limit."""
        valid, errors = schema_validator.validate_database_query(
            query="SELECT * FROM users",
            limit="100",
        )

        assert valid is False
        assert any("integer" in error.lower() for error in errors)

    def test_validate_database_query_limit_range(self, schema_validator):
        """Test validation checks limit range."""
        # Test minimum
        valid, errors = schema_validator.validate_database_query(
            query="SELECT * FROM users",
            limit=0,
        )
        assert valid is False

        # Test maximum
        valid, errors = schema_validator.validate_database_query(
            query="SELECT * FROM users",
            limit=50000,
        )
        assert valid is False

    def test_get_tool_schema(self, schema_validator):
        """Test retrieving tool schema."""
        schema = schema_validator.get_tool_schema("query_database")

        assert schema is not None
        assert "required_fields" in schema
        assert "field_types" in schema
        assert "constraints" in schema

    def test_list_supported_tools(self, schema_validator):
        """Test listing supported tools."""
        tools = schema_validator.list_supported_tools()

        assert "query_database" in tools
        assert "list_tables" in tools
        assert "get_table_schema" in tools
        assert "count_rows" in tools

    def test_add_tool_schema(self, schema_validator):
        """Test adding a new tool schema."""
        new_schema = {
            "required_fields": ["dataset"],
            "field_types": {"dataset": str, "format": (str, type(None))},
            "constraints": {"dataset": {"min_length": 1, "max_length": 255}},
        }

        schema_validator.add_tool_schema("export_data", new_schema)

        retrieved = schema_validator.get_tool_schema("export_data")
        assert retrieved == new_schema

    def test_validate_xss_attempt(self, schema_validator):
        """Test validation detects XSS attempts."""
        valid, errors = schema_validator.validate_tool_call(
            tool="query_database",
            arguments={
                "query": "SELECT * FROM users WHERE name = '<script>alert(1)</script>'",
            },
        )

        assert valid is False
        assert any("injection" in error.lower() for error in errors)

    def test_validate_code_execution_attempt(self, schema_validator):
        """Test validation detects code execution attempts."""
        valid, errors = schema_validator.validate_tool_call(
            tool="query_database",
            arguments={
                "query": "SELECT * FROM exec('DROP TABLE users')",
            },
        )

        assert valid is False
        assert any("injection" in error.lower() for error in errors)

    def test_get_table_schema_valid(self, schema_validator):
        """Test validation of get_table_schema tool."""
        valid, errors = schema_validator.validate_tool_call(
            tool="get_table_schema",
            arguments={"table_name": "users"},
        )

        assert valid is True
        assert len(errors) == 0

    def test_count_rows_valid(self, schema_validator):
        """Test validation of count_rows tool."""
        valid, errors = schema_validator.validate_tool_call(
            tool="count_rows",
            arguments={
                "table_name": "users",
                "where_clause": "role = 'admin'",
            },
        )

        assert valid is True

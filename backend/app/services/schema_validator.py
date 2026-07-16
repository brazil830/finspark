"""Schema Validation Service.

Validates tool calls and database queries against expected schemas.
Detects prompt injection patterns and enforces strict type checking.
"""

import json
import logging
import re
from typing import Any, Dict, List, Optional, Tuple

logger = logging.getLogger(__name__)


class SchemaValidator:
    """Validates tool calls and queries against defined schemas.
    
    Features:
    - Type checking (strings, integers, lists, etc.)
    - Injection pattern detection
    - Limit enforcement (prevent mass extraction)
    - Custom validation rules per tool
    """

    # Define allowed tools and their schemas
    TOOL_SCHEMAS = {
        "query_database": {
            "required_fields": ["query"],
            "field_types": {
                "query": str,
                "params": (list, type(None)),
                "limit": (int, type(None)),
                "timeout_seconds": (int, type(None)),
            },
            "constraints": {
                "query": {"min_length": 1, "max_length": 10000},
                "limit": {"min": 1, "max": 10000},
                "timeout_seconds": {"min": 1, "max": 300},
            },
        },
        "list_tables": {
            "required_fields": [],
            "field_types": {},
            "constraints": {},
        },
        "get_table_schema": {
            "required_fields": ["table_name"],
            "field_types": {
                "table_name": str,
            },
            "constraints": {
                "table_name": {"min_length": 1, "max_length": 255},
            },
        },
        "count_rows": {
            "required_fields": ["table_name"],
            "field_types": {
                "table_name": str,
                "where_clause": (str, type(None)),
            },
            "constraints": {
                "table_name": {"min_length": 1, "max_length": 255},
            },
        },
    }

    # Injection patterns to detect
    INJECTION_PATTERNS = [
        r"(?i)('; *DROP|'; *DELETE|'; *TRUNCATE)",  # SQL injection
        r"(?i)(\" *OR *\"1\"=\"1)",  # SQL injection
        r"(?i)('|\") *OR *('|\") *1 *('|\") *= *('|\")",  # SQL injection
        r"(?i)(UNION.*SELECT)",  # UNION-based injection
        r"(?i)(INSERT.*INTO|UPDATE.*SET|DELETE.*FROM) *[^;]*;",  # Dangerous DML
        r"\$\{.*\}",  # Template injection
        r"\{\{.*\}\}",  # Template injection (Jinja)
        r"exec\(|eval\(|__import__\(|os\.system\(",  # Code execution
        r"<script[^>]*>.*</script>",  # XSS
        r"javascript:",  # XSS
    ]

    def __init__(self):
        """Initialize schema validator."""
        logger.info("SchemaValidator initialized")

    def validate_tool_call(
        self,
        tool: str,
        arguments: Dict[str, Any],
    ) -> Tuple[bool, List[str]]:
        """Validate a tool call against its schema.
        
        Args:
            tool: Tool name
            arguments: Tool arguments
        
        Returns:
            Tuple of (valid: bool, errors: List[str])
        """
        errors = []

        # Check if tool is known
        if tool not in self.TOOL_SCHEMAS:
            errors.append(f"Unknown tool: {tool}")
            return False, errors

        schema = self.TOOL_SCHEMAS[tool]

        # Check required fields
        required_fields = schema.get("required_fields", [])
        for field in required_fields:
            if field not in arguments:
                errors.append(f"Missing required field: '{field}'")

        # Check field types
        field_types = schema.get("field_types", {})
        for field, expected_type in field_types.items():
            if field in arguments:
                value = arguments[field]
                if value is not None:
                    if not isinstance(value, expected_type):
                        errors.append(
                            f"Invalid type for '{field}': "
                            f"expected {expected_type}, got {type(value).__name__}"
                        )

        # Check constraints (min/max length, ranges, etc.)
        constraints = schema.get("constraints", {})
        for field, field_constraints in constraints.items():
            if field in arguments:
                value = arguments[field]
                if value is not None:
                    # Check string length
                    if isinstance(value, str):
                        if "min_length" in field_constraints:
                            if len(value) < field_constraints["min_length"]:
                                errors.append(
                                    f"'{field}' is too short: "
                                    f"minimum {field_constraints['min_length']} characters"
                                )
                        if "max_length" in field_constraints:
                            if len(value) > field_constraints["max_length"]:
                                errors.append(
                                    f"'{field}' is too long: "
                                    f"maximum {field_constraints['max_length']} characters"
                                )

                    # Check numeric ranges
                    if isinstance(value, (int, float)):
                        if "min" in field_constraints:
                            if value < field_constraints["min"]:
                                errors.append(
                                    f"'{field}' is too small: minimum {field_constraints['min']}"
                                )
                        if "max" in field_constraints:
                            if value > field_constraints["max"]:
                                errors.append(
                                    f"'{field}' exceeds maximum: {field_constraints['max']}"
                                )

        # Check for injection patterns in all string values
        injection_errors = self._check_injection_patterns(arguments)
        errors.extend(injection_errors)

        return len(errors) == 0, errors

    def validate_database_query(
        self,
        query: str,
        params: Optional[List[Any]] = None,
        limit: Optional[int] = None,
    ) -> Tuple[bool, List[str]]:
        """Validate a database query.
        
        Args:
            query: SQL query
            params: Query parameters
            limit: Result limit
        
        Returns:
            Tuple of (valid: bool, errors: List[str])
        """
        errors = []

        if not query:
            errors.append("Query cannot be empty")
            return False, errors

        # Check query length
        if len(query) > 10000:
            errors.append("Query exceeds maximum length (10000 characters)")

        # Check for multiple statements (basic check)
        statements = [s.strip() for s in query.split(";") if s.strip()]
        if len(statements) > 1:
            errors.append("Multiple SQL statements not allowed")

        # Check for dangerous keywords
        dangerous_keywords = [
            "DROP",
            "TRUNCATE",
            "DELETE",
            "ALTER",
            "GRANT",
            "REVOKE",
        ]
        query_upper = query.upper()
        for keyword in dangerous_keywords:
            if keyword in query_upper:
                # Allow DELETE with WHERE clause (safer)
                if keyword == "DELETE":
                    if "WHERE" not in query_upper:
                        errors.append(
                            f"'{keyword}' statement without WHERE clause not allowed"
                        )
                else:
                    errors.append(f"'{keyword}' statement not allowed")

        # Check injection patterns
        injection_errors = self._check_injection_patterns({"query": query})
        errors.extend(injection_errors)

        # Validate parameters
        params = params or []
        if not isinstance(params, list):
            errors.append("Query parameters must be a list")

        # Check limit constraints
        if limit is not None:
            if not isinstance(limit, int):
                errors.append("Limit must be an integer")
            elif limit < 1 or limit > 10000:
                errors.append("Limit must be between 1 and 10000")

        return len(errors) == 0, errors

    def _check_injection_patterns(
        self,
        data: Dict[str, Any],
    ) -> List[str]:
        """Check for injection patterns in data.
        
        Args:
            data: Dictionary to check
        
        Returns:
            List of detected injection errors
        """
        errors = []

        def check_value(value: Any, path: str = "") -> None:
            """Recursively check value for injection patterns."""
            if isinstance(value, str):
                for pattern in self.INJECTION_PATTERNS:
                    if re.search(pattern, value):
                        errors.append(
                            f"Potential injection pattern detected in '{path}': "
                            f"matches pattern '{pattern[:30]}...'"
                        )
                        break  # Report first match per field

            elif isinstance(value, dict):
                for key, val in value.items():
                    check_value(val, f"{path}.{key}" if path else key)

            elif isinstance(value, list):
                for i, item in enumerate(value):
                    check_value(item, f"{path}[{i}]")

        for key, value in data.items():
            check_value(value, key)

        return errors

    def get_tool_schema(self, tool: str) -> Optional[Dict[str, Any]]:
        """Get schema definition for a tool.
        
        Args:
            tool: Tool name
        
        Returns:
            Tool schema or None if not found
        """
        return self.TOOL_SCHEMAS.get(tool)

    def list_supported_tools(self) -> List[str]:
        """Get list of supported tools.
        
        Returns:
            List of tool names
        """
        return list(self.TOOL_SCHEMAS.keys())

    def add_tool_schema(
        self,
        tool: str,
        schema: Dict[str, Any],
    ) -> None:
        """Add or update a tool schema.
        
        Args:
            tool: Tool name
            schema: Tool schema definition
        """
        self.TOOL_SCHEMAS[tool] = schema
        logger.info(f"Tool schema added/updated: {tool}")


# Global singleton
_schema_validator: Optional[SchemaValidator] = None


def get_schema_validator() -> SchemaValidator:
    """Get or create global SchemaValidator instance."""
    global _schema_validator
    if _schema_validator is None:
        _schema_validator = SchemaValidator()
    return _schema_validator

"""Honey table detection service."""

import logging
import re
from typing import List, Optional, Set

logger = logging.getLogger(__name__)


class HoneyTableDetector:
    """Detects attempts to access honey tables in SQL queries."""

    # Known honey tables
    HONEY_TABLES: Set[str] = {
        "company_client_global_dump_2026",
        "hr_payroll_confidential",
        "internal_system_audit",
        "admin_master_keys",
        "customer_ssn_database",
        "classified_operations",
    }

    def __init__(self):
        """Initialize honey table detector."""
        self.detection_count = 0
        logger.info(
            f"Honey table detector initialized with {len(self.HONEY_TABLES)} tables"
        )

    def is_honey_table(self, table_name: str) -> bool:
        """Check if a table name is a honey table.

        Args:
            table_name: Table name to check

        Returns:
            True if table is a honey table
        """
        normalized_name = table_name.lower().strip()
        return normalized_name in self.HONEY_TABLES

    def extract_table_names(self, query: str) -> List[str]:
        """Extract table names from SQL query.

        Args:
            query: SQL query string

        Returns:
            List of table names found in query
        """
        # Remove comments
        query = re.sub(r"--.*", "", query)
        query = re.sub(r"/\\*.*?\\*/", "", query, flags=re.DOTALL)

        tables = []

        # Pattern for FROM/JOIN table references
        # Matches: FROM table_name, JOIN table_name, etc.
        from_pattern = r"(?:FROM|JOIN|INTO|UPDATE|DELETE\s+FROM)\s+([`\"']?)(\w+)\1"
        matches = re.finditer(from_pattern, query, re.IGNORECASE)

        for match in matches:
            table_name = match.group(2)
            if table_name:
                tables.append(table_name)

        return tables

    def detect_honey_table_access(
        self, query: str
    ) -> tuple[bool, Optional[str], List[str]]:
        """Detect if query attempts to access honey tables.

        Args:
            query: SQL query string

        Returns:
            Tuple of (detected, honey_table_name, all_tables_in_query)
        """
        try:
            table_names = self.extract_table_names(query)

            # Check for honey table references
            for table_name in table_names:
                if self.is_honey_table(table_name):
                    self.detection_count += 1
                    logger.warning(
                        f"Honey table access attempt detected: {table_name}",
                        extra={
                            "honey_table": table_name,
                            "query_preview": query[:100],
                            "detection_count": self.detection_count,
                        },
                    )
                    return (True, table_name, table_names)

            return (False, None, table_names)
        except Exception as e:
            logger.error(f"Error detecting honey table access: {e}")
            return (False, None, [])

    def add_honey_table(self, table_name: str):
        """Add a new honey table to detection list.

        Args:
            table_name: Table name to add
        """
        normalized_name = table_name.lower().strip()
        self.HONEY_TABLES.add(normalized_name)
        logger.info(f"Added honey table: {normalized_name}")

    def get_honey_tables(self) -> Set[str]:
        """Get list of all known honey tables.

        Returns:
            Set of honey table names
        """
        return self.HONEY_TABLES.copy()

    def get_detection_stats(self) -> dict:
        """Get honey table detection statistics.

        Returns:
            Dictionary with detection stats
        """
        return {
            "total_detections": self.detection_count,
            "honey_table_count": len(self.HONEY_TABLES),
            "honey_tables": sorted(list(self.HONEY_TABLES)),
        }


# Global honey table detector instance
_honey_detector = HoneyTableDetector()


def get_honey_detector() -> HoneyTableDetector:
    """Get the global honey table detector instance."""
    return _honey_detector

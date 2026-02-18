"""
SQL Guard Module
Handles SQL query validation and security checks.
Blocks potentially dangerous operations like DROP, DELETE, UPDATE.
"""

import re
from typing import Tuple


class SQLGuard:
    """Validates and sanitizes SQL queries for security."""
    
    # Dangerous SQL keywords that should be blocked
    DANGEROUS_KEYWORDS = [
        r'\bDROP\b',
        r'\bDELETE\b',
        r'\bUPDATE\b',
        r'\bINSERT\b',
        r'\bALTER\b',
        r'\bTRUNCATE\b',
        r'\bCREATE\s+TABLE\b',
        r'\bGRANT\b',
        r'\bREVOKE\b',
    ]
    
    @staticmethod
    def is_safe_query(sql_query: str) -> Tuple[bool, str]:
        """
        Validate if a SQL query is safe to execute.
        
        Args:
            sql_query: The SQL query string to validate
            
        Returns:
            Tuple of (is_safe: bool, message: str)
        """
        # Remove leading/trailing whitespace
        sql_query = sql_query.strip()
        
        # Check for empty query
        if not sql_query:
            return False, "Query cannot be empty"
        
        # Check for dangerous keywords (case-insensitive)
        for dangerous_keyword in SQLGuard.DANGEROUS_KEYWORDS:
            if re.search(dangerous_keyword, sql_query, re.IGNORECASE):
                keyword = dangerous_keyword.replace(r'\b', '').replace(r'\s+', ' ')
                return False, f"Query contains forbidden operation: {keyword}"
        
        # Basic syntax check - ensure it starts with SELECT
        if not re.match(r'^\s*SELECT\b', sql_query, re.IGNORECASE):
            return False, "Only SELECT queries are allowed"
        
        return True, "Query is safe to execute"
    
    @staticmethod
    def sanitize_query(sql_query: str) -> str:
        """
        Basic sanitization of SQL query (removes extra whitespace).
        
        Args:
            sql_query: The SQL query string to sanitize
            
        Returns:
            Sanitized SQL query
        """
        # Remove multiple spaces, tabs, newlines
        sanitized = re.sub(r'\s+', ' ', sql_query)
        return sanitized.strip()

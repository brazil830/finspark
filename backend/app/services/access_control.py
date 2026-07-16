"""Role-Based Access Control and Session Context Management.

Implements:
- Role hierarchy and permission model
- Session tracking and context management
- User authentication and authorization
"""

import logging
from datetime import datetime, timezone
from enum import Enum as PyEnum
from typing import List, Optional, Set

logger = logging.getLogger(__name__)


class UserRole(str, PyEnum):
    """User role enumeration."""

    ADMIN = "admin"
    ANALYST_L3 = "analyst_l3"
    OPS_TEAM = "ops_team"


class Permission(str, PyEnum):
    """Permission enumeration."""

    # Data access permissions
    READ_USERS = "read_users"
    READ_ACCOUNTS = "read_accounts"
    READ_TICKETS = "read_tickets"
    READ_CONTRACTS = "read_contracts"
    READ_INVOICES = "read_invoices"

    # Write permissions
    WRITE_SECURITY_LOGS = "write_security_logs"
    UPDATE_TICKETS = "update_tickets"

    # Administrative permissions
    ROTATE_HSM_KEYS = "rotate_hsm_keys"
    MANAGE_USERS = "manage_users"
    VIEW_AUDIT_LOGS = "view_audit_logs"

    # Token operations
    MINT_TOKENS = "mint_tokens"
    VERIFY_TOKENS = "verify_tokens"

    # Deception system
    ACCESS_HONEY_TABLES = "access_honey_tables"
    VIEW_INCIDENTS = "view_incidents"


class RoleBasedAccessControl:
    """Role-based access control system.
    
    Defines permissions for each role and verifies access.
    """

    # Role to permissions mapping
    ROLE_PERMISSIONS: dict[UserRole, Set[Permission]] = {
        UserRole.ADMIN: {
            # Admins have full access
            Permission.READ_USERS,
            Permission.READ_ACCOUNTS,
            Permission.READ_TICKETS,
            Permission.READ_CONTRACTS,
            Permission.READ_INVOICES,
            Permission.WRITE_SECURITY_LOGS,
            Permission.UPDATE_TICKETS,
            Permission.ROTATE_HSM_KEYS,
            Permission.MANAGE_USERS,
            Permission.VIEW_AUDIT_LOGS,
            Permission.MINT_TOKENS,
            Permission.VERIFY_TOKENS,
            Permission.ACCESS_HONEY_TABLES,
            Permission.VIEW_INCIDENTS,
        },
        UserRole.ANALYST_L3: {
            # L3 analysts have read access and can mint tokens
            Permission.READ_USERS,
            Permission.READ_ACCOUNTS,
            Permission.READ_TICKETS,
            Permission.READ_CONTRACTS,
            Permission.READ_INVOICES,
            Permission.WRITE_SECURITY_LOGS,
            Permission.UPDATE_TICKETS,
            Permission.MINT_TOKENS,
            Permission.VERIFY_TOKENS,
            Permission.ACCESS_HONEY_TABLES,
            Permission.VIEW_INCIDENTS,
        },
        UserRole.OPS_TEAM: {
            # Ops team has limited read access
            Permission.READ_TICKETS,
            Permission.UPDATE_TICKETS,
            Permission.MINT_TOKENS,
            Permission.VERIFY_TOKENS,
        },
    }

    def __init__(self):
        """Initialize access control."""
        logger.info("RoleBasedAccessControl initialized")

    def has_permission(
        self,
        role: UserRole,
        permission: Permission,
    ) -> bool:
        """Check if a role has a specific permission.
        
        Args:
            role: User role
            permission: Required permission
        
        Returns:
            True if role has permission, False otherwise
        """
        return permission in self.ROLE_PERMISSIONS.get(role, set())

    def has_any_permission(
        self,
        role: UserRole,
        permissions: List[Permission],
    ) -> bool:
        """Check if a role has any of the specified permissions.
        
        Args:
            role: User role
            permissions: List of permissions to check
        
        Returns:
            True if role has any permission, False otherwise
        """
        role_permissions = self.ROLE_PERMISSIONS.get(role, set())
        return any(p in role_permissions for p in permissions)

    def has_all_permissions(
        self,
        role: UserRole,
        permissions: List[Permission],
    ) -> bool:
        """Check if a role has all specified permissions.
        
        Args:
            role: User role
            permissions: List of permissions to check
        
        Returns:
            True if role has all permissions, False otherwise
        """
        role_permissions = self.ROLE_PERMISSIONS.get(role, set())
        return all(p in role_permissions for p in permissions)

    def get_role_permissions(self, role: UserRole) -> Set[Permission]:
        """Get all permissions for a role.
        
        Args:
            role: User role
        
        Returns:
            Set of permissions for the role
        """
        return self.ROLE_PERMISSIONS.get(role, set()).copy()


class SessionContext:
    """Represents the context of a user session.
    
    Tracks:
    - Current user identity and role
    - Active work ticket
    - Request context
    - Authentication status
    """

    def __init__(
        self,
        user_id: int,
        username: str,
        role: UserRole,
        session_id: str,
    ):
        """Initialize session context.
        
        Args:
            user_id: User ID
            username: Username
            role: User role
            session_id: Session identifier
        """
        self.user_id = user_id
        self.username = username
        self.role = role
        self.session_id = session_id
        self.active_ticket_id: Optional[int] = None
        self.authenticated = True
        self.created_at = datetime.now(timezone.utc)
        self.last_activity = datetime.now(timezone.utc)

    def set_active_ticket(self, ticket_id: int) -> None:
        """Set the active work ticket for this session.
        
        Args:
            ticket_id: Ticket ID
        """
        self.active_ticket_id = ticket_id
        self.update_activity()

    def clear_active_ticket(self) -> None:
        """Clear the active work ticket."""
        self.active_ticket_id = None
        self.update_activity()

    def update_activity(self) -> None:
        """Update last activity timestamp."""
        self.last_activity = datetime.now(timezone.utc)

    def verify_role(self, required_role: UserRole) -> bool:
        """Verify user has required role.
        
        Args:
            required_role: Required role
        
        Returns:
            True if user has the role, False otherwise
        """
        return self.role == required_role

    def verify_permission(
        self,
        permission: Permission,
        access_control: RoleBasedAccessControl,
    ) -> bool:
        """Verify user has a specific permission.
        
        Args:
            permission: Required permission
            access_control: Access control system
        
        Returns:
            True if user has permission, False otherwise
        """
        return access_control.has_permission(self.role, permission)

    def to_dict(self) -> dict:
        """Convert session context to dictionary.
        
        Returns:
            Dictionary representation of session
        """
        return {
            "user_id": self.user_id,
            "username": self.username,
            "role": self.role.value,
            "session_id": self.session_id,
            "active_ticket_id": self.active_ticket_id,
            "authenticated": self.authenticated,
            "created_at": self.created_at.isoformat(),
            "last_activity": self.last_activity.isoformat(),
        }

    def __repr__(self) -> str:
        """String representation."""
        return (
            f"<SessionContext(user={self.username}, "
            f"role={self.role}, session={self.session_id})>"
        )


class SessionManager:
    """Manages user sessions.
    
    Stores active sessions and provides session lookup.
    """

    def __init__(self):
        """Initialize session manager."""
        self._sessions: dict[str, SessionContext] = {}
        logger.info("SessionManager initialized")

    def create_session(
        self,
        user_id: int,
        username: str,
        role: UserRole,
        session_id: str,
    ) -> SessionContext:
        """Create a new session.
        
        Args:
            user_id: User ID
            username: Username
            role: User role
            session_id: Session identifier
        
        Returns:
            SessionContext object
        """
        context = SessionContext(user_id, username, role, session_id)
        self._sessions[session_id] = context
        logger.info(f"Session created: {session_id} for user {username}")
        return context

    def get_session(self, session_id: str) -> Optional[SessionContext]:
        """Get a session by ID.
        
        Args:
            session_id: Session identifier
        
        Returns:
            SessionContext or None if not found
        """
        return self._sessions.get(session_id)

    def close_session(self, session_id: str) -> bool:
        """Close a session.
        
        Args:
            session_id: Session identifier
        
        Returns:
            True if session was closed, False if not found
        """
        if session_id in self._sessions:
            del self._sessions[session_id]
            logger.info(f"Session closed: {session_id}")
            return True
        return False

    def list_active_sessions(self) -> List[SessionContext]:
        """Get list of active sessions.
        
        Returns:
            List of SessionContext objects
        """
        return list(self._sessions.values())


# Global singletons
_access_control: Optional[RoleBasedAccessControl] = None
_session_manager: Optional[SessionManager] = None


def get_access_control() -> RoleBasedAccessControl:
    """Get or create global access control instance."""
    global _access_control
    if _access_control is None:
        _access_control = RoleBasedAccessControl()
    return _access_control


def get_session_manager() -> SessionManager:
    """Get or create global session manager instance."""
    global _session_manager
    if _session_manager is None:
        _session_manager = SessionManager()
    return _session_manager

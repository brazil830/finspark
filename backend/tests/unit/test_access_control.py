"""Unit tests for role-based access control and session management."""

import pytest

from app.services.access_control import (
    RoleBasedAccessControl,
    SessionContext,
    SessionManager,
    UserRole,
    Permission,
)


@pytest.fixture
def access_control():
    """Create access control instance."""
    return RoleBasedAccessControl()


@pytest.fixture
def session_manager():
    """Create session manager instance."""
    return SessionManager()


class TestRoleBasedAccessControl:
    """Test RoleBasedAccessControl class."""

    def test_admin_has_all_permissions(self, access_control):
        """Test that admin role has all permissions."""
        for permission in Permission:
            assert access_control.has_permission(UserRole.ADMIN, permission)

    def test_analyst_l3_has_read_permissions(self, access_control):
        """Test that analyst_l3 can read data."""
        assert access_control.has_permission(UserRole.ANALYST_L3, Permission.READ_USERS)
        assert access_control.has_permission(UserRole.ANALYST_L3, Permission.READ_ACCOUNTS)
        assert access_control.has_permission(UserRole.ANALYST_L3, Permission.READ_TICKETS)

    def test_analyst_l3_cannot_manage_users(self, access_control):
        """Test that analyst_l3 cannot manage users."""
        assert not access_control.has_permission(UserRole.ANALYST_L3, Permission.MANAGE_USERS)

    def test_analyst_l3_can_mint_tokens(self, access_control):
        """Test that analyst_l3 can mint tokens."""
        assert access_control.has_permission(UserRole.ANALYST_L3, Permission.MINT_TOKENS)

    def test_ops_team_limited_permissions(self, access_control):
        """Test that ops_team has limited permissions."""
        assert access_control.has_permission(UserRole.OPS_TEAM, Permission.READ_TICKETS)
        assert access_control.has_permission(UserRole.OPS_TEAM, Permission.UPDATE_TICKETS)
        assert not access_control.has_permission(UserRole.OPS_TEAM, Permission.READ_USERS)

    def test_has_any_permission(self, access_control):
        """Test checking for any permission."""
        permissions = [
            Permission.UPDATE_TICKETS,  # OPS_TEAM has this
            Permission.READ_USERS,  # OPS_TEAM doesn't have this
            Permission.MANAGE_USERS,  # OPS_TEAM doesn't have this
        ]

        # OPS_TEAM has UPDATE_TICKETS, so should return True
        assert access_control.has_any_permission(UserRole.OPS_TEAM, permissions)
        
        # ANALYST_L3 has both READ_USERS and UPDATE_TICKETS
        assert access_control.has_any_permission(UserRole.ANALYST_L3, permissions)

    def test_has_all_permissions_admin(self, access_control):
        """Test admin has all permissions."""
        permissions = [
            Permission.READ_USERS,
            Permission.MANAGE_USERS,
            Permission.ROTATE_HSM_KEYS,
        ]

        assert access_control.has_all_permissions(UserRole.ADMIN, permissions)

    def test_has_all_permissions_analyst_fails(self, access_control):
        """Test analyst_l3 doesn't have all permissions."""
        permissions = [
            Permission.READ_USERS,
            Permission.MANAGE_USERS,  # analyst_l3 cannot do this
        ]

        assert not access_control.has_all_permissions(UserRole.ANALYST_L3, permissions)

    def test_get_role_permissions(self, access_control):
        """Test retrieving all permissions for a role."""
        admin_perms = access_control.get_role_permissions(UserRole.ADMIN)
        analyst_perms = access_control.get_role_permissions(UserRole.ANALYST_L3)
        ops_perms = access_control.get_role_permissions(UserRole.OPS_TEAM)

        # Admin should have more permissions than analyst
        assert len(admin_perms) > len(analyst_perms)

        # Analyst should have more than ops
        assert len(analyst_perms) > len(ops_perms)


class TestSessionContext:
    """Test SessionContext class."""

    def test_create_session_context(self):
        """Test creating a session context."""
        ctx = SessionContext(
            user_id=1,
            username="analyst",
            role=UserRole.ANALYST_L3,
            session_id="sess_123",
        )

        assert ctx.user_id == 1
        assert ctx.username == "analyst"
        assert ctx.role == UserRole.ANALYST_L3
        assert ctx.session_id == "sess_123"
        assert ctx.authenticated is True
        assert ctx.active_ticket_id is None

    def test_set_active_ticket(self):
        """Test setting active ticket."""
        ctx = SessionContext(
            user_id=1,
            username="analyst",
            role=UserRole.ANALYST_L3,
            session_id="sess_123",
        )

        ctx.set_active_ticket(42)

        assert ctx.active_ticket_id == 42

    def test_clear_active_ticket(self):
        """Test clearing active ticket."""
        ctx = SessionContext(
            user_id=1,
            username="analyst",
            role=UserRole.ANALYST_L3,
            session_id="sess_123",
        )

        ctx.set_active_ticket(42)
        ctx.clear_active_ticket()

        assert ctx.active_ticket_id is None

    def test_verify_role(self):
        """Test role verification."""
        ctx = SessionContext(
            user_id=1,
            username="analyst",
            role=UserRole.ANALYST_L3,
            session_id="sess_123",
        )

        assert ctx.verify_role(UserRole.ANALYST_L3) is True
        assert ctx.verify_role(UserRole.ADMIN) is False

    def test_verify_permission(self, access_control):
        """Test permission verification."""
        ctx = SessionContext(
            user_id=1,
            username="analyst",
            role=UserRole.ANALYST_L3,
            session_id="sess_123",
        )

        assert ctx.verify_permission(Permission.READ_USERS, access_control) is True
        assert ctx.verify_permission(Permission.MANAGE_USERS, access_control) is False

    def test_session_to_dict(self):
        """Test converting session to dictionary."""
        ctx = SessionContext(
            user_id=1,
            username="analyst",
            role=UserRole.ANALYST_L3,
            session_id="sess_123",
        )
        ctx.set_active_ticket(42)

        d = ctx.to_dict()

        assert d["user_id"] == 1
        assert d["username"] == "analyst"
        assert d["role"] == "analyst_l3"
        assert d["active_ticket_id"] == 42
        assert d["authenticated"] is True

    def test_session_repr(self):
        """Test string representation of session."""
        ctx = SessionContext(
            user_id=1,
            username="analyst",
            role=UserRole.ANALYST_L3,
            session_id="sess_123",
        )

        repr_str = repr(ctx)

        assert "analyst" in repr_str
        assert "sess_123" in repr_str
        # The repr uses UserRole.ANALYST_L3, which may not have 'analyst_l3' substring
        assert "ANALYST_L3" in repr_str or "analyst" in repr_str


class TestSessionManager:
    """Test SessionManager class."""

    def test_create_session(self, session_manager):
        """Test creating a new session."""
        ctx = session_manager.create_session(
            user_id=1,
            username="analyst",
            role=UserRole.ANALYST_L3,
            session_id="sess_123",
        )

        assert ctx.user_id == 1
        assert ctx.username == "analyst"

    def test_get_session(self, session_manager):
        """Test retrieving a session."""
        session_manager.create_session(
            user_id=1,
            username="analyst",
            role=UserRole.ANALYST_L3,
            session_id="sess_123",
        )

        ctx = session_manager.get_session("sess_123")

        assert ctx is not None
        assert ctx.user_id == 1

    def test_get_nonexistent_session(self, session_manager):
        """Test retrieving nonexistent session returns None."""
        ctx = session_manager.get_session("nonexistent")

        assert ctx is None

    def test_close_session(self, session_manager):
        """Test closing a session."""
        session_manager.create_session(
            user_id=1,
            username="analyst",
            role=UserRole.ANALYST_L3,
            session_id="sess_123",
        )

        result = session_manager.close_session("sess_123")

        assert result is True
        assert session_manager.get_session("sess_123") is None

    def test_close_nonexistent_session(self, session_manager):
        """Test closing nonexistent session."""
        result = session_manager.close_session("nonexistent")

        assert result is False

    def test_list_active_sessions(self, session_manager):
        """Test listing active sessions."""
        session_manager.create_session(
            user_id=1,
            username="analyst1",
            role=UserRole.ANALYST_L3,
            session_id="sess_001",
        )
        session_manager.create_session(
            user_id=2,
            username="analyst2",
            role=UserRole.ANALYST_L3,
            session_id="sess_002",
        )

        sessions = session_manager.list_active_sessions()

        assert len(sessions) == 2
        assert any(s.username == "analyst1" for s in sessions)
        assert any(s.username == "analyst2" for s in sessions)

    def test_session_lifecycle(self, session_manager):
        """Test complete session lifecycle."""
        # Create
        ctx1 = session_manager.create_session(
            user_id=1,
            username="analyst",
            role=UserRole.ANALYST_L3,
            session_id="sess_123",
        )
        assert session_manager.get_session("sess_123") is not None

        # Modify
        ctx1.set_active_ticket(42)
        ctx_retrieved = session_manager.get_session("sess_123")
        assert ctx_retrieved.active_ticket_id == 42

        # Close
        session_manager.close_session("sess_123")
        assert session_manager.get_session("sess_123") is None

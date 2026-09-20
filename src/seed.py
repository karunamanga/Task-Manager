import logging
from sqlalchemy.orm import Session

from .database import Base, SessionLocal, engine
from .models.permission import Permission
from .models.role import Role
from .models.role_permission import RolePermission
from .models.task import Task
from .models.user import User

logger = logging.getLogger(__name__)


def init_db(db: Session | None = None) -> None:
    """Create all database tables and seed default roles and permissions."""
    Base.metadata.create_all(bind=engine)

    should_close = False
    if db is None:
        db = SessionLocal()
        should_close = True

    try:
        # 1. Define standard permissions for Task resource
        permissions_data = [
            ("task", "read"),
            ("task", "read_all"),
            ("task", "create"),
            ("task", "update"),
            ("task", "update_all"),
            ("task", "delete"),
            ("task", "delete_all"),
        ]

        permission_map: dict[tuple[str, str], Permission] = {}
        for resource, action in permissions_data:
            perm = (
                db.query(Permission)
                .filter(Permission.resource == resource, Permission.action == action)
                .first()
            )
            if perm is None:
                perm = Permission(resource=resource, action=action)
                db.add(perm)
                db.flush()
            permission_map[(resource, action)] = perm

        # 2. Define standard roles
        member_role = db.query(Role).filter(Role.name == "MEMBER").first()
        if member_role is None:
            member_role = Role(name="MEMBER")
            db.add(member_role)
            db.flush()

        admin_role = db.query(Role).filter(Role.name == "ADMIN").first()
        if admin_role is None:
            admin_role = Role(name="ADMIN")
            db.add(admin_role)
            db.flush()

        # 3. Associate permissions to roles
        # Member permissions: read, create, update, delete own tasks
        member_permissions = [
            ("task", "read"),
            ("task", "create"),
            ("task", "update"),
            ("task", "delete"),
        ]
        for key in member_permissions:
            perm = permission_map.get(key)
            if perm:
                exists = (
                    db.query(RolePermission)
                    .filter(
                        RolePermission.role_id == member_role.id,
                        RolePermission.permission_id == perm.id,
                    )
                    .first()
                )
                if not exists:
                    db.add(RolePermission(role_id=member_role.id, permission_id=perm.id))

        # Admin permissions: all permissions
        for perm in permission_map.values():
            exists = (
                db.query(RolePermission)
                .filter(
                    RolePermission.role_id == admin_role.id,
                    RolePermission.permission_id == perm.id,
                )
                .first()
            )
            if not exists:
                db.add(RolePermission(role_id=admin_role.id, permission_id=perm.id))

        db.commit()
        logger.info("Database initialized and seeded successfully.")
    except Exception:
        db.rollback()
        raise
    finally:
        if should_close:
            db.close()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    print("Seeding database...")
    init_db()
    print("Database seeding completed.")

from sqlalchemy.orm import Session

from .models.permission import Permission
from .models.role_permission import RolePermission
from .models.user_role import UserRole


def user_has_permission(
    db: Session,
    user_id: int,
    resource: str,
    action: str,
) -> bool:
    permission = (
        db.query(Permission)
        .join(
            RolePermission,
            RolePermission.permission_id == Permission.id,
        )
        .join(
            UserRole,
            UserRole.role_id == RolePermission.role_id,
        )
        .filter(
            UserRole.user_id == user_id,
            Permission.resource == resource,
            Permission.action == action,
        )
        .first()
    )

    return permission is not None
from sqlalchemy.orm import Session
from models.role_permission_model import RolePermission
from models.permission_model import Permission, PermissionsOfRole
from models.role_model import Role
from utils.validation.model import check_exists


def get_permissions_of_role(db: Session, role_id: str):
    check_exists(db, Role, role_id=role_id)
    
    role = db.query(Role).filter(Role.role_id == role_id).first()
    role_permissions = db.query(RolePermission).filter(RolePermission.role_id == role_id).all()
    result = []
    for rp in role_permissions:
        permission = db.query(Permission).filter(Permission.permission_id == rp.permission_id).first()
        result.append(
            {
                "permission_id": rp.permission_id,
                "permission_name": permission.permission_name if role else None,
                "role_id": rp.role_id,
                "role_name": role.role_name if role else None,
            }
        )
    return result


def assign_permissions_for_role(db: Session, role_id: str, permission_ids: list[str]):
    check_exists(db, Role, role_id=role_id)
    
    result = []
    if not permission_ids:
        db.query(RolePermission).filter(RolePermission.role_id == role_id).delete()
        db.commit()
        return result
    
    valid_permissions = db.query(Permission.permission_id).filter(Permission.permission_id.in_(permission_ids)).all()
    valid_permission_ids = {u[0] for u in valid_permissions}
    invalid_permissions = set(permission_ids) - valid_permission_ids
    if invalid_permissions:
        raise ValueError(f"Permission không tồn tại: {list(invalid_permissions)}")
    
    db.query(RolePermission).filter(RolePermission.role_id == role_id).delete()
    for permission_id in permission_ids:
        db.add(RolePermission(permission_id=permission_id, role_id=role_id))
    db.commit()
    
    role = db.query(Role).filter(Role.role_id == role_id).first()
    role_permissions = db.query(RolePermission).filter(RolePermission.role_id == role_id).all()
    for rp in role_permissions:
        permission = db.query(Permission).filter(Permission.permission_id == rp.permission_id).first()
        result.append(
            {
                "role_id": rp.role_id,
                "role_name": role.role_name if role else None,
                "permission_id": rp.permission_id,
                "permission_name": permission.permission_name if permission else None,
            }
        )
    return result


def remove_role_from_permissions(db: Session, role_id: str):
    role_permissions = db.query(RolePermission).filter(RolePermission.role_id == role_id).all()
    for role_permission in role_permissions:
        db.delete(role_permission)
    
    db.commit()
    return role_permissions

def remove_permission_from_roles(db: Session, permission_id: str):
    role_permissions = db.query(RolePermission).filter(RolePermission.permission_id == permission_id).all()
    for role_permission in role_permissions:
        db.delete(role_permission)
    
    db.commit()
    return role_permissions

from sqlalchemy.orm import Session
from models.role_permission_model import RolePermission, AssignPermissionsForRole
from models.permission_model import Permission, PermissionsOfRole
from models.role_model import Role
from fastapi import HTTPException, status


def get_permissions_of_role(db: Session, role_id: str):
    permissions = (
        db.query(Permission.permission_id, Permission.permission_name)
        .join(RolePermission, RolePermission.permission_id == Permission.permission_id)
        .filter(RolePermission.role_id == role_id)
        .all()
    )
    
    permissions=[PermissionsOfRole(permission_id=p[0], permission_name=p[1]) for p in permissions]
    
    return permissions


def assign_permissions_for_role(db: Session, payload: AssignPermissionsForRole):
    role_id = payload.role_id
    permission_ids = payload.permission_ids
    # 1. Kiểm tra role tồn tại
    role = db.query(Role).filter(Role.role_id == role_id).first()
    if not role:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Role not found")

    # Nếu mảng rỗng => xóa toàn bộ permissions của role
    if not permission_ids:
        db.query(RolePermission).filter(RolePermission.role_id == role_id).delete()
        db.commit()
        return {"message": f"All permissions removed from role {role_id}"}

    # 2. Kiểm tra tất cả permission_ids đều tồn tại
    existing_permissions = db.query(Permission.permission_id).filter(
        Permission.permission_id.in_(permission_ids)
    ).all()
    existing_permission_ids = {p[0] for p in existing_permissions}

    if len(existing_permission_ids) != len(permission_ids):
        invalid_ids = set(permission_ids) - existing_permission_ids
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid permission_ids: {list(invalid_ids)}"
        )

    # 3. Xóa toàn bộ quyền cũ của role
    db.query(RolePermission).filter(RolePermission.role_id == role_id).delete()

    # 4. Thêm mới danh sách quyền
    new_relations = [
        RolePermission(role_id=role_id, permission_id=pid)
        for pid in permission_ids
    ]
    db.add_all(new_relations)
    db.commit()

    return {"message": "Permissions updated", "assigned": permission_ids}


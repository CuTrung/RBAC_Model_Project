from sqlalchemy.orm import Session
from models.permission_model import Permission, PermissionCreate

def get_permissions(db: Session):
    return db.query(Permission).all()

def get_permission(db: Session, permission_id: str):
    return db.query(Permission).filter(Permission.permission_id == permission_id).first()

def create_permission(db: Session, permission: PermissionCreate):
    new_permission = Permission(
        permission_name=permission.permission_name,
        description=permission.description,
        resource_id=permission.resource_id
    )
    db.add(new_permission)
    db.commit()
    db.refresh(new_permission)
    return new_permission

def update_permission(db: Session, permission_id: str, updated_permission: PermissionCreate):
    permission = db.query(Permission).filter(Permission.permission_id == permission_id).first()
    if permission:
        permission.permission_name = updated_permission.permission_name
        permission.description = updated_permission.description
        permission.resource_id = updated_permission.resource_id
        db.commit()
        db.refresh(permission)
    return permission

def delete_permission(db: Session, permission_id: str):
    permission = db.query(Permission).filter(Permission.permission_id == permission_id).first()
    if permission:
        db.delete(permission)
        db.commit()
    return permission

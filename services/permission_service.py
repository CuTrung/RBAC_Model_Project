from sqlalchemy import select
from sqlalchemy.orm import Session
from models.permission_model import Permission, PermissionCreate, PermissionUpdate
from models.resource_model import Resource
from utils.string import coalesce
from utils.validation.model import check_unique, check_exists
from services import role_permission_service

def get_permissions(db: Session):
    stmt = (
        select(
            Permission.permission_id,
            Permission.permission_name,
            Permission.description,
            Resource.resource_id,
            Resource.resource_name,
        )
        .outerjoin(Resource, Permission.resource_id == Resource.resource_id)
    )
    return db.execute(stmt).mappings().all()


def get_permission(db: Session, permission_id: str):
    return db.query(Permission).filter(Permission.permission_id == permission_id).first()


def validate_permission(db: Session, permission: PermissionCreate):
    check_unique(db, Permission, permission_name=permission.permission_name)
    
    resource_id=getattr(permission, "resource_id", None)
    if resource_id:
        check_exists(db, Resource, resource_id=resource_id)


def create_permission(db: Session, permission: PermissionCreate):
    validate_permission(db, permission)
    
    new_permission = Permission(
        permission_name=permission.permission_name,
        description=permission.description,
        resource_id=permission.resource_id
    )
    db.add(new_permission)
    db.commit()
    db.refresh(new_permission)
    return new_permission


def update_permission(db: Session, permission_id: str, updated_permission: PermissionUpdate):
    check_exists(db, Permission, permission_id=permission_id)
    
    validate_permission(db, updated_permission)
    
    permission = get_permission(db, permission_id)
    permission.permission_name = coalesce(updated_permission.permission_name, permission.permission_name)
    permission.description = coalesce(updated_permission.description, permission.description)
    permission.resource_id = coalesce(updated_permission.resource_id, permission.resource_id)
    
    db.commit()
    db.refresh(permission)
    return permission


def delete_permission(db: Session, permission_id: str):
    check_exists(db, Permission, permission_id=permission_id)
    permission = get_permission(db, permission_id)
    db.delete(permission)
    
    role_permission_service.remove_permission_from_roles(db, permission_id)
    
    db.commit()
    return permission


def update_permissions_of_resource(db: Session, resource_id: str):
    permissions = db.query(Permission).filter(Permission.resource_id == resource_id).all()
    for per in permissions:
        per.resource_id = None
        update_permission(db, per.permission_id, per)

   
def remove_resource_from_permissions(db: Session, resource_id: str):
    db.query(Permission).filter(Permission.resource_id == resource_id).update(
        {"resource_id": None}, synchronize_session=False
    )
    db.commit()

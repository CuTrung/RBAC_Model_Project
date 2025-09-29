from collections import defaultdict
from click import File
from fastapi import UploadFile
import pandas as pd
from sqlalchemy import select
from sqlalchemy.orm import Session
from models.role_permission_model import RolePermission
from models.permission_model import Permission, PermissionCreate
from models.role_model import Role, RoleCreate
from services import permission_service, role_service
from utils.excel import export_excel, import_excel
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


def export_role_permissions(db: Session):
    stmt = (
        select(
            Role.role_name,
            Permission.permission_name,
        )
        .outerjoin(RolePermission, RolePermission.permission_id == Permission.permission_id)
        .outerjoin(Role, Role.role_id == RolePermission.role_id)
    )
    data = db.execute(stmt).mappings().all()
    return export_excel(data, filename="role_permissions.xlsx", sheet_name="RolePermissions")


async def import_role_permissions(db: Session, file: UploadFile = File(...)):
    role_permission_name_list = await import_excel(file)
    role_permissions_map = defaultdict(list) 
    
    for rp in role_permission_name_list:
        role_name = rp.get("role_name")
        permission_name = rp.get("permission_name")

        
        if not role_name or not permission_name:
            continue
        
        if not pd.isna(role_name): 
            role = role_service.get_role_by_name(db, role_name)
            if not role:
                role = role_service.create_role(
                    db, 
                    RoleCreate(role_name=role_name, description=role_name + " desc")
                )
            role_id = role.role_id
        
        if not pd.isna(permission_name): 
            permission = permission_service.get_permission_by_name(db, permission_name)
            if not permission:
                permission = permission_service.create_permission(
                    db, 
                    PermissionCreate(
                        permission_name=permission_name, 
                        description=permission_name + " desc", 
                        resource_id=None
                    )
                )
            permission_id = permission.permission_id
        
        if role_id and permission_id:
            role_permissions_map[role_id].append(permission_id)
            role_id = None
            permission_id = None
    

    for role_id, permission_ids in role_permissions_map.items():
        assign_permissions_for_role(db, role_id, permission_ids) 
    
    
    return {
        "số lượng record đã import": sum(len(pids) for pids in role_permissions_map.values())
    }

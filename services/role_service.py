from sqlalchemy.orm import Session
from models.role_model import Role, RoleCreate
from utils.validation.model import check_unique, check_exists
from services import group_role_service
from services import role_permission_service


def get_roles(db: Session):
    return db.query(Role).all()


def get_role(db: Session, role_id: str):
    return db.query(Role).filter(Role.role_id == role_id).first()


def create_role(db: Session, role: RoleCreate):
    check_unique(db, Role, role_name=role.role_name)
    
    new_role = Role(
        role_name=role.role_name,
        description=role.description
    )
    db.add(new_role)
    db.commit()
    db.refresh(new_role)
    return new_role

def update_role(db: Session, role_id: str, updated_role: RoleCreate):
    check_exists(db, Role, role_id=role_id)
    check_unique(db, Role, role_name=updated_role.role_name)
    
    role = get_role(db, role_id)
    role.role_name = updated_role.role_name
    role.description = updated_role.description
    
    db.commit()
    db.refresh(role)
    return role


def delete_role(db: Session, role_id: str):
    check_exists(db, Role, role_id=role_id)
    role = get_role(db, role_id)
    db.delete(role)
    
    group_role_service.remove_role_from_groups(db, role_id)
    role_permission_service.remove_role_from_permissions(db, role_id)
    
    db.commit()
    return role

from sqlalchemy.orm import Session
from models.role_model import Role, RoleCreate


def get_roles(db: Session):
    return db.query(Role).all()


def get_role(db: Session, role_id: int):
    return db.query(Role).filter(Role.id == role_id).first()


def create_role(db: Session, role: RoleCreate):
    new_role = Role(role_name=role.role_name, description=role.description)
    db.add(new_role)
    db.commit()
    db.refresh(new_role)
    return new_role


def update_role(db: Session, role_id: int, updated_role: RoleCreate):
    role = db.query(Role).filter(Role.id == role_id).first()
    if role:
        role.role_name = updated_role.role_name
        role.description = updated_role.description
        db.commit()
        db.refresh(role)
    return role


def delete_role(db: Session, role_id: int):
    role = db.query(Role).filter(Role.id == role_id).first()
    if role:
        db.delete(role)
        db.commit()
    return role

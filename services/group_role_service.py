from sqlalchemy.orm import Session
from models.group_role_model import GroupRole, GroupRoleCreate


def get_group_roles(db: Session):
    return db.query(GroupRole).all()


def get_group_role(db: Session, group_role_id: int):
    return db.query(GroupRole).filter(GroupRole.id == group_role_id).first()


def create_group_role(db: Session, group_role: GroupRoleCreate):
    new_group_role = GroupRole(group_id=group_role.group_id, role_id=group_role.role_id)
    db.add(new_group_role)
    db.commit()
    db.refresh(new_group_role)
    return new_group_role


def delete_group_role(db: Session, group_role_id: int):
    group_role = db.query(GroupRole).filter(GroupRole.id == group_role_id).first()
    if group_role:
        db.delete(group_role)
        db.commit()
    return group_role

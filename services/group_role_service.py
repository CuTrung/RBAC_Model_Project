from sqlalchemy.orm import Session
from models.group_role_model import GroupRole
from models.role_model import Role
from models.group_model import Group
from models.user_group_model import UserGroup
from utils.validation.model import check_exists

def get_roles_of_group(db: Session, group_id: str):
    check_exists(db, Group, group_id=group_id)
    
    group = db.query(Group).filter(Group.group_id == group_id).first()
    group_roles = db.query(GroupRole).filter(GroupRole.group_id == group_id).all()
    result = []
    for gr in group_roles:
        role = db.query(Role).filter(Role.role_id == gr.role_id).first()
        result.append(
            {
                "role_id": gr.role_id,
                "role_name": role.role_name if role else None,
                "group_id": gr.group_id,
                "group_name": group.group_name if group else None,
            }
        )
    return result


def assign_roles_for_group(db: Session, group_id: str, role_ids: list[str]):
    check_exists(db, Group, group_id=group_id)

    result = []
    if not role_ids:
        db.query(GroupRole).filter(GroupRole.group_id == group_id).delete()
        db.commit()
        return result
        
    valid_roles = db.query(Role.role_id).filter(Role.role_id.in_(role_ids)).all()
    valid_role_ids = {r[0] for r in valid_roles}
    invalid_roles = set(role_ids) - valid_role_ids
    if invalid_roles:
        raise ValueError(f"Permission không tồn tại: {list(invalid_roles)}")
    
    db.query(GroupRole).filter(GroupRole.group_id == group_id).delete()
    for role_id in role_ids:
        db.add(GroupRole(group_id=group_id, role_id=role_id))
    db.commit()

    group = db.query(Group).filter(Group.group_id == group_id).first()
    group_roles = db.query(GroupRole).filter(GroupRole.group_id == group_id).all()
    for gr in group_roles:
        role = db.query(Role).filter(Role.role_id == gr.role_id).first()
        result.append(
            {
                "group_id": gr.group_id,
                "group_name": group.group_name if group else None,
                "role_id": gr.role_id,
                "role_name": role.role_name if role else None,
            }
        )
    return result


def remove_group_from_roles(db: Session, group_id: str):
    group_roles = db.query(GroupRole).filter(GroupRole.group_id == group_id).all()
    for group_role in group_roles:
        db.delete(group_role)
    
    db.commit()
    return group_roles

def remove_role_from_groups(db: Session, role_id: str):
    group_roles = db.query(GroupRole).filter(GroupRole.role_id == role_id).all()
    for group_role in group_roles:
        db.delete(group_role)
    
    db.commit()
    return group_roles
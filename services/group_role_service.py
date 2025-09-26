from sqlalchemy.orm import Session
from models.group_role_model import GroupRole
from models.role_model import Role
from models.group_model import Group


def get_roles_of_group(db: Session, group_id: int):
    group = db.query(Group).filter(Group.group_id == group_id).first()
    if not group:
        raise ValueError("Không tìm thấy nhóm")
    group_roles = db.query(GroupRole).filter(GroupRole.group_id == group_id).all()
    result = []
    for gr in group_roles:
        role = db.query(Role).filter(Role.role_id == gr.role_id).first()
        result.append(
            {
                "group_id": gr.group_id,
                "group_name": group.group_name,
                "role_id": gr.role_id,
                "role_name": role.role_name if role else None,
            }
        )
    return result


def assign_roles_for_group(db: Session, group_id: int, role_ids: list[int]):
    group = db.query(Group).filter(Group.group_id == group_id).first()
    if not group:
        raise ValueError("Nhóm không tồn tại")
    valid_roles = db.query(Role.role_id).filter(Role.role_id.in_(role_ids)).all()
    valid_role_ids = {r[0] for r in valid_roles}
    invalid_roles = set(role_ids) - valid_role_ids
    if invalid_roles:
        raise ValueError(f"Quyền không tồn tại: {list(invalid_roles)}")
    current_role_ids = set(
        gr.role_id
        for gr in db.query(GroupRole).filter(GroupRole.group_id == group_id).all()
    )
    if set(role_ids) == current_role_ids and len(role_ids) == len(current_role_ids):
        raise ValueError("Tất cả quyền đã được gán vào nhóm này")
    already_assigned = set(role_ids) & current_role_ids
    if already_assigned:
        raise ValueError(
            f"Quyền đã được gán vào nhóm này: {list(already_assigned)}"
        )
    db.query(GroupRole).filter(GroupRole.group_id == group_id).delete()
    for role_id in role_ids:
        db.add(GroupRole(group_id=group_id, role_id=role_id))
    db.commit()
    # Trả về danh sách role thuộc group sau khi gán
    group_roles = db.query(GroupRole).filter(GroupRole.group_id == group_id).all()
    result = []
    for gr in group_roles:
        role = db.query(Role).filter(Role.role_id == gr.role_id).first()
        group = db.query(Group).filter(Group.group_id == gr.group_id).first()
        result.append(
            {
                "group_id": gr.group_id,
                "group_name": group.group_name if group else None,
                "role_id": gr.role_id,
                "role_name": role.role_name if role else None,
            }
        )
    return result

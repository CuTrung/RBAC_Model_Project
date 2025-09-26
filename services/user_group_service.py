from sqlalchemy.orm import Session
from models.user_group_model import UserGroup
from models.user_model import User
from models.group_model import Group


def get_groups_of_user(db: Session, user_id: int):
    user = db.query(User).filter(User.user_id == user_id).first()
    if not user:
        raise ValueError("Không tìm thấy người dùng")
    user_groups = db.query(UserGroup).filter(UserGroup.user_id == user_id).all()
    result = []
    for ug in user_groups:
        group = db.query(Group).filter(Group.group_id == ug.group_id).first()
        result.append(
            {
                "user_id": ug.user_id,
                "username": user.username,
                "group_id": ug.group_id,
                "group_name": group.group_name if group else None,
            }
        )
    return result


def assign_users_for_group(db: Session, group_id: int, user_ids: list[int]):
    group = db.query(Group).filter(Group.group_id == group_id).first()
    if not group:
        raise ValueError("Nhóm không tồn tại")
    valid_users = db.query(User.user_id).filter(User.user_id.in_(user_ids)).all()
    valid_user_ids = {u[0] for u in valid_users}
    invalid_users = set(user_ids) - valid_user_ids
    if invalid_users:
        raise ValueError(f"Người dùng không tồn tại: {list(invalid_users)}")
    # Lấy danh sách user_id hiện tại của group
    current_user_ids = set(
        u.user_id
        for u in db.query(UserGroup).filter(UserGroup.group_id == group_id).all()
    )
    # Nếu danh sách truyền vào giống hệt danh sách hiện tại, báo lỗi
    if set(user_ids) == current_user_ids and len(user_ids) == len(current_user_ids):
        raise ValueError("Tất cả người dùng đã được gán vào nhóm này")
    # Nếu có user đã được assign, báo rõ user nào
    already_assigned = set(user_ids) & current_user_ids
    if already_assigned:
        raise ValueError(
            f"Người dùng đã được gán vào nhóm này: {list(already_assigned)}"
        )
    # Xóa hết user cũ và gán lại user mới
    db.query(UserGroup).filter(UserGroup.group_id == group_id).delete()
    for user_id in user_ids:
        db.add(UserGroup(user_id=user_id, group_id=group_id))
    db.commit()
    # Trả về danh sách user thuộc group sau khi gán
    user_groups = db.query(UserGroup).filter(UserGroup.group_id == group_id).all()
    result = []
    for ug in user_groups:
        user = db.query(User).filter(User.user_id == ug.user_id).first()
        group = db.query(Group).filter(Group.group_id == ug.group_id).first()
        result.append(
            {
                "user_id": ug.user_id,
                "username": user.username if user else None,
                "group_id": ug.group_id,
                "group_name": group.group_name if group else None,
            }
        )
    return result

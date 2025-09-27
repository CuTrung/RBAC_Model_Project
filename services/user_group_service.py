from sqlalchemy.orm import Session
from models.user_group_model import UserGroup
from models.user_model import User
from models.group_model import Group
from utils.validation.model import check_exists


def get_users_of_group(db: Session, group_id: str):
    check_exists(db, Group, group_id=group_id)
    
    group = db.query(Group).filter(Group.group_id == group_id).first()
    user_groups = db.query(UserGroup).filter(UserGroup.group_id == group_id).all()
    result = []
    for ug in user_groups:
        user = db.query(User).filter(User.user_id == ug.user_id).first()
        result.append(
            {
                "group_id": ug.group_id,
                "group_name": group.group_name if group else None,
                "user_id": ug.user_id,
                "username": user.username if user else None,
            }
        )
    return result


def assign_users_for_group(db: Session, group_id: str, user_ids: list[str]):
    check_exists(db, Group, group_id=group_id)

    result = []
    # Xóa hết user trong group nếu user_ids rỗng
    if not user_ids:
        db.query(UserGroup).filter(UserGroup.group_id == group_id).delete()
        db.commit()
        return result
    
    valid_users = db.query(User.user_id).filter(User.user_id.in_(user_ids)).all()
    valid_user_ids = {u[0] for u in valid_users}
    invalid_users = set(user_ids) - valid_user_ids
    if invalid_users:
        raise ValueError(f"User không tồn tại: {list(invalid_users)}")
    
    # Xóa hết user cũ và gán lại user mới
    db.query(UserGroup).filter(UserGroup.group_id == group_id).delete()
    for user_id in user_ids:
        db.add(UserGroup(user_id=user_id, group_id=group_id))
    db.commit()
    
    # Users thuộc group sau khi gán
    group = db.query(Group).filter(Group.group_id == group_id).first()
    user_groups = db.query(UserGroup).filter(UserGroup.group_id == group_id).all()
    for ug in user_groups:
        user = db.query(User).filter(User.user_id == ug.user_id).first()
        result.append(
            {
                "user_id": ug.user_id,
                "username": user.username if user else None,
                "group_id": ug.group_id,
                "group_name": group.group_name if group else None,
            }
        )
    return result


def remove_user_from_groups(db: Session, user_id: str):
    user_groups = db.query(UserGroup).filter(UserGroup.user_id == user_id).all()
    for user_group in user_groups:
        db.delete(user_group)
    
    db.commit()
    return user_groups

def remove_group_from_users(db: Session, group_id: str):
    user_groups = db.query(UserGroup).filter(UserGroup.group_id == group_id).all()
    for user_group in user_groups:
        db.delete(user_group)
    
    db.commit()
    return user_groups
from sqlalchemy.orm import Session

def check_unique(db: Session, model, **kwargs):
    query = db.query(model)
    for field, value in kwargs.items():
        query = query.filter(getattr(model, field) == value)
    
    if query.first():
        fields_str = ", ".join([f"{k}: {v}" for k, v in kwargs.items()])
        raise ValueError(f"{model.__name__} đã tồn tại với `{fields_str}`")
    
def check_exists(db: Session, model, **kwargs):
    query = db.query(model)
    for field, value in kwargs.items():
        query = query.filter(getattr(model, field) == value)
    
    if not query.first():
        fields_str = ", ".join([f"{k}: {v}" for k, v in kwargs.items()])
        raise ValueError(f"{model.__name__} không tồn tại với `{fields_str}`")

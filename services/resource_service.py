from sqlalchemy.orm import Session
from models.resource_model import Resource, ResourceCreate

def get_resources(db: Session):
    return db.query(Resource).all()

def get_resource(db: Session, resource_id: str):
    return db.query(Resource).filter(Resource.resource_id == resource_id).first()

def create_resource(db: Session, resource: ResourceCreate):
    new_resource = Resource(
        resource_name=resource.resource_name,
        description=resource.description
    )
    db.add(new_resource)
    db.commit()
    db.refresh(new_resource)
    return new_resource

def update_resource(db: Session, resource_id: str, updated_resource: ResourceCreate):
    resource = db.query(Resource).filter(Resource.resource_id == resource_id).first()
    if resource:
        resource.resource_name = updated_resource.resource_name
        resource.description = updated_resource.description
        db.commit()
        db.refresh(resource)
    return resource

def delete_resource(db: Session, resource_id: str):
    resource = db.query(Resource).filter(Resource.resource_id == resource_id).first()
    if resource:
        db.delete(resource)
        db.commit()
    return resource

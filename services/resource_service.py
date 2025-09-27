from sqlalchemy.orm import Session
from models.resource_model import Resource, ResourceCreate
from utils.validation.model import check_unique, check_exists
from services import permission_service


def get_resources(db: Session):
    return db.query(Resource).all()


def get_resource(db: Session, resource_id: str):
    return db.query(Resource).filter(Resource.resource_id == resource_id).first()


def create_resource(db: Session, resource: ResourceCreate):
    check_unique(db, Resource, resource_name=resource.resource_name)
    
    new_resource = Resource(
        resource_name=resource.resource_name,
        description=resource.description
    )
    db.add(new_resource)
    db.commit()
    db.refresh(new_resource)
    return new_resource

def update_resource(db: Session, resource_id: str, updated_resource: ResourceCreate):
    check_exists(db, Resource, resource_id=resource_id)
    check_unique(db, Resource, resource_name=updated_resource.resource_name)
    
    resource = get_resource(db, resource_id)
    resource.resource_name = updated_resource.resource_name
    resource.description = updated_resource.description
    
    db.commit()
    db.refresh(resource)
    return resource


def delete_resource(db: Session, resource_id: str):
    check_exists(db, Resource, resource_id=resource_id)
    resource = get_resource(db, resource_id)
    db.delete(resource)
    
    permission_service.remove_resource_from_permissions(db, resource_id)
    
    db.commit()
    return resource

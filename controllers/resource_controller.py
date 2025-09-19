from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from models.resource_model import ResourceCreate, ResourceResponse
from services import resource_service
from views import resource_view
from database import get_db

router = APIRouter()

@router.get("/", response_model=list[ResourceResponse])
def get_resources(db: Session = Depends(get_db)):
    resources = resource_service.get_resources(db)
    return resources

@router.get("/{resource_id}", response_model=ResourceResponse)
def get_resource(resource_id: str, db: Session = Depends(get_db)):
    resource = resource_service.get_resource(db, resource_id)
    if resource:
        return resource
    return resource_view.error_response("Resource not found", 404)

@router.post("/", response_model=ResourceResponse)
def create_resource(resource: ResourceCreate, db: Session = Depends(get_db)):
    return resource_service.create_resource(db, resource)

@router.put("/{resource_id}", response_model=ResourceResponse)
def update_resource(resource_id: str, resource: ResourceCreate, db: Session = Depends(get_db)):
    updated = resource_service.update_resource(db, resource_id, resource)
    if updated:
        return updated
    return resource_view.error_response("Resource not found", 404)

@router.delete("/{resource_id}")
def delete_resource(resource_id: str, db: Session = Depends(get_db)):
    deleted = resource_service.delete_resource(db, resource_id)
    if deleted:
        return resource_view.success_response({"resource_id": deleted.resource_id}, "Resource deleted")
    return resource_view.error_response("Resource not found", 404)

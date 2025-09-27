from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from models.resource_model import ResourceCreate, ResourceResponse
from services import resource_service
from views import resource_view
from database import get_db

router = APIRouter()

@router.get("/", response_model=list[ResourceResponse])
def get_resources(db: Session = Depends(get_db)):
    try:
        return resource_view.success_response(
            resource_service.get_resources(db)
        )
    except ValueError as ve:
        return resource_view.error_response(str(ve), 400)

@router.get("/{resource_id}", response_model=ResourceResponse)
def get_resource(resource_id: str, db: Session = Depends(get_db)):
    try:
        return resource_view.success_response(
            resource_service.get_resource(db, resource_id)
        )
    except ValueError as ve:
        return resource_view.error_response(str(ve), 400)

@router.post("/", response_model=ResourceResponse)
def create_resource(resource: ResourceCreate, db: Session = Depends(get_db)):
    try:
        return resource_view.success_response(
            resource_service.create_resource(db, resource), 
            "Tạo resource thành công"
        )
    except ValueError as ve:
        return resource_view.error_response(str(ve), 400)
    

@router.put("/{resource_id}", response_model=ResourceResponse)
def update_resource(resource_id: str, resource: ResourceCreate, db: Session = Depends(get_db)):
    try:
        return resource_view.success_response(
            resource_service.update_resource(db, resource_id, resource), 
            "Cập nhật resource thành công"
        )
    except ValueError as ve:
        return resource_view.error_response(str(ve), 400)


@router.delete("/{resource_id}")
def delete_resource(resource_id: str, db: Session = Depends(get_db)):
    try:
        return resource_view.success_response(
            resource_service.delete_resource(db, resource_id), 
            "Xóa resource thành công"
        )
    except ValueError as ve:
        return resource_view.error_response(str(ve), 400)

    

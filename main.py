from fastapi import FastAPI
from controllers.user_controller import router as user_router
from database import Base, engine

Base.metadata.create_all(bind=engine)

app = FastAPI(title="RBAC Model Project")

app.include_router(user_router, prefix="/users", tags=["Users"])

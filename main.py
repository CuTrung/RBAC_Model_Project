from fastapi import FastAPI
from controllers.user_controller import router as user_router
from controllers.group_controller import router as group_router
from controllers.role_controller import router as role_router
from controllers.user_group_controller import router as user_group_router
from controllers.group_role_controller import router as group_role_router
from controllers.permission_controller import router as permission_router
from controllers.role_permission_controller import router as role_permission_router
from controllers.resource_controller import router as resource_router

from database import Base, engine

Base.metadata.create_all(bind=engine)

app = FastAPI(title="RBAC Model Project")

app.include_router(user_router, prefix="/users", tags=["Users"])
app.include_router(group_router, prefix="/groups", tags=["Groups"])
app.include_router(role_router, prefix="/roles", tags=["Roles"])
app.include_router(user_group_router, prefix="/user-groups", tags=["UserGroups"])
app.include_router(group_role_router, prefix="/group-roles", tags=["GroupRoles"])
app.include_router(permission_router, prefix="/permissions", tags=["Permissions"])
app.include_router(role_permission_router, prefix="/role-permissions", tags=["RolePermissions"])
app.include_router(resource_router, prefix="/resources", tags=["Resources"])

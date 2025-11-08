from fastapi import APIRouter

router = APIRouter()

from .tenants import router as tenants_router
from .users import router as users_router

router.include_router(tenants_router)
router.include_router(users_router)


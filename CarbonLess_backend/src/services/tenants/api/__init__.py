from fastapi import APIRouter

router = APIRouter()

from .tenants import router as tenants_router

router.include_router(tenants_router)


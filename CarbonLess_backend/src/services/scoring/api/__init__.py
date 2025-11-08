from fastapi import APIRouter

router = APIRouter()

from .routes import router as scoring_router

router.include_router(scoring_router)

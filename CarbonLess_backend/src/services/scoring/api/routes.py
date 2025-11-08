from fastapi import APIRouter, Depends

from services.scoring.schemas.schemas import TransportationFormSchema
from src.services.scoring.services.services import submit_transportation_form
from src.utils.jwt_handler import get_current_user

router = APIRouter(prefix='/scoring')

@router.get('/healthy')
async def health_check():
    return {"status": "ok"}

@router.get('/transportation')
async def submit_transportation(form_data: TransportationFormSchema, current_user=Depends(get_current_user)):
    return await submit_transportation_form(current_user, form_data)
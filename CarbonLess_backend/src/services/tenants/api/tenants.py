from fastapi import APIRouter

router = APIRouter(prefix='/tenants')

@router.get('/about')
async def get_healthy():
    return {'service':'tenants'}
from fastapi import APIRouter
from src.services.tenants.schemas.schemas import UserRegister, UserLogin, UpdateUser
from src.services.tenants.services.services import register_user, login_user, patch_user

router = APIRouter(prefix='/users')

@router.get('/about')
async def get_healthy():
    return {'service':'users'}

@router.post('/register')
async def register(request: UserRegister):
    return await register_user(request)

@router.post('/login')
async def login(request: UserLogin):
    return await login_user(request)

@router.patch('/id/{user_id}')
async def login(user_id, request: UpdateUser):
    return await patch_user(user_id, request)


@router.patch('/id/{user_id}/initial-form')
async def login(user_id, request: UpdateUser):
    return await patch_user(user_id, request)
from fastapi.exceptions import HTTPException

from src.services.tenants.schemas.schemas import UserRegister, UserLogin, UpdateUser, UserInitialForm
from src.services.tenants.models import models
from src.utils.jwt_handler import create_jwt


async def register_user(request: UserRegister):
    exists = await models.Users.filter(username=request.username).get_or_none()
    if exists:
        raise HTTPException(403, 'USER_WITH_USERNAME_EXISTS')
    if not exists:
        exists = await models.Users.filter(email=request.email).get_or_none()
        if exists:
            raise HTTPException(403, 'USER_WITH_EMAIL_EXISTS')

    data = request.model_dump()
    data.update({'password':models.Users.generate_password()})
    user = await models.Users.create(**data)
    await user.save()
    return {"username":user.username, "password":user.password, 'id':user.id}


async def login_user(request: UserLogin):
    tenant = await models.Tenants.filter(code=request.tenant_code).get_or_none()
    if not tenant:
        raise HTTPException(404, 'TENANT_NOT_FOUND')

    user = await models.Users.filter(username=request.username, id_tenant=tenant.id).get_or_none()
    if not user:
        raise HTTPException(404, 'USER_NOT_FOUND')

    if request.password != user.password:
        raise HTTPException(401, 'UNAUTHORIZED')

    token = create_jwt(user.id_tenant, user.id, 240, user.survey_completed)
    return {
        'token': str(token)
    }

async def patch_user(user_id, request: UpdateUser):

    user = await models.Users.filter(username=user_id).get_or_none()
    if not user:
        raise HTTPException(404, 'USER_NOT_FOUND')

    update_data = request.model_dump(exclude_unset=True)
    await user.update_from_dict(update_data)
    await user.save()

    return {k: getattr(user, k) for k in update_data.keys()}

async def initial_form_update(user_id, request: UserInitialForm):

    user = await models.Users.filter(username=user_id).get_or_none()
    if not user:
        raise HTTPException(404, 'USER_NOT_FOUND')

    user.survey_completed = True
    await user.save()
    return {"message":"in progress"}
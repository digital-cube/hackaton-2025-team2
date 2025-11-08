from fastapi import APIRouter, Request, HTTPException

from src.services.tenants.models import models

router = APIRouter(prefix='/tenants')

@router.get('/about')
async def get_healthy():
    return {'service':'tenants'}

@router.get("/info")
async def get_info(request: Request):

    code = get_tenant_code_based_on_referrer(request)

    tenant = await models.Tenants.filter(code=code).get_or_none()
    if not tenant:
        raise HTTPException(status_code=404, detail="Tenant not found")

    return {
        "id_tenant": tenant.id,
        "code": tenant.code,
        "name": tenant.display_name,
    }

def get_tenant_code_based_on_referrer(request: Request):
    referer = request.headers.get("Referer")
    if not referer:
        referer = request.headers.get("host")
    try:

        origin = referer.split(':')[0].strip('/').upper().split('/')[0]
        code = origin.split('.')[0]
        code = code[:-len('-ESCAPE')]
    except Exception as e:
        raise HTTPException(403, 'INVALID_URL')
    return code

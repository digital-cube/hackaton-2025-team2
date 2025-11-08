import random
import string
import uuid

from tortoise import fields
from tortoise import Model

class BaseModel(Model):
    id = fields.UUIDField(default=uuid.uuid4, pk=True)
    id_tenant = fields.UUIDField(null=False, default=uuid.uuid4)
    created_at = fields.DatetimeField(auto_now=True)
    last_updated = fields.DatetimeField(auto_now_add=True)
    active= fields.BooleanField(default=True)


class Tenants(BaseModel):
    class Meta:
        table = "tenants"

    address = fields.CharField(512, null=True)
    address_coords = fields.CharField(32, null=True)
    display_name = fields.CharField(256, null=True)
    code = fields.CharField(64, null=True)


class Users(BaseModel):
    class Meta:
        table = "users"

    address = fields.CharField(512, null=True)
    address_coords = fields.CharField(32, null=True)
    display_name = fields.CharField(256, null=True)
    username = fields.CharField(32, null=True, unique=True)
    email = fields.CharField(64, null=True, unique=True)
    password = fields.CharField(128, null=True)
    first_name = fields.CharField(128, null=True)
    last_name = fields.CharField(128, null=True)
    primary_transport = fields.CharField(128, null=True)
    balance = fields.IntField(null=True)
    survey_completed = fields.BooleanField(default=False)

    @classmethod
    def generate_password(cls, length: int = 8) -> str:
        chars = string.ascii_letters + string.digits
        password = ''.join(random.choice(chars) for _ in range(length))
        return password


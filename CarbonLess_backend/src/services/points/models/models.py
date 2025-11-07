from CarbonLess_backend.src.shared.models.base_model import BaseModel
from tortoise import fields

class UsersPoints(BaseModel):
    user_id = fields.ForeignKeyField()
    points = fields.IntField(default=0)
    action_type = fields.CharField(max_length=100)

    class Meta:
        table = "users_points"
        indexes = [("user_id",)]
from enum import Enum

from CarbonLess_backend.src.shared.models.base_model import BaseModel
from tortoise import fields

class ActionTypeEnum(Enum, str):
    TRANSPORTATION = "transportation"
    RECYCLING = "recycling"
    ENERGY_SAVING = "energy_saving"
    WATER_SAVING = "water_saving"
    WASTE_REDUCTION = "waste_reduction"
    SUSTAINABLE_SHOPPING = "sustainable_shopping"
    COMMUNITY_INVOLVEMENT = "community_involvement"
    EDUCATION_AWARENESS = "education_awareness"
    OTHER = "other"

class UsersPoints(BaseModel):

    user_id = fields.ForeignKeyField("models.User", related_name="points_records",)
    points = fields.IntField(default=0)
    action_type = fields.CharField(max_length=100)
    c02_emission = fields.FloatField(null=True)

    class Meta:
        table = "users_points"
        indexes = [("user_id",), ("action_type",)]
from tortoise import fields, Model

class BaseModel(Model):

    id = fields.UUIDField(primary_key=True)
    created = fields.DatetimeField(auto_now_add=True)
    last_updated = fields.DatetimeField(auto_now=True)

    created_by = fields.UUIDField(null=True, db_index=True)
    last_update_by = fields.UUIDField(null=True, db_index=True)

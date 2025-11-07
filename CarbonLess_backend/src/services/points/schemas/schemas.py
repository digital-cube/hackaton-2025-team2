from pydantic import BaseModel


class TransportationFormSchema(BaseModel):
    mode_of_transportation: str
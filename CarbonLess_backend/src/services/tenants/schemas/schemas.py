from pydantic import BaseModel, EmailStr


class UserRegister(BaseModel):
    email: EmailStr
    username: str
    first_name: str
    last_name: str

class UserLogin(BaseModel):
    username: str
    password: str
    tenant_code: str

class InitialFormRequest(BaseModel):
    username: str
    password: str
    
class UpdateUser(BaseModel):
    address : str | None = None
    address_coords : str | None = None
    display_name : str | None = None
    username : str | None = None
    email : str | None = None
    first_name : str | None = None
    last_name : str | None = None
    primary_transport : str | None = None
    balance : int | None = None

class UserInitialForm(BaseModel):
    address : str | None = None
    address_coords : str | None = None
    primary_transport : str | None = None

from pydantic import BaseModel

class UserBase(BaseModel):
    id: int
    first_name: str
    last_name: str
    email: str
    profile_image: str

    class Config:
        from_attributes = True
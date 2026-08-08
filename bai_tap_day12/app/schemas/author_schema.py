from pydantic import BaseModel, ConfigDict, EmailStr


class AuthorResponse(BaseModel):
    id: int
    name: str
    email: EmailStr

    model_config = ConfigDict(from_attributes=True)

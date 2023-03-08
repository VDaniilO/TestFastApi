from pydantic import BaseModel, validator, Field


class UserSchema(BaseModel):
    user_name: str
    money: int
    # Field(..., gt=0, description='Can not be negative')

    class Config:
        orm_mode = True
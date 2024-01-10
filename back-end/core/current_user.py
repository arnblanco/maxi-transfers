from pydantic import BaseModel, Field


class CurrentUser(BaseModel):
    username: str = Field(None, description="username")

    class Config:
        validate_assignment = True

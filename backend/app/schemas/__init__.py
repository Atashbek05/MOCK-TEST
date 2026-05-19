# Pydantic schema definitions package
# Schemas define the shape of API request/response bodies

from pydantic import BaseModel


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

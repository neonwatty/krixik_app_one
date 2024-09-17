from pydantic import BaseModel, ValidationError, Field, ConfigDict, EmailStr
from typing import Optional


uuid4_pattern = r"^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$"


class File(BaseModel):
    id: str = Field(pattern=uuid4_pattern)
    email: EmailStr
    model_config = ConfigDict(extra="forbid")


def validator(input_dict: dict) -> None:
    try:
        check = File(**input_dict)
        return None
    except ValidationError as e:
        raise e

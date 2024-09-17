from pydantic import BaseModel, ValidationError, Field, ConfigDict
from typing import Optional

uuid4_pattern = r"^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$"


class History(BaseModel):
    request_id: str = Field(pattern=uuid4_pattern)
    user_id: Optional[str] = Field(None, pattern=uuid4_pattern)
    exception: Optional[str] = None
    model_config = ConfigDict(extra="forbid")


def validator(input_dict: dict) -> None:
    try:
        check = History(**input_dict)
        return None
    except ValidationError as e:
        raise e

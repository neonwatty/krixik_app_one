from pydantic import BaseModel, ValidationError, Field, ConfigDict
from typing import Optional


uuid4_pattern = r"^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$"


class File(BaseModel):
    file_id: str = Field(pattern=uuid4_pattern)
    file_name: Optional[str] = Field(None, min_length=6, max_length=19)
    user_id: Optional[str] = Field(None, pattern=uuid4_pattern)
    tag_1: Optional[str] = Field(None, min_length=0, max_length=10)
    tag_2: Optional[str] = Field(None, min_length=0, max_length=10)
    tag_3: Optional[str] = Field(None, min_length=0, max_length=10)
    expire_time: Optional[int] = Field(None, ge=0)
    is_processed: Optional[bool] = None
    model_config = ConfigDict(extra="forbid")


def validator(input_dict: dict) -> None:
    try:
        check = File(**input_dict)
        return None
    except ValidationError as e:
        raise e

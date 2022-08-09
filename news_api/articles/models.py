import json
from datetime import datetime
from typing import Any, Optional

from bson.errors import InvalidId
from bson.objectid import ObjectId
from dateutil.parser import parse
from pydantic import BaseModel as PydanticBaseModel
from pydantic import Field, validator

# from uuid import UUID, uuid4


def is_future_date(date_input: datetime) -> bool:
    now = datetime.now()
    if date_input.timestamp() < now.timestamp():
        return False
    else:
        return True


class FutureDate(Exception):
    pass


class CustomBaseModel(PydanticBaseModel):
    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {
            datetime: lambda v: str(v.timestamp()),
            ObjectId: lambda v: str(v),
        }


class Article(CustomBaseModel):
    id: Optional[ObjectId] = Field(alias="_id")
    # uuid: UUID = Field(default_factory=uuid4)
    title: str
    text: str
    date: datetime = Field(default_factory=datetime.utcnow)  # not created by default
    author: str
    tags: Optional[list[str]]

    @validator("id", pre=True)
    def convert_to_objectid(cls, value):
        try:
            valid_id = ObjectId(value)
            return valid_id
        except (InvalidId, TypeError):
            raise ValueError("Invalid article id")

    @validator("tags")
    def validate_tags_as_list(cls, values):
        for val in values:
            try:
                assert isinstance(val, str)
                assert len(val) < 30
            except AssertionError:
                raise ValueError("Invalid tag")

    @validator("date", pre=True)
    def format_raw_date(cls, value) -> datetime:
        if isinstance(value, datetime):
            return value
        else:
            return parse(value, dayfirst=False)

    @validator("date")
    def validate_no_future_date(cls, value) -> datetime:
        if is_future_date(value):
            raise FutureDate("Invalid (future) date")  # TODO: display to user
        else:
            return value

    @validator("title", pre=True)
    def lower_case_title(cls, value) -> str:
        return value.title()


def format_response(article: Article) -> dict[str, Any]:
    model_to_json = article.json(
        exclude_none=True, exclude_unset=True, models_as_dict=False
    )
    return json.loads(model_to_json)

from datetime import datetime
from typing import Optional, Union
from uuid import UUID, uuid4

from bson.errors import InvalidId
from bson.objectid import ObjectId
from dateutil.parser import parse
from pydantic import BaseModel as PydanticBaseModel
from pydantic import Field, validator


def is_future_date(date_input: datetime) -> bool:
    now = datetime.now()
    if date_input.timestamp() < now.timestamp():
        return False
    else:
        return True


# def add_padding(date_input: int) -> str:
#     return f"0{date_input}" if date_input < 10 else str(date_input)


# class FormattedDate(datetime):
#     def __repr__(self):
#         # day = f"{add_padding(self.day)}"
#         # month = f"{add_padding(self.month)}"
#         return self.strftime("%d-%m-%Y")
#         # return f"{day}-{month}-{self.year}"


class FutureDate(Exception):
    pass


class CustomBaseModel(PydanticBaseModel):
    class Config:
        arbitrary_types_allowed = True


class Article(CustomBaseModel):
    article_id: Union[UUID, ObjectId] = Field(default_factory=uuid4)
    title: str
    text: str
    date: datetime = Field(default_factory=datetime.utcnow)
    author: str
    genre: Optional[str]
    tags: Optional[list[str]]

    @validator("article_id", pre=True)
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
            return parse(value, dayfirst=True)

    @validator("date")
    def validate_no_future_date(cls, value):
        if is_future_date(value):
            raise FutureDate("Invalid (future) date")

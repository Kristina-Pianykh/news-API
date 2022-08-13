from datetime import datetime
from typing import Optional

from bson.objectid import ObjectId
from dateutil.parser import parse
from pydantic import BaseModel as PydanticBaseModel
from pydantic import Field, validator
from pydantic.errors import DateNotInThePastError


class PastDate(datetime):
    """
    A similar structure to pydantic.types.PastDate but inheriting
    from datetime to allow comparisons with the entries added today
    """

    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, value: datetime) -> datetime:
        if value >= datetime.now():
            raise DateNotInThePastError()

        return value


class CustomBaseModel(PydanticBaseModel):
    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True


class Article(CustomBaseModel):
    id: Optional[str] = Field(alias="_id")
    title: str
    text: str
    date: PastDate = Field(default_factory=datetime.utcnow().date)
    author: str

    @validator("id", pre=True)
    def convert_to_objectid(cls, value) -> str:
        if isinstance(value, ObjectId):
            return str(value)
        else:
            return value

    @validator("date", pre=True)
    def format_raw_date(cls, value) -> PastDate:
        if isinstance(value, str):
            return parse(value)  # type: ignore
        else:  # datetime type
            return value

    @validator("title", "author", pre=True)
    def lower_case_title(cls, value) -> str:
        return value.title()

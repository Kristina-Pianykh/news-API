from datetime import datetime
from typing import Any, MutableMapping, Union
from uuid import UUID

from bson.errors import InvalidId
from bson.objectid import ObjectId
from pymongo import MongoClient

from .models import Article

client = MongoClient("mongodb://127.0.0.1:27017")
db = client.local
news = db.news

Document = MutableMapping[
    str,
    Union[ObjectId, UUID, datetime, str],
]

# client.close() ?


def get(query_param: str) -> Union[Article, None]:  # by id, uuid, title
    filter_by: Document = {}
    try:
        filter_by["_id"] = ObjectId(query_param)
    except InvalidId:
        filter_by["uuid"] = UUID(query_param)
    except ValueError:
        filter_by["title"] = query_param

    result: Union[MutableMapping, None] = news.find_one(filter_by)
    try:
        return Article(**result)
    except TypeError:
        return None


def get_many():  # by author, date
    raise NotImplementedError


def update():
    raise NotImplementedError


def delete():
    raise NotImplementedError


def create(input_data: dict[str, Any]) -> ObjectId:
    article = Article(**input_data)
    result = news.insert_one(article.dict())
    return result.inserted_id

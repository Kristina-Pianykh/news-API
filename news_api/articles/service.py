import os
from typing import Any, MutableMapping, Optional, Union

from bson.errors import InvalidId
from bson.objectid import ObjectId
from pymongo import MongoClient

from .models import Article

connection_string = os.environ["DB_CONNECTION_STRING"]
client = MongoClient(connection_string)
db = client.local
news = db.news

Document = MutableMapping[
    str,
    Union[ObjectId, str],
]


def get_one(article_id: str) -> Optional[Article]:
    try:
        object_id = ObjectId(article_id)
    except (ValueError, InvalidId):
        return

    if result := news.find_one({"_id": object_id}):
        article = Article(**result)
        return article


def get_many(query_param: str, field_name: str) -> list[Article]:
    articles: list[Article] = []
    filter_by = {field_name: query_param.title()}
    if results := news.find(filter_by):
        articles = [Article(**record) for record in results]
    return articles


def update(article_id: str, new_values: Article) -> Optional[Article]:
    article: Optional[Article] = get_one(article_id)
    if article:
        filter_by = {"_id": ObjectId(article.id)}
        values_to_update = {"$set": new_values.dict(exclude={"_id"})}
        news.update_one(filter_by, values_to_update, upsert=False)
        new_values.id = article_id
        return new_values


def delete(article_id: str) -> int:
    try:
        object_id = ObjectId(article_id)
    except (TypeError, InvalidId):
        return -1
    result = news.delete_one({"_id": object_id})
    return result.deleted_count


def create(input_data: dict[str, Any]) -> Article:
    article = Article(**input_data)
    news.insert_one(article.dict())
    return article

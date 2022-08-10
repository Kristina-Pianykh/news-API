from typing import MutableMapping, Union

from bson.objectid import ObjectId
from bson.errors import InvalidId
from pymongo import MongoClient

from .models import Article

client = MongoClient("mongodb://127.0.0.1:27017")
db = client.local
news = db.news

Document = MutableMapping[
    str,
    Union[ObjectId, str],
]


def get_one(query_param: str) -> Union[Article, None]:  # by id or title
    filter_by: Document = {}
    try:
        filter_by["_id"] = ObjectId(query_param)
    except (ValueError, InvalidId):
        filter_by["title"] = query_param

    result = news.find_one(filter_by)
    if result:
        article = Article(**result)
        return article
    else:
        return None


def get_many(author: str) -> list[Article]:
    articles: list[Article] = []
    filter_by = {"author": author.title()}
    results = news.find(filter_by)
    if results:
        articles = [Article(**record) for record in results]
    return articles


def update(article_id: str, new_values: Article) -> Union[Article, None]:
    article: Union[Article, None] = get_one(article_id)
    if not article:
        return None
    else:
        filter_by = {"_id": ObjectId(article.id)}
        values_to_update = {"$set": new_values.dict(exclude={"_id"})}
        news.update_one(filter_by, values_to_update, upsert=False)
        new_values.id = article_id
        return new_values


def delete(article_id: str):
    filter_by: Document = {}
    filter_by["_id"] = ObjectId(article_id)
    news.delete_one(filter_by)


def create(article: Article) -> str:
    result = news.insert_one(article.dict(exclude_none=True))
    return str(result.inserted_id)

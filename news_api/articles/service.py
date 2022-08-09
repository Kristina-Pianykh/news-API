from typing import MutableMapping, Union

from bson.objectid import ObjectId
from pymongo import MongoClient

from .models import Article

client = MongoClient("mongodb://127.0.0.1:27017")
db = client.local
news = db.news

Document = MutableMapping[
    str,
    Union[ObjectId, str],
]

# client.close() ?


def get_one(query_param: str) -> Union[Article, None]:  # by id, uuid, title
    filter_by: Document = {}
    try:
        filter_by["_id"] = ObjectId(query_param)
    except ValueError:
        filter_by["title"] = query_param

    result = news.find_one(filter_by)
    if result:
        article = Article(**result)
        return article
    else:
        return None


def get_many(query_param: str) -> list[Article]:  # by author
    articles: list[Article] = []
    filter_by = {"author": query_param.title()}
    results = news.find(filter_by)
    if results:
        articles = [Article(**record) for record in results]
    return articles


def update():
    raise NotImplementedError


def delete(article_id: str):  # delete by document id
    filter_by: Document = {}
    filter_by["_id"] = ObjectId(article_id)
    news.delete_one(filter_by)


def create(article: Article) -> ObjectId:
    result = news.insert_one(article.dict(exclude_none=True))
    return result.inserted_id

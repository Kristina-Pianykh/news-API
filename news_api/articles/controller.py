from typing import Any, Union

from bson.errors import InvalidId
from fastapi import APIRouter
from pydantic import ValidationError

import news_api.articles.service as service
from news_api.articles.models import Article, FutureDate, format_response

router = APIRouter(prefix="/articles")


@router.get("/article/{query_item}")  # article id, uuid or title
async def get(query_item: str):
    try:
        result: Union[Article, None] = service.get_one(query_item)
        if result:
            return format_response(result)
        else:
            message = f"no result for {query_item}"
            return message
            # TODO: proper handling of no result (if result == None)
    except (FutureDate, ValidationError) as exc:  # TODO: what exceptions to handle?
        print(str(exc))
        return str(exc)


@router.get("/articles/{query_item}")  # author
async def get_many(query_item: str):
    try:
        results: list[Article] = service.get_many(query_item)
        if results:
            return [format_response(article) for article in results]
        else:
            message = f"no result for {query_item}"
            return message
            # TODO: proper handling of no result (if result == None)
    except (FutureDate, ValidationError) as exc:  # TODO: what exceptions to handle?
        print(str(exc))
        return str(exc)


@router.post("/")
async def create_article(request_body: dict[str, Any]):
    article = Article(**request_body)
    inserted_id = service.create(article)
    if inserted_id:
        message = f"Successfuly created an article with {inserted_id}"
    else:
        message = "Failed to create an article"
    return message


@router.delete("/{article_id}")
async def delete_articles(article_id: str):
    try:
        service.delete(article_id)
        message = f"Successfuly deleted {article_id}"
    except InvalidId:
        message = f"Invalid article id {article_id}"
    return message

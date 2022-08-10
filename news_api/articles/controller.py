from typing import Any, Union

from fastapi import APIRouter

import news_api.articles.service as service
from news_api.articles.models import Article

router = APIRouter(prefix="/articles")


@router.get("/article/{query_item}", response_model=Article)  # article id or title
async def get(query_item: str):
    result: Union[Article, None] = service.get_one(query_item)
    return result


@router.get("/articles/{query_item}", response_model=list[Article])  # author
async def get_many(query_item: str):
    results: list[Article] = service.get_many(query_item)
    if results:
        return results
    else:
        message = f"no result for {query_item}"
        return message
        # TODO: proper handling of no result (if result == None)


@router.post("/")
async def create_article(request_body: dict[str, Any]) -> str:
    article = Article(**request_body)
    inserted_id = service.create(article)
    return inserted_id


@router.delete("/{article_id}")
async def delete_articles(article_id: str):
    service.delete(article_id)


@router.put("/{article_id}", response_model=Article)
async def update_articles(article_id: str, new_values: Article):
    return service.update(article_id, new_values)

from typing import Any, Union

from fastapi import APIRouter, status, Response

import news_api.articles.service as service
from news_api.articles.models import Article
from news_api.api import (
    InvalidIdError,
)  # FIXME:Error loading ASGI app. Could not import module "news_api.api".

router = APIRouter(prefix="/articles")


@router.get("/article/{query_item}", response_model=Article)  # by article id or title
async def get(query_item: str, response: Response):
    result: Union[Article, None] = service.get_one(query_item)
    if not result:
        response.status_code = status.HTTP_404_NOT_FOUND
    return result


@router.get("/articles/{author}", response_model=list[Article])
async def get_many(author: str, response: Response):
    results: list[Article] = service.get_many(author)
    if results:
        return results
    else:
        response.status_code = status.HTTP_404_NOT_FOUND


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_article(input_data: dict[str, Any]) -> str:
    inserted_id = service.create(input_data)
    return inserted_id


@router.delete("/{article_id}")
async def delete_articles(article_id: str, response: Response):
    deleted_articles = service.delete(article_id)
    if deleted_articles == 0:
        response.status_code = status.HTTP_404_NOT_FOUND
    elif deleted_articles < 0:
        raise InvalidIdError(article_id)


@router.put(
    "/{article_id}", response_model=Article, status_code=status.HTTP_201_CREATED
)
async def update_articles(article_id: str, new_values: Article, response: Response):
    result = service.update(article_id, new_values)
    if not result:
        response.status_code = status.HTTP_404_NOT_FOUND

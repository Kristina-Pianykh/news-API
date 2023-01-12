from typing import Any

from fastapi import APIRouter, HTTPException, Response, status

from .models import Article
from .service import create, delete, get_many, get_one, update

router = APIRouter(prefix="/articles")


@router.get("/id/{query_item}", response_model=Article)
async def get(query_item: str, response: Response):
    if article := get_one(query_item):
        return article
    response.status_code = status.HTTP_404_NOT_FOUND


@router.get("/title/{title}", response_model=list[Article])
async def get_many_by_title(title: str, response: Response):
    if articles := get_many(title, "title"):
        return articles
    response.status_code = status.HTTP_404_NOT_FOUND


@router.get("/author/{author}", response_model=list[Article])
async def get_many_by_author(author: str, response: Response):
    if articles := get_many(author, "author"):
        return articles
    response.status_code = status.HTTP_404_NOT_FOUND


@router.post("/", response_model=Article, status_code=status.HTTP_201_CREATED)
async def create_article(input_data: dict[str, Any]) -> Article:
    new_article = create(input_data)
    return new_article


@router.delete("/{article_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_articles(article_id: str, response: Response):
    deleted_articles = delete(article_id)
    if deleted_articles == 0:
        response.status_code = status.HTTP_404_NOT_FOUND
    elif deleted_articles < 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=f"Invalid id {article_id}"
        )


@router.put("/{article_id}", response_model=Article, status_code=status.HTTP_201_CREATED)
async def update_articles(article_id: str, new_values: Article, response: Response):
    if updated_article := update(article_id, new_values):
        return updated_article
    response.status_code = status.HTTP_404_NOT_FOUND

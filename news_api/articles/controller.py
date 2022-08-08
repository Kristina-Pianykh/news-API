from typing import Union

from fastapi import APIRouter

import news_api.articles.service as service
from news_api.articles.models import Article

router = APIRouter(prefix="/articles")


@router.get("/")
def get_many():
    return NotImplementedError


@router.get("/{query_item}")  # article id, uuid or title
async def get(query_item: str) -> Union[Article, None]:
    try:
        result: Union[Article, None] = service.get(query_item)
        if result:
            return result
        else:
            print()
            # TODO: proper handling
    except Exception:  # TODO: what exceptions to handle?
        pass

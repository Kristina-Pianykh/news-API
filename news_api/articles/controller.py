from fastapi import APIRouter

# import news_api.articles.service as service

router = APIRouter(prefix="/articles")


@router.get("/")
def get_many():
    return NotImplementedError


@router.get("/{article_id}")
def get():
    raise NotImplementedError

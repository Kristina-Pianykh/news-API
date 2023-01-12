import json
import os
from tqdm import tqdm
from faker import Faker
from .models import Article
from pymongo import MongoClient


def create_mock_json(article_count: int, fake: Faker) -> list[Article]:
    pydantic_articles: list[Article] = []
    for i in tqdm(range(article_count), desc="Creating json mock data"):
        pydantic_articles.append(
            Article(
                author=fake.name(),
                title=fake.sentence(nb_words=4).strip("."),
                text=fake.text(max_nb_chars=200),
                date=fake.date(pattern="%d-%m-%Y", end_datetime="now"),
                id=fake.uuid4(),
            )
        )
    return pydantic_articles


# connection_string = os.environ["DB_CONNECTION_STRING"]
connection_string = "mongodb://localhost:27017"
client = MongoClient(connection_string)
db = client.local
news = db.news

if __name__ == "__main__":
    article_count = 50
    fake = Faker(["en_US"])
    Faker.seed(4321)

    data = create_mock_json(article_count, fake)
    news.insert_many([article.dict() for article in data])
    print("Done")
    with open("mock_artiles.json", "w") as outfile:
        outfile.write(json.dumps([article.json() for article in data]))

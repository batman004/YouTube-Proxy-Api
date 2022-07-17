from dotenv import dotenv_values

config = dotenv_values(".env")
from pymongo import MongoClient
from ...config import settings


class DataSearchHandler:
    def __init__(self) -> None:
        mongodb_uri = config["DB_URL"]
        client = MongoClient(mongodb_uri, int(config["PORT"]))
        db = client[config["DB_NAME"]]
        self.collection_name = db.videos

    def init_db(self):
        mongodb_uri = settings.DB_URL
        client = MongoClient(mongodb_uri, int(settings.PORT))
        db = client[settings.DB_NAME]
        self.collection_name = db.videos

    def fuzzy_matching(self, search_query):
        self.init_db()
        search_result = self.collection_name.aggregate(
            [
                {
                    "$search": {
                        "index": "language_search",
                        "text": {"query": search_query, "path": "title", "fuzzy": {}},
                    }
                },
                {"$limit": 10},
            ]
        )

        return search_result

from pymongo import MongoClient
from ...config import settings


class DataSearchHandler:
    def __init__(self) -> None:
        mongodb_uri = settings.DB_URL
        client = MongoClient(mongodb_uri, int(settings.PORT))
        db = client[settings.DB_NAME]
        self.collection_name = db.videos

    def fuzzy_matching(self, search_query):

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

        print(list(search_result))

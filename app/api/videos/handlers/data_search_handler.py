from pymongo import MongoClient
from api.config import settings


class DataSearchHandler:
    def __init__(self, request) -> None:
        mongodb_uri = settings.DB_URL
        client = MongoClient(mongodb_uri, int(settings.PORT))
        db = client[settings.DB_NAME]
        self.collection_name = db.videos
        self.collection_name_async = request.app.mongodb["videos"]

    def fuzzy_matching(self, search_query, field):

        # define pipeline
        pipeline = [
            {
                "$search": {
                    "index": "title_search",
                    "autocomplete": {"query": search_query, "path": field},
                }
            },
            {"$limit": 20},
        ]
        # run pipeline
        result = self.collection_name.aggregate(pipeline)
        # print results
        return list(result)

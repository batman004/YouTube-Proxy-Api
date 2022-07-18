def get_latest_date(collection_name):
    latest_record = list(collection_name.find().sort("_id", 1).limit(1))
    for doc in latest_record:
        date = doc["publishedAt"]
    return date

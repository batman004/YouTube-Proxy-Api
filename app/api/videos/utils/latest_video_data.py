import datetime


def get_latest_date(collection_name):
    latest_record = list(collection_name.find().sort("_id", 1).limit(1))
    for doc in latest_record:
        date = doc["publishedAt"]
    return date


def get_rtc_3339():
    # getting current time in rtc 3339 format
    now_utc = datetime.datetime.now()
    now_rtc = now_utc.isoformat("T") + "Z"
    return now_rtc

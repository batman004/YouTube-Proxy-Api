from googleapiclient.discovery import build
import asyncio
import datetime
from fastapi import HTTPException
from dotenv import dotenv_values

config = dotenv_values(".env")
from pymongo import MongoClient


class YoutubeDataHelper:
    def __init__(self) -> None:
        self.mongodb_uri = config["DB_URL"]
        self.client = MongoClient(self.mongodb_uri, int(config["PORT"]))
        self.db = self.client[config["DB_NAME"]]
        self.collection_name = self.db.videos

    @staticmethod
    def get_current_time():
        # getting current time in rtc 3339 format
        now_utc = datetime.datetime.now()
        now_rtc = now_utc.isoformat("T") + "Z"
        return now_rtc

    async def get_video_data(self):
        # initialising google api client object
        # constructor takes in params : api name, version and apiKey
        youtube_obj = build("youtube", "v3", developerKey=self.YOUTUBE_API_AUTH)

        # Gives out results based on newest first approach
        query = youtube_obj.search().list(
            part="snippet",
            q="football",
            type="video",
            order="date",
            publishedAfter=self.get_current_time(),
            maxResults=5,
        )

        res = query.execute()
        items = res["items"]

        return items

    # async function to insert records queried from Youtube API into DB
    async def insert_in_db(self):
        cnt = 0
        # adding data to db at an interval of 10 sec
        while True:
            try:
                videos = self.get_data()
                # traverses through latest video data of 5 entries
                for vid in videos:

                    VId = vid["id"]["videoId"]
                    video = vid["snippet"]  # obj for each individual video
                    video["_id"] = VId

                    # adding new video to db if it does not already exist
                    if (
                        self.collection_name["videos"].find_one({"_id": VId})
                    ) is not None:
                        print("Video already in DB !")

                    else:
                        new_video = self.collection_name.insert_one(video)
                        print(f"video titled :{video['title']} added")

            except Exception as e:
                print(e)
                print("Not added to DB ", "\n")

            # creating interval of 10 sec
            print("sleeping for 10 secs", "\n")
            await asyncio.sleep(10)
            cnt = cnt + 1

            # loop utility counter for api rate-limiting
            if cnt > 3:
                break

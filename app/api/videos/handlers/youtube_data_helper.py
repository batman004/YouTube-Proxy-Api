from googleapiclient.discovery import build
import asyncio
import datetime
from pymongo import MongoClient
from ...config import settings
from ..utils.latest_video_data import get_latest_date


class YoutubeDataHelper:
    def __init__(self, request: None) -> None:
        self.YOUTUBE_API_AUTH = settings.YOUTUBE_API_TOKEN
        self.collection_name_async = request.app.mongodb["videos"]
        self.collection_name = None

    def pymongo_db_init(self):
        mongodb_uri = settings.DB_URL
        client = MongoClient(mongodb_uri, int(settings.PORT))
        db = client[settings.DB_NAME]
        self.collection_name = db.videos

    def is_db_empty(self):
        query = self.collection_name.find()
        if not query:
            return True
        return False

    def get_current_time(self):
        self.pymongo_db_init()
        if self.is_db_empty():
            # getting current time in rtc 3339 format
            now_utc = datetime.datetime.now()
            now_rtc = now_utc.isoformat("T") + "Z"
            return now_rtc
        # check date for latest video added in db
        else:
            latest_date = get_latest_date(self.collection_name)
            return latest_date

    def get_video_data(self, keyword):
        # initialising google api client object
        # constructor takes in params : api name, version and apiKey
        youtube_obj = build("youtube", "v3", developerKey=self.YOUTUBE_API_AUTH)

        # Gives out results based on newest first approach
        query = youtube_obj.search().list(
            part="snippet",
            q=keyword,
            type="video",
            order="date",
            publishedAfter=self.get_current_time(),
            maxResults=5,
        )

        res = query.execute()
        items = res["items"]

        return items

    async def get_all_video_data(self):
        videos = []
        for doc in await self.collection_name_async.find().to_list(length=50):
            videos.append(doc)

        # sorting list in descending order
        videos = videos[::-1]
        return videos

    # async function to insert records queried from Youtube API into DB
    async def insert_in_db(self, keyword, iterations):
        cnt = 0
        response = {}
        # adding data to db at an interval of 10 sec
        while True:
            try:
                videos = self.get_video_data(keyword)
                # traverses through latest video data of 5 entries
                for vid in videos:

                    VId = vid["id"]["videoId"]
                    video = vid["snippet"]  # obj for each individual video
                    video["_id"] = VId

                    # adding new video to db if it does not already exist
                    if (
                        await self.collection_name_async.find_one({"_id": VId})
                    ) is not None:
                        response[video["title"]] = "already in DB"
                        print("Video already in DB !")

                    else:
                        new_video = await self.collection_name_async.insert_one(video)
                        print(f"video titled :{video['title']} added")
                        response[video["title"]] = "added"

            except Exception as e:
                print(e)
                print("Not added to DB ", "\n")

            # creating interval of 10 sec
            print("sleeping for 10 secs", "\n")
            await asyncio.sleep(10)
            cnt = cnt + 1

            # loop utility counter for api rate-limiting
            if cnt > iterations - 1:
                break
        return response

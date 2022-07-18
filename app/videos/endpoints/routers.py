from fastapi import APIRouter, Request, HTTPException
from fastapi_pagination import Page, paginate
from ..handlers.youtube_data_helper import YoutubeDataHelper
from ..handlers.data_search_handler import DataSearchHandler
from ..endpoints.models import VideoData

# router object for handling api routes
router = APIRouter()


@router.post("/", response_description="Add videos")
async def add_videos(keyword: str, iterations: int):
    # adding data to db
    try:
        response = await YoutubeDataHelper().insert_in_db(keyword, iterations)
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Exception : {e}")


# get videos from db ordered by time of upload
@router.get("/", response_description="List all videos", response_model=Page[VideoData])
async def list_all_videos(request: Request):
    videos = []
    for doc in await request.app.mongodb["videos"].find().to_list(length=50):
        videos.append(doc)

    # sorting list in descending order
    videos = videos[::-1]
    return paginate(videos)


# search videos from db based on title
@router.get("/search/{title}", response_description="List all videos based on search")
async def search(title: str):
    try:
        search_results = DataSearchHandler().fuzzy_matching(title)
        return search_results
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Exception : {e}")

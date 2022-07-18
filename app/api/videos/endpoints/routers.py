from fastapi import APIRouter, Request, HTTPException
from fastapi_pagination import Page, paginate
from ..handlers.youtube_data_helper import YoutubeDataHelper
from ..handlers.data_search_handler import DataSearchHandler
from ..endpoints.models import VideoData

# router object for handling api routes
router = APIRouter()


@router.post("/", response_description="Add videos")
async def add_videos(keyword: str, iterations: int, request: Request):
    # adding data to db
    try:
        response = await YoutubeDataHelper(request).insert_in_db(keyword, iterations)
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Exception : {e}")


# get videos from db ordered by time of upload
@router.get("/", response_description="List all videos", response_model=Page[VideoData])
async def list_all_videos(request: Request):
    try:
        videos = await YoutubeDataHelper(request).get_all_video_data()
        return paginate(videos)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Exception : {e}")


# search videos from db based on title
@router.get(
    "/search/{title}",
    response_description="List all videos based on search",
    response_model=Page[VideoData],
)
async def search(title: str, request: Request):
    data_search_handler = DataSearchHandler(request)
    try:
        search_results = data_search_handler.fuzzy_matching(title)
        return paginate(search_results)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Exception : {e}")

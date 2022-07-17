from fastapi import APIRouter, Request, HTTPException
from ..handlers.youtube_data_helper import YoutubeDataHelper
from ..handlers.data_search_handler import DataSearchHandler

# router object for handling api routes
router = APIRouter()


@router.post("/", response_description="Add videos")
async def add_videos(request: Request):
    # adding data to db
    try:
        response = await YoutubeDataHelper().insert_in_db()
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Exception : {e}")


# get videos from db ordered by time of upload
@router.get("/", response_description="List all videos")
async def list_all_videos(request: Request):
    videos = []
    for doc in await request.app.mongodb["videos"].find().to_list(length=100):
        videos.append(doc)

    # sorting list in descending order
    videos = videos[::-1]
    return videos


# search videos from db based on title
@router.get("/search/{title}", response_description="List all videos based on search")
async def search(title: str, request: Request):
    try:
        search_results = DataSearchHandler().fuzzy_matching(title)
        return search_results
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Exception : {e}")

from fastapi import APIRouter, Request

# router object for handling api routes
router = APIRouter()


@router.post("/", response_description="Add videos")
async def add_videos(request: Request):
    # adding data to db
    pass


# get videos from db ordered by time of upload
@router.get("/", response_description="List all videos")
async def list_all_videos(request: Request):
    pass


# search videos from db based on title
@router.get("/search/{title}", response_description="List all videos based on search")
async def search(title: str, request: Request):
    pass

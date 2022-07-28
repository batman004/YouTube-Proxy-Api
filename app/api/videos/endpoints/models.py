from pydantic import BaseModel


class VideoData(BaseModel):
    _id: int
    publishedAt: str
    channelId: str
    title: str
    description: str
    thumbnails: dict
    channelTitle: str
    liveBroadcastContent: str
    publishTime: str

    class Config:
        orm_mode = True

### Tech Stack
 - Python(FastAPI)
 - MongoDB cloud Atlas

### Directory Structure
```
.
├── LICENSE
├── README.md
├── app
│   ├── Dockerfile
│   ├── __init__.py
│   ├── api
│   │   ├── __init__.py
│   │   ├── config.py
│   │   └── videos
│   │       ├── __init__.py
│   │       ├── auth
│   │       │   ├── __init__.py
│   │       │   └── auth_helper.py
│   │       ├── endpoints
│   │       │   ├── __init__.py
│   │       │   ├── models.py
│   │       │   └── routers.py
│   │       ├── handlers
│   │       │   ├── __init__.py
│   │       │   ├── data_search_handler.py
│   │       │   └── youtube_data_helper.py
│   │       └── utils
│   │           └── latest_video_data.py
│   ├── main.py
│   └── requirements.txt
├── fampay.postman_collection.json
└── run.sh

```
### Database Schema

#### video
```
    _id: int
    publishedAt: str
    channelId: str
    title: str
    description: str
    thumbnails: dict
    channelTitle: str
    liveBroadcastContent: str
    publishTime: str

    "example":{

          "_id": "wqjq2m1EQy8",
          "publishedAt": "2022-07-17T04:39:58Z",
          "channelId": "UCyrHueZqBqzCPizy4qYIV5A",
          "title": "LOOK at these INSANE DRIBBLES 🥶🥶🔥#shorts  #football",
          "description": "Make Money watching youtube videos - https://youtu.be/CnLweYfBKeY funniest football youtube channel ...",
          "thumbnails": {
            "default": {
              "url": "https://i.ytimg.com/vi/wqjq2m1EQy8/default.jpg",
              "width": 120,
              "height": 90
            },
            "medium": {
              "url": "https://i.ytimg.com/vi/wqjq2m1EQy8/mqdefault.jpg",
              "width": 320,
              "height": 180
            },
            "high": {
              "url": "https://i.ytimg.com/vi/wqjq2m1EQy8/hqdefault.jpg",
              "width": 480,
              "height": 360
            }
          },
          "channelTitle": "Skill District",
          "liveBroadcastContent": "none",
          "publishTime": "2022-07-17T04:39:58Z"
      }
```
### API Routes


#### `videos` Module

Routes | HTTP | Description
--- | --- | ---
**/video/** | `GET` | Get all videos
**/video/search/{title}** | `GET` | Get video data based on title
**/video/search/{description}** | `GET` | Get video data based on description
**/video/** | `POST` | add videos to DB

### Steps to run

Open terminal and run the following commands
```
git clone https://github.com/batman004/YouTube-Proxy-Api
cd YouTube-Proxy-Api
```

add a `.env` file inside `./app` (refer .env.example)
```
#fill in credentials :
    DB_URL=
    DB_NAME=
    PORT=
    API_KEY=
```

setting up a databse


- Create an Atlas account. Register for an Atlas account using your Google Account or an email address.
- Deploy a free cluster.
- Add your connection IP address to your IP access list.
- Create a database user for your cluster.
- Connect to your cluster via the DB URI provided (refer [Docs](https://www.mongodb.com/docs/atlas/tutorial/connect-to-your-cluster/))


run the `run.sh` script to Dockerize the project and run it
```
sh run.sh
```

The server will start running at `port:80`


Sample payloads

> :warning: **Current limit is set to 5 requests/api-key**

1. Getting the API-KEY

```
curl --location --request GET 'localhost:80/api-key'
```

2. Adding Videos to the DB

```
curl --location --request POST 'localhost:80/video?keyword=football&iterations=2' \
--header 'Authorization: Bearer {{token}}'

```
3. Fetching video data from DB

```
curl --location --request GET 'localhost:80/video?page=1&size=3' \
--header 'Authorization: Bearer {{token}}'

```
4. Searching based on video title

```
curl --location --request GET 'localhost:80/video/search/football/?page=1&size=10' \
--header 'Authorization: Bearer {{token}}'
```

5. Search based on video description
```
curl --location --request GET 'localhost:80/video/search/football and messi/?page=1&size=10' \
--header 'Authorization: Bearer {{token}}'
```

### Available Features 🍻


- [x] Add data to DB in async manner after recieving interval and keyword from user
- [x] API Key support to authenticate user and limit calls 🔐
- [x] View all entries with pagination settings available 🗒️
- [x] Fuzzy search based on title and description of video ✍️

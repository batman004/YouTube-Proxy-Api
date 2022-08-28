cd app
docker build --tag=youtube-proxy-api .
docker run --env-file .env --rm -it --name yt-api -p 80:80 youtube-proxy-api

cd app
docker build --tag=youtube-proxy-api .
docker run --env-file .env --rm -it --name fampay-assignment -p 80:80 youtube-proxy-api

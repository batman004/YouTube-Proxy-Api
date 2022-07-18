docker build --tag=youtube-proxy-api .
docker run --env-file ./app/.env --rm -it --name fampay-assignment -p 80:80 youtube-proxy-api

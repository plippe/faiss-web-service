# Faiss Web Service

### Getting started
The fastest way to get started is to run the following commands:
```sh
# Create a docker image for the faiss service
docker build -t faiss:d3c8456 github.com/facebookresearch/faiss#d3c8456

# Create a docker image for the faiss web service
docker build -t faiss-web-service:7ad970c github.com/Plippe/faiss-web-service#7ad970c

# Run a docker container
docker run --rm --detach --publish 5000:5000 faiss-web-service:7ad970c
```

Once the container is running, you should be able to ping the service:
```sh
# Healthcheck
curl "localhost:5000/ping"

# Faiss search for id 1, 3, and 3
curl "localhost:5000/faiss?k=5&ids=1&ids=2&ids=3"
```

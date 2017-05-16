# Faiss Web Service

### Getting started
The fastest way to get started is to use
[the docker hub image](https://hub.docker.com/r/plippe/faiss-web-service/) with the following
command:
```sh
docker run --rm --detach --publish 5000:5000 plippe/faiss-web-service
```

Once the container is running, you should be able to ping the service:
```sh
# Healthcheck
curl "localhost:5000/ping"

# Faiss search for id 1, 2, and 3
curl "localhost:5000/faiss?k=5&ids=1&ids=2&ids=3"
```

### Custom config
By default, the faiss web service will load a local file for the faiss index, and for the ids to
vectors mapping. This behavior can be overwritten by writting your own configuration file, and
having its path as an environment variable `FAISS_WEB_SERVICE_CONFIG`.

```sh
docker run \
    --rm \
    --detach \
    --publish 5000:5000 \
    --volume [PATH_TO_YOUR_CONFIG]:/tmp/your_config.py \
    --env FAISS_WEB_SERVICE_CONFIG=/tmp/your_config.py \
    plippe/faiss-web-service
```

Examples of how to write a config file can be found in the
[faiss_web_service_config](https://github.com/Plippe/faiss-web-service/tree/master/faiss_web_service_config)
folder.

Another solution would be to create a new docker image
[from `plippe/faiss-web-service`](https://docs.docker.com/engine/reference/builder/#from),
that [sets the environement variable](https://docs.docker.com/engine/reference/builder/#env),
and [adds your config file](https://docs.docker.com/engine/reference/builder/#add).

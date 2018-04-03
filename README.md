# Faiss Web Service

### Getting started
The fastest way to get started is to use [the docker hub image](https://hub.docker.com/r/plippe/faiss-web-service/) with the following command:
```sh
docker run --rm --detach --publish 5000:5000 plippe/faiss-web-service
```

Once the container is running, you should be able to ping the service:
```sh
# Healthcheck
curl 'localhost:5000/ping'

# Faiss search for ids 1, 2, and 3
curl 'localhost:5000/faiss/search' -X POST -d '{"k": 5, "ids": [1, 2, 3]}'

# Faiss search for a vector
curl 'localhost:5000/faiss/search' -X POST -d '{"k": 5, "vectors": [[54.7, 0.3, 0.6, 0.4, 0.1, 0.7, 0.2, 0.0, 0.6, 0.5, 0.3, 0.2, 0.1, 0.9, 0.3, 0.6, 0.2, 0.9, 0.5, 0.0, 0.9, 0.1, 0.9, 0.1, 0.5, 0.5, 0.8, 0.8, 0.5, 0.2, 0.6, 0.2, 0.2, 0.7, 0.1, 0.7, 0.8, 0.2, 0.9, 0.0, 0.4, 0.4, 0.9, 0.0, 0.6, 0.4, 0.4, 0.6, 0.6, 0.2, 0.5, 0.0, 0.1, 0.6, 0.0, 0.0, 0.4, 0.7, 0.5, 0.7, 0.2, 0.5, 0.5, 0.7]]}'
```

### Custom config
By default, the faiss web service will download files for the faiss index, and for the ids to vectors mapping. This behavior can be overwritten by writting your own configuration file, and having its path as an environment variable `FAISS_WEB_SERVICE_CONFIG`.

```sh
docker run \
    --rm \
    --tty \
    --interactive \
    --publish 5000:5000 \
    --volume [PATH_TO_YOUR_CONFIG]:/tmp/your_config.py \
    --env FAISS_WEB_SERVICE_CONFIG=/tmp/your_config.py \
    plippe/faiss-web-service
```

Examples of how to write a config file can be found in the [resources](https://github.com/Plippe/faiss-web-service/tree/master/resources) folder.

Another solution would be to create a new docker image [from `plippe/faiss-web-service`](https://docs.docker.com/engine/reference/builder/#from), that [sets the environement variable](https://docs.docker.com/engine/reference/builder/#env), and [adds your config file](https://docs.docker.com/engine/reference/builder/#add).


### Production
`docker run` will run the application with Flask's build in server. Flask's documentation clearly states [it is not suitable for production](http://flask.pocoo.org/docs/0.12/deploying/). To run the application with `uWSGI` you must add `production` to the `run` command, i.e:

```sh
# Flask's build in server
docker run --rm --detach --publish 5000:5000 plippe/faiss-web-service

# uWSGI server
docker run --rm --detach --publish 5000:5000 plippe/faiss-web-service production
```

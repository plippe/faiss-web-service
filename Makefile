.PHONY: build run

FAISS_COMMIT := d3c8456
COMMIT := $(shell git describe --dirty --always)

ifneq (, $(shell which nvidia-docker > /dev/null))
DOCKER_CMD := nvidia-docker
else
DOCKER_CMD := docker
endif

build:
ifeq (,$(shell ${DOCKER_CMD} images -q faiss:${FAISS_COMMIT} 2> /dev/null))
	@echo Failed to find docker image faiss:${FAISS_COMMIT}
	@echo Building docker image faiss:${FAISS_COMMIT}
	${DOCKER_CMD} build -t faiss:${FAISS_COMMIT} github.com/facebookresearch/faiss\#${FAISS_COMMIT}
endif

	# ${DOCKER_CMD} build -t faiss-web-service --build-arg FAISS_COMMIT=${FAISS_COMMIT} .
	${DOCKER_CMD} build -t faiss-web-service:${COMMIT} .

run: build
	${DOCKER_CMD} run \
		--rm \
		--detach \
		--publish 5000:5000 \
		faiss-web-service:${COMMIT}

push: build
	${DOCKER_CMD} tag faiss:${FAISS_COMMIT} plippe/faiss:${FAISS_COMMIT}
	${DOCKER_CMD} push plippe/faiss:${FAISS_COMMIT}

	${DOCKER_CMD} tag faiss-web-service:${COMMIT} plippe/faiss-web-service:${COMMIT}
	${DOCKER_CMD} push plippe/faiss-web-service:${COMMIT}

sandbox: build
	${DOCKER_CMD} run \
		--rm \
		--publish 5000:5000 \
		--tty \
		--interactive \
		--volume ${PWD}:/opt/faiss-web-service \
		--entrypoint bash \
		faiss-web-service

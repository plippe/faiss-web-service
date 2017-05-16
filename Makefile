.PHONY: build run

FAISS_COMMIT := d3c8456
COMMIT := $(shell git describe --dirty --always)

ifneq (, $(shell which nvidia-docker > /dev/null))
DOCKER_CMD := nvidia-docker
else
DOCKER_CMD := docker
endif

build:
ifeq (,$(shell ${DOCKER_CMD} images -q plippe/faiss:${FAISS_COMMIT} 2> /dev/null))
	@echo Failed to find docker image plippe/faiss:${FAISS_COMMIT}
	@echo Building docker image plippe/faiss:${FAISS_COMMIT}
	${DOCKER_CMD} build -t plippe/faiss:${FAISS_COMMIT} github.com/facebookresearch/faiss\#${FAISS_COMMIT}
endif

	# https://github.com/moby/moby/pull/31352
	# ${DOCKER_CMD} build -t plippe/faiss-web-service --build-arg FAISS_COMMIT=${FAISS_COMMIT} .
	${DOCKER_CMD} build -t plippe/faiss-web-service:${COMMIT} .

run: build
	${DOCKER_CMD} run \
		--rm \
		--detach \
		--publish 5000:5000 \
		plippe/faiss-web-service:${COMMIT}

push: build
	${DOCKER_CMD} push plippe/faiss:${FAISS_COMMIT}
	${DOCKER_CMD} push plippe/faiss-web-service:${COMMIT}

sandbox: build
	${DOCKER_CMD} run \
		--rm \
		--publish 5000:5000 \
		--tty \
		--interactive \
		--volume ${PWD}:/opt/faiss-web-service \
		--entrypoint bash \
		plippe/faiss-web-service

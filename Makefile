.PHONY: build run push sandbox

COMMIT := $(shell git describe --dirty --always)
FAISS_COMMIT := $(shell curl -s https://api.github.com/repos/facebookresearch/faiss/git/refs?per_page=1 | \
	grep -o '"sha": ".\{7\}' | \
	cut -d'"' -f4)

ifneq (, $(shell which nvidia-docker > /dev/null))
DOCKER_CMD := nvidia-docker
else
DOCKER_CMD := docker
endif

build:
ifeq (,$(shell ${DOCKER_CMD} images -q plippe/faiss:${FAISS_COMMIT} 2> /dev/null))
	@echo Failed to find docker image plippe/faiss:${FAISS_COMMIT}
	@echo Building docker image plippe/faiss:${FAISS_COMMIT}
	${DOCKER_CMD} build \
		-t plippe/faiss \
		-t plippe/faiss:${FAISS_COMMIT} \
		github.com/facebookresearch/faiss
endif

	${DOCKER_CMD} build \
		-t plippe/faiss-web-service \
		-t plippe/faiss-web-service:${COMMIT} \
		--build-arg FAISS_COMMIT=${FAISS_COMMIT} .

push: build
ifneq (,$(findstring dirty,${COMMIT}))
	@echo Docker push cancelled, repository dirty
else
	${DOCKER_CMD} push plippe/faiss:${FAISS_COMMIT}
	${DOCKER_CMD} push plippe/faiss-web-service:${COMMIT}
endif

run = ${DOCKER_CMD} run \
	--rm \
	--tty \
	--interactive \
	--publish 5000:5000 \
	${2} \
	plippe/faiss-web-service:${COMMIT} ${1}

prod: build
	$(call run,production)

dev: build
	$(call run,development,--volume ${PWD}:/opt/faiss-web-service)

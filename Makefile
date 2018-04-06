.PHONY: build run test release
.DEFAULT_GOAL := build

DOCKER_IMAGE := plippe/faiss-web-service
DOCKER_TAG := $(shell git describe --dirty --always)

build:
	docker build \
		--build-arg IMAGE=plippe/faiss-docker:1.2.1-cpu \
		--tag $(DOCKER_IMAGE) \
		--tag $(DOCKER_IMAGE):$(DOCKER_TAG)-cpu .

	docker build \
		--build-arg IMAGE=plippe/faiss-docker:1.2.1-gpu \
		--tag $(DOCKER_IMAGE):$(DOCKER_TAG)-gpu .

run: run-development
run-%:
	docker run \
		--rm \
		--tty \
		--interactive \
		--volume $(PWD):/opt/faiss-web-service \
		--publish 5000:5000 \
		$(DOCKER_IMAGE):$(DOCKER_TAG)-cpu $*

test:
	docker run \
		--rm \
		--tty \
		--interactive \
		--volume $(PWD):/opt/faiss-web-service \
		--entrypoint bash \
		$(DOCKER_IMAGE):$(DOCKER_TAG)-cpu -c "python -m unittest discover"

release:
ifneq ($(findstring dirty,$(DOCKER_TAG)),)
	$(error Release cancelled, repository dirty)
endif

	docker push $(DOCKER_IMAGE)
	docker push $(DOCKER_IMAGE):$(DOCKER_TAG)-cpu
	docker push $(DOCKER_IMAGE):$(DOCKER_TAG)-gpu

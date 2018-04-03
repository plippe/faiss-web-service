.PHONY: build run test release
.DEFAULT_GOAL := build

DOCKER_IMAGE := plippe/faiss-web-service
DOCKER_TAG := $(shell git describe --dirty --always)

build:
	docker build \
		--tag $(DOCKER_IMAGE) \
		--tag $(DOCKER_IMAGE):cpu \
		--tag $(DOCKER_IMAGE):cpu-$(DOCKER_TAG) .

	docker build \
		--build-arg IMAGE=nvidia/cuda:8.0-runtime-ubuntu16.04 \
		--build-arg VERSION=gpu \
		--tag $(DOCKER_IMAGE):gpu \
		--tag $(DOCKER_IMAGE):gpu-$(DOCKER_TAG) .

run: run-development
run-%:
	docker run \
		--rm \
		--tty \
		--interactive \
		--volume $(PWD):/opt/faiss-web-service \
		--publish 5000:5000 \
		$(DOCKER_IMAGE):cpu-$(DOCKER_TAG) $*

test:
	docker run \
		--rm \
		--tty \
		--interactive \
		--volume $(PWD):/opt/faiss-web-service \
		--entrypoint bash \
		$(DOCKER_IMAGE):cpu-$(DOCKER_TAG) -c "python -m unittest discover"

release:
ifneq ($(findstring dirty,$(DOCKER_TAG)),)
	$(error Release cancelled, repository dirty)
endif

	docker push $(DOCKER_IMAGE)
	docker push $(DOCKER_IMAGE):cpu
	docker push $(DOCKER_IMAGE):cpu-$(DOCKER_TAG)

	docker push $(DOCKER_IMAGE):gpu
	docker push $(DOCKER_IMAGE):gpu-$(DOCKER_TAG)

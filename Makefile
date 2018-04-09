.PHONY: build run test release
.DEFAULT_GOAL := build

FAISS_VERSION := $(shell curl -s https://api.github.com/repos/facebookresearch/faiss/releases/latest | jq -r .tag_name | cut -c2-)
VERSION := $(shell git describe --dirty --always)

DOCKER_IMAGE := plippe/faiss-web-service
DOCKER_TAG := $(shell git describe --dirty --always)

build:
	docker build \
		--build-arg IMAGE=plippe/faiss-docker:1.2.1-cpu \
		--tag $(DOCKER_IMAGE):$(FAISS_VERSION)-cpu \
		--tag $(DOCKER_IMAGE):$(FAISS_VERSION)-cpu-$(VERSION) .

	docker build \
		--build-arg IMAGE=plippe/faiss-docker:1.2.1-gpu \
		--tag $(DOCKER_IMAGE):$(FAISS_VERSION)-gpu \
		--tag $(DOCKER_IMAGE):$(FAISS_VERSION)-gpu-$(VERSION) .

run: run-development
run-%:
	docker run \
		--rm \
		--tty \
		--interactive \
		--volume $(PWD):/opt/faiss-web-service \
		--publish 5000:5000 \
		$(DOCKER_IMAGE):$(FAISS_VERSION)-cpu $*

test:
	docker run \
		--rm \
		--tty \
		--interactive \
		--volume $(PWD):/opt/faiss-web-service \
		--entrypoint bash \
		$(DOCKER_IMAGE):$(FAISS_VERSION)-cpu -c "python -m unittest discover"

release:
	docker push $(DOCKER_IMAGE):$(FAISS_VERSION)-cpu
	docker push $(DOCKER_IMAGE):$(FAISS_VERSION)-cpu-$(VERSION)
	docker push $(DOCKER_IMAGE):$(FAISS_VERSION)-gpu
	docker push $(DOCKER_IMAGE):$(FAISS_VERSION)-gpu-$(VERSION)

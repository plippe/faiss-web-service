.PHONY: build run test release
.DEFAULT_GOAL := build

DOCKER_IMAGE := plippe/faiss-web-service
FAISS_VERSION := $(shell curl -s https://api.github.com/repos/facebookresearch/faiss/releases/latest | jq -r .tag_name | cut -c2-)

build:
	docker build \
		--build-arg IMAGE=plippe/faiss-docker:1.2.1-cpu \
		--tag $(DOCKER_IMAGE):$(FAISS_VERSION)-cpu \
		--tag $(DOCKER_IMAGE):latest .

	docker build \
		--build-arg IMAGE=plippe/faiss-docker:1.2.1-gpu \
		--tag $(DOCKER_IMAGE):$(FAISS_VERSION)-gpu .

run: run-development
run-%:
	docker run \
		--rm \
		--tty \
		--interactive \
		--volume $(PWD):/opt/faiss-web-service \
		--publish 5000:5000 \
		$(DOCKER_IMAGE) $*

test:
	docker run \
		--rm \
		--tty \
		--interactive \
		--volume $(PWD):/opt/faiss-web-service \
		--entrypoint bash \
		$(DOCKER_IMAGE) -c "python -m unittest discover"

release:
	docker push $(DOCKER_IMAGE)
	docker push $(DOCKER_IMAGE):$(FAISS_VERSION)-cpu
	docker push $(DOCKER_IMAGE):$(FAISS_VERSION)-gpu

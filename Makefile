.PHONY: build run publish
.DEFAULT_GOAL := build

DOCKER_IMAGE := plippe/faiss-web-service
DOCKER_TAG := $(shell git describe --dirty --always)

build:
	docker build \
		--tag $(DOCKER_IMAGE) \
		--tag $(DOCKER_IMAGE):$(DOCKER_TAG) .

run: run-development
run-%:
	docker run \
		--rm \
		--tty \
		--interactive \
		--publish 5000:5000 \
		--volume $(PWD):/opt/faiss-web-service \
		$(DOCKER_IMAGE):$(DOCKER_TAG) $*

publish:
ifneq ($(findstring dirty,$(VERSION)),)
	$(error Docker push cancelled, repository dirty)
endif

	docker push $(DOCKER_IMAGE):$(DOCKER_VERSION)

.PHONY: build release run
.DEFAULT_GOAL := build

# https://github.com/facebookresearch/faiss/tags
FAISS_RELEASE := 1.5.2

build:
	docker build \
		--build-arg FAISS_RELEASE=$(FAISS_RELEASE) \
		--tag plippe/faiss-web-service:$(FAISS_RELEASE) \
		.

release:
	docker push plippe/faiss-web-service:$(FAISS_RELEASE)

run:
	docker run \
		--rm \
		--interactive \
		--tty \
		--publish 5000:5000 \
		plippe/faiss-web-service:$(FAISS_RELEASE)

test:
	curl localhost:5000/ping
	curl localhost:5000/faiss/search -d '{"k": 5, "ids": [1, 2, 3]}'
	curl localhost:5000/faiss/search -d '{"k": 5, "vectors": [[54.7, 0.3, 0.6, 0.4, 0.1, 0.7, 0.2, 0.0, 0.6, 0.5, 0.3, 0.2, 0.1, 0.9, 0.3, 0.6, 0.2, 0.9, 0.5, 0.0, 0.9, 0.1, 0.9, 0.1, 0.5, 0.5, 0.8, 0.8, 0.5, 0.2, 0.6, 0.2, 0.2, 0.7, 0.1, 0.7, 0.8, 0.2, 0.9, 0.0, 0.4, 0.4, 0.9, 0.0, 0.6, 0.4, 0.4, 0.6, 0.6, 0.2, 0.5, 0.0, 0.1, 0.6, 0.0, 0.0, 0.4, 0.7, 0.5, 0.7, 0.2, 0.5, 0.5, 0.7]]}'

.PHONY: build release run test
.DEFAULT_GOAL := build

# https://github.com/facebookresearch/faiss/tags
FAISS_RELEASE := latest
EXTERNAL_PORT := 9001

build:
	docker build \
		--build-arg FAISS_RELEASE \
		--tag 123wowow123/faiss-web-service:$(FAISS_RELEASE) \
		.

release:
	docker push 123wowow123/faiss-web-service:$(FAISS_RELEASE)

run:
	docker run \
		--rm \
		--interactive \
		--tty \
		--publish $(EXTERNAL_PORT):5000 \
		123wowow123/faiss-web-service:$(FAISS_RELEASE)

test:
	curl localhost:$(EXTERNAL_PORT)/ping
	curl localhost:$(EXTERNAL_PORT)/faiss/search -d '{"k": 5, "ids": [1, 2, 3]}'
	curl localhost:$(EXTERNAL_PORT)/faiss/search -d '{"k": 5, "vectors": [[54.7, 0.3, 0.6, 0.4, 0.1, 0.7, 0.2, 0.0, 0.6, 0.5, 0.3, 0.2, 0.1, 0.9, 0.3, 0.6, 0.2, 0.9, 0.5, 0.0, 0.9, 0.1, 0.9, 0.1, 0.5, 0.5, 0.8, 0.8, 0.5, 0.2, 0.6, 0.2, 0.2, 0.7, 0.1, 0.7, 0.8, 0.2, 0.9, 0.0, 0.4, 0.4, 0.9, 0.0, 0.6, 0.4, 0.4, 0.6, 0.6, 0.2, 0.5, 0.0, 0.1, 0.6, 0.0, 0.0, 0.4, 0.7, 0.5, 0.7, 0.2, 0.5, 0.5, 0.7]]}'

ARG IMAGE
FROM ${IMAGE}

COPY requirements.txt /opt/faiss-web-service/requirements.txt
RUN conda install -y -c conda-forge --file /opt/faiss-web-service/requirements.txt

COPY bin /opt/faiss-web-service/bin
COPY src /opt/faiss-web-service/src
COPY resources /opt/faiss-web-service/resources

WORKDIR /opt/faiss-web-service

ENTRYPOINT ["/opt/faiss-web-service/bin/faiss_web_service.sh"]

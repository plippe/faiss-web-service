ARG FAISS_RELEASE
FROM plippe/faiss-docker:${FAISS_RELEASE}

RUN cd /opt/faiss/python && \
  make install && \
  yum install -y epel-release && \
  yum install -y python-pip && \
  pip install --upgrade pip && \
  pip install Flask==1.1.1 jsonschema==3.2.0

COPY resources /opt/faiss-web-service/resources
COPY src /opt/faiss-web-service/src

ENTRYPOINT ["python", "/opt/faiss-web-service/src/app.py"]

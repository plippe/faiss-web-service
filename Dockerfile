ARG FAISS_COMMIT
FROM plippe/faiss:${FAISS_COMMIT}

ENV PYTHONPATH=/opt/faiss

COPY requirements.txt /opt/faiss-web-service/requirements.txt

RUN pip install --upgrade pip && \
    pip install --requirement /opt/faiss-web-service/requirements.txt

COPY . /opt/faiss-web-service

ENTRYPOINT ["/opt/faiss-web-service/bin/faiss_web_service.sh"]

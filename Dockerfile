# https://github.com/moby/moby/pull/31352
# ARG FAISS_COMMIT
# FROM faiss:${FAISS_COMMIT}

FROM faiss:d3c8456

ENV PYTHONPATH=/opt/faiss

COPY requirements.txt /opt/faiss-web-service/requirements.txt

RUN pip install --upgrade pip && \
    pip install --requirement /opt/faiss-web-service/requirements.txt

COPY . /opt/faiss-web-service

ENTRYPOINT python /opt/faiss-web-service/faiss_web_service/app.py

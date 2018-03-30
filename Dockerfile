FROM debian

COPY requirements.txt /opt/faiss-web-service/requirements.txt

RUN apt-get update && \
    apt-get install -y curl bzip2  && \
    curl https://repo.continuum.io/miniconda/Miniconda2-latest-Linux-x86_64.sh > /tmp/conda.sh && \
    bash /tmp/conda.sh -b -p /opt/conda && \
    /opt/conda/bin/conda update -n base conda && \
    /opt/conda/bin/conda install -y -c pytorch faiss-cpu && \
    /opt/conda/bin/conda install -y -c conda-forge --file /opt/faiss-web-service/requirements.txt && \
    apt-get remove -y --auto-remove curl bzip2 && \
    apt-get clean && \
    rm -fr /tmp/conda.sh

ENV PATH="/opt/conda/bin:${PATH}"

COPY . /opt/faiss-web-service

ENTRYPOINT ["/opt/faiss-web-service/bin/faiss_web_service.sh"]

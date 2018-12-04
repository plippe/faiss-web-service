#!/bin/sh

ROOT=$(realpath $(dirname ${0})/..)

export FAISS_WEB_SERVICE_CONFIG=${FAISS_WEB_SERVICE_CONFIG:-${ROOT}/src/utils/faiss_index_local_file.py}

development () {
  python ${ROOT}/src/app.py
}

production () {
    mkdir -p /var/log/faiss_web_service

    uwsgi \
        --http :5000 \
        --chdir ${ROOT}/src \
        --module app:app \
        --master \
        --processes 4 \
        --threads 2 \
        --metric-dir /var/log/faiss_web_service \
        --logto /var/log/faiss_web_service/app.log
}

case "${1}" in
   "production") production ;;
   *) development ;;
esac

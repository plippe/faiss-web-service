#!/bin/sh

ROOT=$(realpath $(dirname ${0})/..)
export FAISS_WEB_SERVICE_CONFIG=${ROOT}/faiss_web_service_config/faiss_index_local_file.py

development () {
  python ${ROOT}/faiss_web_service/app.py
}

production () {
    mkdir -p /var/log/faiss_web_service

    uwsgi \
        --http :5000 \
        --chdir ${ROOT}/faiss_web_service \
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

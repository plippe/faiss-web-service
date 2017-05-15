#!/bin/sh

ROOT=$(realpath $(dirname ${0})/..)

python ${ROOT}/faiss_web_service/app.py

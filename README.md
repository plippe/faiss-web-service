# Faiss Web Service

## 简述

本项目 forked from [plippe/faiss-web-service](https://github.com/plippe/faiss-web-service)。
添加了提取图片特征向量、构建 Faiss 索引以及构建运行docker三部分。

### 1. 图片特征提取

使用opencv 的SIFT 特征提取算法，代码位置：`src/utils/feature_detect.py`

### 2. 索引构建

简单的构建，代码位置为：`src/train_index/train_index.py`。

因为SIFT默认输出维度为128维，如果觉得太低，可以使用词袋模型（BOW），代码实现位置在：`src/train_index/train_index_bow.py`。

## 开始

### 准备环境

可以到 [the docker hub image](https://hub.docker.com/r/plippe/faiss-web-service/) 下载基础镜像:

```sh
docker pull plippe/faiss-web-service:1.2.1-gpu
```

由于提取图片特征向量时，需要用到Opencv，所以还需要在镜像中安装它。

## API 使用规则

### 构建索引

启动docker 容器，进入容器中，运行：

```bash
cd src/train_index
python train_index.py
```

### 查询API

```sh
# Faiss search for ids 1, 2, and 3
curl 'localhost:5000/faiss/search' -X POST -d '{"k": 5, "ids": [1, 2, 3]}'

# Faiss search for image path
curl 'localhost:5000/faiss/search' -X POST -d '{"k": 5, "image": “/image/path/imagename”}'

# Faiss search for vector file path
curl 'localhost:5000/faiss/search' -X POST -d '{"k": 5, "vectors": “/vector/file/path”}'
```

## 运行

进入docker container 中，运行 bin/faiss_web_service.sh 即可。

### 检测状态

检测镜像是否成功启动：
```sh
# Healthcheck
curl 'localhost:5000/ping'

```

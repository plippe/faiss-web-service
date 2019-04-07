# Faiss Web Service

## 简述

本项目 forked from [plippe/faiss-web-service](https://github.com/plippe/faiss-web-service)。
添加了提取图片特征向量、构建 Faiss 索引以及构建运行docker三部分。

关于 Faiss 以及其他此项目的详细信息，可以在我的blog上找到，地址在[这里](https://waltyou.github.io/Faiss-In-Project/)。

### 1. 图片特征提取

使用opencv 的SIFT 特征提取算法，代码位置：`src/utils/feature_detect.py`

### 2. 索引构建

#### 简单的构建

代码位置为：`src/train_index/train_index.py`。
这个代码里面使用的是不需要 `train` 的索引。

#### 构建需要预训练的索引

在真实使用场景下，我们会使用一些需要预训练的索引，比如"IVFx,Flat"等，关于如何选择合适的索引，请参考[这里](https://waltyou.github.io/Faiss-Indexs/#%E6%8C%91%E4%B8%80%E4%B8%AA%E5%90%88%E9%80%82%E7%9A%84-index)。
代码位置为：`src/train_index/train_index_with_pre_train.py`。

#### 词袋模型

因为SIFT默认输出维度为128维，如果觉得太低，可以使用词袋模型（BOW）。
代码实现位置在：`src/train_index/train_index_bow.py`。

#### 基于Javacv提取出的特征构建索引

代码实现位置在：`src/train_index/train_index_from_java.py`。

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

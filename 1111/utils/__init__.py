# -*- coding: utf-8 -*-
# @Author  : ajay huang <jbp06c@163.com>
# @Time    : 2025/7/14 10:58
# @File    : __init__.py.py
from config import Config
from utils.minio_client import MinioClient
from utils.oss_client import OssClient


# oss_cli = OssClient(
#     host=Config.OSS_ENDPOINT,
#     access_key=Config.OSS_ACCESS_KEY,
#     secret_key=Config.OSS_SECRET_KEY,
#     bucket=Config.OSS_BUCKET,
#     prefix_path=Config.OSS_PATH
# )
oss_cli = MinioClient(
    endpoint=Config.MINIO_ENDPOINT,
    access_key=Config.MINIO_ACCESS_KEY,
    secret_key=Config.MINIO_SECRET_KEY,
    bucket=Config.MINIO_BUCKET,
    prefix_path=Config.MINIO_PATH
)
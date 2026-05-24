# -*- coding: utf-8 -*-
# @Author  : ajay huang <jbp06c@163.com>
# @Time    : 2025/7/14 13:20
# @File    : config.py
import os, json
from typing import Union, List
from pydantic import field_validator
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    class Config:
        env_file = f'{os.getenv("ENV", "")}.env'
        env_file_encoding = 'utf-8'


class GlobalConfig(Settings):
    COMFYUI_SERVER_ADDRESS: Union[List[str], str]
    MINIO_ENDPOINT: str
    MINIO_ACCESS_KEY: str
    MINIO_SECRET_KEY: str
    MINIO_BUCKET: str
    MINIO_PATH: str
    OSS_ENDPOINT: str
    OSS_ACCESS_KEY: str
    OSS_SECRET_KEY: str
    OSS_BUCKET: str
    OSS_PATH: str

    @field_validator("COMFYUI_SERVER_ADDRESS", mode="before")
    @classmethod
    def parse_comfyui_server_address(cls, val):
        if isinstance(val, str):
            return [item.strip() for item in val.split(',') if item.strip()]
        return []


Config = GlobalConfig()
print(Config)
import datetime
import io
import os
import json
import time
import backoff
import zipfile
import requests
from minio import Minio, S3Error
from loguru import logger
from pathlib import Path
from typing import Union
from urllib.parse import urlparse, unquote
from requests.exceptions import RequestException
from concurrent.futures import ThreadPoolExecutor, as_completed


class MinioClient():
    def __init__(self, *, endpoint: str = None, access_key: str = None, secret_key: str = None, bucket: str = None, prefix_path: str = None):
        self.endpoint = endpoint
        self.access_key = access_key
        self.secret_key = secret_key
        self.bucket = bucket
        self.client = Minio(
            self.endpoint,
            access_key=self.access_key,
            secret_key=self.secret_key,
            secure=False
        )
        self.prefix_path = prefix_path if prefix_path is not None else ''

    def get_upload_object_url(self, obj_name: str):
        try:
            res = self.client.presigned_get_object(self.bucket, obj_name)
            res_list = res.strip().split('?')
            if len(res_list) > 1:
                return res_list[0]
            else:
                raise RequestException(f"Invalid MinIO path: {res}")
        except Exception as e:
            raise RequestException(f'get_upload_object_url error: {str(e)}')

    @backoff.on_exception(backoff.expo, exception=RequestException, max_tries=3)
    def upload(self, file_path_or_data: Union[str, bytes], filename: str = None) -> str:
        if isinstance(file_path_or_data, str):
            if not os.path.exists(file_path_or_data):
                raise ValueError(f'文件目录{file_path_or_data}不存在')
            with open(file_path_or_data, 'rb') as f:
                content = f.read()
        elif isinstance(file_path_or_data, bytes):
            content = file_path_or_data
        else:
            raise ValueError(f'参数`file_path_or_data`类型{type(file_path_or_data)}不支持')

        data = io.BytesIO(content)
        size = len(content)
        if filename is not None:
            obj_name = f'{self.prefix_path}/{filename}'
        else:
            obj_name = f'{self.prefix_path}/{int(time.time())}.png'
        try:
            self.client.put_object(self.bucket, obj_name, data, size)
            return obj_name
        except Exception as e:
            raise RequestException(f'output_upload error: {str(e)}')

    @backoff.on_exception(backoff.expo, exception=RequestException, max_tries=3)
    def upload_no_file(self, file_obj, obj_name) -> str:
        try:
            content = file_obj.read()
            data = io.BytesIO(content)
            size = len(content)
            self.client.put_object(self.bucket, obj_name, data, size)
            return self.get_upload_object_url(obj_name)
        except Exception as e:
            raise RequestException(f'output_upload error: {str(e)}')

    def get_obj_bytes(self, obj_name: str) -> bytes:
        return self.client.get_object(self.bucket, obj_name).read()

    # 下载图片到本地
    def download_image(self, url, filename):
        response = requests.get(url)
        with open(filename, 'wb') as f:
            f.write(response.content)

    def zip_multi_files(self, file_paths: list):
        zip_file_names = []
        # 1. 下载文件
        for url in file_paths:
            obj_name = unquote(urlparse(url).path.split("/")[-1])
            self.download_image(url, obj_name)
            zip_file_names.append(obj_name)
            logger.info(f"download file {obj_name} for zip")

        # 2. 压缩文件
        zip_name = f'{time.time_ns()}.zip'
        with zipfile.ZipFile(zip_name, 'w') as zipf:
            for file in zip_file_names:
                zipf.write(file)
                os.remove(file)
        return zip_name

    @backoff.on_exception(backoff.expo, exception=Exception, max_tries=3)
    def concurrent_upload_batch_files(self, files_path) -> dict:
        with ThreadPoolExecutor(max_workers=len(files_path)) as t:
            st = time.perf_counter()  # 记录开始时间，用于计算总耗时
            worker_dict = {}
            for i in files_path:
                worker = t.submit(self.upload, i)
                worker_dict[worker] = i
            ret_dict = {}
            for future in as_completed(worker_dict):
                file = worker_dict[future]
                try:
                    ret = future.result()
                    ret_dict[Path(file).stem] = ret
                except Exception as e:
                    ret_dict[file] = 'error'
                    logger.error(f'Minio upload filename: {file}  error: {str(e)}')
            logger.info(f'concurrent_minio_upload, total cost: {time.perf_counter() - st:.4f}, ret: {json.dumps(ret_dict)}')
            return ret_dict

    def object_is_exist(self, object_name: str) -> bool:
        try:
            self.client.stat_object(self.bucket, object_name)
        except S3Error as e:
            if e.code == 'NoSuchKey':
                return False
            raise e
        else:
            return True


if __name__ == '__main__':
    cli = MinioClient(endpoint='10.26.37.50:9000',
                      access_key='admin',
                      secret_key='E9mS5Ag_hV0v3Gn6',
                      bucket='aigc-poc',
                      )

    # 上传图片
    image_path = r'E:\imgs\4.png'
    # image_url = cli.upload(image_path)
    # print(image_url)

    # # 列出所有对象
    # objects = cli.client.list_objects(cli.bucket)
    # for obj in objects:
    #     print(obj.object_name)

    # cli.client.remove_bucket(cli.bucket)
    # cli.client.remove_object(cli.bucket, '1742897612_format1.PNG')

    cli.client.fget_object('aigc-poc', '1743130948_unix_947940.png', image_path)

    # from PIL import Image
    # obj = requests.get("http://0.0.0.0:8002/mj/public/pic/173144~1.PNG").content
    # print(obj)
    # with open(image_path, 'wb') as f:
    #     f.write(b'{"detail":"\xe6\x8c\x87\xe5\xae\x9a\xe5\x9b\xbe\xe7\x89\x87\xe4\xb8\x8d\xe5\xad\x98\xe5\x9c\xa8"}')
    # image = Image.open(image_path)
    # #
    # policy = cli.client.get_bucket_policy(cli.bucket)
    # print(policy)

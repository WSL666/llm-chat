## pip install boto3 -i https://pypi.tuna.tsinghua.edu.cn/simple
import io
import os
import backoff
import boto3
import time
import json
import requests
import zipfile
from typing import Union
from pathlib import Path
from loguru import logger
from botocore.client import Config
from urllib.parse import urlparse, unquote
from requests.exceptions import RequestException
from concurrent.futures import ThreadPoolExecutor, as_completed


class OssClient:
    def __init__(self, *, host: str, access_key: str, secret_key: str, bucket: str, prefix_path: str = None):
        self.host = host
        self.access_key = access_key
        self.secret_key = secret_key
        self.bucket = bucket
        self.pool_worker = 3
        self.oss_cfg = Config(
            signature_version='s3v4',
            s3={'addressing_style': 'virtual'},
            connect_timeout=5,
            read_timeout=10,
            retries={
                'total_max_attempts': 5,
            }
        )
        self.client = boto3.client(service_name='s3',
                                   endpoint_url=self.host,
                                   aws_access_key_id=self.access_key,
                                   aws_secret_access_key=self.secret_key,
                                   config=self.oss_cfg)
        self.prefix_path = prefix_path if prefix_path is not None else ''

    def get_upload_object_url(self, obj_name: str):
        res = self.client.generate_presigned_url('get_object', Params={'Bucket': self.bucket, 'Key': obj_name})
        li_resp = res.strip().split('?')
        if len(li_resp) > 1:
            return li_resp[0]
        else:
            print(f"Invalid oss path: {res}")

    def object_is_exist(self, obj_name: str) -> bool:
        try:
            self.client.head_object(Bucket=self.bucket, Key=obj_name)
            return True
        except:
            return False

    def get_obj_bytes(self, obj_name: str) -> bytes:
        bytes_io = io.BytesIO()
        self.client.download_fileobj(self.bucket, obj_name, bytes_io)
        bytes_io.seek(0)
        content = bytes_io.read()
        bytes_io.close()
        return content

    @backoff.on_exception(backoff.expo, exception=RequestException, max_tries=3)
    def upload(self, file_or_data: Union[bytes, io.BytesIO, str], filename: str = None):
        if isinstance(file_or_data, str):
            with open(file_or_data, 'rb') as f:
                content = f.read()
            file = io.BytesIO(content)
        elif isinstance(file_or_data, bytes):
            file = io.BytesIO(file_or_data)
        elif isinstance(file_or_data, io.BytesIO):
            file = file_or_data
        else:
            raise Exception(f'不支持的`file_or_data`类型：{type(file_or_data)}。')
        file.seek(0)
        if filename is not None:
            obj_name = f'{self.prefix_path}/{filename}'
        else:
            obj_name = f'{self.prefix_path}/{int(time.time())}.png'
        self.client.upload_fileobj(file, self.bucket, obj_name, ExtraArgs={'ACL': 'public-read'})
        return self.get_upload_object_url(obj_name)

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
            logger.info(
                f'concurrent_minio_upload, total cost: {time.perf_counter() - st:.4f}, ret: {json.dumps(ret_dict)}')
            return ret_dict


if __name__ == "__main__":
    # oss_conf = {
    #     'host': 'https://oss-cn-uat.midea.com',
    #     'access_key': 'jzhf6dhtjluqyy6xt9cnvass',
    #     'secret_key': 'ibqxsdvu6wd1ys9uqjycsbegp0rruw7i',
    #     'bucket': 'aios',
    # }
    # oss_conf = {
    #     "host": "https://oss-cn-foshan.midea.com",
    #     "access_key": "8OIrrGIRhlYilOXCm0r6Zhsn",
    #     "secret_key": "zPh0mCr9bqPL7gLfq8olRueG1USwPCXi",
    #     "bucket": "dedp-algorithm"
    # }

    # oss_conf = {
    #     "host": "http://aios-data-ga.midea.com:30222",
    #     "access_key": "6afzwoaeutxy",
    #     "secret_key": "vt6u11easfrnxnc5690xdog636iibu82",
    #     "bucket": "alias"
    # }
    oss_conf = {
        "host": "http://192.168.16.148:8060",
        "access_key": "2ax9k7bll1siqeuyla1q",
        "secret_key": "r2qzz6agxbvwc52tiyvlu2fu7f4yroi3fzrxc4v4",
        "bucket": "bucket-ai"
    }
    oss = OssClient(**oss_conf)

    from tqdm import tqdm

    img_dir = r"E:\drawing_papi\mj\public\pic"
    files = os.listdir(img_dir)
    for file in tqdm(files):
        filepath = os.path.join(img_dir, file)
        url = oss.upload_file(
            filepath,
            f"/ai/pcportal/aitest/drawing_papi/{file}")


    # res = oss.download_file("/robot_evaluation/test_data_dianzi_20250613_outputs_20250616170908.csv")
    # with open('../../test_data_dianzi_20250613_outputs_20250616170908.csv', 'wb') as f:
    #     f.write(res)
    # res = oss.is_file_exists('/robot_evaluation/坐席工作台测试集0610_outputs_20250610185935_outputs_20250611114641.csv')
    # print(res)
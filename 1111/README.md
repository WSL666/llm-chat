# ComfyUI-API

本服务为mdesign接入ComfyUI的服务，使用Python3.10+FastAPI搭建，包含以下功能：

- **Flux文生图**
- **flux文生图垫图**
- **Flux专业版**
- **FluxKontext文修图**
- **局部重绘**
- **AI扩图**
- **抠图**
- **高清放大**
- **超分放大**

本服务无需使用GPU资源。

### 接口文档地址
请参考[api_docs](./api_docs.md)


### 启动前配置
需配置[config.py](config.py)，配置文件中有如下配置：
```python
COMFYUI_SERVER_ADDRESS: str  # ComfyUI服务地址
# OSS对象存储配置
MINIO_ADDR: str 
MINIO_ACCESS_KEY: str 
MINIO_SECRET_KEY: str 
MINIO_BUCKET: str  
# OSS对象存储中图片存储路径
MINIO_PATH: str  
```

### 启动命令
- **python默认启动方式**
```shell
pip install -r requirements.txt
python main.py
```

- **uvicorn启动方式**
```shell
# uvicorn启动fastapi服务
uvicorn main:app --host 0.0.0.0 --port 5000
```

- **docker启动方式**
```shell
# docker打包镜像
docker build -t comfyui-api:v1 .
# docker启动
docker run -ti -d --name comfyui-api -v /apps/jay/comfyui-api:/apps/comfyui-api -p 5000:5000 comfyui-api:v1 uvicorn main:app --host 0.0.0.0 --port 5000
```

- **compose启动方式**
```shell
docker-compose up -d
```


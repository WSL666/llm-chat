import base64
import os
import re
import aiohttp
import websocket
import uuid
import json
import io
import asyncio
import urllib.request
import urllib.parse
import urllib.error
import mimetypes
from PIL import Image
from utils import oss_cli, compress_image
import time

# 定义向服务器发送提示的函数
def queue_prompt(client_id, server_address, prompt):
    p = {"prompt": prompt, "client_id": client_id}
    data = json.dumps(p).encode('utf-8')
    req = urllib.request.Request("http://{}/prompt".format(server_address), data=data)
    return json.loads(urllib.request.urlopen(req).read())


# 定义从服务器下载图像数据的函数
def get_image(server_address, filename, subfolder, folder_type):
    data = {"filename": filename, "subfolder": subfolder, "type": folder_type}
    url_values = urllib.parse.urlencode(data)
    with urllib.request.urlopen("http://{}/view?{}".format(server_address, url_values)) as response:
        if response.code != 200:
            raise Exception(f'错误的HTTP状态码，{response.code}')
        return response.read()


def upload_image(server_address, image_path_or_url):

    if image_path_or_url.startswith('http://') or image_path_or_url.startswith('https://'):
        ret = re.search(u'[\u4e00-\u9fa5]+', image_path_or_url)
        if ret:
            image_path_or_url = urllib.parse.quote(image_path_or_url, safe=':/?&=')
        try:
            with urllib.request.urlopen(image_path_or_url, timeout=20) as res:
                if res.code != 200:
                    raise Exception(f'错误的HTTP状态码，{res.code}')
                data = res.read()
        except urllib.error.HTTPError as e:
            raise Exception(f"HTTP 错误码：{e.code}")
        except urllib.error.URLError as e:
            raise Exception(f"请求 {image_path_or_url} 失败，原因：{e.reason}")
        except Exception as e:
            raise Exception(f'请求 {image_path_or_url} 失败，原因：{str(e)}')
    elif image_path_or_url.startswith("BASE64,") or image_path_or_url.startswith('base64,'):
        data = base64.b64decode(image_path_or_url.replace("BASE64,", "").replace('base64,', ''))
    elif os.path.exists(image_path_or_url):
        with open(image_path_or_url, 'rb') as f:
            data = f.read()
    elif oss_cli.object_is_exist(image_path_or_url):
        data = oss_cli.get_obj_bytes(image_path_or_url)
    else:
        raise ValueError(f'获取图片路径 {image_path_or_url} 失败')

    boundary = f'----WebKitFormBoundary{uuid.uuid4().hex}'
    CRLF = b'\r\n'
    body = []
    body.append(f'--{boundary}'.encode())
    body.append(f'Content-Disposition: form-data; name="type"'.encode())
    body.append(b'')
    body.append(b'input')
    # 文件字段
    mime_type = mimetypes.guess_type(image_path_or_url)[0] or 'application/octet-stream'
    body.append(f'--{boundary}'.encode())
    filename = os.path.basename(image_path_or_url)
    body.append(f'Content-Disposition: form-data; name="image"; filename="{filename}"'.encode())
    body.append(f'Content-Type: {mime_type}'.encode())
    body.append(b'')
    body.append(data)
    body.append(f'--{boundary}--'.encode())
    body.append(b'')
    data = CRLF.join(body)
    headers = {
        'Content-Type': f'multipart/form-data; boundary={boundary}',
        'Content-Length': str(len(data))
    }
    url = 'http://{}/api/upload/image'.format(server_address)
    req = urllib.request.Request(url, data=data, headers=headers, method='POST')
    response = urllib.request.urlopen(req)
    return json.loads(response.read())


# 定义获取历史记录的函数
def get_history(server_address, prompt_id):
    # with urllib.request.urlopen("http://{}/history/{}".format(server_address, prompt_id)) as response:
    with urllib.request.urlopen("http://{}/history?prompt_id={}".format(server_address, prompt_id)) as response:
        return json.loads(response.read())


# 定义通过WebSocket接收消息并下载图像的函数
def get_images(server_address, prompt, client_id=None):
    if client_id is None:
        # 设置服务器地址和客户端ID
        client_id = str(uuid.uuid4())
    # 创建一个WebSocket连接到服务器
    # ws = websocket.WebSocket()
    # ws.connect("ws://{}/ws?clientId={}".format(server_address, client_id))
    prompt_id = queue_prompt(client_id, server_address, prompt)['prompt_id']
    # while True:
    #     out = ws.recv()
    #     if isinstance(out, str):
    #         message = json.loads(out)
    #         if message['type'] == 'executing':
    #             data = message['data']
    #             if data['node'] is None and data['prompt_id'] == prompt_id:
    #                 break  # 执行完成
    #     else:
    #         continue  # 预览是二进制数据
    # ws.close()

    poll_interval = 2  # 轮询间隔2秒
    max_poll_times = 60  # 最大轮询60次（超时120秒）
    poll_count = 0
    while poll_count < max_poll_times:
        try:
            # 获取历史记录
            history = get_history(server_address, prompt_id)
            if prompt_id in history:
                task_history = history[prompt_id]
                # 判断任务完成：有输出图片 或 执行状态结束
                has_output = 'outputs' in task_history and task_history['outputs']
                is_executed = 'executing' in task_history and task_history['executing'].get('node') is None
                if has_output or is_executed:
                    break
            time.sleep(poll_interval)
            poll_count += 1
        except Exception as e:
            print(f"轮询失败，重试：{e}")
            time.sleep(poll_interval)
            poll_count += 1
    # 超时判断
    if poll_count >= max_poll_times:
        raise TimeoutError(f"任务 {prompt_id} 执行超时")
    history = get_history(server_address, prompt_id)[prompt_id]
    filenames = []
    image_datas = []
    for node_id, node_output in history['outputs'].items():
        if 'images' in node_output:
            for image in node_output['images']:
                filenames.append(image['filename'])
                image_data = get_image(server_address, image['filename'], image['subfolder'], image['type'])
                image_datas.append(image_data)

    # 压缩图片
    image_datas = [compress_image.chunk_compress_png(data) for data in image_datas]

    return filenames, image_datas


def get_videos(server_address, prompt, client_id=None, timeout_seconds=1800):
    """专用于视频生成工作流。
    与 get_images 的三处关键差异：
      1. 超时 1800 秒（视频生成需 5~30 分钟）
      2. 读取 'videos' 键（SaveVideo节点）或 'gifs' 键（SaveAnimatedGIF/WEBP节点），兼容两者
      3. 不做 PNG 压缩，直接返回原始字节
    """
    if client_id is None:
        client_id = str(uuid.uuid4())
    prompt_id = queue_prompt(client_id, server_address, prompt)['prompt_id']

    poll_interval = 5          # 视频生成较慢，5 秒轮询一次
    max_poll = timeout_seconds // poll_interval
    poll_count = 0

    while poll_count < max_poll:
        try:
            h = get_history(server_address, prompt_id)
            if prompt_id in h:
                t = h[prompt_id]
                # 只有 outputs 非空才算真正完成，避免任务刚入队 executing.node=None 时误判提前退出
                if 'outputs' in t and bool(t['outputs']):
                    break
            time.sleep(poll_interval)
            poll_count += 1
        except Exception as e:
            print(f"视频轮询失败，重试：{e}")
            time.sleep(poll_interval)
            poll_count += 1

    if poll_count >= max_poll:
        raise TimeoutError(f"视频任务 {prompt_id} 执行超时（{timeout_seconds}s）")

    history = get_history(server_address, prompt_id)[prompt_id]
    filenames = []
    video_datas = []
    for _, node_output in history['outputs'].items():
        # SaveVideo 节点实际使用 'images' 键存放视频文件（.mp4），兼容 images/videos/gifs 三种键名
        video_items = node_output.get('images') or node_output.get('videos') or node_output.get('gifs') or []
        for v in video_items:
            filenames.append(v['filename'])
            video_datas.append(
                get_image(server_address, v['filename'], v['subfolder'], v['type'])
            )

    # 不压缩，直接返回原始视频字节
    return filenames, video_datas


# async def upload_image(url: str, filename: str, data: bytes):
#     async with aiohttp.ClientSession() as sess:
#         form = aiohttp.FormData()
#         form.add_field(
#             name='file',
#             value=data,
#             filename=filename,
#             content_type='application/octet-stream'
#         )
#         async with sess.post(
#                 url,
#                 data=form
#         ) as res:
#             if res.status == 200:
#                 res_json = await res.json()
#                 code = res_json.get('code')
#                 data = res_json.get('data')
#                 msg = res_json.get('msg')
#                 if code != 0:
#                     raise Exception(f'Response Error, response code is {code}, error message is {msg}.')
#                 return data
#             raise Exception(
#                 f'Request url:{url} status is {res.status}, please check the endpoint server from {url}.'
#             )


if __name__ == '__main__':
    server_address = "101.126.159.88:5020"

    from templates import ComfyUIPromptTemplate
    templte = ComfyUIPromptTemplate.from_template(path='../temps/normal-txt2img.tpl')
    p = '(best quality,4k,8k,highres,masterpiece:1.2),ultra-detailed,(realistic,photorealistic,photo-realistic:1.37),true-life,a girl playing on the beach,beautiful detailed eyes,beautiful detailed lips,extremely detailed eyes and face,long eyelashes,smiling,happy expression,wearing a summer dress,blonde hair,wind blowing through hair,holding a beach ball,sandy beach,clear blue sky,bright sunlight,shadows on the sand,soft waves in the background,photography,vivid colors,sharp focus,studio lighting,physically-based rendering,extreme detail description,professional'
    prompt = templte.render_json(POS_PROMPT=p, WIDTH=512, HEIGHT=512, BATCH_SIZE=1, NOISE_SEED=47837)
    print(prompt)

    # 调用get_images()函数来获取图像
    filenames, images = get_images(server_address, prompt)
    image = Image.open(io.BytesIO(images[0]))
    image.show()
    image.show()
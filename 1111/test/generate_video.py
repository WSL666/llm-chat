import os
import requests
from minio import Minio

url = "http://localhost:8001/api/comfyui/generate"

# LTX2.3 文生视频请求参数
payload = {
    "id": "ltx-img2video-001",
    "way": "LTX2.3-img2video",
    "pos_prompt": "A man walking in the desert, cinematic lighting",
    "input_img": "E:/myworkspace/april/ai-comfyui-api/test/output_0.png",
    "ltx_width": 1280,
    "ltx_height": 720,
    "ltx_frame_rate": 25,
    "ltx_duration": 5
}

client = Minio(
    "10.26.37.211:9000",
    access_key="admin",
    secret_key="s20r-z~Mu2tf",
    secure=False
)

print("正在请求生成视频，请稍候（视频生成耗时较长）...")
response = requests.post(url, json=payload, timeout=1800)  # 视频生成耗时长，超时设为 30 分钟
result = response.json()
print(result)

# result 格式：{'code': 0, 'data': {'videos': ['/drawing_papi/.../xxx.mp4']}, 'msg': 'success'}
if result.get('code') == 0:
    video_urls = result['data']['videos']
    for index, video_url in enumerate(video_urls):
        # 从 OSS 路径推断原始扩展名（视频通常为 .mp4）
        ext = os.path.splitext(video_url)[-1] or ".mp4"
        local_filename = f"output_video_{index}{ext}"
        client.fget_object(
            "aigc-sit",
            video_url,
            local_filename
        )
        print(f"下载完成：{local_filename}  (来源: {video_url})")
else:
    print(f"请求失败：{result.get('msg')}")

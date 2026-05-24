import requests

url = "http://localhost:8001/api/comfyui/generate"

# 测试 Flux 文生图
payload =   {
            "id": "ernie-image-001",
            "way": "ERNIEIMAGE-txt2img",
            "pos_prompt": "这是一张展现高时尚风格夏季服装的图表，其特色是色彩协调的悬浮元素以优雅的扩展圆形构图方式排列。其中包括透气的草帽、无袖有机棉上衣、飘逸的褶皱长裙、手工制作的皮革凉鞋以及编织的棕榈叶手提包。精美的注释强调了面料的透气性、清新的质地、吸湿排汗的特性以及季节的舒适感。色彩搭配采用了温暖的中性色调——象牙白、陶土色、沙色和柔和的棕色调。微妙的动态轨迹和流动的布料漩涡营造出轻柔的夏日微风的感觉，而明亮的自然阳光则形成柔和的阴影和被阳光亲吻的光泽，呈现出地中海风格。",
            "output_width": 1024,
            "output_height": 1024,
            "batch_size": 1,
            "ernie_steps": 50,
            "ernie_cfg": 4
        }

from minio import Minio

client = Minio(
    "10.26.37.211:9000",
    access_key="admin",
    secret_key="s20r-z~Mu2tf",
    secure=False
)


response = requests.post(url, json=payload)
result = response.json()
print(result)
# result 格式：{'code': 0, 'data': {'images': ['/drawing_papi/mj/public/pic/...png']}, 'msg': 'success'}
if result.get('code') == 0:
    image_urls = result['data']['images']
    for index, image_url in enumerate(image_urls):
        client.fget_object(
            "aigc-sit",
            image_url,
            f"output_{index}.png"  # 保存到本地的文件名
        )
        print(f"下载完成：output_{index}.png")
else:
    print(f"请求失败：{result.get('msg')}")

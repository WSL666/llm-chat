# -*- coding: utf-8 -*-
# @Author  : ajay huang <jbp06c@163.com>
# @Time    : 2025/12/18 10:35
# @File    : compress_image.py
from typing import Union
from PIL import Image


def chunk_compress_png(
        input_img: Union[bytes, str],
        max_size_mb: int = 10,
        reduction_factor: int = 0.8,
        max_iterations: int = 10
) -> bytes:
    """
    分块压缩法：逐步调整图片尺寸和质量
    """
    import os
    import io
    import base64
    import requests
    import math
    max_size_bytes = max_size_mb * 1024 * 1024

    if isinstance(input_img, str):
        if input_img.startswith('http://') or input_img.startswith('https://'):
            res = requests.get(input_img)
            if res.status_code != 200:
                raise Exception(f"获取图片 {input_img} 失败，{res.text}")
            input_img_bytes = res.content
        elif os.path.exists(input_img):
            with open(input_img, 'rb') as f:
                input_img_bytes = f.read()
        else:
            try:
                input_img_bytes = base64.b64decode(input_img)
            except Exception as e:
                raise Exception(f"获取base64图片失败，{str(e)}")
    elif isinstance(input_img, bytes):
        input_img_bytes = input_img
    else:
        raise Exception("输入图片格式错误")
    original_size = len(input_img_bytes)
    img = Image.open(io.BytesIO(input_img_bytes))
    width, height = img.size

    print(f"原始尺寸: {width}x{height}, 大小: {original_size / 1024 / 1024:.2f} MB")

    # 如果已经是目标大小内
    if original_size <= max_size_bytes:
        return input_img_bytes

    # 计算需要的压缩比例
    ratio_needed = max_size_bytes / original_size

    # 估算压缩后的尺寸（经验公式）
    # PNG文件大小与像素数量大致成线性关系
    current_width, current_height = width, height

    for iteration in range(max_iterations):
        # 计算新的尺寸
        scale_factor = math.sqrt(ratio_needed) * (reduction_factor ** iteration)
        new_width = int(current_width * scale_factor)
        new_height = int(current_height * scale_factor)

        # 确保最小尺寸
        new_width = max(new_width, 100)
        new_height = max(new_height, 100)

        # 调整尺寸
        resized_img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)

        # 保存到内存测试大小
        import io
        buffer = io.BytesIO()

        # 尝试不同压缩级别
        compress_levels = [9, 6, 3, 1]

        for level in compress_levels:
            buffer.seek(0)
            buffer.truncate(0)

            resized_img.save(buffer, format='PNG', optimize=True,
                             compress_level=level)

            buffer_size = buffer.tell()
            print(f"迭代 {iteration + 1}: {new_width}x{new_height}, "
                  f"压缩级别 {level}, 大小: {buffer_size / 1024 / 1024:.2f} MB")

            if buffer_size <= max_size_bytes:
                # 成功！保存文件
                buffer.seek(0)
                print(f"✓ 成功压缩到目标大小！")
                print(f"最终尺寸: {new_width}x{new_height}")
                print(f"最终大小: {buffer_size / 1024 / 1024:.2f} MB")
                return buffer.getvalue()

        # 如果还没达到目标，继续缩小
        current_width, current_height = new_width, new_height

    print("⚠ 无法在最大迭代次数内压缩到目标大小")
    # 保存最佳尝试
    buffer.seek(0)
    return buffer.getvalue()


if __name__ == '__main__':
    p = r"D:\Users\huangzj271\Downloads\20251218094120416026matting-img_00001_.png"
    with open(p, 'rb') as f:
        con = f.read()
    res = chunk_compress_png(con)
    with open('out.png', 'wb') as f:
        f.write(res)

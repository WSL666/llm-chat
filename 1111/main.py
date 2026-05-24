# -*- coding: utf-8 -*-
# @Author  : ajay huang <jbp06c@163.com>
# @Time    : 2025/7/14 9:23
# @File    : main.py
import base64
import json
import asyncio
import uvicorn, random
import datetime
from config import Config
from loguru import logger
from pydantic import BaseModel
from fastapi import FastAPI
from typing import Literal, Optional, Any, List
from utils.templates import ComfyUIPromptTemplate
from utils.comfyui_api import upload_image, get_images, get_videos
from utils import oss_cli
from fastapi.concurrency import run_in_threadpool

app = FastAPI()
GLOBAL_INVOKE = 0
LOCK = asyncio.Lock()
VIDEO_WAYS = {'LTX2.3-txt2video'}  # 视频工作流集合，走 get_videos()


class FluxBasePayload(BaseModel):
    '''flux基础版'''
    id: Optional[str] = None
    pos_prompt: Optional[str] = None
    neg_prompt: Optional[str] = None
    output_width: int = 768
    output_height: int = 768
    batch_size: int = 1
    denose_number: float = 0.8
    input_img: str | List[str] | None = None  # 输入图
    input_mask_img: Optional[str] = None  # 输入掩码图
    input_ref_img: str | List[str] | None = None  # 输入参考图
    way: Literal[
        'normal-txt2img',  # flux文生图
        'normal-txt2img-4steps',  # flux 4步生图
        'normal-txt2img-pad',  # flux文生图垫图
        'flux-lora-t2i',  # Flux专业版
        'flux-lora-t2i-pro',  # Flux专业版-controlnet
        'flux-kontext-edit',  # Flux-kontext
        'flux-kontext-edit-8steps',  # Flux-kontext
        'partial-repair',   # 重绘
        'padding-img',   # 扩图
        'matting-img',   # 抠图
        'scaleup',  # 高清放大
        'superir-scaleup',  # 超分放大
        'qwen-image',  # Qwen-Image文生图 
        'qwen-image-edit',  # Qwen-Image-Edit2511文生图
        'z-image-turbo',
        'z-image',
        'ERNIEIMAGE-txt2img',  # ERNIE-Image文生图
        'ERNIEIMAGE-txt2img-turbo',  # ERNIE-Image-Turbo文生图
        'LTX2.3-txt2video',  # LTX2.3文生视频
        'LTX2.3-img2video'   # LTX2.3图生视频
    ]

    # 扩图参数
    pad_bottom: Optional[int] = None
    pad_left: Optional[int] = None
    pad_right: Optional[int] = None
    pad_top: Optional[int] = None

    # 高清放大
    pixel: Optional[int] = 2048

    # Qwen-Image参数
    qwen_steps: int = 20 # Qwen采样步数
    qwen_cfg: float = 4  # Qwen CFG系数
             
    # z-image
    z_steps: int = 30  
    z_cfg: float = 4  
    # z-image-turbo
    z_turbo_steps:int = 8
    z_turbo_cfg: float = 1
    # ERNIE-Image参数
    ernie_steps: int = 50   # ERNIE采样步数
    ernie_cfg: float = 4    # ERNIE CFG系数
    # ERNIE-Image-Turbo参数
    ernie_turbo_steps: int = 8    # ERNIE-Turbo采样步数（Turbo版推荐4~12）
    ernie_turbo_cfg: float = 1    # ERNIE-Turbo CFG系数（Turbo版推荐1）
    # LTX2.3视频通用参数（txt2video / img2video 共用）
    ltx_width: int = 1280         # 视频宽度（建议 512~1920）
    ltx_height: int = 720         # 视频高度（建议 512~1080）
    ltx_frame_rate: int = 25      # 帧率（建议 24~30）
    ltx_duration: int = 5         # 视频时长（秒，建议 1~30）
class FluxProPayload(BaseModel):
    '''flux专业版'''
    id: Optional[str]
    prompt_text: Optional[str] = None
    width: int = 768
    height: int = 768
    batch: int = 1
    model_id: Optional[str] = "flux_lora/光影艺术-FLUX_V1.0.safetensors"  # Flux LoRA模型
    lora_strength: float = 1.0  # LoRA强度
    denoise_ratio: float = 1.0  # 降噪强度

    # flux controlnet
    ctrl1: Literal[
        'canny',
        'depth',
        'pose',
        'blur',
    ] = 'canny'
    img_ctl1: Optional[str] = None
    preprocess_ctrl1: Optional[str] = None
    preprocess_pixel1: int = 1024
    strength_ctrl1: float = 0.35  # controlnet强度


class TaskPayload(FluxBasePayload, FluxProPayload):
    return_format: Literal["URL", "BASE64"] = "URL"


class ResultPayload(BaseModel):
    prompt_id: str


class BaseResponse(BaseModel):
    code: int = 0
    data: Any | None = None
    msg: str = None


@app.post('/api/comfyui/generate')
async def comfyui_infer(payload: TaskPayload):
    global GLOBAL_INVOKE, LOCK
    # 调用次数+1，轮训方式切换不同的节点
    async with LOCK:
        if isinstance(Config.COMFYUI_SERVER_ADDRESS, str):
            comfyui_server_addr = Config.COMFYUI_SERVER_ADDRESS
        else:
            comfyui_server_addr = Config.COMFYUI_SERVER_ADDRESS[GLOBAL_INVOKE % len(Config.COMFYUI_SERVER_ADDRESS)]
        GLOBAL_INVOKE += 1
    logger.info(f"总调用数：{GLOBAL_INVOKE}，当前节点：{comfyui_server_addr} ...")
    # if payload.output_width is not None or payload.output_height is not None:
        # if not 768 <= payload.output_width <= 1536:
        #     err_msg = f'`output_width` 超出范围 [768,1536]'
        #     logger.error(err_msg)
        #     return BaseResponse(
        #         code=1,
        #         msg=err_msg
        #     )
        # if not 768 <= payload.width <= 1536:
        #     err_msg = f'`output_width` 超出范围 [768,1536]'
        #     logger.error(err_msg)
        #     return BaseResponse(
        #         code=1,
        #         msg=err_msg
        #     )
        # if not 768 <= payload.output_height <= 1536:
        #     err_msg = '`output_height` 超出范围 [768,1536]'
        #     logger.error(err_msg)
        #     return BaseResponse(
        #         code=1,
        #         msg=err_msg
        #     )
        #
        # if not 768 <= payload.height <= 1536:
        #     err_msg = '`output_height` 超出范围 [768,1536]'
        #     logger.error(err_msg)
        #     return BaseResponse(
        #         code=1,
        #         msg=err_msg
        #     )

    if payload.batch_size is not None:
        if payload.batch_size > 4:
            err_msg = f'`batch_size` 超出范围 [4]'
            logger.error(err_msg)
            return BaseResponse(
                code=1,
                msg=err_msg
            )

    # 上传图片
    if payload.input_img:
        try:
            if isinstance(payload.input_img, list):
                if len(payload.input_img) == 0:
                    raise ValueError("input_img 列表为空")
                img_path = payload.input_img[0]  # 取第一张
            else:
                img_path = payload.input_img
            res = await run_in_threadpool(upload_image, comfyui_server_addr, img_path)
            payload.input_img = res['name']
        except Exception as e:
            err_msg = f'上传图片到ComfyUI错误，{str(e)}。'
            logger.error(err_msg)
            return BaseResponse(
                code=1,
                msg=err_msg
            )

    if payload.input_ref_img:
        try:
            if isinstance(payload.input_ref_img, list):
                if len(payload.input_ref_img) == 0:
                    raise ValueError("input_ref_img 列表为空")
                img_path = payload.input_ref_img[0]  # 取第一张
            else:
                img_path = payload.input_ref_img
            res = await run_in_threadpool(upload_image, comfyui_server_addr, img_path)
            payload.input_ref_img = res['name']
        except Exception as e:
            err_msg = f'上传图片到ComfyUI错误，{str(e)}。'
            logger.error(err_msg)
            return BaseResponse(
                code=1,
                msg=err_msg
            )

    if payload.img_ctl1:
        try:
            res = await run_in_threadpool(upload_image, comfyui_server_addr, payload.img_ctl1)
            payload.img_ctl1 = res['name']
        except Exception as e:
            err_msg = f'上传图片到ComfyUI错误，{str(e)}。'
            logger.error(err_msg)
            return BaseResponse(
                code=1,
                msg=err_msg
            )

    if payload.input_mask_img:
        try:
            res = await run_in_threadpool(upload_image, comfyui_server_addr, payload.input_mask_img)
            payload.input_mask_img = res['name']
        except Exception as e:
            err_msg = f'上传MASK图片 {payload.input_mask_img} 到ComfyUI错误，{str(e)}。'
            logger.error(err_msg)
            return BaseResponse(
                code=1,
                msg=err_msg
            )
    if payload.way == "normal-txt2img":
        logger.info("normal-txt2img {}".format(payload.id))
        if not all([payload.output_width, payload.output_height, payload.batch_size, payload.pos_prompt]):
            err_msg = f'缺少参数'
            logger.error(err_msg)
            return BaseResponse(
                code=1,
                msg=err_msg
            )
        # 保存结果
        img_prefix = datetime.datetime.now().strftime("%Y%m%d%H%M%S%f")
        filename_prefix = img_prefix + "normal-txt2img"

        prompt = ComfyUIPromptTemplate.from_template(path='temps/{}.tpl'.format(payload.way)).render_json(
            FILENAME_PREFIX=json.dumps(filename_prefix),
            WIDTH=payload.output_width,
            HEIGHT=payload.output_height,
            BATCH_SIZE=payload.batch_size,
            NOISE_SEED=random.randint(1, 4294967294),
            POS_PROMPT=json.dumps(payload.pos_prompt)
        )
    elif payload.way == "normal-txt2img-4steps":
        logger.info("flux 4步生图 {}".format(payload.id))
        if not all([payload.output_width, payload.output_height, payload.batch_size, payload.pos_prompt]):
            err_msg = f'缺少参数'
            logger.error(err_msg)
            return BaseResponse(
                code=1,
                msg=err_msg
            )
        # 保存结果
        img_prefix = datetime.datetime.now().strftime("%Y%m%d%H%M%S%f")
        filename_prefix = img_prefix + "normal-txt2img-4steps"

        prompt = ComfyUIPromptTemplate.from_template(path='temps/{}.tpl'.format(payload.way)).render_json(
            FILENAME_PREFIX=json.dumps(filename_prefix),
            WIDTH=payload.output_width,
            HEIGHT=payload.output_height,
            BATCH_SIZE=payload.batch_size,
            NOISE_SEED=random.randint(1, 4294967294),
            POS_PROMPT=json.dumps(payload.pos_prompt)
        )
    elif payload.way == 'normal-txt2img-pad':
        logger.info("normal-txt2img-pad {}".format(payload.id))
        if not all([payload.batch_size, payload.pos_prompt, payload.input_ref_img]):
            err_msg = f'缺少参数'
            logger.error(err_msg)
            return BaseResponse(
                code=1,
                msg=err_msg
            )

        # 保存结果
        img_prefix = datetime.datetime.now().strftime("%Y%m%d%H%M%S%f")
        filename_prefix = img_prefix + "normal-txt2img-pad"

        prompt = ComfyUIPromptTemplate.from_template(path='temps/{}.tpl'.format(payload.way)).render_json(
            FILENAME_PREFIX=json.dumps(filename_prefix),
            BATCH_SIZE=payload.batch_size,
            NOISE_SEED=random.randint(1, 4294967294),
            POS_PROMPT=json.dumps(payload.pos_prompt),
            DENOSE_NUMBER=payload.denose_number,
            INPUT_REF_IMG=json.dumps(payload.input_ref_img)
        )
    elif payload.way == 'flux-lora-t2i':
        logger.info("flux-lora-t2i {}".format(payload.id))
        if not all([payload.batch, payload.width, payload.height, payload.prompt_text, payload.model_id]):
            err_msg = f'缺少参数'
            logger.error(err_msg)
            return BaseResponse(
                code=1,
                msg=err_msg
            )
        if payload.model_id == '无':
            payload.model_id = 'flux_lora/光影艺术-FLUX_V1.0.safetensors'

        # 保存结果
        img_prefix = datetime.datetime.now().strftime("%Y%m%d%H%M%S%f")
        filename_prefix = img_prefix + "flux-lora-t2i"

        prompt = ComfyUIPromptTemplate.from_template(path='temps/{}.tpl'.format(payload.way)).render_json(
            FILENAME_PREFIX=json.dumps(filename_prefix),
            BATCH_SIZE=payload.batch,
            WIDTH=payload.width,
            HEIGHT=payload.height,
            NOISE_SEED=random.randint(1, 4294967294),
            PROMPT_TEXT=json.dumps(payload.prompt_text),
            DENOISE_RATIO=payload.denoise_ratio,
            LORA=json.dumps(payload.model_id),
            LORA_STRENGTH=payload.lora_strength,
        )
    elif payload.way == 'flux-lora-t2i-pro':
        logger.info("flux-lora-t2i-pro {}".format(payload.id))
        if not all([
            payload.batch,
            payload.width,
            payload.height,
            payload.prompt_text,
            payload.model_id,
            payload.img_ctl1,
            payload.preprocess_ctrl1,
            payload.preprocess_pixel1,
            payload.strength_ctrl1
        ]):
            err_msg = f'缺少参数'
            logger.error(err_msg)
            return BaseResponse(
                code=1,
                msg=err_msg
            )
        if payload.model_id == '无':
            payload.model_id = 'flux_lora/光影艺术-FLUX_V1.0.safetensors'

        # 保存结果
        img_prefix = datetime.datetime.now().strftime("%Y%m%d%H%M%S%f")
        filename_prefix = img_prefix + "flux-lora-t2i-pro"

        # blur转为tile
        if payload.ctrl1 == "blur":
            payload.ctrl1 = 'tile'
        elif payload.ctrl1 == 'canny':
            payload.ctrl1 = 'canny/lineart/anime_lineart/mlsd'
        elif payload.ctrl1 == 'pose':
            payload.ctrl1 = 'openpose'

        prompt = ComfyUIPromptTemplate.from_template(path='temps/{}.tpl'.format(payload.way)).render_json(
            FILENAME_PREFIX=json.dumps(filename_prefix),
            BATCH_SIZE=payload.batch,
            WIDTH=payload.width,
            HEIGHT=payload.height,
            NOISE_SEED=random.randint(1, 4294967294),
            PROMPT_TEXT=json.dumps(payload.prompt_text),
            DENOISE_RATIO=payload.denoise_ratio,
            LORA=json.dumps(payload.model_id),
            LORA_STRENGTH=payload.lora_strength,
            STRENGTH_CTRL1=payload.strength_ctrl1,
            CTRL1=json.dumps(payload.ctrl1),
            IMG_CTL1=json.dumps(payload.img_ctl1)
        )
    elif payload.way == 'flux-kontext-edit':
        logger.info("flux-kontext-edit {}".format(payload.id))
        if not all([payload.input_img, payload.pos_prompt]):
            err_msg = f'缺少参数'
            logger.error(err_msg)
            return BaseResponse(
                code=1,
                msg=err_msg
            )

        # 保存结果
        img_prefix = datetime.datetime.now().strftime("%Y%m%d%H%M%S%f")
        filename_prefix = img_prefix + 'flux-kontext-edit'

        prompt = ComfyUIPromptTemplate.from_template(path='temps/{}.tpl'.format(payload.way)).render_json(
            POS_PROMPT=json.dumps(payload.pos_prompt),
            INPUT_IMG=json.dumps(payload.input_img),
            NOISE_SEED=random.randint(1, 4294967294),
            FILENAME_PREFIX=json.dumps(filename_prefix)
        )
    elif payload.way == 'flux-kontext-edit-8steps':
        logger.info("flux-kontext-edit-8steps {}".format(payload.id))
        if not all([payload.input_img, payload.pos_prompt]):
            err_msg = f'缺少参数'
            logger.error(err_msg)
            return BaseResponse(
                code=1,
                msg=err_msg
            )

        # 保存结果
        img_prefix = datetime.datetime.now().strftime("%Y%m%d%H%M%S%f")
        filename_prefix = img_prefix + 'flux-kontext-edit-8steps'

        prompt = ComfyUIPromptTemplate.from_template(path='temps/{}.tpl'.format(payload.way)).render_json(
            POS_PROMPT=json.dumps(payload.pos_prompt),
            INPUT_IMG=json.dumps(payload.input_img),
            NOISE_SEED=random.randint(1, 4294967294),
            FILENAME_PREFIX=json.dumps(filename_prefix)
        )
    elif payload.way == 'partial-repair':
        logger.info("partial-repair {}".format(payload.id))
        if not all([payload.input_img, payload.input_mask_img]):
            err_msg = f'缺少参数 `input_img`和`input_mask_img`'
            logger.error(err_msg)
            return BaseResponse(
                code=1,
                msg=err_msg
            )

        # 保存结果
        img_prefix = datetime.datetime.now().strftime("%Y%m%d%H%M%S%f")
        filename_prefix = img_prefix + 'partial-repair'

        prompt = ComfyUIPromptTemplate.from_template(path='temps/{}.tpl'.format(payload.way)).render_json(
            FILENAME_PREFIX=json.dumps(filename_prefix),
            BATCH_SIZE=payload.batch_size,
            NOISE_SEED=random.randint(1, 4294967294),
            POS_PROMPT=json.dumps(payload.pos_prompt),
            NEG_PROMPT=json.dumps(payload.neg_prompt),
            INPUT_IMG=json.dumps(payload.input_img),
            INPUT_MASK_IMG=json.dumps(payload.input_mask_img)
        )
    elif payload.way == 'padding-img':
        logger.info("padding-img {}".format(payload.id))
        if not all([payload.input_img, payload.pad_top, payload.pad_bottom, payload.pad_left, payload.pad_right]):
            err_msg = f'缺少参数'
            logger.error(err_msg)
            return BaseResponse(
                code=1,
                msg=err_msg
            )

        # 保存结果
        img_prefix = datetime.datetime.now().strftime("%Y%m%d%H%M%S%f")
        filename_prefix = img_prefix + 'padding-img'

        prompt = ComfyUIPromptTemplate.from_template(path='temps/{}.tpl'.format(payload.way)).render_json(
            FILENAME_PREFIX=json.dumps(filename_prefix),
            INPUT_IMG=json.dumps(payload.input_img),
            PAD_LEFT=payload.pad_left,
            PAD_TOP=payload.pad_top,
            PAD_RIGHT=payload.pad_right,
            PAD_BOTTOM=payload.pad_bottom,
            NOISE_SEED=random.randint(1, 4294967294),
        )
    elif payload.way == 'matting-img':
        logger.info("matting-img {}".format(payload.id))
        if not all([payload.input_img]):
            err_msg = f'缺少参数'
            logger.error(err_msg)
            return BaseResponse(
                code=1,
                msg=err_msg
            )

        # 保存结果
        img_prefix = datetime.datetime.now().strftime("%Y%m%d%H%M%S%f")
        filename_prefix = img_prefix + 'matting-img'

        prompt = ComfyUIPromptTemplate.from_template(path='temps/{}.tpl'.format(payload.way)).render_json(
            FILENAME_PREFIX=json.dumps(filename_prefix),
            INPUT_IMG=json.dumps(payload.input_img),
        )
    elif payload.way == 'scaleup':
        logger.info("scaleup {}".format(payload.id))
        if not all([payload.input_img, payload.pixel]):
            err_msg = f'缺少参数'
            logger.error(err_msg)
            return BaseResponse(
                code=1,
                msg=err_msg
            )

        if not 1024 <= payload.pixel <= 8192:
            err_msg = f'`pixel`像素提升超出范围 [1024,8192]'
            logger.error(err_msg)
            return BaseResponse(
                code=1,
                msg=err_msg
            )

        # 保存结果
        img_prefix = datetime.datetime.now().strftime("%Y%m%d%H%M%S%f")
        filename_prefix = img_prefix + 'scaleup'

        prompt = ComfyUIPromptTemplate.from_template(path='temps/{}.tpl'.format(payload.way)).render_json(
            PIXEL=payload.pixel,
            INPUT_IMG=json.dumps(payload.input_img),
            FILENAME_PREFIX=json.dumps(filename_prefix)
        )
    elif payload.way == 'superir-scaleup':
        logger.info("superir-scaleup {}".format(payload.id))
        if not all([payload.input_img, payload.pixel]):
            err_msg = f'缺少参数'
            logger.error(err_msg)
            return BaseResponse(
                code=1,
                msg=err_msg
            )

        if not 1024 <= payload.pixel <= 8192:
            err_msg = f'`pixel`像素提升超出范围 [1024,3072]'
            logger.error(err_msg)
            return BaseResponse(
                code=1,
                msg=err_msg
            )

        # 保存结果
        img_prefix = datetime.datetime.now().strftime("%Y%m%d%H%M%S%f")
        filename_prefix = img_prefix + 'superir-scaleup'

        prompt = ComfyUIPromptTemplate.from_template(path='temps/{}.tpl'.format(payload.way)).render_json(
            PIXEL=payload.pixel,
            INPUT_IMG=json.dumps(payload.input_img),
            FILENAME_PREFIX=json.dumps(filename_prefix),
            NOISE_SEED=random.randint(1, 4294967294),
        )

    elif payload.way == "qwen-image":
        logger.info("Qwen-Image2512文生图 {}".format(payload.id))

        if not all([payload.output_width, payload.output_height, payload.batch_size, payload.pos_prompt]):
            err_msg = f'缺少必要参数（output_width/output_height/batch_size/pos_prompt）'
            logger.error(err_msg)
            return BaseResponse(
                code=1,
                msg=err_msg
            )

        if payload.qwen_steps < 1 or payload.qwen_steps > 100:
            err_msg = f'`qwen_steps` 超出范围 [1,100]'
            logger.error(err_msg)
            return BaseResponse(
                code=1,
                msg=err_msg
            )
        if payload.qwen_cfg < 1.0 or payload.qwen_cfg > 10.0:
            err_msg = f'`qwen_cfg` 超出范围 [1.0,10.0]'
            logger.error(err_msg)
            return BaseResponse(
                code=1,
                msg=err_msg
            )
        
        img_prefix = datetime.datetime.now().strftime("%Y%m%d%H%M%S%f")
        filename_prefix = img_prefix + "qwen-image"
        
        prompt = ComfyUIPromptTemplate.from_template(path='temps/{}.tpl'.format(payload.way)).render_json(
            FILENAME_PREFIX=json.dumps(filename_prefix),  # 文件名前缀（字符串需JSON序列化）
            WIDTH=payload.output_width,                  # 宽度（数字）
            HEIGHT=payload.output_height,                # 高度（数字）
            NOISE_SEED=random.randint(1, 4294967294),    # 随机种子（数字）
            POS_PROMPT=json.dumps(payload.pos_prompt),   # 正向提示词（字符串需JSON序列化）
            NEG_PROMPT=json.dumps(payload.neg_prompt if payload.neg_prompt else ""),  # 负向提示词
            STEPS=payload.qwen_steps,                    # 采样步数（数字）
            CFG=payload.qwen_cfg                         # CFG系数（数字）
        )

    elif payload.way == "qwen-image-edit":
        logger.info("Qwen-Image-Edit2511 图像编辑 {}".format(payload.id))
        if not all([payload.input_img, payload.pos_prompt]):
            err_msg = f'缺少必要参数'
            logger.error(err_msg)
            return BaseResponse(
                code=1,
                msg=err_msg
            )

        if payload.qwen_steps < 1 or payload.qwen_steps > 100:
            err_msg = f'`qwen_steps` 超出范围 [1,100]'
            logger.error(err_msg)
            return BaseResponse(code=1, msg=err_msg)
        
        if payload.qwen_cfg < 1.0 or payload.qwen_cfg > 10.0:
            err_msg = f'`qwen_cfg` 超出范围 [1.0,10.0]'
            logger.error(err_msg)
            return BaseResponse(code=1, msg=err_msg)
        
        if payload.denose_number < 0.0 or payload.denose_number > 1.0:
            err_msg = f'`denose_number` 去噪强度超出范围 [0.0,1.0]'
            logger.error(err_msg)
            return BaseResponse(code=1, msg=err_msg)
        
        img_prefix = datetime.datetime.now().strftime("%Y%m%d%H%M%S%f")
        filename_prefix = img_prefix + "qwen-image-edit2511"

        prompt = ComfyUIPromptTemplate.from_template(path='temps/{}.tpl'.format(payload.way)).render_json(
            FILENAME_PREFIX=json.dumps(filename_prefix),
            INPUT_IMAGE_PATH=json.dumps(payload.input_img),
            POS_PROMPT=json.dumps(payload.pos_prompt),
            NEG_PROMPT=json.dumps(payload.neg_prompt if payload.neg_prompt else ""),
            NOISE_SEED=random.randint(1, 4294967294),
            STEPS=payload.qwen_steps,
            DENOISE=payload.denose_number,
            CFG=payload.qwen_cfg  
        )
        
    elif payload.way == "z-image":
        logger.info("Z-Image 文生图 {}".format(payload.id))
        if not all([payload.output_width, payload.output_height, payload.batch_size, payload.pos_prompt]):
            err_msg = f'缺少必要参数（output_width/output_height/batch_size/pos_prompt）'
            logger.error(err_msg)
            return BaseResponse(
                code=1,
                msg=err_msg
            )
        if payload.z_steps < 1 or payload.z_steps > 100:
            err_msg = f'`steps` 超出范围 [1,100]'
            logger.error(err_msg)
            return BaseResponse(
                code=1,
                msg=err_msg
            )
        if payload.z_cfg < 1.0 or payload.z_cfg > 10.0:
            err_msg = f'`cfg` 超出范围 [1.0,10.0]'
            logger.error(err_msg)
            return BaseResponse(
                code=1,
                msg=err_msg
            )
        
        img_prefix = datetime.datetime.now().strftime("%Y%m%d%H%M%S%f")
        filename_prefix = img_prefix + "z-image"
        prompt = ComfyUIPromptTemplate.from_template(path='temps/{}.tpl'.format(payload.way)).render_json(
            FILENAME_PREFIX=json.dumps(filename_prefix), 
            WIDTH=payload.output_width,                 
            HEIGHT=payload.output_height,                
            NOISE_SEED=random.randint(1, 4294967294),   
            POS_PROMPT=json.dumps(payload.pos_prompt),   
            NEG_PROMPT=json.dumps(payload.neg_prompt if payload.neg_prompt else ""), 
            STEPS=payload.z_steps,                   
            CFG=payload.z_cfg,                              
            UNET_NAME=json.dumps(getattr(payload, 'unet_name', "z_image_bf16.safetensors")),
            CLIP_NAME=json.dumps(getattr(payload, 'clip_name', "qwen_3_4b.safetensors")),
            VAE_NAME=json.dumps(getattr(payload, 'vae_name', "ae.safetensors"))
        )
    elif payload.way == "z-image-turbo":
        logger.info("Z-Image-Turbo 文生图 {}".format(payload.id))
        if not all([payload.output_width, payload.output_height, payload.batch_size, payload.pos_prompt]):
            err_msg = f'缺少必要参数（output_width/output_height/batch_size/pos_prompt）'
            logger.error(err_msg)
            return BaseResponse(code=1, msg=err_msg)
        if payload.z_turbo_steps < 1 or payload.z_turbo_steps > 20:
            err_msg = f'`steps` 超出范围 [1,20]（Turbo版推荐8~15）'
            logger.error(err_msg)
            return BaseResponse(code=1, msg=err_msg)
        
        img_prefix = datetime.datetime.now().strftime("%Y%m%d%H%M%S%f")
        filename_prefix = img_prefix + "z-image-turbo"
        
        prompt = ComfyUIPromptTemplate.from_template(path='temps/{}.tpl'.format(payload.way)).render_json(
            FILENAME_PREFIX=json.dumps(filename_prefix),
            WIDTH=payload.output_width,
            HEIGHT=payload.output_height,
            NOISE_SEED=random.randint(1, 4294967294),
            POS_PROMPT=json.dumps(payload.pos_prompt),
            STEPS=payload.z_turbo_steps,
            UNET_NAME=json.dumps(getattr(payload, 'unet_name', "z_image_turbo_bf16.safetensors")),
            CLIP_NAME=json.dumps(getattr(payload, 'clip_name', "qwen_3_4b.safetensors")),
            VAE_NAME=json.dumps(getattr(payload, 'vae_name', "ae.safetensors"))
        )
    elif payload.way == "ERNIEIMAGE-txt2img":
        logger.info("ERNIE-Image 文生图 {}".format(payload.id))

        # 必要参数校验
        if not all([payload.output_width, payload.output_height, payload.batch_size, payload.pos_prompt]):
            err_msg = f'缺少必要参数（output_width/output_height/batch_size/pos_prompt）'
            logger.error(err_msg)
            return BaseResponse(code=1, msg=err_msg)

        # 参数范围校验
        if payload.ernie_steps < 1 or payload.ernie_steps > 100:
            err_msg = f'`ernie_steps` 超出范围 [1,100]'
            logger.error(err_msg)
            return BaseResponse(code=1, msg=err_msg)

        if payload.ernie_cfg < 1.0 or payload.ernie_cfg > 20.0:
            err_msg = f'`ernie_cfg` 超出范围 [1.0,20.0]'
            logger.error(err_msg)
            return BaseResponse(code=1, msg=err_msg)

        # 生成文件名前缀
        img_prefix = datetime.datetime.now().strftime("%Y%m%d%H%M%S%f")
        filename_prefix = img_prefix + "ERNIEIMAGE-txt2img"

        prompt = ComfyUIPromptTemplate.from_template(path='temps/{}.tpl'.format(payload.way)).render_json(
            FILENAME_PREFIX=json.dumps(filename_prefix),
            WIDTH=payload.output_width,
            HEIGHT=payload.output_height,
            BATCH_SIZE=payload.batch_size,
            NOISE_SEED=random.randint(1, 4294967294),
            POS_PROMPT=json.dumps(payload.pos_prompt),
            STEPS=payload.ernie_steps,
            CFG=payload.ernie_cfg,
        )
    elif payload.way == "ERNIEIMAGE-txt2img-turbo":
        logger.info("ERNIE-Image-Turbo 文生图 {}".format(payload.id))

        # 必要参数校验
        if not all([payload.output_width, payload.output_height, payload.batch_size, payload.pos_prompt]):
            err_msg = f'缺少必要参数（output_width/output_height/batch_size/pos_prompt）'
            logger.error(err_msg)
            return BaseResponse(code=1, msg=err_msg)

        # 参数范围校验
        if payload.ernie_turbo_steps < 1 or payload.ernie_turbo_steps > 20:
            err_msg = f'`ernie_turbo_steps` 超出范围 [1,20]（Turbo版推荐4~12）'
            logger.error(err_msg)
            return BaseResponse(code=1, msg=err_msg)

        if payload.ernie_turbo_cfg < 0.1 or payload.ernie_turbo_cfg > 5.0:
            err_msg = f'`ernie_turbo_cfg` 超出范围 [0.1,5.0]'
            logger.error(err_msg)
            return BaseResponse(code=1, msg=err_msg)

        # 生成文件名前缀
        img_prefix = datetime.datetime.now().strftime("%Y%m%d%H%M%S%f")
        filename_prefix = img_prefix + "ERNIEIMAGE-txt2img-turbo"

        prompt = ComfyUIPromptTemplate.from_template(path='temps/{}.tpl'.format(payload.way)).render_json(
            FILENAME_PREFIX=json.dumps(filename_prefix),
            WIDTH=payload.output_width,
            HEIGHT=payload.output_height,
            BATCH_SIZE=payload.batch_size,
            NOISE_SEED=random.randint(1, 4294967294),
            POS_PROMPT=json.dumps(payload.pos_prompt),
            STEPS=payload.ernie_turbo_steps,
            CFG=payload.ernie_turbo_cfg,
        )
    elif payload.way == "LTX2.3-txt2video":
        logger.info("LTX2.3 文生视频 {}".format(payload.id))

        # 必要参数校验
        if not payload.pos_prompt:
            err_msg = f'缺少必要参数：pos_prompt'
            logger.error(err_msg)
            return BaseResponse(code=1, msg=err_msg)

        # 参数范围校验
        if payload.ltx_width < 128 or payload.ltx_width > 1920:
            err_msg = f'`ltx_width` 超出范围 [128, 1920]'
            logger.error(err_msg)
            return BaseResponse(code=1, msg=err_msg)

        if payload.ltx_height < 128 or payload.ltx_height > 1080:
            err_msg = f'`ltx_height` 超出范围 [128, 1080]'
            logger.error(err_msg)
            return BaseResponse(code=1, msg=err_msg)

        if payload.ltx_frame_rate < 1 or payload.ltx_frame_rate > 60:
            err_msg = f'`ltx_frame_rate` 超出范围 [1, 60]'
            logger.error(err_msg)
            return BaseResponse(code=1, msg=err_msg)

        if payload.ltx_duration < 1 or payload.ltx_duration > 30:
            err_msg = f'`ltx_duration` 超出范围 [1, 30]'
            logger.error(err_msg)
            return BaseResponse(code=1, msg=err_msg)

        # 生成文件名前缀
        img_prefix = datetime.datetime.now().strftime("%Y%m%d%H%M%S%f")
        filename_prefix = "video/" + img_prefix + "LTX2.3-txt2video"

        prompt = ComfyUIPromptTemplate.from_template(path='temps/{}.tpl'.format(payload.way)).render_json(
            FILENAME_PREFIX=json.dumps(filename_prefix),
            WIDTH=payload.ltx_width,
            HEIGHT=payload.ltx_height,
            FRAME_RATE=payload.ltx_frame_rate,
            DURATION=payload.ltx_duration,
            NOISE_SEED_1=random.randint(1, 4294967294),
            NOISE_SEED_2=random.randint(1, 4294967294),
            POS_PROMPT=json.dumps(payload.pos_prompt),
        )
    elif payload.way == "LTX2.3-img2video":
        logger.info("LTX2.3 图生视频 {}".format(payload.id))

        # 必要参数校验
        if not payload.pos_prompt:
            err_msg = f'缺少必要参数：pos_prompt'
            logger.error(err_msg)
            return BaseResponse(code=1, msg=err_msg)

        if not payload.input_img:
            err_msg = f'缺少必要参数：input_img（输入图片路径）'
            logger.error(err_msg)
            return BaseResponse(code=1, msg=err_msg)

        # 参数范围校验
        if payload.ltx_width < 128 or payload.ltx_width > 1920:
            err_msg = f'`ltx_width` 超出范围 [128, 1920]'
            logger.error(err_msg)
            return BaseResponse(code=1, msg=err_msg)

        if payload.ltx_height < 128 or payload.ltx_height > 1080:
            err_msg = f'`ltx_height` 超出范围 [128, 1080]'
            logger.error(err_msg)
            return BaseResponse(code=1, msg=err_msg)

        if payload.ltx_frame_rate < 1 or payload.ltx_frame_rate > 60:
            err_msg = f'`ltx_frame_rate` 超出范围 [1, 60]'
            logger.error(err_msg)
            return BaseResponse(code=1, msg=err_msg)

        if payload.ltx_duration < 1 or payload.ltx_duration > 30:
            err_msg = f'`ltx_duration` 超出范围 [1, 30]'
            logger.error(err_msg)
            return BaseResponse(code=1, msg=err_msg)

        # input_img 取第一张（支持字符串或列表）
        input_img = payload.input_img if isinstance(payload.input_img, str) else payload.input_img[0]

        # 生成文件名前缀
        img_prefix = datetime.datetime.now().strftime("%Y%m%d%H%M%S%f")
        filename_prefix = "video/" + img_prefix + "LTX2.3-img2video"

        prompt = ComfyUIPromptTemplate.from_template(path='temps/{}.tpl'.format(payload.way)).render_json(
            FILENAME_PREFIX=json.dumps(filename_prefix),
            WIDTH=payload.ltx_width,
            HEIGHT=payload.ltx_height,
            FRAME_RATE=payload.ltx_frame_rate,
            DURATION=payload.ltx_duration,
            NOISE_SEED_1=random.randint(1, 4294967294),
            NOISE_SEED_2=random.randint(1, 4294967294),
            POS_PROMPT=json.dumps(payload.pos_prompt),
            INPUT_IMG=json.dumps(input_img),
        )
    else:
        err_msg = f'不支持的调用方式 {payload.way}'
        logger.error(err_msg)
        return BaseResponse(
            code=1,
            msg=err_msg
        )

    logger.info('【START】ComfyUI生成')
    client_id = payload.id
    logger.info("client id {}".format(client_id))
    VIDEO_WAYS = {'LTX2.3-txt2video', 'LTX2.3-img2video'}
    if payload.way in VIDEO_WAYS:
        filenames, images = await run_in_threadpool(get_videos, comfyui_server_addr, prompt, client_id=client_id)
    else:
        filenames, images = await run_in_threadpool(get_images, comfyui_server_addr, prompt, client_id=client_id)
    logger.info('【END】ComfyUI生成')

    return_files = []
    if payload.return_format == "URL":
        # 上传文件到OSS
        logger.info('【START】上传图片到OSS')
        for filename, image_data in zip(filenames, images):
            img = await run_in_threadpool(oss_cli.upload, image_data, filename=filename)
            return_files.append(img)
        logger.info('【END】上传图片到OSS')
    else:
        for img in images:
            return_files.append(base64.b64encode(img).decode())

    # 视频请求返回 videos 字段，图片请求返回 images 字段
    is_video = payload.way in VIDEO_WAYS
    return BaseResponse(
        code=0,
        data={
            "videos" if is_video else "images": return_files
        },
        msg='success'
    )


if __name__ == '__main__':
    uvicorn.run(app,port=8001)

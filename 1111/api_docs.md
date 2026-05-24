## 通用信息
- **协议**: HTTP/HTTPS

- **域名**: `http://192.168.16.85:5061`

- **版本**: v1

- **格式**: JSON

  


## 接口列表

#### 1、ComfyUI API

- **接口描述**

  依据不用方式请求comfyui-api，生成图像

- **请求方式**

  `POST`

- **URL**

  `/api/comfyui/generate`

- **请求参数**

  | 参数名         | 类型   | 必填 | 描述                                                         | 默认值         |
  | -------------- | ------ | ---- | ------------------------------------------------------------ | -------------- |
  | id             | string | 是   | 会话ID，为随机生成的uuid4，每一次请求都必传                  |                |
  | pos_prompt     | string | 否   | 正向提示词                                                   |                |
  | neg_prompt     | string | 否   | 方向提示词                                                   |                |
  | output_width   | int    | 否   | 生产图片的宽                                                 | 512            |
  | output_height  | int    | 否   | 生产图片的长                                                 | 512            |
  | batch_size     | int    | 否   | 生成的图片数量                                               | 1              |
  | denose_number  | float  | 否   | 降噪强度，范围0~1，越接近于1.0，生成的图自由度越高，适用于文生图；越接近于0，生成的图像自由度越低，适用于图生图或局部修复等 | 0.5            |
  | input_img      | string | 否   | 输入图                                                       |                |
  | input_mask_img | string | 否   | 输入掩码图                                                   |                |
  | input_ref_img  | string | 否   | 输入参考图                                                   |                |
  | way            | string | 是   | 调用方式，包含以下几种：<br />1. **normal-txt2img**: Flux文生图<br />2. **normal-txt2img-pad**: Flux文生图垫图<br />3. **partial-repair**: 局部重绘<br />4. **flux-lora-t2i**: Flux专业版<br />5. **flux-lora-t2i-pro**: Flux专业版Controlnet<br />6. **flux-kontext-edit**: FluxKontext文修图<br />7. **padding-img**: AI扩图<br />8. **matting-img**: 抠图<br />9. **scaleup**: 高清放大<br />10. **superir-scaleup**: 超分放大<br />11. **qwen-image**: Qwen-Image文生图<br />12. **qwen-image-edit**: Qwen-Image-Edit文生图 <br />13. **z-image**: z-image文生图文生图<br />14. **z-image-turbo**: z-image-turbo文生图<br />15. **ERNIEIMAGE-txt2img**: ERNIE-Image文生图<br />16. **ERNIEIMAGE-txt2img-turbo**: ERNIE-Image-Turbo文生图<br />17. **LTX2.3-txt2video**: LTX2.3文生视频<br />| normal-txt2img |
  | model_id       | string | 否   | LoRA 模型ID                                                  |                |
  | pad_bottom     | int    | 否   | AI扩图所需参数，往底边扩图分辨率                             |                |
  | pad_left       | int    | 否   | AI扩图所需参数，往左边扩图分辨率                             |                |
  | pad_right      | int    | 否   | AI扩图所需参数，往右边扩图分辨率                             |                |
  | pad_top        | int    | 否   | AI扩图所需参数，往顶边扩图分辨率                             |                |
  | pixel          | int    | 否   | 高清放大、超分放大所需参数，图像放大分辨率                   |                |
  
  - **请求示例**

    1. **Flux文生图（normal-txt2img）**

       ```json
       {
           "id": "637d9f30-d128-4d87-acb5-a44ee8f37513",
           "way": "normal-txt2img",
           "pos_prompt": "一个女孩，长发，穿着红色裙子",
           "output_width": 768,
           "output_height": 1020,
           "batch_size": 1
       }
       ```

    2. **Flux文生图垫图（normal-txt2img-pad）**

       ```json
       {
           "id": "637d9f30-d128-4d87-acb5-a44ee8f37513",
           "way": "normal-txt2img-pad",
           "pos_prompt": "A girl",
           "batch_size": 1,
           "input_ref_img": "https://draw.oss-cn-uat.midea.com/1726195858_unix_%25E6%25B8%2585%25E6%2594%25BE%25E5%25A4%25A7%25E6%25A1%2588%25E4%25BE%258B%25E5%259B%25BE.png"
       }
       ```
    
    3. **局部重绘（partial-repair）**

       ```json
       {
           "id": "2702c6fd-f38c-4dd8-819a-cad8d61a151e",
           "way": "partial-repair",
           "input_img": "https://draw.oss-cn-foshan.midea.com/1752570013416213985_unix_ClLJpAL1NZbGL2XG6qclkw%3D%3D_051925.png",
           "input_mask_img": "https://draw.oss-cn-foshan.midea.com/1752570039851297357_unix_0rXKM72XD2SmMB-nWuLrIg%3D%3D_image.png",
           "pos_prompt": "Small dots on the eyes"
       }
       ```
    
    4. **Flux专业版（flux-lora-t2i）**

       ```json
       {
           "id": "637d9f30-d128-4d87-acb5-a44ee8f37513",
           "way": "flux-lora-t2i",
           "pos_prompt": "A girl",
           "batch_size": 1,
           "output_width": 1024,
           "output_height": 1024,
           "model_id": "无"
       }
       ```
    
    5. **Flux专业版Controlnet（flux-lora-t2i-pro）**

       ```json
       {
           "id": "637d9f30-d128-4d87-acb5-a44ee8f37513",
           "way": "flux-lora-t2i",
           "pos_prompt": "A girl",
           "batch_size": 1,
           "output_width": 1024,
           "output_height": 1024,
           "model_id": "无"
       }
       ```
    
    6. **FluxKontext文修图（flux-kontext-edit）**

       ```json
       {
           "id": "d4b22e3f-b14a-4498-b913-4fc17b086e12",
           "way": "flux-context-edit",
           "pos_prompt": "change women's hair color to red",
           "input_img": "https://draw.oss-cn-foshan.midea.com/1752570013416213985_unix_ClLJpAL1NZbGL2XG6qclkw%3D%3D_051925.png"
       }
       ```

    7. **AI扩图（padding-img）**

       ```json
       {
           "id": "0474e066-dabe-470b-9120-453851a83c08",
           "way": "padding-img",
           "input_img": "https://draw.oss-cn-foshan.midea.com/1752570186951259759_unix_jT1gagV_MtS7qx0_X5s9IQ%253D%253D_%25E6%25B8%2585%25E6%2594%25BE%25E5%25A4%25A7%25E6%25A1%2588%25E4%25BE%258B%25E5%259B%25BE.png",
           "pad_left": 159,
           "pad_right": 159,
           "pad_top": 119,
           "pad_bottom": 119
       }
       ```
    
    8. **抠图（matting-img）**

       ```json
       {
           "id": "0474e066-dabe-470b-9120-453851a83c08",
           "way": "matting-img",
           "input_img": "https://draw.oss-cn-foshan.midea.com/1752570186951259759_unix_jT1gagV_MtS7qx0_X5s9IQ%253D%253D_%25E6%25B8%2585%25E6%2594%25BE%25E5%25A4%25A7%25E6%25A1%2588%25E4%25BE%258B%25E5%259B%25BE.png"
       }
       ```
    
    9. **高清放大（scaleup）**

       ```json
       {
           "id": "1a9a5b2f-2e07-478f-8043-fc477e050f17",
           "way": "scaleup",
           "input_img": "https://draw.oss-cn-uat.midea.com/1726195858_unix_%E6%B8%85%E6%94%BE%E5%A4%A7%E6%A1%88%E4%BE%8B%E5%9B%BE.png",
           "pixel": 2048
       }
       ```
    
    10. **超分放大（superir-scaleup）**
        ```json
        {
           "id": "955dfa7c-5370-478d-b760-76646171bef3",
           "way": "superir-scaleup",
           "input_img": "https://draw.oss-cn-uat.midea.com/1726195858_unix_%E6%B8%85%E6%94%BE%E5%A4%A7%E6%A1%88%E4%BE%8B%E5%9B%BE.png",
           "pixel": 2048
        }
        ```

    11. **Qwen-Image文生图（qwen-image）**
        ```json
        {
            "id": "test_qwen_001",
            "pos_prompt": "A girl",
            "neg_prompt": "",
            "output_width": 1328,
            "output_height": 1328,
            "batch_size": 1,
            "way": "qwen-image",
        }
        ```

    12. **Qwen-Image-Edit文生图（qwen-image-edit）**
        ```json
        {
            "id": "edit-20260309170000-001",
            "way": "qwen-image-edit",
            "input_img": "https://draw.oss-cn-uat.midea.com/1726195858_unix_%E6%B8%85%E6%94%BE%E5%A4%A7%E6%A1%88%E4%BE%8B%E5%9B%BE.png",  
            "pos_prompt": "将图中衣服换成红色",
            "denose_number": 0.9
        }
        ``` 
    13. **z-image（z-image）**
        ```json
        {
            "id": "z-image",
            "way": "z-image",
            "output_width": 1024,
            "output_height": 1024,
            "batch_size": 1,
            "pos_prompt": "一个女孩，长发，穿白裙子"
            }
        ```
    14. **z-image-turbo（z-image-turbo）**
        ```json
        {
            "id": "z-image-turbo",
            "way": "z-image-turbo",
            "output_width": 1024,
            "output_height": 1024,
            "batch_size": 1,
            "pos_prompt": "一个女孩，长发，穿白裙子"
        }
        ```
    15. **ERNIE-Image文生图（ERNIEIMAGE-txt2img）**
        ```json
        {
            "id": "ernie-image-001",
            "way": "ERNIEIMAGE-txt2img",
            "pos_prompt": "一个女孩，长发，穿着红色裙子",
            "output_width": 1024,
            "output_height": 1024,
            "batch_size": 1,
            "ernie_steps": 50,
            "ernie_cfg": 4
        }
        ```

    16. **ERNIE-Image-Turbo文生图（ERNIEIMAGE-txt2img-turbo）**
        ```json
        {
            "id": "ernie-image-turbo-001",
            "way": "ERNIEIMAGE-txt2img-turbo",
            "pos_prompt": "一个女孩，长发，穿着红色裙子",
            "output_width": 1024,
            "output_height": 1024,
            "batch_size": 1,
            "ernie_turbo_steps": 8,
            "ernie_turbo_cfg": 1
        }
        ```

    17. **LTX2.3文生视频（LTX2.3-txt2video）**
        ```json
        {
            "id": "ltx-video-001",
            "way": "LTX2.3-txt2video",
            "pos_prompt": "A handsome bartender making cocktails, cinematic lighting, 8K",
            "ltx_width": 1280,
            "ltx_height": 720,
            "ltx_frame_rate": 25,
            "ltx_duration": 5
        }
        ```

- **响应参数**

  | 参数名 | 类型   | 描述         |
  | ------ | ------ |------------|
  | code   | int    | 返回码：200为成功 |
  | msg    | string | 返回消息       |
  | data   | object | 返回体        |

- **响应示例**

  ```json
  {
      "code": 200,
      "msg": "success",
      "data": null
  }
  ```
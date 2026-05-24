{
  "6": {
    "inputs": {
      "text": {{ PROMPT_TEXT }},
      "clip": [
        "38",
        1
      ]
    },
    "class_type": "CLIPTextEncode",
    "_meta": {
      "title": "CLIP文本编码器"
    }
  },
  "8": {
    "inputs": {
      "samples": [
        "13",
        0
      ],
      "vae": [
        "10",
        0
      ]
    },
    "class_type": "VAEDecode",
    "_meta": {
      "title": "VAE解码"
    }
  },
  "9": {
    "inputs": {
      "filename_prefix": {{ FILENAME_PREFIX }},
      "images": [
        "8",
        0
      ]
    },
    "class_type": "SaveImage",
    "_meta": {
      "title": "保存图像"
    }
  },
  "10": {
    "inputs": {
      "vae_name": "models--black-forest-labs--FLUX.1-Kontext-dev/ae.safetensors"
    },
    "class_type": "VAELoader",
    "_meta": {
      "title": "VAE加载器"
    }
  },
  "11": {
    "inputs": {
      "clip_name1": "t5xxl_fp8_e4m3fn.safetensors",
      "clip_name2": "ViT-L-14-TEXT-detail-improved-hiT-GmP-HF.safetensors",
      "type": "flux",
      "device": "default"
    },
    "class_type": "DualCLIPLoader",
    "_meta": {
      "title": "双CLIP加载器"
    }
  },
  "12": {
    "inputs": {
      "unet_name": "flux1-dev-fp8.safetensors",
      "weight_dtype": "fp8_e4m3fn"
    },
    "class_type": "UNETLoader",
    "_meta": {
      "title": "UNET加载器"
    }
  },
  "13": {
    "inputs": {
      "noise": [
        "25",
        0
      ],
      "guider": [
        "22",
        0
      ],
      "sampler": [
        "16",
        0
      ],
      "sigmas": [
        "17",
        0
      ],
      "latent_image": [
        "27",
        0
      ]
    },
    "class_type": "SamplerCustomAdvanced",
    "_meta": {
      "title": "自定义采样器(高级)"
    }
  },
  "16": {
    "inputs": {
      "sampler_name": "euler"
    },
    "class_type": "KSamplerSelect",
    "_meta": {
      "title": "K采样器选择"
    }
  },
  "17": {
    "inputs": {
      "scheduler": "simple",
      "steps": 20,
      "denoise": {{ DENOISE_RATIO }},
      "model": [
        "30",
        0
      ]
    },
    "class_type": "BasicScheduler",
    "_meta": {
      "title": "基础调度器"
    }
  },
  "22": {
    "inputs": {
      "model": [
        "30",
        0
      ],
      "conditioning": [
        "26",
        0
      ]
    },
    "class_type": "BasicGuider",
    "_meta": {
      "title": "基础引导"
    }
  },
  "25": {
    "inputs": {
      "noise_seed": {{ NOISE_SEED }}
    },
    "class_type": "RandomNoise",
    "_meta": {
      "title": "随机噪波"
    }
  },
  "26": {
    "inputs": {
      "guidance": 3.5,
      "conditioning": [
        "6",
        0
      ]
    },
    "class_type": "FluxGuidance",
    "_meta": {
      "title": "Flux引导"
    }
  },
  "27": {
    "inputs": {
      "width": {{ WIDTH }},
      "height": {{ HEIGHT }},
      "batch_size": {{ BATCH_SIZE }}
    },
    "class_type": "EmptySD3LatentImage",
    "_meta": {
      "title": "空Latent_SD3"
    }
  },
  "30": {
    "inputs": {
      "max_shift": 1.1500000000000001,
      "base_shift": 0.5000000000000001,
      "width": {{ WIDTH }},
      "height": {{ HEIGHT }},
      "model": [
        "38",
        0
      ]
    },
    "class_type": "ModelSamplingFlux",
    "_meta": {
      "title": "模型采样算法Flux"
    }
  },
  "38": {
    "inputs": {
    "lora_name": {{ LORA }},
    "strength_model": {{ LORA_STRENGTH }},
    "strength_clip": {{ LORA_STRENGTH }},
    "model": [
        "53",
        0
      ],
      "clip": [
        "53",
        1
      ]
    },
    "class_type": "LoraLoader",
    "_meta": {
      "title": "LoRA加载器"
    }
  },
  "53": {
    "inputs": {
      "lora_name": "flux_lora/AWPortrait-FL-lora.safetensors",
      "strength_model": 0,
      "strength_clip": 0,
      "model": [
        "12",
        0
      ],
      "clip": [
        "11",
        0
      ]
    },
    "class_type": "LoraLoader",
    "_meta": {
      "title": "LoRA加载器"
    }
  }
}
{
  "23": {
    "inputs": {
      "image": {{ IMG_CTL1 }}
    },
    "class_type": "LoadImage",
    "_meta": {
      "title": "加载图像"
    }
  },
  "25": {
    "inputs": {
      "width": {{ WIDTH }},
      "height": {{ HEIGHT }},
      "batch_size": {{ BATCH_SIZE }}
    },
    "class_type": "EmptyLatentImage",
    "_meta": {
      "title": "空Latent图像"
    }
  },
  "28": {
    "inputs": {
      "width": 768,
      "height": 1024,
      "interpolation": "nearest",
      "method": "stretch",
      "condition": "always",
      "multiple_of": 0,
      "image": [
        "23",
        0
      ]
    },
    "class_type": "ImageResize+",
    "_meta": {
      "title": "🔧 Image Resize"
    }
  },
  "32": {
    "inputs": {
      "unet_name": "flux1-dev-fp8.safetensors",
      "weight_dtype": "fp8_e4m3fn"
    },
    "class_type": "UNETLoader",
    "_meta": {
      "title": "UNet加载器"
    }
  },
  "33": {
    "inputs": {
      "clip_name1": "t5xxl_fp8_e4m3fn.safetensors",
      "clip_name2": "clip_l.safetensors",
      "type": "flux",
      "device": "default"
    },
    "class_type": "DualCLIPLoader",
    "_meta": {
      "title": "双CLIP加载器"
    }
  },
  "34": {
    "inputs": {
      "vae_name": "models--black-forest-labs--FLUX.1-dev/ae.safetensors"
    },
    "class_type": "VAELoader",
    "_meta": {
      "title": "加载VAE"
    }
  },
  "36": {
    "inputs": {
      "strength": {{ STRENGTH_CTRL1 }},
      "start_percent": 0,
      "end_percent": 0.6000000000000001,
      "positive": [
        "66",
        0
      ],
      "negative": [
        "67",
        0
      ],
      "control_net": [
        "69",
        0
      ],
      "vae": [
        "34",
        0
      ],
      "image": [
        "28",
        0
      ]
    },
    "class_type": "ControlNetApplySD3",
    "_meta": {
      "title": "应用ControlNet"
    }
  },
  "37": {
    "inputs": {
      "preprocessor": "CannyEdgePreprocessor",
      "resolution": 1024,
      "image": [
        "28",
        0
      ]
    },
    "class_type": "AIO_Preprocessor",
    "_meta": {
      "title": "AIO Aux Preprocessor"
    }
  },
  "39": {
    "inputs": {
      "noise": [
        "43",
        0
      ],
      "guider": [
        "40",
        0
      ],
      "sampler": [
        "41",
        0
      ],
      "sigmas": [
        "42",
        0
      ],
      "latent_image": [
        "25",
        0
      ]
    },
    "class_type": "SamplerCustomAdvanced",
    "_meta": {
      "title": "自定义采样器（高级）"
    }
  },
  "40": {
    "inputs": {
      "model": [
        "74",
        0
      ],
      "conditioning": [
        "36",
        0
      ]
    },
    "class_type": "BasicGuider",
    "_meta": {
      "title": "基本引导器"
    }
  },
  "41": {
    "inputs": {
      "sampler_name": "euler"
    },
    "class_type": "KSamplerSelect",
    "_meta": {
      "title": "K采样器选择"
    }
  },
  "42": {
    "inputs": {
      "scheduler": "simple",
      "steps": 20,
      "denoise": {{ DENOISE_RATIO }},
      "model": [
        "74",
        0
      ]
    },
    "class_type": "BasicScheduler",
    "_meta": {
      "title": "基本调度器"
    }
  },
  "43": {
    "inputs": {
      "noise_seed": {{ NOISE_SEED }}
    },
    "class_type": "RandomNoise",
    "_meta": {
      "title": "随机噪波"
    }
  },
  "45": {
    "inputs": {
      "samples": [
        "39",
        0
      ],
      "vae": [
        "34",
        0
      ]
    },
    "class_type": "VAEDecode",
    "_meta": {
      "title": "VAE解码"
    }
  },
  "47": {
    "inputs": {
      "preprocessor": "DepthAnythingPreprocessor",
      "resolution": 1024,
      "image": [
        "28",
        0
      ]
    },
    "class_type": "AIO_Preprocessor",
    "_meta": {
      "title": "AIO Aux Preprocessor"
    }
  },
  "51": {
    "inputs": {
      "preprocessor": "TilePreprocessor",
      "resolution": 1024,
      "image": [
        "28",
        0
      ]
    },
    "class_type": "AIO_Preprocessor",
    "_meta": {
      "title": "AIO Aux Preprocessor"
    }
  },
  "53": {
    "inputs": {
      "preprocessor": "OpenposePreprocessor",
      "resolution": 1024,
      "image": [
        "28",
        0
      ]
    },
    "class_type": "AIO_Preprocessor",
    "_meta": {
      "title": "AIO Aux Preprocessor"
    }
  },
  "66": {
    "inputs": {
      "clip_l": {{ PROMPT_TEXT }},
      "t5xxl": {{ PROMPT_TEXT }},
      "guidance": 4,
      "speak_and_recognation": {
        "__value__": [
          false,
          true
        ]
      },
      "clip": [
        "73",
        1
      ]
    },
    "class_type": "CLIPTextEncodeFlux",
    "_meta": {
      "title": "CLIP文本编码Flux"
    }
  },
  "67": {
    "inputs": {
      "clip_l": "",
      "t5xxl": "",
      "guidance": 4,
      "speak_and_recognation": {
        "__value__": [
          false,
          true
        ]
      },
      "clip": [
        "73",
        1
      ]
    },
    "class_type": "CLIPTextEncodeFlux",
    "_meta": {
      "title": "CLIP文本编码Flux"
    }
  },
  "69": {
    "inputs": {
      "type": {{ CTRL1 }},
      "control_net": [
        "70",
        0
      ]
    },
    "class_type": "SetUnionControlNetType",
    "_meta": {
      "title": "设置UnionControlNet类型"
    }
  },
  "70": {
    "inputs": {
      "control_net_name": "FLUX.1-dev-Controlnet-Union.safetensors"
    },
    "class_type": "ControlNetLoader",
    "_meta": {
      "title": "加载ControlNet模型"
    }
  },
  "71": {
    "inputs": {
      "filename_prefix": {{ FILENAME_PREFIX }},
      "images": [
        "45",
        0
      ]
    },
    "class_type": "SaveImage",
    "_meta": {
      "title": "保存图像"
    }
  },
  "72": {
    "inputs": {
      "lora_name": "flux_lora/AWPortrait-FL-lora.safetensors",
      "strength_model": 0,
      "strength_clip": 0,
      "model": [
        "32",
        0
      ],
      "clip": [
        "33",
        0
      ]
    },
    "class_type": "LoraLoader",
    "_meta": {
      "title": "LoRA加载器"
    }
  },
  "73": {
    "inputs": {
      "lora_name": {{ LORA }},
      "strength_model": {{ LORA_STRENGTH }},
      "strength_clip": {{ LORA_STRENGTH }},
      "model": [
        "72",
        0
      ],
      "clip": [
        "72",
        1
      ]
    },
    "class_type": "LoraLoader",
    "_meta": {
      "title": "LoRA加载器"
    }
  },
  "74": {
    "inputs": {
      "max_shift": 1.1500000000000001,
      "base_shift": 0.4100000000000001,
      "width": 1024,
      "height": 1024,
      "model": [
        "73",
        0
      ]
    },
    "class_type": "ModelSamplingFlux",
    "_meta": {
      "title": "模型采样算法Flux"
    }
  }
}
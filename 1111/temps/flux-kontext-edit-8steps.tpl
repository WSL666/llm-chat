{
  "6": {
    "inputs": {
      "text": {{ POS_PROMPT }},
      "clip": [
        "38",
        0
      ]
    },
    "class_type": "CLIPTextEncode",
    "_meta": {
      "title": "CLIP Text Encode (Positive Prompt)"
    }
  },
  "8": {
    "inputs": {
      "samples": [
        "31",
        0
      ],
      "vae": [
        "39",
        0
      ]
    },
    "class_type": "VAEDecode",
    "_meta": {
      "title": "VAE解码"
    }
  },
  "31": {
    "inputs": {
      "seed": {{ NOISE_SEED }},
      "steps": 8,
      "cfg": 1,
      "sampler_name": "euler",
      "scheduler": "simple",
      "denoise": 1,
      "model": [
        "192",
        0
      ],
      "positive": [
        "35",
        0
      ],
      "negative": [
        "135",
        0
      ],
      "latent_image": [
        "124",
        0
      ]
    },
    "class_type": "KSampler",
    "_meta": {
      "title": "K采样器"
    }
  },
  "35": {
    "inputs": {
      "guidance": 2.5,
      "conditioning": [
        "177",
        0
      ]
    },
    "class_type": "FluxGuidance",
    "_meta": {
      "title": "Flux引导"
    }
  },
  "37": {
    "inputs": {
      "unet_name": "flux1-dev-kontext_fp8_scaled.safetensors",
      "weight_dtype": "default"
    },
    "class_type": "UNETLoader",
    "_meta": {
      "title": "UNet加载器"
    }
  },
  "38": {
    "inputs": {
      "clip_name1": "clip_l.safetensors",
      "clip_name2": "t5xxl_fp8_e4m3fn.safetensors",
      "type": "flux",
      "device": "default"
    },
    "class_type": "DualCLIPLoader",
    "_meta": {
      "title": "双CLIP加载器"
    }
  },
  "39": {
    "inputs": {
      "vae_name": "models--black-forest-labs--FLUX.1-Kontext-dev/ae.safetensors"
    },
    "class_type": "VAELoader",
    "_meta": {
      "title": "加载VAE"
    }
  },
  "124": {
    "inputs": {
      "pixels": [
        "189",
        0
      ],
      "vae": [
        "39",
        0
      ]
    },
    "class_type": "VAEEncode",
    "_meta": {
      "title": "VAE编码"
    }
  },
  "135": {
    "inputs": {
      "conditioning": [
        "6",
        0
      ]
    },
    "class_type": "ConditioningZeroOut",
    "_meta": {
      "title": "条件零化"
    }
  },
  "136": {
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
  "177": {
    "inputs": {
      "conditioning": [
        "6",
        0
      ],
      "latent": [
        "124",
        0
      ]
    },
    "class_type": "ReferenceLatent",
    "_meta": {
      "title": "ReferenceLatent"
    }
  },
  "189": {
    "inputs": {
      "image": {{ INPUT_IMG }}
    },
    "class_type": "LoadImage",
    "_meta": {
      "title": "加载图像"
    }
  },
  "192": {
    "inputs": {
      "lora_name": "flux_lora/Hyper-FLUX.1-dev-8steps-lora.safetensors",
      "strength_model": 0.13000000000000003,
      "model": [
        "37",
        0
      ]
    },
    "class_type": "LoraLoaderModelOnly",
    "_meta": {
      "title": "LoRA加载器（仅模型）"
    }
  }
}
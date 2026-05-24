{
  "9": {
    "inputs": {
      "filename_prefix": {{ FILENAME_PREFIX }},
      "images": [
        "143:141",
        0
      ]
    },
    "class_type": "SaveImage",
    "_meta": {
      "title": "保存图像"
    }
  },
  "41": {
    "inputs": {
      "image": {{ INPUT_IMAGE_PATH }}
    },
    "class_type": "LoadImage",
    "_meta": {
      "title": "加载图像"
    }
  },
  "143:119": {
    "inputs": {
      "shift": 3.1,
      "model": [
        "143:121",
        0
      ]
    },
    "class_type": "ModelSamplingAuraFlow",
    "_meta": {
      "title": "采样算法（AuraFlow）"
    }
  },
  "143:120": {
    "inputs": {
      "vae_name": "qwen_image_vae.safetensors"
    },
    "class_type": "VAELoader",
    "_meta": {
      "title": "加载VAE"
    }
  },
  "143:122": {
    "inputs": {
      "reference_latents_method": "index_timestep_zero",
      "conditioning": [
        "143:124",
        0
      ]
    },
    "class_type": "FluxKontextMultiReferenceLatentMethod",
    "_meta": {
      "title": "FluxKontext多参考潜在方法"
    }
  },
  "143:123": {
    "inputs": {
      "reference_latents_method": "index_timestep_zero",
      "conditioning": [
        "143:126",
        0
      ]
    },
    "class_type": "FluxKontextMultiReferenceLatentMethod",
    "_meta": {
      "title": "FluxKontext多参考潜在方法"
    }
  },
  "143:124": {
    "inputs": {
      "prompt": {{ NEG_PROMPT }},
      "clip": [
        "143:127",
        0
      ],
      "vae": [
        "143:120",
        0
      ],
      "image1": [
        "143:142",
        0
      ]
    },
    "class_type": "TextEncodeQwenImageEditPlus",
    "_meta": {
      "title": "文本编码（QwenImageEditPlus）"
    }
  },
  "143:126": {
    "inputs": {
      "prompt": {{ POS_PROMPT }},
      "clip": [
        "143:127",
        0
      ],
      "vae": [
        "143:120",
        0
      ],
      "image1": [
        "143:142",
        0
      ]
    },
    "class_type": "TextEncodeQwenImageEditPlus",
    "_meta": {
      "title": "TextEncodeQwenImageEditPlus (Positive)"
    }
  },
  "143:129": {
    "inputs": {
      "strength": 1,
      "model": [
        "143:119",
        0
      ]
    },
    "class_type": "CFGNorm",
    "_meta": {
      "title": "CFG归一化"
    }
  },
  "143:131": {
    "inputs": {
      "value": 4
    },
    "class_type": "PrimitiveInt",
    "_meta": {
      "title": "Steps"
    }
  },
  "143:132": {
    "inputs": {
      "value": {{ CFG }}
    },
    "class_type": "PrimitiveFloat",
    "_meta": {
      "title": "CFG"
    }
  },
  "143:133": {
    "inputs": {
      "value": 1
    },
    "class_type": "PrimitiveFloat",
    "_meta": {
      "title": "CFG"
    }
  },
  "143:137": {
    "inputs": {
      "pixels": [
        "143:142",
        0
      ],
      "vae": [
        "143:120",
        0
      ]
    },
    "class_type": "VAEEncode",
    "_meta": {
      "title": "VAE编码"
    }
  },
  "143:141": {
    "inputs": {
      "samples": [
        "143:128",
        0
      ],
      "vae": [
        "143:120",
        0
      ]
    },
    "class_type": "VAEDecode",
    "_meta": {
      "title": "VAE解码"
    }
  },
  "143:128": {
    "inputs": {
      "seed": {{ NOISE_SEED }},
      "steps": {{ STEPS }},
      "cfg": [
        "143:134",
        0
      ],
      "sampler_name": "euler",
      "scheduler": "simple",
      "denoise": {{ DENOISE }},
      "model": [
        "143:135",
        0
      ],
      "positive": [
        "143:123",
        0
      ],
      "negative": [
        "143:122",
        0
      ],
      "latent_image": [
        "143:137",
        0
      ]
    },
    "class_type": "KSampler",
    "_meta": {
      "title": "K采样器"
    }
  },
  "143:139": {
    "inputs": {
      "value": {{ STEPS }}
    },
    "class_type": "PrimitiveInt",
    "_meta": {
      "title": "Steps"
    }
  },
  "143:142": {
    "inputs": {
      "image": [
        "41",
        0
      ]
    },
    "class_type": "FluxKontextImageScale",
    "_meta": {
      "title": "图像缩放为FluxKontext"
    }
  },
  "143:121": {
    "inputs": {
      "unet_name": "qwen_image_edit_2511_fp8mixed.safetensors",
      "weight_dtype": "default"
    },
    "class_type": "UNETLoader",
    "_meta": {
      "title": "UNet加载器"
    }
  },
  "143:127": {
    "inputs": {
      "clip_name": "qwen_2.5_vl_7b_fp8_scaled.safetensors",
      "type": "qwen_image",
      "device": "default"
    },
    "class_type": "CLIPLoader",
    "_meta": {
      "title": "加载CLIP"
    }
  },
  "143:138": {
    "inputs": {
      "value": false
    },
    "class_type": "PrimitiveBoolean",
    "_meta": {
      "title": "Enable 4steps LoRA?"
    }
  },
  "143:135": {
    "inputs": {
      "switch": [
        "143:138",
        0
      ],
      "on_false": [
        "143:129",
        0
      ],
      "on_true": [
        "143:129",
        0
      ]
    },
    "class_type": "ComfySwitchNode",
    "_meta": {
      "title": "Switch (Model)"
    }
  },
  "143:136": {
    "inputs": {
      "switch": [
        "143:138",
        0
      ],
      "on_false": [
        "143:139",
        0
      ],
      "on_true": [
        "143:131",
        0
      ]
    },
    "class_type": "ComfySwitchNode",
    "_meta": {
      "title": "Switch (Steps)"
    }
  },
  "143:134": {
    "inputs": {
      "switch": [
        "143:138",
        0
      ],
      "on_false": [
        "143:132",
        0
      ],
      "on_true": [
        "143:133",
        0
      ]
    },
    "class_type": "ComfySwitchNode",
    "_meta": {
      "title": "Switch (CFG)"
    }
  }
}
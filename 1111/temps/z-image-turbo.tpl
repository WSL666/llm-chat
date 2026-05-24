{
  "28": {
    "inputs": {
      "unet_name": {{ UNET_NAME }},
      "weight_dtype": "default"
    },
    "class_type": "UNETLoader",
    "_meta": {
      "title": "UNet加载器 (Turbo)"
    }
  },
  "30": {
    "inputs": {
      "clip_name": {{ CLIP_NAME }},
      "type": "lumina2",
      "device": "default"
    },
    "class_type": "CLIPLoader",
    "_meta": {
      "title": "加载CLIP (Turbo)"
    }
  },
  "29": {
    "inputs": {
      "vae_name": {{ VAE_NAME }}
    },
    "class_type": "VAELoader",
    "_meta": {
      "title": "加载VAE (Turbo)"
    }
  },
  "27": {
    "inputs": {
      "text": {{ POS_PROMPT }},
      "clip": [
        "30",
        0
      ]
    },
    "class_type": "CLIPTextEncode",
    "_meta": {
      "title": "CLIP Text Encode (Positive Prompt)"
    }
  },
  "33": {
    "inputs": {
      "conditioning": [
        "27",
        0
      ]
    },
    "class_type": "ConditioningZeroOut",
    "_meta": {
      "title": "Conditioning Zero Out (负向提示词替代)"
    }
  },
  "13": {
    "inputs": {
      "width": {{ WIDTH }},
      "height": {{ HEIGHT }},
      "batch_size": 1
    },
    "class_type": "EmptySD3LatentImage",
    "_meta": {
      "title": "空Latent图像（SD3）"
    }
  },
  "11": {
    "inputs": {
      "shift": 3,
      "model": [
        "28",
        0
      ]
    },
    "class_type": "ModelSamplingAuraFlow",
    "_meta": {
      "title": "采样算法（AuraFlow）"
    }
  },
  "3": {
    "inputs": {
      "seed": {{ NOISE_SEED }},
      "steps": {{ STEPS }},
      "cfg": 1.0,
      "sampler_name": "res_multistep",
      "scheduler": "simple",
      "denoise": 1,
      "model": [
        "11",
        0
      ],
      "positive": [
        "27",
        0
      ],
      "negative": [
        "33",
        0
      ],
      "latent_image": [
        "13",
        0
      ]
    },
    "class_type": "KSampler",
    "_meta": {
      "title": "K采样器 (Turbo)"
    }
  },
  "8": {
    "inputs": {
      "samples": [
        "3",
        0
      ],
      "vae": [
        "29",
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
  }
}
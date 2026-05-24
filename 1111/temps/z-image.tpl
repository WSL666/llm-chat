{
  "67": {
    "inputs": {
      "text": {{ POS_PROMPT }},
      "clip": [
        "62",
        0
      ]
    },
    "class_type": "CLIPTextEncode",
    "_meta": {
      "title": "CLIP Text Encode (Positive Prompt)"
    }
  },
  "71": {
    "inputs": {
      "text": {{ NEG_PROMPT }},
      "clip": [
        "62",
        0
      ]
    },
    "class_type": "CLIPTextEncode",
    "_meta": {
      "title": "CLIP Text Encode (Negative Prompt)"
    }
  },
  "68": {
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
  "66": {
    "inputs": {
      "unet_name": {{ UNET_NAME }},
      "weight_dtype": "default"
    },
    "class_type": "UNETLoader",
    "_meta": {
      "title": "UNet加载器"
    }
  },
  "62": {
    "inputs": {
      "clip_name": {{ CLIP_NAME }},
      "type": "lumina2",
      "device": "default"
    },
    "class_type": "CLIPLoader",
    "_meta": {
      "title": "加载CLIP"
    }
  },
  "63": {
    "inputs": {
      "vae_name": {{ VAE_NAME }}
    },
    "class_type": "VAELoader",
    "_meta": {
      "title": "加载VAE"
    }
  },
  "70": {
    "inputs": {
      "shift": 3,
      "model": [
        "66",
        0
      ]
    },
    "class_type": "ModelSamplingAuraFlow",
    "_meta": {
      "title": "采样算法（AuraFlow）"
    }
  },
  "69": {
    "inputs": {
      "seed": {{ NOISE_SEED }},
      "steps": {{ STEPS }},
      "cfg": {{ CFG }},
      "sampler_name": "res_multistep",
      "scheduler": "simple",
      "denoise": 1,
      "model": [
        "70",
        0
      ],
      "positive": [
        "67",
        0
      ],
      "negative": [
        "71",
        0
      ],
      "latent_image": [
        "68",
        0
      ]
    },
    "class_type": "KSampler",
    "_meta": {
      "title": "K采样器"
    }
  },
  "65": {
    "inputs": {
      "samples": [
        "69",
        0
      ],
      "vae": [
        "63",
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
        "65",
        0
      ]
    },
    "class_type": "SaveImage",
    "_meta": {
      "title": "保存图像"
    }
  }
}
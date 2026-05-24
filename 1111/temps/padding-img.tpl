{
  "9": {
    "inputs": {
      "fill": "telea",
      "falloff": 0,
      "image": [
        "22",
        0
      ],
      "mask": [
        "22",
        1
      ]
    },
    "class_type": "INPAINT_MaskedFill",
    "_meta": {
      "title": "Fill Masked Area"
    }
  },
  "10": {
    "inputs": {
      "blur": 40,
      "falloff": 0,
      "image": [
        "9",
        0
      ],
      "mask": [
        "22",
        1
      ]
    },
    "class_type": "INPAINT_MaskedBlur",
    "_meta": {
      "title": "Blur Masked Area"
    }
  },
  "11": {
    "inputs": {
      "ckpt_name": "juggernautXL_v9Rdphoto2Lightning.safetensors"
    },
    "class_type": "CheckpointLoaderSimple",
    "_meta": {
      "title": "Checkpoint加载器(简易)"
    }
  },
  "12": {
    "inputs": {
      "text": "",
      "clip": [
        "11",
        1
      ]
    },
    "class_type": "CLIPTextEncode",
    "_meta": {
      "title": "CLIP文本编码器"
    }
  },
  "13": {
    "inputs": {
      "text": "",
      "clip": [
        "11",
        1
      ]
    },
    "class_type": "CLIPTextEncode",
    "_meta": {
      "title": "CLIP文本编码器"
    }
  },
  "14": {
    "inputs": {
      "positive": [
        "12",
        0
      ],
      "negative": [
        "13",
        0
      ],
      "vae": [
        "11",
        2
      ],
      "pixels": [
        "10",
        0
      ],
      "mask": [
        "22",
        1
      ]
    },
    "class_type": "INPAINT_VAEEncodeInpaintConditioning",
    "_meta": {
      "title": "VAE Encode & Inpaint Conditioning"
    }
  },
  "15": {
    "inputs": {
      "head": "fooocus_inpaint_head.pth",
      "patch": "inpaint_v26.fooocus.patch"
    },
    "class_type": "INPAINT_LoadFooocusInpaint",
    "_meta": {
      "title": "Load Fooocus Inpaint"
    }
  },
  "16": {
    "inputs": {
      "model": [
        "11",
        0
      ],
      "patch": [
        "15",
        0
      ],
      "latent": [
        "14",
        2
      ]
    },
    "class_type": "INPAINT_ApplyFooocusInpaint",
    "_meta": {
      "title": "Apply Fooocus Inpaint"
    }
  },
  "17": {
    "inputs": {
      "model": [
        "16",
        0
      ]
    },
    "class_type": "DifferentialDiffusion",
    "_meta": {
      "title": "Differential Diffusion"
    }
  },
  "18": {
    "inputs": {
      "seed": {{ NOISE_SEED }},
      "steps": 8,
      "cfg": 2,
      "sampler_name": "dpmpp_sde",
      "scheduler": "normal",
      "denoise": 1,
      "model": [
        "17",
        0
      ],
      "positive": [
        "14",
        0
      ],
      "negative": [
        "14",
        1
      ],
      "latent_image": [
        "14",
        3
      ]
    },
    "class_type": "KSampler",
    "_meta": {
      "title": "K采样器"
    }
  },
  "19": {
    "inputs": {
      "samples": [
        "18",
        0
      ],
      "vae": [
        "11",
        2
      ]
    },
    "class_type": "VAEDecode",
    "_meta": {
      "title": "VAE解码"
    }
  },
  "22": {
    "inputs": {
      "left": {{ PAD_LEFT }},
      "top": {{ PAD_TOP }},
      "right": {{ PAD_RIGHT }},
      "bottom": {{ PAD_BOTTOM }},
      "feathering": 60,
      "image": [
        "24",
        0
      ]
    },
    "class_type": "ImagePadForOutpaint",
    "_meta": {
      "title": "外补画板"
    }
  },
  "23": {
    "inputs": {
      "image": {{ INPUT_IMG }}
    },
    "class_type": "LoadImage",
    "_meta": {
      "title": "加载图像"
    }
  },
  "24": {
    "inputs": {
      "max_width": 1024,
      "max_height": 1024,
      "min_width": 0,
      "min_height": 0,
      "crop_if_required": "no",
      "images": [
        "23",
        0
      ]
    },
    "class_type": "ConstrainImage|pysssss",
    "_meta": {
      "title": "限制图像区域"
    }
  },
  "25": {
    "inputs": {
      "x": 0,
      "y": 0,
      "resize_source": false,
      "destination": [
        "22",
        0
      ],
      "source": [
        "19",
        0
      ],
      "mask": [
        "22",
        1
      ]
    },
    "class_type": "ImageCompositeMasked",
    "_meta": {
      "title": "图像遮罩复合"
    }
  },
  "27": {
    "inputs": {
      "filename_prefix": {{ FILENAME_PREFIX }},
      "images": [
        "25",
        0
      ]
    },
    "class_type": "SaveImage",
    "_meta": {
      "title": "保存图像"
    }
  }
}
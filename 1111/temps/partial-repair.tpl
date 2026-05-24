{
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
      "title": "VAE Decode"
    }
  },
  "10": {
    "inputs": {
      "vae_name": "models--black-forest-labs--FLUX.1-dev/ae.safetensors"
    },
    "class_type": "VAELoader",
    "_meta": {
      "title": "Load VAE"
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
      "title": "DualCLIPLoader"
    }
  },
  "12": {
    "inputs": {
      "unet_name": "flux1-dev-fp8.safetensors",
      "weight_dtype": "fp8_e4m3fn"
    },
    "class_type": "UNETLoader",
    "_meta": {
      "title": "Load Diffusion Model"
    }
  },
  "13": {
    "inputs": {
      "noise": [
        "25",
        0
      ],
      "guider": [
        "141",
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
        "139",
        0
      ]
    },
    "class_type": "SamplerCustomAdvanced",
    "_meta": {
      "title": "SamplerCustomAdvanced"
    }
  },
  "16": {
    "inputs": {
      "sampler_name": "euler"
    },
    "class_type": "KSamplerSelect",
    "_meta": {
      "title": "KSamplerSelect"
    }
  },
  "17": {
    "inputs": {
      "scheduler": "beta",
      "steps": 16,
      "denoise": 1,
      "model": [
        "151",
        0
      ]
    },
    "class_type": "BasicScheduler",
    "_meta": {
      "title": "BasicScheduler"
    }
  },
  "25": {
    "inputs": {
      "noise_seed": {{ NOISE_SEED }}
    },
    "class_type": "RandomNoise",
    "_meta": {
      "title": "RandomNoise"
    }
  },
  "35": {
    "inputs": {
      "action": "append",
      "tidy_tags": "no",
      "text_a": {{ POS_PROMPT }},
      "text_b": "",
      "text_c": "",
      "result": ""
    },
    "class_type": "StringFunction|pysssss",
    "_meta": {
      "title": "String Function 🐍"
    }
  },
  "72": {
    "inputs": {
      "clip_l": [
        "35",
        0
      ],
      "t5xxl": [
        "35",
        0
      ],
      "guidance": 3.5,
      "clip": [
        "151",
        1
      ]
    },
    "class_type": "CLIPTextEncodeFlux",
    "_meta": {
      "title": "CLIPTextEncodeFlux"
    }
  },
  "128": {
    "inputs": {
      "strength": 0.8500000000000002,
      "start_percent": 0,
      "end_percent": 1,
      "positive": [
        "72",
        0
      ],
      "negative": [
        "131",
        0
      ],
      "control_net": [
        "133",
        0
      ],
      "vae": [
        "10",
        0
      ],
      "image": [
        "130",
        0
      ],
      "mask": [
        "138",
        0
      ]
    },
    "class_type": "ControlNetInpaintingAliMamaApply",
    "_meta": {
      "title": "ControlNetInpaintingAliMamaApply"
    }
  },
  "130": {
    "inputs": {
      "image": {{ INPUT_IMG }}
    },
    "class_type": "LoadImage",
    "_meta": {
      "title": "Load Image"
    }
  },
  "131": {
    "inputs": {
      "clip_l": "",
      "t5xxl": {{ NEG_PROMPT }},
      "guidance": 3.5,
      "clip": [
        "151",
        1
      ]
    },
    "class_type": "CLIPTextEncodeFlux",
    "_meta": {
      "title": "CLIPTextEncodeFlux"
    }
  },
  "133": {
    "inputs": {
      "control_net_name": "flux_inpaint/FLUX.1-dev-Controlnet-Inpainting-beta.safetensors"
    },
    "class_type": "ControlNetLoader",
    "_meta": {
      "title": "Load ControlNet Model"
    }
  },
  "134": {
    "inputs": {
      "mask": [
        "138",
        0
      ]
    },
    "class_type": "MaskToImage",
    "_meta": {
      "title": "Convert Mask to Image"
    }
  },
  "138": {
    "inputs": {
      "expand": 5,
      "incremental_expandrate": 0,
      "tapered_corners": false,
      "flip_input": false,
      "blur_radius": 2,
      "lerp_alpha": 1,
      "decay_factor": 1,
      "fill_holes": false,
      "mask": [
        "155",
        0
      ]
    },
    "class_type": "GrowMaskWithBlur",
    "_meta": {
      "title": "Grow Mask With Blur"
    }
  },
  "139": {
    "inputs": {
      "width": [
        "152",
        0
      ],
      "height": [
        "152",
        1
      ],
      "batch_size": {{ BATCH_SIZE }}
    },
    "class_type": "EmptySD3LatentImage",
    "_meta": {
      "title": "EmptySD3LatentImage"
    }
  },
  "141": {
    "inputs": {
      "cfg": 3.5,
      "model": [
        "151",
        0
      ],
      "positive": [
        "128",
        0
      ],
      "negative": [
        "128",
        1
      ]
    },
    "class_type": "CFGGuider",
    "_meta": {
      "title": "CFGGuider"
    }
  },
  "150": {
    "inputs": {
      "input_mode": "simple",
      "lora_count": 3,
      "lora_name_1": "flux_lora/Hyper-FLUX.1-dev-16steps-lora.safetensors",
      "lora_wt_1": 0.13000000000000003,
      "model_str_1": 1.0000000000000002,
      "clip_str_1": 1.0000000000000002,
      "lora_name_2": "flux_lora/filmfotos.safetensors",
      "lora_wt_2": 0.8000000000000002,
      "model_str_2": 1.0000000000000002,
      "clip_str_2": 1.0000000000000002,
      "lora_name_3": "flux_lora/富士影调_flux_富士V1.safetensors",
      "lora_wt_3": 0.6000000000000001,
      "model_str_3": 1.0000000000000002,
      "clip_str_3": 1.0000000000000002
    },
    "class_type": "LoRA Stacker",
    "_meta": {
      "title": "LoRA Stacker"
    }
  },
  "151": {
    "inputs": {
      "model": [
        "12",
        0
      ],
      "clip": [
        "11",
        0
      ],
      "lora_stack": [
        "150",
        0
      ]
    },
    "class_type": "CR Apply LoRA Stack",
    "_meta": {
      "title": "💊 CR Apply LoRA Stack"
    }
  },
  "152": {
    "inputs": {
      "image": [
        "153",
        0
      ]
    },
    "class_type": "GetImageSize",
    "_meta": {
      "title": "Get Image Size"
    }
  },
  "153": {
    "inputs": {
      "size": 768,
      "interpolation_mode": "bicubic",
      "image": [
        "130",
        0
      ]
    },
    "class_type": "JWImageResizeByShorterSide",
    "_meta": {
      "title": "Image Resize by Shorter Side"
    }
  },
  "154": {
    "inputs": {
      "image": {{ INPUT_MASK_IMG }}
    },
    "class_type": "LoadImage",
    "_meta": {
      "title": "Load Image"
    }
  },
  "155": {
    "inputs": {
      "channel": "red",
      "image": [
        "154",
        0
      ]
    },
    "class_type": "ImageToMask",
    "_meta": {
      "title": "Image To Mask"
    }
  },
  "156": {
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
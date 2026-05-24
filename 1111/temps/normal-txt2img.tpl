{
  "48": {
    "inputs": {
      "text": [
        "71",
        0
      ],
      "clip": [
        "64",
        1
      ]
    },
    "class_type": "CLIPTextEncode",
    "_meta": {
      "title": "CLIP Text Encode (Prompt)"
    }
  },
  "49": {
    "inputs": {
      "samples": [
        "54",
        0
      ],
      "vae": [
        "51",
        0
      ]
    },
    "class_type": "VAEDecode",
    "_meta": {
      "title": "VAE Decode"
    }
  },
  "50": {
    "inputs": {
      "filename_prefix": {{ FILENAME_PREFIX }},
      "images": [
        "49",
        0
      ]
    },
    "class_type": "SaveImage",
    "_meta": {
      "title": "Save Image"
    }
  },
  "51": {
    "inputs": {
      "vae_name": "models--black-forest-labs--FLUX.1-dev/ae.safetensors"
    },
    "class_type": "VAELoader",
    "_meta": {
      "title": "Load VAE"
    }
  },
  "52": {
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
  "53": {
    "inputs": {
      "unet_name": "flux1-dev-fp8.safetensors",
      "weight_dtype": "fp8_e4m3fn"
    },
    "class_type": "UNETLoader",
    "_meta": {
      "title": "Load Diffusion Model"
    }
  },
  "54": {
    "inputs": {
      "noise": [
        "59",
        0
      ],
      "guider": [
        "56",
        0
      ],
      "sampler": [
        "60",
        0
      ],
      "sigmas": [
        "55",
        0
      ],
      "latent_image": [
        "58",
        0
      ]
    },
    "class_type": "SamplerCustomAdvanced",
    "_meta": {
      "title": "SamplerCustomAdvanced"
    }
  },
  "55": {
    "inputs": {
      "scheduler": "beta",
      "steps": 16,
      "denoise": 1,
      "model": [
        "64",
        0
      ]
    },
    "class_type": "BasicScheduler",
    "_meta": {
      "title": "BasicScheduler"
    }
  },
  "56": {
    "inputs": {
      "model": [
        "64",
        0
      ],
      "conditioning": [
        "48",
        0
      ]
    },
    "class_type": "BasicGuider",
    "_meta": {
      "title": "BasicGuider"
    }
  },
  "58": {
    "inputs": {
      "width": {{ WIDTH }},
      "height": {{ HEIGHT }},
      "batch_size": {{ BATCH_SIZE }}
    },
    "class_type": "EmptyLatentImage",
    "_meta": {
      "title": "Empty Latent Image"
    }
  },
  "59": {
    "inputs": {
      "noise_seed": {{ NOISE_SEED }}
    },
    "class_type": "RandomNoise",
    "_meta": {
      "title": "RandomNoise"
    }
  },
  "60": {
    "inputs": {
      "sampler_name": "euler"
    },
    "class_type": "KSamplerSelect",
    "_meta": {
      "title": "KSamplerSelect"
    }
  },
  "62": {
    "inputs": {
      "clip_name": "longclip-L.pt",
      "clip": [
        "52",
        0
      ]
    },
    "class_type": "LongCLIPTextEncodeFlux",
    "_meta": {
      "title": "LongCLIPTextEncodeFlux"
    }
  },
  "63": {
    "inputs": {
      "input_mode": "advanced",
      "lora_count": 3,
      "lora_name_1": "flux_lora/Hyper-FLUX.1-dev-16steps-lora.safetensors",
      "lora_wt_1": 0.13000000000000003,
      "model_str_1": 0.13000000000000003,
      "clip_str_1": 0.13000000000000003,
      "lora_name_2": "flux_lora/aidmaImageUpgrader-FLUX-V0.1.safetensors",
      "lora_wt_2": 0,
      "model_str_2": 0.10000000000000002,
      "clip_str_2": 0.8000000000000002,
      "lora_name_3": "flux_lora/flux_vividizer.safetensors",
      "lora_wt_3": 0,
      "model_str_3": 0.10000000000000002,
      "clip_str_3": 0.8000000000000002
    },
    "class_type": "LoRA Stacker",
    "_meta": {
      "title": "LoRA Stacker"
    }
  },
  "64": {
    "inputs": {
      "model": [
        "68",
        0
      ],
      "clip": [
        "62",
        0
      ],
      "lora_stack": [
        "63",
        0
      ]
    },
    "class_type": "CR Apply LoRA Stack",
    "_meta": {
      "title": "CR Apply LoRA Stack"
    }
  },
  "68": {
    "inputs": {
      "hard_mode": true,
      "boost": true,
      "model": [
        "53",
        0
      ]
    },
    "class_type": "Automatic CFG",
    "_meta": {
      "title": "Automatic CFG"
    }
  },
  "71": {
    "inputs": {
      "text": [
        "72",
        0
      ]
    },
    "class_type": "TextInput_",
    "_meta": {
      "title": "TextInput_"
    }
  },
  "72": {
    "inputs": {
      "original_prompt": {{ POS_PROMPT }},
      "target_language": "en",
      "max_tokens_override": 500,
      "temperature_override": 0
    },
    "class_type": "UniversalPromptTranslator",
    "_meta": {
      "title": "Universal Prompt Translator"
    }
  }
}

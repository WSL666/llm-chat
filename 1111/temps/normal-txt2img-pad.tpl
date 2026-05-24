{
  "6": {
    "inputs": {
      "text": [
        "44",
        0
      ],
      "clip": [
        "11",
        0
      ]
    },
    "class_type": "CLIPTextEncode",
    "_meta": {
      "title": "CLIP Text Encode (Prompt)"
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
      "title": "VAE Decode"
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
      "title": "Save Image"
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
      "clip_name2": "clip_l.safetensors",
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
        "47",
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
      "denoise": {{ DENOSE_NUMBER }},
      "model": [
        "12",
        0
      ]
    },
    "class_type": "BasicScheduler",
    "_meta": {
      "title": "BasicScheduler"
    }
  },
  "22": {
    "inputs": {
      "model": [
        "12",
        0
      ],
      "conditioning": [
        "6",
        0
      ]
    },
    "class_type": "BasicGuider",
    "_meta": {
      "title": "BasicGuider"
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
  "27": {
    "inputs": {
      "image": {{ INPUT_REF_IMG }}
    },
    "class_type": "LoadImage",
    "_meta": {
      "title": "Load Image"
    }
  },
  "30": {
    "inputs": {
      "pixels": [
        "31",
        0
      ],
      "vae": [
        "10",
        0
      ]
    },
    "class_type": "VAEEncode",
    "_meta": {
      "title": "VAE Encode"
    }
  },
  "31": {
    "inputs": {
      "upscale_method": "nearest-exact",
      "scale_by": 1.0000000000000002,
      "image": [
        "27",
        0
      ]
    },
    "class_type": "ImageScaleBy",
    "_meta": {
      "title": "Upscale Image By"
    }
  },
  "44": {
    "inputs": {
      "text": [
        "49",
        0
      ]
    },
    "class_type": "TextInput_",
    "_meta": {
      "title": "Text Input ♾️Mixlab"
    }
  },
  "47": {
    "inputs": {
      "amount": [
        "48",
        0
      ],
      "samples": [
        "30",
        0
      ]
    },
    "class_type": "RepeatLatentBatch",
    "_meta": {
      "title": "Repeat Latent Batch"
    }
  },
  "48": {
    "inputs": {
      "value": {{ BATCH_SIZE }}
    },
    "class_type": "JWInteger",
    "_meta": {
      "title": "BatchSize"
    }
  },
  "49": {
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
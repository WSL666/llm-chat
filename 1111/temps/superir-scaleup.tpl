{
  "59": {
    "inputs": {
      "upscale_model": [
        "154",
        0
      ],
      "image": [
        "91",
        0
      ]
    },
    "class_type": "ImageUpscaleWithModel",
    "_meta": {
      "title": "图像通过模型放大"
    }
  },
  "91": {
    "inputs": {
      "image": {{ INPUT_IMG }}
    },
    "class_type": "LoadImage",
    "_meta": {
      "title": "加载图像"
    }
  },
  "132": {
    "inputs": {
      "supir_model": "SUPIR-v0Q_fp16.safetensors",
      "fp8_unet": false,
      "diffusion_dtype": "auto",
      "high_vram": false,
      "model": [
        "133",
        0
      ],
      "clip": [
        "133",
        1
      ],
      "vae": [
        "133",
        2
      ]
    },
    "class_type": "SUPIR_model_loader_v2",
    "_meta": {
      "title": "SUPIR模型加载器_V2"
    }
  },
  "133": {
    "inputs": {
      "ckpt_name": "juggernautXL_v9Rdphoto2Lightning.safetensors"
    },
    "class_type": "CheckpointLoaderSimple",
    "_meta": {
      "title": "Checkpoint加载器(简易)"
    }
  },
  "134": {
    "inputs": {
      "use_tiled_vae": true,
      "encoder_tile_size": 512,
      "decoder_tile_size": 512,
      "encoder_dtype": "auto",
      "SUPIR_VAE": [
        "132",
        1
      ],
      "image": [
        "152",
        0
      ]
    },
    "class_type": "SUPIR_first_stage",
    "_meta": {
      "title": "SUPIR阶段一"
    }
  },
  "135": {
    "inputs": {
      "use_tiled_vae": true,
      "encoder_tile_size": 512,
      "encoder_dtype": "auto",
      "SUPIR_VAE": [
        "134",
        0
      ],
      "image": [
        "134",
        1
      ]
    },
    "class_type": "SUPIR_encode",
    "_meta": {
      "title": "SUPIR编码"
    }
  },
  "136": {
    "inputs": {
      "positive_prompt": [
        "180",
        0
      ],
      "negative_prompt": "bad quality, blurry, messy",
      "SUPIR_model": [
        "132",
        0
      ],
      "latents": [
        "134",
        2
      ]
    },
    "class_type": "SUPIR_conditioner",
    "_meta": {
      "title": "SUPIR条件"
    }
  },
  "138": {
    "inputs": {
      "seed": {{ NOISE_SEED }},
      "steps": 10,
      "cfg_scale_start": 2.0000000000000004,
      "cfg_scale_end": 1.5000000000000002,
      "EDM_s_churn": 5,
      "s_noise": 1.0030000000000003,
      "DPMPP_eta": 1.0000000000000002,
      "control_scale_start": 1.0000000000000002,
      "control_scale_end": 0.9000000000000001,
      "restore_cfg": 1.0000000000000002,
      "keep_model_loaded": false,
      "sampler": "RestoreDPMPP2MSampler",
      "sampler_tile_size": 1024,
      "sampler_tile_stride": 512,
      "SUPIR_model": [
        "132",
        0
      ],
      "latents": [
        "135",
        0
      ],
      "positive": [
        "136",
        0
      ],
      "negative": [
        "136",
        1
      ]
    },
    "class_type": "SUPIR_sample",
    "_meta": {
      "title": "SUPIR采样"
    }
  },
  "139": {
    "inputs": {
      "use_tiled_vae": true,
      "decoder_tile_size": 512,
      "SUPIR_VAE": [
        "132",
        1
      ],
      "latents": [
        "138",
        0
      ]
    },
    "class_type": "SUPIR_decode",
    "_meta": {
      "title": "SUPIR解码"
    }
  },
  "140": {
    "inputs": {
      "method": "mkl",
      "image_ref": [
        "91",
        0
      ],
      "image_target": [
        "139",
        0
      ]
    },
    "class_type": "ColorMatch",
    "_meta": {
      "title": "图像调色"
    }
  },
  "151": {
    "inputs": {
      "model": "wd-v1-4-moat-tagger-v2",
      "threshold": 0.20000000000000004,
      "character_threshold": 0.8500000000000002,
      "replace_underscore": false,
      "trailing_comma": false,
      "exclude_tags": "",
      "tags": "1girl, solo, looking_at_viewer, smile, short_hair, bangs, brown_hair, long_sleeves, brown_eyes, closed_mouth, collarbone, upper_body, outdoors, japanese_clothes, sky, day, artist_name, blurry, tree, blue_sky, lips, sash, depth_of_field, blurry_background, watermark, bob_cut, nature, mountain, realistic, nose, fence",
      "image": [
        "91",
        0
      ]
    },
    "class_type": "WD14Tagger|pysssss",
    "_meta": {
      "title": "WD14反推提示词"
    }
  },
  "152": {
    "inputs": {
      "factor": [
        "165",
        1
      ],
      "supersample": false,
      "resampling": "bicubic",
      "image": [
        "59",
        0
      ]
    },
    "class_type": "Image Resize Factor (mtb)",
    "_meta": {
      "title": "图像缩放系数"
    }
  },
  "153": {
    "inputs": {
      "image": [
        "91",
        0
      ]
    },
    "class_type": "easy imageSize",
    "_meta": {
      "title": "图像尺寸"
    }
  },
  "154": {
    "inputs": {
      "model_name": "4xFaceUpSharpDAT.pth"
    },
    "class_type": "UpscaleModelLoader",
    "_meta": {
      "title": "放大模型加载器"
    }
  },
  "158": {
    "inputs": {
      "int": [
        "153",
        0
      ]
    },
    "class_type": "Int To Number (mtb)",
    "_meta": {
      "title": "整数到数字"
    }
  },
  "159": {
    "inputs": {
      "int": [
        "153",
        1
      ]
    },
    "class_type": "Int To Number (mtb)",
    "_meta": {
      "title": "整数到数字"
    }
  },
  "160": {
    "inputs": {
      "mode": true,
      "a": [
        "158",
        0
      ],
      "b": [
        "159",
        0
      ]
    },
    "class_type": "ImpactMinMax",
    "_meta": {
      "title": "求极值"
    }
  },
  "161": {
    "inputs": {
      "int": [
        "160",
        0
      ]
    },
    "class_type": "Int To Number (mtb)",
    "_meta": {
      "title": "整数到数字"
    }
  },
  "162": {
    "inputs": {
      "operation": "division",
      "number_a": [
        "163",
        0
      ],
      "number_b": [
        "161",
        0
      ]
    },
    "class_type": "Number Operation",
    "_meta": {
      "title": "数字运算"
    }
  },
  "163": {
    "inputs": {
      "int": [
        "166",
        0
      ]
    },
    "class_type": "Int To Number (mtb)",
    "_meta": {
      "title": "整数到数字"
    }
  },
  "164": {
    "inputs": {
      "int": [
        "167",
        0
      ]
    },
    "class_type": "Int To Number (mtb)",
    "_meta": {
      "title": "整数到数字"
    }
  },
  "165": {
    "inputs": {
      "operation": "division",
      "number_a": [
        "162",
        0
      ],
      "number_b": [
        "164",
        0
      ]
    },
    "class_type": "Number Operation",
    "_meta": {
      "title": "数字运算"
    }
  },
  "166": {
    "inputs": {
      "Value": {{ PIXEL }}
    },
    "class_type": "DF_Integer",
    "_meta": {
      "title": "Integer"
    }
  },
  "167": {
    "inputs": {
      "Value": 4
    },
    "class_type": "DF_Integer",
    "_meta": {
      "title": "Integer"
    }
  },
  "168": {
    "inputs": {
      "operation": "greater-than",
      "number_a": [
        "162",
        0
      ],
      "number_b": [
        "164",
        0
      ]
    },
    "class_type": "Number Operation",
    "_meta": {
      "title": "数字运算"
    }
  },
  "180": {
    "inputs": {
      "text1": "Cinematic, High Contrast, highly detailed, taken using a Canon EOS R camera, hyper detailed photo - realistic maximum detail, 32k, Color Grading, ultra HD, extreme meticulous detailing, skin pore detailing, hyper sharpness, perfect without deformations.",
      "text2": [
        "151",
        0
      ],
      "text3": "",
      "text4": "",
      "text5": "",
      "text6": "",
      "text7": "",
      "text8": "",
      "text9": "",
      "text10": "",
      "text11": "",
      "text12": "",
      "text13": "",
      "separator": ","
    },
    "class_type": "Concat Text _O",
    "_meta": {
      "title": "Concat Text _O"
    }
  },
  "181": {
    "inputs": {
      "filename_prefix": {{ FILENAME_PREFIX }},
      "images": [
        "140",
        0
      ]
    },
    "class_type": "SaveImage",
    "_meta": {
      "title": "保存图像"
    }
  }
}
{
  "59": {
    "inputs": {
      "upscale_model": [
        "176",
        0
      ],
      "image": [
        "91",
        0
      ]
    },
    "class_type": "ImageUpscaleWithModel",
    "_meta": {
      "title": "Upscale Image (using Model)"
    }
  },
  "60": {
    "inputs": {
      "model_name": "RealESRGAN_x4.pth"
    },
    "class_type": "UpscaleModelLoader",
    "_meta": {
      "title": "Load Upscale Model"
    }
  },
  "91": {
    "inputs": {
      "image": {{ INPUT_IMG }}
    },
    "class_type": "LoadImage",
    "_meta": {
      "title": "Load Image"
    }
  },
  "152": {
    "inputs": {
      "factor": [
        "167",
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
      "title": "Image Resize Factor (mtb)"
    }
  },
  "155": {
    "inputs": {
      "image": [
        "91",
        0
      ]
    },
    "class_type": "GetImageSize",
    "_meta": {
      "title": "GetImageSize"
    }
  },
  "159": {
    "inputs": {
      "int": [
        "155",
        0
      ]
    },
    "class_type": "Int To Number (mtb)",
    "_meta": {
      "title": "Int To Number (mtb)"
    }
  },
  "160": {
    "inputs": {
      "int": [
        "155",
        1
      ]
    },
    "class_type": "Int To Number (mtb)",
    "_meta": {
      "title": "Int To Number (mtb)"
    }
  },
  "161": {
    "inputs": {
      "mode": true,
      "a": [
        "159",
        0
      ],
      "b": [
        "160",
        0
      ]
    },
    "class_type": "ImpactMinMax",
    "_meta": {
      "title": "ImpactMinMax"
    }
  },
  "162": {
    "inputs": {
      "int": [
        "161",
        0
      ]
    },
    "class_type": "Int To Number (mtb)",
    "_meta": {
      "title": "Int To Number (mtb)"
    }
  },
  "163": {
    "inputs": {
      "operation": "division",
      "number_a": [
        "164",
        0
      ],
      "number_b": [
        "162",
        0
      ]
    },
    "class_type": "Number Operation",
    "_meta": {
      "title": "Number Operation"
    }
  },
  "164": {
    "inputs": {
      "int": [
        "171",
        0
      ]
    },
    "class_type": "Int To Number (mtb)",
    "_meta": {
      "title": "Int To Number (mtb)"
    }
  },
  "166": {
    "inputs": {
      "int": [
        "172",
        0
      ]
    },
    "class_type": "Int To Number (mtb)",
    "_meta": {
      "title": "Int To Number (mtb)"
    }
  },
  "167": {
    "inputs": {
      "operation": "division",
      "number_a": [
        "163",
        0
      ],
      "number_b": [
        "201",
        0
      ]
    },
    "class_type": "Number Operation",
    "_meta": {
      "title": "Number Operation"
    }
  },
  "171": {
    "inputs": {
      "Value": {{ PIXEL }}
    },
    "class_type": "DF_Integer",
    "_meta": {
      "title": "Integer"
    }
  },
  "172": {
    "inputs": {
      "Value": 2
    },
    "class_type": "DF_Integer",
    "_meta": {
      "title": "Integer"
    }
  },
  "176": {
    "inputs": {
      "select": 1,
      "sel_mode": true,
      "input1": [
        "177",
        0
      ],
      "input2": [
        "177",
        0
      ],
      "input3": [
        "178",
        0
      ],
      "input4": [
        "60",
        0
      ]
    },
    "class_type": "ImpactSwitch",
    "_meta": {
      "title": "Switch (Any)"
    }
  },
  "177": {
    "inputs": {
      "model_name": "RealESRGAN_x4.pth"
    },
    "class_type": "UpscaleModelLoader",
    "_meta": {
      "title": "Load Upscale Model"
    }
  },
  "178": {
    "inputs": {
      "model_name": "RealESRGAN_x8.pth"
    },
    "class_type": "UpscaleModelLoader",
    "_meta": {
      "title": "Load Upscale Model"
    }
  },
  "187": {
    "inputs": {
      "operation": "greater-than",
      "number_a": [
        "163",
        0
      ],
      "number_b": [
        "166",
        0
      ]
    },
    "class_type": "Number Operation",
    "_meta": {
      "title": "Number Operation"
    }
  },
  "188": {
    "inputs": {
      "operation": "greater-than",
      "number_a": [
        "163",
        0
      ],
      "number_b": [
        "191",
        0
      ]
    },
    "class_type": "Number Operation",
    "_meta": {
      "title": "Number Operation"
    }
  },
  "190": {
    "inputs": {
      "Value": 4
    },
    "class_type": "DF_Integer",
    "_meta": {
      "title": "Integer"
    }
  },
  "191": {
    "inputs": {
      "int": [
        "190",
        0
      ]
    },
    "class_type": "Int To Number (mtb)",
    "_meta": {
      "title": "Int To Number (mtb)"
    }
  },
  "196": {
    "inputs": {
      "operation": "addition",
      "number_a": [
        "187",
        0
      ],
      "number_b": [
        "188",
        0
      ]
    },
    "class_type": "Number Operation",
    "_meta": {
      "title": "Number Operation"
    }
  },
  "197": {
    "inputs": {
      "Value": 1
    },
    "class_type": "DF_Integer",
    "_meta": {
      "title": "Integer"
    }
  },
  "198": {
    "inputs": {
      "int": [
        "197",
        0
      ]
    },
    "class_type": "Int To Number (mtb)",
    "_meta": {
      "title": "Int To Number (mtb)"
    }
  },
  "199": {
    "inputs": {
      "operation": "addition",
      "number_a": [
        "196",
        0
      ],
      "number_b": [
        "198",
        0
      ]
    },
    "class_type": "Number Operation",
    "_meta": {
      "title": "Number Operation"
    }
  },
  "201": {
    "inputs": {
      "select": 1,
      "sel_mode": true,
      "input1": [
        "191",
        0
      ],
      "input2": [
        "191",
        0
      ],
      "input3": [
        "203",
        0
      ],
      "input4": [
        "166",
        0
      ]
    },
    "class_type": "ImpactSwitch",
    "_meta": {
      "title": "Switch (Any)"
    }
  },
  "202": {
    "inputs": {
      "Value": 8
    },
    "class_type": "DF_Integer",
    "_meta": {
      "title": "Integer"
    }
  },
  "203": {
    "inputs": {
      "int": [
        "202",
        0
      ]
    },
    "class_type": "Int To Number (mtb)",
    "_meta": {
      "title": "Int To Number (mtb)"
    }
  },
  "204": {
    "inputs": {
      "filename_prefix": {{ FILENAME_PREFIX }},
      "images": [
        "152",
        0
      ]
    },
    "class_type": "SaveImage",
    "_meta": {
      "title": "保存图像"
    }
  }
}
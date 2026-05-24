{
  "10": {
    "inputs": {
      "image": {{ INPUT_IMG }}
    },
    "class_type": "LoadImage",
    "_meta": {
      "title": "Load Image"
    }
  },
  "124": {
    "inputs": {
      "detail_method": "VITMatte",
      "detail_erode": 4,
      "detail_dilate": 2,
      "black_point": 0.010000000000000002,
      "white_point": 0.99,
      "process_detail": true,
      "device": "cuda",
      "max_megapixels": 2,
      "image": [
        "10",
        0
      ],
      "birefnet_model": [
        "125",
        0
      ]
    },
    "class_type": "LayerMask: BiRefNetUltraV2",
    "_meta": {
      "title": "LayerMask: BiRefNet Ultra V2(Advance)"
    }
  },
  "125": {
    "inputs": {
      "version": "RMBG-2.0"
    },
    "class_type": "LayerMask: LoadBiRefNetModelV2",
    "_meta": {
      "title": "LayerMask: Load BiRefNet Model V2(Advance)"
    }
  },
  "127": {
    "inputs": {
      "RGB_image": [
        "124",
        0
      ],
      "mask": [
        "124",
        1
      ]
    },
    "class_type": "LayerUtility: ImageCombineAlpha",
    "_meta": {
      "title": "LayerUtility: ImageCombineAlpha"
    }
  },
  "128": {
    "inputs": {
      "mask": [
        "124",
        1
      ]
    },
    "class_type": "MaskToImage",
    "_meta": {
      "title": "Convert Mask to Image"
    }
  },
  "129": {
    "inputs": {
      "filename_prefix": {{ FILENAME_PREFIX }},
      "images": [
        "127",
        0
      ]
    },
    "class_type": "SaveImage",
    "_meta": {
      "title": "Save Image"
    }
  }
}
import json
from jinja2 import Template


class ComfyUIPromptTemplate(Template):

    def __new__(cls, *args, **kwargs):
        return super(ComfyUIPromptTemplate, cls).__new__(cls, *args, **kwargs)

    @classmethod
    def from_template(cls, data: str = None, path: str = None) -> "ComfyUIPromptTemplate":
        if data is None and path is None:
            raise ValueError('The param data and path are both None.')
        if data is None:
            with open(path, 'r', encoding='utf8') as f:
                data = f.read()
        return cls(data)

    def render_json(self, *args, **kwargs):
        temp = self.render(*args, **kwargs)
        try:
            temp_json = json.loads(temp)
        except json.decoder.JSONDecodeError:
            raise Exception('The template is not json format.')
        except Exception as e:
            raise e
        return temp_json


if __name__ == '__main__':
    templte = ComfyUIPromptTemplate.from_template(path='temps/flux-lora-t2i.tpl')
    p = '(best quality,4k,8k,highres,masterpiece:1.2),ultra-detailed,(realistic,photorealistic,photo-realistic:1.37),realistic style,a girl playing on the beach,beautiful detailed eyes,beautiful detailed lips,extremely detailed eyes and face,long eyelashes,smiling,happy expression,wearing a summer dress,blonde hair,wind blowing through hair,holding a beach ball,sandy beach,clear blue sky,bright sunlight,shadows on the sand,soft waves in the background,photography,vivid colors,sharp focus,studio lighting,physically-based rendering,extreme detail description,professional'
    prompt = templte.render_json(
        PROMPT_TEXT=f'"{p}"',
        FILENAME_PREFIX='"flux"',
        WIDTH=780,
        HEIGHT=780,
        BATCH_SIZE=1,
        DENOISE_RATIO=1.0,
        NOISE_SEED=42,
        LORA='"flux_lora/your_lora.safetensors"',
        LORA_STRENGTH=0.8,
    )
    print(type(prompt))
    print(prompt)

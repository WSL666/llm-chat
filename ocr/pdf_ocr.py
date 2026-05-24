import base64
import os
import re
import sys
import fitz  # pymupdf
from openai import OpenAI

#  模型配置 
API_KEY  = "sk-lueuazgpxpfwuvnpkfkzblkuwyphhipriylxruociasmkiln"
BASE_URL = "https://api.siliconflow.cn/v1"
MODEL    = "deepseek-ai/DeepSeek-OCR"
MAX_TOKENS = 4096   # 每页输出的最大 token 数


def clean_ocr_noise(text: str) -> str:
    """
    清洗 DeepSeek-OCR 输出中的定位标签噪声。
    清除形如 <|ref|>...<|/ref|><|det|>[[x,y,w,h]]<|/det|> 的整行标签。
    """
    # 删除包含 <|ref|>...<|/ref|><|det|>...</|det|> 的整行（含换行符）
    text = re.sub(r'[ \t]*<\|ref\|>.*?<\|/ref\|><\|det\|>.*?<\|/det\|>[ \t]*\n?', '', text)
    # 兜底：删除任何残留的 <|ref|>、<|/ref|>、<|det|>、<|/det|> 标签
    text = re.sub(r'<\|/?(ref|det)\|>', '', text)
    # 删除其他模型特殊 token，如 <|grounding|> 等
    text = re.sub(r'<\|[^|]+\|>', '', text)
    # 合并超过两个的连续空行
    text = re.sub(r'\n{3,}', '\n\n', text)
    return text.strip()


def parse_page_to_markdown(client: OpenAI, page_pdf_bytes: bytes, page_num: int) -> str:
    """将单页 PDF 字节调用 OCR 模型，返回 Markdown 文本。"""
    pdf_base64 = base64.b64encode(page_pdf_bytes).decode("utf-8")

    response = client.chat.completions.create(
        model=MODEL,
        max_tokens=MAX_TOKENS,
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": "data:application/pdf;base64," + pdf_base64
                        }
                    },
                    {
                        "type": "text",
                        "text": "<image>\n<|grounding|>Convert the document to markdown. "
                    }
                ]
            }
        ]
    )

    finish_reason = response.choices[0].finish_reason
    if finish_reason == "length":
        print(f"  [警告] 第 {page_num} 页输出被 max_tokens 截断，内容可能不完整。")

    raw = response.choices[0].message.content
    return clean_ocr_noise(raw)


def parse_pdf_to_markdown(pdf_path: str) -> str:
    """
    按页拆分 PDF，逐页调用 OCR 模型，合并所有页的 Markdown 结果。

    :param pdf_path: PDF 文件的本地路径
    :return: 完整的 Markdown 字符串
    """
    client = OpenAI(api_key=API_KEY, base_url=BASE_URL)
    doc = fitz.open(pdf_path)
    total_pages = len(doc)
    print(f"共 {total_pages} 页，逐页解析中...")

    all_pages_md = []
    for i, page in enumerate(doc, start=1):
        print(f"  正在处理第 {i}/{total_pages} 页...", flush=True)
        # 将单页导出为独立 PDF 字节
        single_page_doc = fitz.open()
        single_page_doc.insert_pdf(doc, from_page=i - 1, to_page=i - 1)
        page_bytes = single_page_doc.tobytes()
        single_page_doc.close()

        md = parse_page_to_markdown(client, page_bytes, i)
        all_pages_md.append(f"<!-- Page {i} -->\n{md}")

    doc.close()
    return "\n\n".join(all_pages_md)


# ===== 输入输出路径配置 =====
PDF_INPUT  = r"e:\Myworkspace\ocr\王石林 (4).pdf"   # 输入 PDF 路径
MD_OUTPUT  = r"e:\Myworkspace\ocr\王石林_clean.md"    # 输出 Markdown 路径
# ============================

if __name__ == "__main__":
    if not os.path.exists(PDF_INPUT):
        print(f"File not found: {PDF_INPUT}")
        sys.exit(1)

    print(f"正在解析: {PDF_INPUT}")
    markdown_result = parse_pdf_to_markdown(PDF_INPUT)

    with open(MD_OUTPUT, "w", encoding="utf-8") as f:
        f.write(markdown_result)

    print(f"\n解析完成，已保存至: {MD_OUTPUT}")

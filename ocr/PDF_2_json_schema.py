import json
import os
from openai import OpenAI

client = OpenAI(
    api_key="sk-xxxx",
    base_url="https://api.siliconflow.cn/v1"
)

# 读取 md 文件原始内容（不做任何清洗或格式处理）
MD_FILE = os.path.join(os.path.dirname(__file__), "王石林_clean.md")

with open(MD_FILE, "r", encoding="utf-8") as f:
    md_content = f.read()

system_prompt = """
你是一名专业的 AI 简历解析助手。

请从用户markdown格式的简历中提取信息，并严格按照指定 JSON Schema 返回结果。

要求：

1. 仅返回合法 JSON
2. 不要输出 markdown
3. 不要输出解释
4. 不要添加 schema 中不存在的字段
5. 如果字段不存在，返回空字符串或空数组
6. 自动提取专业技能，非常详细一个一个提取
7. 专业技能提取名字要么是中文，英文，不要有中英文混杂，但是：多模态agent，Multi-agent这种不可拆分的需要保留
8. 自动提取项目名称,最多3个项目名称，按时间顺序排列
9. 自动将技能名称标准化为行业通用写法
10. 自动修复缩写、别名、大小写不统一问题
11. skills 中仅保留专业技能，不包含软技能
12. 保持行业通用性
13. 学历education固定填写，不得填写其他名词并且只保留最高一个学历：小学，初中，高中，专科，本科，硕士，博士

技能标准化示例：

- js → JavaScript
- ts → TypeScript
- reactjs → React
- react.js → React
- node → Node.js
- py → Python


返回 JSON Schema：

{
  "basic_info": {
    "name": "",
    "title": "",
    "school": "",
    "education": "",
    "major": "",
    "phone": "",
    "email": ""
  },

  "skills": [],

  "projects": []
}

注意：

- 输出必须是可直接 JSON.parse 的标准 JSON
- 不允许出现 ```json
- 不允许出现注释
- 不允许出现额外文本
- 不允许遗漏字段

下面开始解析简历：
"""

response = client.chat.completions.create(
    model="Pro/moonshotai/Kimi-K2.6",
    messages=[
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": md_content}
    ]
)

result_text = response.choices[0].message.content
print(result_text)

# 保存为 JSON 文件
output_file = os.path.join(os.path.dirname(__file__), "王石林 (4).json")
try:
    result_json = json.loads(result_text)
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(result_json, f, ensure_ascii=False, indent=2)
    print(f"\n已保存至：{output_file}")
except json.JSONDecodeError as e:
    print(f"\n[警告] 模型返回内容不是合法 JSON，原始内容已打印，未保存文件。错误：{e}")
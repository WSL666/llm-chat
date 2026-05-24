import json
import requests
import math

API_URL = "https://api.siliconflow.cn/v1/embeddings"
HEADERS = {
    "Authorization": "Bearer sk-fheemcmucmbmyllrobngdxxkqumzjbsrpecfkqgzvpzkvnxj",
    "Content-Type": "application/json"
}

def get_embedding(text):
    payload = {"model": "BAAI/bge-m3", "input": text}
    response = requests.post(API_URL, json=payload, headers=HEADERS)
    response.raise_for_status()
    return response.json()["data"][0]["embedding"]

def cosine_similarity(a, b):
    dot = sum(x*y for x,y in zip(a,b))
    na = sum(x*x for x in a)**0.5
    nb = sum(x*x for x in b)**0.5
    return dot/(na*nb) if na and nb else 0.0

with open("dj_result.json", encoding="utf-8") as f:
    dj_data = json.load(f)
with open("pdf_result.json", encoding="utf-8") as f:
    pdf_data = json.load(f)

jd_title     = dj_data["job_info"]["title"]
resume_title = pdf_data["basic_info"]["title"]
jd_skills    = dj_data["skills"]
cv_skills    = pdf_data["skills"]
jd_edu_list  = dj_data.get("education", [])
cv_edu       = pdf_data["basic_info"].get("education", "")

print("JD 职位名称   :", jd_title)
print("简历职位头衔  :", resume_title)
print("正在获取 Title Embedding ...")
title_sim = cosine_similarity(get_embedding(jd_title), get_embedding(resume_title))

jd_set      = {s.lower() for s in jd_skills}
cv_set      = {s.lower() for s in cv_skills}
matched     = jd_set & cv_set
missed      = jd_set - cv_set
skill_score = len(matched) / len(jd_set)

edu_bonus = 0.1 if cv_edu in jd_edu_list else 0.0
final_score = title_sim * 0.7 + skill_score * 0.3 + edu_bonus

print()
print("=" * 50)
print("【Title 相似度】")
print(f"  余弦相似度   : {title_sim:.4f}  ({title_sim*100:.2f}%)")
print()
print("【Skills 硬匹配】")
print(f"  JD  技能总数 : {len(jd_set)}")
print(f"  命中技能数   : {len(matched)}")
print(f"  命中技能     : {", ".join(sorted(matched))}")
print(f"  缺失技能     : {", ".join(sorted(missed))}")
print(f"  技能匹配得分 : {len(matched)}/{len(jd_set)} = {skill_score:.4f}  ({skill_score*100:.2f}%)")
print()
print("【学历匹配】")
print(f"  JD 学历要求  : {", ".join(jd_edu_list)}")
print(f"  简历学历     : {cv_edu}")
print(f"  是否匹配     : {'✅ 是' if edu_bonus > 0 else '❌ 否'}")
print(f"  学历加分     : +{edu_bonus:.2f}")
print()
print("【综合评分】")
print(f"  Title  × 0.7 : {title_sim*0.7:.4f}")
print(f"  Skills × 0.3 : {skill_score*0.3:.4f}")
print(f"  学历加分     : +{edu_bonus:.4f}")
print(f"  最终得分     : {final_score:.4f}  ({final_score*100:.2f}%)")
print("=" * 50)

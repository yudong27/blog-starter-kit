import os
import requests
from typing import List
from loguru import logger

from formatter import DataFetchFormatter



# 2. 大模型 API 配置 (以 DeepSeek 为例)
# 如果你没有 DeepSeek，可以用 Kimi/阿里/OpenAI，只需修改 BASE_URL 和 API_KEY
LLM_API_KEY = os.getenv("DEEPSEEK_API_KEY") 

# 👈 3. 加上一层安全校验（如果没读到 Key，就立刻停止程序，防止报错乱码）
if not LLM_API_KEY:
    logger.error("未找到 DEEPSEEK_API_KEY 环境变量，程序无法继续运行！")
    exit(1)
LLM_BASE_URL = "https://api.deepseek.com/chat/completions"
LLM_MODEL = "deepseek-chat"





def generate_war_report(post: DataFetchFormatter) -> DataFetchFormatter:
    """调用大模型生成战报和极客词典"""
    logger.debug(f"🔍 传入 LLM 的数据: {post}")
    
    # 我们精心设计的“战地记者+词典” Prompt
    system_prompt = """
    你是一名科技战地记者。我会给你一条英文科技新闻的标题。
    请你过滤废话，直接输出以下中文格式：
    
    【🔥 战况摘要】：(用一句极其精炼的人话总结这篇新闻的核心，注意如果极客词典是英语并出现在这里，最好保留英语模式，可以放在汉语翻译的后面，并用方括号括起来)
    【💡 极客词典】：(从新闻中挑出一个最硬核的专有名词或缩写，如果标题里没有，就根据事件背景推测一个相关词汇。然后用极其通俗、幽默的“说人话”方式解释它，不超过50字)
    """
    
    payload = {
        "model": LLM_MODEL,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"新闻标题：{post.title}"}
        ],
        "temperature": 0.7
    }
    
    headers = {
        "Authorization": f"Bearer {LLM_API_KEY}",
        "Content-Type": "application/json"
    }
    
    response = requests.post(LLM_BASE_URL, headers=headers, json=payload)
    
    if response.status_code == 200:
        content = response.json()['choices'][0]['message']['content']
        logger.debug(f"🔍 LLM 返回的内容: {content}")
        post.llm_content = content
        post.llm_has_content = True
        return post
    else:
        logger.error(f"❌ AI 破译失败: {response.text}")
        post.llm_content = "⚠️ AI 破译失败，无法生成战报。"
        return post

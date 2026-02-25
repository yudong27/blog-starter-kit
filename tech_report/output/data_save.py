import os
import datetime
from typing import List
from loguru import logger
from formatter import DataFetchFormatter

def save_to_markdown(posts_with_reports: List[DataFetchFormatter]):
    """把生成的战报保存为 Markdown 文件供 Vercel 渲染"""
    
    # 获取今天的日期，格式如：2026-02-24
    today_str = datetime.datetime.now().strftime("%Y-%m-%d")
    
    # 确保保存文章的文件夹存在（假设我们存放在 _posts 目录下）
    os.makedirs("_posts", exist_ok=True)
    
    file_path = f"_posts/{today_str}-daily-report.md"
    
    # Markdown 文件的头部元数据 (Frontmatter)，Vercel 模板靠它来识别标题和日期
    md_content = f"""---
title: "极客战地快报：{today_str}"
date: "{today_str}"
description: "今日 AI 前沿与极客黑话解析"
tags: ["Daily Report", "AI", "Tech"]
---

# 🚀 {today_str} 极客战地快报

"""
    # 拼接每条新闻的战报内容
    full_report_text = ""
    for i, post in enumerate(posts_with_reports, 1):
        full_report_text += f"## 📰 情报 #{i}\n"
        full_report_text += f"- **原文**: {post.title}\n"
        full_report_text += f"- **来源**: {post.url}\n\n"
        if post.llm_has_content:
            full_report_text += f"{post.llm_content}\n\n"
        else:
            full_report_text += "⚠️ AI 破译失败，无法生成战报。\n\n"
        full_report_text += "---\n\n"
    # 拼接正文
    md_content += full_report_text

    # 写入本地文件
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(md_content)
        
    print(f"📁 战报已成功保存为本地文件: {file_path}")

# 在你的 main() 函数最后调用它：
# save_to_markdown(posts, 拼接好的战报总文本)
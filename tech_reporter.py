import requests
import json
import os
from log import logger

from fetch import fetch_hackernews_ai_posts
from generate import generate_war_report
from output.data_save import save_to_markdown
from output.send_email import send_email

def main():
    print("====================================")
    print("      🚀 极客战地快报生成系统 v1.0     ")
    print("====================================\n")
    


    # 1. 抓取数据
    # posts = fetch_reddit_top_posts()
    # posts = fetch_hackernews_top_posts()
    posts = fetch_hackernews_ai_posts()  # 直接狙击 AI 相关的新闻
    if not posts:
        logger.warning("⚠️ 没有获取到任何情报，程序即将退出。")
        return

    print("\n✅ 情报获取成功！开始生成战报...\n")
    print("-" * 40)
    
    # 2. 遍历处理并打印
    for i, post in enumerate(posts, 1):
        report = generate_war_report(post)
        
        # 打印到控制台
        print(f"【情报 #{i}】原文: {post.title}")
        print(f"【来源】: {post.url}")
        print(report.llm_content)
        print("-" * 40)
        
    # 3. 保存为 Markdown 文件
    save_to_markdown(posts)
    # 生成完毕后，发送邮件！
    # send_email(email_body)

    print("\n🎉 今日战报播送完毕！")

if __name__ == "__main__":
    main()
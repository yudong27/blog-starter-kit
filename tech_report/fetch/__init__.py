import requests
import os
from typing import List

from loguru import logger
from formatter import DataFetchFormatter

# ================= 配置区 =================
# 1. Reddit 配置
SUBREDDIT = "technology"  # 你可以换成 MachineLearning, LocalLLaMA 等硬核板块
LIMIT = 3                 # 每次抓取前 3 条测试
# ⚠️ 极其重要：必须伪装 User-Agent，否则会被 Reddit 100% 拦截！
HEADERS = {
    "User-Agent": "TechReporterBot/1.0 (by /u/dan)" 
}


def fetch_reddit_top_posts():
    """从 Reddit 获取今日最热新闻"""
    print(f"📡 正在潜入前线 r/{SUBREDDIT} 获取机密情报...")
    url = f"https://www.reddit.com/r/{SUBREDDIT}/top.json?limit={LIMIT}&t=day"
    
    response = requests.get(url, headers=HEADERS)
    if response.status_code != 200:
        print(f"❌ 获取失败，状态码: {response.status_code}")
        return []
    
    posts = []
    data = response.json()
    for item in data['data']['children']:
        post_data = item['data']
        posts.append({
            "title": post_data['title'],
            "url": post_data['url']
        })
    return posts

def fetch_hackernews_top_posts():
    """从 Hacker News 获取今日最热硬核新闻"""
    print("📡 正在潜入前线 Hacker News 获取机密情报...")
    
    # 步骤 1：获取热门文章的 ID 列表
    top_stories_url = "https://hacker-news.firebaseio.com/v0/topstories.json"
    
    # 如果你在国内不开代理运行，可能会卡住。
    # 建议保持你的代理软件开启（通常 requests 库会自动走系统全局代理）。
    try:
        response = requests.get(top_stories_url, timeout=10)
        if response.status_code != 200:
            print(f"❌ 获取 ID 列表失败，状态码: {response.status_code}")
            return []
            
        story_ids = response.json()[:LIMIT] # 取前 3 个新闻的 ID
        
        posts = []
        # 步骤 2：根据 ID 获取具体新闻的标题和链接
        for story_id in story_ids:
            item_url = f"https://hacker-news.firebaseio.com/v0/item/{story_id}.json"
            item_resp = requests.get(item_url, timeout=10).json()
            
            # 过滤掉没有 URL 的讨论帖
            if 'url' in item_resp and 'title' in item_resp:
                posts.append({
                    "title": item_resp['title'],
                    "url": item_resp['url']
                })
        return posts
        
    except Exception as e:
        print(f"❌ 网络请求异常: {e}\n(💡 提示：请确保你的代理软件处于'全局路由'或 TUN 模式)")
        return []

def fetch_hackernews_ai_posts() -> List[DataFetchFormatter]:
    """使用 Algolia 接口精准狙击 Hacker News 上的 AI 前沿情报"""
    logger.info("📡 正在调用 HN Algolia 雷达，扫描高价值 AI 情报...")
    
    url = "https://hn.algolia.com/api/v1/search"
    
    # 核心魔法在这里：精准的查询参数
    query = ["AI", "LLM", "OpenAI", "ChatGPT", "Machine Learning", "MoE", "Token", "Context Window"]
    params = {
        # 1. 查询词全部用空格隔开（不要加 OR）
        "query": " ".join(query),
        # 2. 魔法参数：告诉 Algolia 这些词是“可选”的，只要命中一个就算匹配！
        "optionalWords": ",".join(query), 
        # 只搜索正式的文章（过滤掉评论）
        "tags": "story",
        # 过滤条件：只看点赞数大于 30 的（过滤掉没人看的垃圾贴）
        "numericFilters": "points>30",
        # 每次取前 3 条最相关的
        "hitsPerPage": 3
    }
    logger.debug(f"🔍 查询参数: {params}")
    
    try:
        response = requests.get(url, params=params, timeout=10)
        if response.status_code != 200:
            logger.error(f"❌ 雷达扫描失败，状态码: {response.status_code}")
            return []
            
        data = response.json()
        # logger.debug(f"🔍 原始数据: {data}")  # 输出原始数据看看结构，方便调试
        posts = []
        
        # 解析返回的数据
        for item in data['hits']:
            # 有些 HN 帖子只有文字没有外链，我们尽量抓有外链的
            post = DataFetchFormatter(
                title=item.get('title'),
                url=item.get('url', f"https://news.ycombinator.com/item?id={item['objectID']}"),
                author=item.get('author', 'unknown'),
                num_comments=item.get('num_comments', 0),
                objectID=item.get('objectID', ''),
                updated_at=item.get('updated_at', '')
            )
            
            if post.title:
                posts.append(post)
                
        return posts
        
    except Exception as e:
        logger.exception(f"雷达扫描异常: {str(e)}")
        return []


if __name__ == "__main__":
    # 直接测试抓取函数
    posts = fetch_hackernews_ai_posts()
    for post in posts:
        print("POST:", post)
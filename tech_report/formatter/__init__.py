from dataclasses import dataclass

@dataclass
class DataFetchFormatter:
    """
    数据抓取格式化器
    负责将原始数据转换成适合 LLM 输入的格式
    """
    title: str
    url: str = ""
    author: str = "unknown"
    num_comments: int = 0
    objectID: str = ""
    updated_at: str = ""
    llm_has_content: bool = False
    llm_content: str = ""

    def format_reddit_posts(self, posts):
        """
        将 Reddit 的帖子列表格式化成字符串
        """
        formatted = ""
        for post in posts:
            formatted += f"标题: {post['title']}\n"
            formatted += f"链接: {post['url']}\n"
            formatted += f"评论数: {post['num_comments']}\n"
            formatted += "-" * 40 + "\n"
        return formatted
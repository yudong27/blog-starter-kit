import os
import smtplib # 发邮件的核心库
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


# 邮箱配置 (从 GitHub Secrets 获取)
EMAIL_SENDER = os.getenv("EMAIL_SENDER")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
EMAIL_RECEIVER = os.getenv("EMAIL_RECEIVER")
# SMTP 服务器地址：QQ邮箱是 smtp.qq.com, 163是 smtp.163.com, Gmail是 smtp.gmail.com
SMTP_SERVER = "smtp.qq.com" 
SMTP_SERVER = "smtp.gmail.com" # 如果你用 Gmail，记得开启“允许不够安全的应用”或者使用 App Password
SMTP_PORT = 465 # SSL 加密端口通常是 465

def send_email(html_content):
    """将生成的战报通过邮件发送"""
    if not all([EMAIL_SENDER, EMAIL_PASSWORD, EMAIL_RECEIVER]):
        print("⚠️ 邮箱环境变量不全，跳过发送邮件步骤。")
        return

    print("✉️ 正在将今日战报打包发送至邮箱...")
    
    # 构建邮件主体
    msg = MIMEMultipart()
    msg['From'] = EMAIL_SENDER
    msg['To'] = EMAIL_RECEIVER
    msg['Subject'] = "🚀 极客战地快报：今日 AI 前沿与黑话解析"
    
    # 附上 HTML 格式的邮件正文
    msg.attach(MIMEText(html_content, 'html', 'utf-8'))

    try:
        # 连接 SMTP 服务器并发送
        server = smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT)
        server.login(EMAIL_SENDER, EMAIL_PASSWORD)
        server.send_message(msg)
        server.quit()
        print("✅ 邮件发送成功！请查收。")
    except Exception as e:
        print(f"❌ 邮件发送失败: {e}")


def format_email_content(report_list):
    """将战报内容格式化为 HTML 邮件正文"""
    # 初始化一份精美的 HTML 邮件模板
    email_body = """
    <div style="font-family: sans-serif; max-width: 600px; margin: 0 auto; color: #333;">
        <h2 style="color: #2c3e50; border-bottom: 2px solid #3498db; padding-bottom: 10px;">
            🚀 极客战地快报 
        </h2>
    """
    # 将大模型输出的换行符 \n 转换为 HTML 的 <br> 标签，保证邮件排版不乱

    for report in report_list:
        formatted_report = report.replace('\n', '<br>')
        
        # 将每一条情报拼接到邮件正文中
        email_body += f"""
        <div style="margin-bottom: 30px; padding: 15px; background-color: #f8f9fa; border-radius: 8px;">
            <h3 style="margin-top: 0;">
                <a href="{post['url']}" style="color: #2980b9; text-decoration: none;">🔗 {post['title']}</a>
            </h3>
            <p style="line-height: 1.6;">{formatted_report}</p>
        </div>
        """
    
    email_body += '<p style="font-size: 12px; color: #7f8c8d; text-align: center;">由 GitHub Actions 自动化生成</p></div>'
    return email_body
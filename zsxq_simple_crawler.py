"""
知识星球爬虫脚本
使用 requests + BeautifulSoup，支持 cookies 登录，抓取页面标题和正文并保存到 CSV。
"""
import requests
from bs4 import BeautifulSoup
import csv
import time

# 请将你的 cookies 粘贴到此处
COOKIE = "zsxq_access_token=xxx; abcdef=123456; ..."

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
    "Cookie": COOKIE
}

# 访问间隔（秒）
REQUEST_INTERVAL = 2


def fetch_page(url):
    """获取网页 HTML"""
    try:
        response = requests.get(url, headers=HEADERS, timeout=10)
        response.raise_for_status()
        return response.text
    except Exception as e:
        print(f"[错误] 获取页面失败: {e}")
        return None


def parse_page(html):
    """解析页面标题和正文"""
    try:
        soup = BeautifulSoup(html, "html.parser")
        title = soup.title.string if soup.title else ""
        # 假设正文在 <div class="post-content">，请根据实际页面结构调整
        content_div = soup.find("div", class_="post-content")
        content = content_div.get_text(strip=True) if content_div else ""
        return {"title": title, "content": content}
    except Exception as e:
        print(f"[错误] 解析页面失败: {e}")
        return {"title": "", "content": ""}


def save_to_csv(data, filename="output.csv"):
    """保存数据到 CSV 文件"""
    try:
        with open(filename, "w", newline='', encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=["title", "content"])
            writer.writeheader()
            for row in data:
                writer.writerow(row)
        print(f"[提示] 数据已保存到 {filename}")
    except Exception as e:
        print(f"[错误] 保存 CSV 失败: {e}")


def main():
    """主调度函数"""
    # 示例：爬取多个帖子页面
    urls = [
        "https://wx.zsxq.com/dweb2/index/topic_detail/12345678",
        # 可添加更多帖子链接
    ]
    results = []
    for url in urls:
        print(f"[提示] 正在抓取: {url}")
        html = fetch_page(url)
        if html:
            data = parse_page(html)
            results.append(data)
        time.sleep(REQUEST_INTERVAL)
    save_to_csv(results)


if __name__ == "__main__":
    main()

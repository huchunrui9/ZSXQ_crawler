# -*- coding: utf-8 -*-
"""
知识星球网页版爬虫示例脚本

此脚本用于爬取知识星球网页版的内容，包括发帖人、标题、内容和图片。
使用方法：
python crawl_zsxq_web.py
"""

import os
import sys
import json
import time
import random
from zsxq_crawler import ZsxqCrawler

def print_color(text, color="green"):
    """彩色输出文本"""
    colors = {
        "red": "\033[91m",
        "green": "\033[92m",
        "yellow": "\033[93m",
        "blue": "\033[94m",
        "purple": "\033[95m",
        "cyan": "\033[96m",
        "end": "\033[0m"
    }
    print(f"{colors.get(color, colors['green'])}{text}{colors['end']}")

def main():
    print("=" * 50)
    print_color("知识星球网页版爬虫", "blue")
    print("=" * 50)
    print("此脚本用于爬取知识星球网页版的内容")
    print("使用前请确保您有权限访问相关内容，并遵守知识星球的使用条款")
    
    # 获取用户输入
    print("\n请提供以下信息:")
    cookies = input("请输入知识星球的cookies: ")
    if not cookies:
        print_color("错误: cookies不能为空", "red")
        return
    
    url = input("请输入要爬取的知识星球URL: ")
    if not url:
        print_color("错误: URL不能为空", "red")
        return
    
    # 创建输出目录
    output_dir = "output"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # 创建爬虫实例
    try:
        crawler = ZsxqCrawler(cookies=cookies)
        
        print_color(f"\n正在爬取URL: {url}", "cyan")
        
        # 爬取网页内容
        output_file = os.path.join(output_dir, "web_posts.json")
        posts = crawler.crawl_web_page(
            url=url,
            save_images=True,
            output_file=output_file
        )
        
        if not posts:
            print_color("\n未获取到任何帖子内容", "yellow")
            return
        
        print_color(f"\n爬取完成，共获取 {len(posts)} 条帖子", "green")
        print(f"数据已保存到 {output_file}")
        
        # 打印帖子摘要
        print("\n" + "-" * 30)
        print_color("帖子内容摘要：", "purple")
        for i, post in enumerate(posts[:3], 1):  # 只显示前3条
            print(f"\n[{i}] 作者: {post['author']['name']}")
            print(f"标题: {post['title'] or '无标题'}")
            content = post['content']
            if len(content) > 100:
                content = content[:100] + "..."
            print(f"内容: {content}")
            print(f"图片数量: {len(post['images'])}")
            print(f"点赞数: {post['likes']}")
            print(f"评论数: {post['comments_count']}")
            
    except Exception as e:
        print_color(f"\n爬取过程中出错: {e}", "red")

if __name__ == "__main__":
    main()
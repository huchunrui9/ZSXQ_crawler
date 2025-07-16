# -*- coding: utf-8 -*-
"""
知识星球爬虫示例脚本

此脚本用于爬取知识星球的帖子内容，包括发帖人、标题、内容和图片。
使用方法：
python crawl_zsxq_posts.py
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
    # 用户提供的cookie
    cookies = "_c_WBKFRo=fYYt7Qtg7TmayWrG84py1YPxlbRqCFEgeCmrVXru; _nb_ioWEgULi=; zsxq_access_token=15F6A9B4-2BB1-467A-ADE6-7AE2080478C4_5BE752EA2994DCD6; abtest_env=product; sajssdk_2015_cross_new_user=1; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%22415842454114218%22%2C%22first_id%22%3A%22195fe2d35a3716-0fd1b760fdf696-26011d51-1382400-195fe2d35a41190%22%2C%22props%22%3A%7B%7D%2C%22identities%22%3A%22eyIkaWRlbnRpdHlfY29va2llX2lkIjoiMTk1ZmUyZDM1YTM3MTYtMGZkMWI3NjBmZGY2OTYtMjYwMTFkNTEtMTM4MjQwMC0xOTVmZTJkMzVhNDExOTAiLCIkaWRlbnRpdHlfbG9naW5faWQiOiI0MTU4NDI0NTQxMTQyMTgifQ%3D%3D%22%2C%22history_login_id%22%3A%7B%22name%22%3A%22%24identity_login_id%22%2C%22value%22%3A%22415842454114218%22%7D%7D"
    
    # 要爬取的星球ID
    group_id = "28888412851511"
    
    # 创建输出目录
    output_dir = "output"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # 创建图片目录
    image_dir = os.path.join(output_dir, "images")
    if not os.path.exists(image_dir):
        os.makedirs(image_dir)
    
    print("=" * 50)
    print_color("知识星球爬虫示例", "blue")
    print("=" * 50)
    
    try:
        # 创建爬虫实例
        crawler = ZsxqCrawler(cookies=cookies)
        
        print_color(f"正在爬取星球ID: {group_id}", "cyan")
        
        # 获取星球信息
        group_info = crawler.get_group_info(group_id)
        if group_info:
            group_data = group_info.get('resp_data', {}).get('group', {})
            print_color(f"星球名称: {group_data.get('name', '未知')}", "green")
            print(f"星球简介: {group_data.get('description', '无')}")
            print(f"成员数量: {group_data.get('member_count', 0)}")
        
        # 爬取帖子内容
        print("\n" + "-" * 30)
        print_color("开始爬取帖子内容...", "yellow")
        
        # 设置爬取参数
        post_count = 10  # 爬取帖子数量
        get_comments = True  # 是否获取评论
        save_images = True  # 是否保存图片
        
        # 爬取帖子
        posts = crawler.crawl_group_posts(
            group_id=group_id,
            count=post_count,
            save_images=save_images,
            output_file=os.path.join(output_dir, "posts.json"),
            get_comments=get_comments
        )
        
        print_color(f"\n爬取完成，共获取 {len(posts)} 条帖子", "green")
        print(f"数据已保存到 {os.path.join(output_dir, 'posts.json')}")
        
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
            print(f"评论数量: {len(post.get('comments', []))}")
        
        # 使用requests爬取网页版内容
        print("\n" + "-" * 30)
        print_color("使用requests爬取网页版内容...", "yellow")
        url = f"https://wx.zsxq.com/dweb2/index/group/{group_id}"
        
        html = crawler.use_selenium(url)
        if html:
            web_posts = crawler.parse_html_posts(html)
            print_color(f"从网页版获取 {len(web_posts)} 条帖子", "green")
            crawler.save_to_json(web_posts, os.path.join(output_dir, "web_posts.json"))
            print(f"网页版数据已保存到 {os.path.join(output_dir, 'web_posts.json')}")
            
            # 打印网页版帖子摘要
            print("\n" + "-" * 30)
            print_color("网页版帖子内容摘要：", "purple")
            for i, post in enumerate(web_posts[:3], 1):  # 只显示前3条
                print(f"\n[{i}] 作者: {post['author']['name']}")
                print(f"标题: {post['title'] or '无标题'}")
                content = post['content']
                if len(content) > 100:
                    content = content[:100] + "..."
                print(f"内容: {content}")
                print(f"图片数量: {len(post['images'])}")
        else:
            print_color("获取网页版内容失败", "red")
        
        print("\n" + "=" * 50)
        print_color("爬取任务完成！", "green")
        print("=" * 50)
        print(f"所有数据已保存到 {output_dir} 目录")
        
    except Exception as e:
        print_color(f"爬取过程中出错: {str(e)}", "red")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
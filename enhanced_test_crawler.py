# -*- coding: utf-8 -*-
"""
知识星球爬虫增强测试脚本

此脚本是test_crawler.py的增强版，提供更多功能：
1. 测试登录凭证是否有效
2. 测试获取星球信息
3. 测试获取帖子列表
4. 测试获取评论
5. 测试反爬机制应对策略
6. 提供更多反爬策略实现
7. 支持保存测试结果
8. 支持自动重试

使用方法：
python enhanced_test_crawler.py
"""

import time
import random
import sys
import os
import json
import datetime
from zsxq_crawler import ZsxqCrawler

# 颜色输出函数
def print_color(text, color="green"):
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

# 测试步骤装饰器
def test_step(func):
    def wrapper(*args, **kwargs):
        print("\n" + "=" * 50)
        print_color(f"[测试] {func.__name__.replace('_', ' ').title()}", "blue")
        print("=" * 50)
        result = func(*args, **kwargs)
        return result
    return wrapper

# 重试装饰器
def retry(max_retries=3, delay=2):
    def decorator(func):
        def wrapper(*args, **kwargs):
            retries = 0
            while retries < max_retries:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    retries += 1
                    if retries < max_retries:
                        print_color(f"发生错误: {str(e)}，{delay}秒后重试 ({retries}/{max_retries})...", "yellow")
                        time.sleep(delay)
                    else:
                        print_color(f"达到最大重试次数，操作失败: {str(e)}", "red")
                        raise
        return wrapper
    return decorator

@test_step
def test_login(cookies=None, token=None):
    """测试登录凭证是否有效"""
    if not cookies and not token:
        print_color("错误：需要提供cookies或token才能测试登录", "red")
        return None
        
    print("正在测试登录凭证...")
    crawler = ZsxqCrawler(cookies=cookies, token=token)
    
    # 尝试获取一个公开星球的信息来验证登录状态
    test_group_id = input("请输入一个要测试的星球ID: ")
    
    try:
        info = crawler.get_group_info(test_group_id)
        if info and isinstance(info, dict):
            print_color("登录凭证有效！成功获取星球信息", "green")
            print(f"星球名称: {info.get('resp_data', {}).get('group', {}).get('name', '未知')}")
            return crawler
        else:
            print_color("登录凭证无效或已过期", "red")
            return None
    except Exception as e:
        print_color(f"测试登录时出错: {str(e)}", "red")
        return None

@test_step
@retry(max_retries=3)
def test_group_info(crawler, group_id):
    """测试获取星球信息"""
    print(f"正在获取星球 {group_id} 的基本信息...")
    # 添加随机延时，避免频繁请求
    time.sleep(random.uniform(1, 2))
    
    try:
        info = crawler.get_group_info(group_id)
        if info:
            group_data = info.get('resp_data', {}).get('group', {})
            print_color("成功获取星球信息！", "green")
            print(f"星球名称: {group_data.get('name', '未知')}")
            print(f"星球简介: {group_data.get('description', '无')}")
            print(f"成员数量: {group_data.get('member_count', 0)}")
            return info
        else:
            print_color("获取星球信息失败", "red")
            return None
    except Exception as e:
        print_color(f"获取星球信息时出错: {str(e)}", "red")
        raise

@test_step
@retry(max_retries=3)
def test_topics(crawler, group_id, count=5):
    """测试获取帖子列表"""
    print(f"正在获取星球 {group_id} 的最新 {count} 条帖子...")
    # 添加随机延时，避免频繁请求
    time.sleep(random.uniform(1, 2))
    
    try:
        topics = crawler.get_topics(group_id, count=count)
        if topics and len(topics) > 0:
            print_color(f"成功获取 {len(topics)} 条帖子！", "green")
            for i, topic in enumerate(topics[:3], 1):  # 只显示前3条
                topic_data = topic.get('topic', {})
                print(f"\n帖子 {i}:")
                print(f"标题: {topic_data.get('title', '无标题')}")
                print(f"创建时间: {topic_data.get('create_time', '未知')}")
                print(f"类型: {topic_data.get('type', '未知')}")
            return topics
        else:
            print_color("获取帖子列表失败或没有帖子", "red")
            return []
    except Exception as e:
        print_color(f"获取帖子列表时出错: {str(e)}", "red")
        raise

@test_step
@retry(max_retries=3)
def test_comments(crawler, topics):
    """测试获取评论"""
    if not topics or len(topics) == 0:
        print_color("没有帖子可以测试评论", "yellow")
        return False
        
    # 选择第一个帖子获取评论
    topic = topics[0]
    topic_id = topic.get('topic_id')
    topic_title = topic.get('topic', {}).get('title', '无标题')
    
    print(f"正在获取帖子 '{topic_title}' 的评论...")
    # 添加随机延时，避免频繁请求
    time.sleep(random.uniform(1, 2))
    
    try:
        comments = crawler.get_comments(topic_id)
        if comments and len(comments) > 0:
            print_color(f"成功获取 {len(comments)} 条评论！", "green")
            for i, comment in enumerate(comments[:3], 1):  # 只显示前3条
                comment_data = comment.get('comment', {})
                print(f"\n评论 {i}:")
                print(f"内容: {comment_data.get('text', '无内容')}")
                print(f"作者: {comment_data.get('owner', {}).get('name', '未知')}")
                print(f"时间: {comment_data.get('create_time', '未知')}")
            return comments
        else:
            print_color("该帖子没有评论或获取评论失败", "yellow")
            return []
    except Exception as e:
        print_color(f"获取评论时出错: {str(e)}", "red")
        raise

@test_step
@retry(max_retries=2)
def test_selenium(crawler, topic_id=None):
    """测试Selenium获取页面"""
    if not topic_id:
        print_color("没有帖子ID可以测试Selenium", "yellow")
        return False
        
    url = f"https://wx.zsxq.com/dweb2/index/topic_detail/{topic_id}"
    print(f"正在使用Selenium获取页面: {url}")
    try:
        html = crawler.use_selenium(url)
        if html and len(html) > 100:  # 简单判断HTML是否有效
            print_color("成功使用Selenium获取页面内容！", "green")
            print(f"获取到HTML内容长度: {len(html)} 字符")
            print(f"HTML内容预览: {html[:100]}...")
            return html
        else:
            print_color("使用Selenium获取页面失败或内容为空", "red")
            return None
    except Exception as e:
        print_color(f"使用Selenium时出错: {str(e)}", "red")
        raise

@test_step
def test_anti_crawling_strategy():
    """测试反爬策略"""
    print("知识星球可能存在以下反爬机制，以及应对策略：")
    
    strategies = [
        ("请求频率限制", "控制请求间隔，添加随机延时"),
        ("User-Agent检测", "使用真实浏览器的User-Agent，定期更换"),
        ("Cookie/登录凭证校验", "保持登录状态，定期更新登录凭证"),
        ("IP封禁", "使用代理IP，定期更换IP"),
        ("验证码", "使用OCR识别或人工处理验证码"),
        ("JavaScript渲染", "使用Selenium等工具模拟浏览器环境"),
        ("请求头检测", "添加Referer、Origin等请求头模拟正常访问"),
        ("行为模式检测", "模拟人类浏览行为，添加随机操作和停顿"),
        ("URL参数检测", "添加正确的URL参数，如时间戳等"),
        ("指纹识别", "模拟真实浏览器指纹特征")
    ]
    
    for i, (mechanism, strategy) in enumerate(strategies, 1):
        print(f"\n{i}. {mechanism}")
        print_color(f"   应对策略: {strategy}", "cyan")
    
    print("\n实现反爬策略的代码示例:")
    print_color("""    
    # 1. 添加随机延时
    time.sleep(random.uniform(1, 3))
    
    # 2. 更换User-Agent
    user_agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Safari/605.1.15",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0"
    ]
    headers["User-Agent"] = random.choice(user_agents)
    
    # 3. 添加Referer和其他请求头
    headers["Referer"] = "https://wx.zsxq.com/dweb2/"
    headers["Origin"] = "https://wx.zsxq.com"
    headers["Accept"] = "application/json, text/plain, */*"
    headers["Accept-Language"] = "zh-CN,zh;q=0.9,en;q=0.8"
    
    # 4. 使用代理IP
    proxies = {
        "http": "http://your_proxy_ip:port",
        "https": "https://your_proxy_ip:port"
    }
    response = requests.get(url, headers=headers, cookies=cookies, proxies=proxies)
    
    # 5. 添加重试机制
    max_retries = 3
    for retry in range(max_retries):
        try:
            response = requests.get(url, headers=headers, cookies=cookies)
            if response.status_code == 200:
                break
        except Exception as e:
            print(f"请求失败，重试 {retry+1}/{max_retries}")
            time.sleep(random.uniform(2, 5))
    
    # 6. 模拟真实浏览行为（使用Selenium）
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight/2)")
    time.sleep(random.uniform(1, 3))
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
    """, "purple")
    
    return True

@test_step
def test_enhanced_headers(crawler):
    """测试增强请求头"""
    print("为了更好地模拟真实浏览器行为，可以增强请求头信息")
    
    # 原始headers
    original_headers = crawler.headers.copy()
    print("原始请求头:")
    for key, value in original_headers.items():
        print(f"  {key}: {value}")
    
    # 增强headers
    enhanced_headers = {
        "User-Agent": crawler.headers["User-Agent"],
        "Content-Type": "application/json;charset=utf8",
        "Accept": "application/json, text/plain, */*",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive",
        "Referer": "https://wx.zsxq.com/dweb2/",
        "Origin": "https://wx.zsxq.com",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-site",
        "Pragma": "no-cache",
        "Cache-Control": "no-cache"
    }
    
    print("\n增强后的请求头:")
    for key, value in enhanced_headers.items():
        print(f"  {key}: {value}")
    
    print("\n使用增强请求头的代码示例:")
    print_color("""
    # 更新爬虫类的headers属性
    crawler.headers.update({
        "Accept": "application/json, text/plain, */*",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive",
        "Referer": "https://wx.zsxq.com/dweb2/",
        "Origin": "https://wx.zsxq.com",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-site",
        "Pragma": "no-cache",
        "Cache-Control": "no-cache"
    })
    """, "cyan")
    
    return enhanced_headers

def save_test_results(results, filename="test_results.json"):
    """保存测试结果到文件"""
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(results, f, ensure_ascii=False, indent=2)
        print_color(f"测试结果已保存到 {filename}", "green")
        return True
    except Exception as e:
        print_color(f"保存测试结果失败: {str(e)}", "red")
        return False

def main():
    print("\n" + "*" * 60)
    print_color("知识星球爬虫增强测试程序", "cyan")
    print("*" * 60)
    print("此程序将帮助您测试知识星球爬虫的各项功能，并提供反爬策略建议")
    print("请按照提示输入必要的信息进行测试")
    print("\n注意：使用此脚本前，请确保您有权限访问相关内容，并遵守知识星球的使用条款")
    
    # 获取登录凭证
    print("\n请选择登录方式:")
    print("1. 使用Cookies登录")
    print("2. 使用Token登录")
    login_type = input("请输入选择(1/2): ")
    
    crawler = None
    if login_type == "1":
        cookies = input("请输入Cookies字符串: ")
        crawler = test_login(cookies=cookies)
    elif login_type == "2":
        token = input("请输入Token: ")
        crawler = test_login(token=token)
    else:
        print_color("无效的选择，程序退出", "red")
        return
    
    if not crawler:
        print_color("登录测试失败，程序退出", "red")
        return
    
    # 获取要测试的星球ID
    group_id = input("\n请输入要测试的星球ID: ")
    
    # 初始化测试结果字典
    test_results = {
        "test_time": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "group_id": group_id,
        "results": {}
    }
    
    # 测试获取星球信息
    group_info = test_group_info(crawler, group_id)
    if not group_info:
        print_color("获取星球信息失败，可能无权限访问该星球或星球ID不正确", "red")
        test_results["results"]["group_info"] = {"status": "failed"}
        save_test_results(test_results)
        return
    else:
        test_results["results"]["group_info"] = {
            "status": "success",
            "group_name": group_info.get('resp_data', {}).get('group', {}).get('name', '未知')
        }
    
    # 测试获取帖子列表
    topics = test_topics(crawler, group_id)
    test_results["results"]["topics"] = {
        "status": "success" if topics else "failed",
        "count": len(topics)
    }
    
    # 测试获取评论
    if topics and len(topics) > 0:
        comments = test_comments(crawler, topics)
        test_results["results"]["comments"] = {
            "status": "success" if comments else "failed",
            "count": len(comments) if comments else 0
        }
        
        # 测试Selenium
        topic_id = topics[0].get('topic_id')
        html = test_selenium(crawler, topic_id)
        test_results["results"]["selenium"] = {
            "status": "success" if html else "failed",
            "html_length": len(html) if html else 0
        }
    
    # 测试反爬策略
    test_anti_crawling_strategy()
    test_results["results"]["anti_crawling"] = {"status": "info_provided"}
    
    # 测试增强请求头
    enhanced_headers = test_enhanced_headers(crawler)
    test_results["results"]["enhanced_headers"] = {"status": "info_provided"}
    
    # 保存测试结果
    save_test_results(test_results)
    
    print("\n" + "*" * 60)
    print_color("测试完成！", "green")
    print("*" * 60)
    print("测试结果摘要:")
    for test_name, result in test_results["results"].items():
        status = result.get("status", "unknown")
        status_color = "green" if status == "success" else "yellow" if status == "info_provided" else "red"
        print(f"- {test_name}: ", end="")
        print_color(status, status_color)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print_color("\n程序被用户中断", "yellow")
    except Exception as e:
        print_color(f"\n程序出错: {str(e)}", "red")
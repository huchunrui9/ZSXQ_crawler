# 知识星球爬虫

这是一个用于爬取知识星球内容的Python脚本，支持获取星球信息、帖子列表、评论等数据。

## 使用前提

使用此脚本前，请确保您有权限访问相关内容，并遵守知识星球的使用条款。

## 环境要求

- Python 3.6+
- 以下Python库：
  - requests
  - json
  - time
  - os
  - csv
  - BeautifulSoup4
  - selenium
  - webdriver-manager (可选，用于自动管理WebDriver)

可以通过以下命令安装所需依赖：

```bash
pip install requests beautifulsoup4 selenium webdriver-manager
```

## 使用方法

### 1. 获取登录凭证

您需要提供知识星球的登录凭证，可以是cookies或token：

- **获取Cookies**：登录知识星球网页版，通过浏览器开发者工具获取cookies
- **获取Token**：登录后，从请求头中获取Authorization字段的Bearer token

### 2. 确定要爬取的内容

- 星球ID：从URL中获取，例如`https://wx.zsxq.com/dweb2/index/group/12345678`中的`12345678`
- 内容类型：帖子、评论等

### 3. 使用示例

```python
# 导入爬虫类
from zsxq_crawler import ZsxqCrawler

# 使用cookies初始化爬虫
cookies = "zsxq_access_token=xxx; abcdef=123456; ..."
crawler = ZsxqCrawler(cookies=cookies)

# 或者使用token初始化
# token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
# crawler = ZsxqCrawler(token=token)

# 获取星球信息
group_id = "12345678"
group_info = crawler.get_group_info(group_id)

# 获取帖子列表
topics = crawler.get_topics(group_id, count=50)

# 获取特定帖子的评论
topic_id = topics[0]['topic_id']
comments = crawler.get_comments(topic_id)

# 保存数据
crawler.save_to_json(topics, 'topics.json')
crawler.save_to_csv(comments, 'comments.csv')

# 使用Selenium获取需要JavaScript渲染的页面
url = f"https://wx.zsxq.com/dweb2/index/topic_detail/{topic_id}"
html = crawler.use_selenium(url)
```

## 注意事项

1. 知识星球可能有反爬机制，请合理控制爬取频率
2. 登录凭证有时效性，过期需要重新获取
3. 使用Selenium需要安装对应版本的Chrome浏览器和ChromeDriver

## 功能说明

- `get_group_info`: 获取星球基本信息
- `get_topics`: 获取帖子列表
- `get_comments`: 获取评论列表
- `save_to_json`: 保存数据为JSON文件
- `save_to_csv`: 保存数据为CSV文件
- `use_selenium`: 使用Selenium获取需要JavaScript渲染的页面

## 可能的扩展

- 添加更多数据处理功能
- 实现自动翻页获取更多内容
- 添加图片、附件下载功能
- 实现多线程爬取提高效率
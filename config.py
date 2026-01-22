# config.py
# Editorial Manager 账户配置文件
# 从环境变量读取配置（用于 GitHub Actions）

import os
import json

# ============================================
# 账户配置 - 从环境变量读取
# ============================================
# GitHub Actions 环境变量：ACCOUNTS_JSON
# 本地运行时可以在此填入账户信息进行测试
ACCOUNTS_ENV = os.environ.get('ACCOUNTS_JSON')

if ACCOUNTS_ENV:
    try:
        ACCOUNTS = json.loads(ACCOUNTS_ENV)
    except json.JSONDecodeError:
        print("错误: ACCOUNTS_JSON 环境变量格式不正确")
        ACCOUNTS = []
else:
    # 本地运行时的默认配置（测试用）
    ACCOUNTS = []

# ============================================
# Server酱配置（微信推送）
# ============================================
# GitHub Actions 环境变量：SERVERCHAN_SENDKEY
SERVERCHAN_SENDKEY = os.environ.get('SERVERCHAN_SENDKEY', '')
# 获取方式：访问 https://sctapi.ftqq.com/ 注册并获取 SendKey

# ============================================
# 日志配置
# ============================================
LOG_FILE = 'em_tracker.log'      # 日志文件名
LOG_LEVEL = os.environ.get('LOG_LEVEL', 'INFO')  # 日志级别: DEBUG, INFO, WARNING, ERROR

# ============================================
# 网络请求常量
# ============================================
BASE_URL = "https://www.editorialmanager.com"
LOGIN_SUCCESS_FLAG = "Default.aspx?pg=AuthorMainMenu.aspx"
DEFAULT_RETRY_COUNT = 3
RETRY_DELAY_SECONDS = 5
DEFAULT_TIMEOUT = 20

# ============================================
# 模拟浏览器头
# ============================================
BROWSER_HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'Accept-Language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7',
    'DNT': '1',
    'Upgrade-Insecure-Requests': '1',
}

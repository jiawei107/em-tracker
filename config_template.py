# config_template.py
# Editorial Manager 账户配置模板文件
#
# 本地运行使用：
# 1. 复制此文件为 config.py
# 2. 填写 ACCOUNTS 和 SERVERCHAN_SENDKEY
#
# GitHub Actions 运行使用：
# 1. 在仓库 Settings -> Secrets and variables -> Actions 中添加以下 secrets：
#    - ACCOUNTS_JSON: 账户信息（JSON 格式）
#    - SERVERCHAN_SENDKEY: Server酱 SendKey

# ============================================
# 账户配置（本地运行时使用）
# ============================================
ACCOUNTS = [
    # 示例账户配置 - 请复制并修改以下模板
    {
        'journal_short_name': 'GASTRO',           # 期刊简称
        'journal_full_name': 'Gastroenterology',  # 期刊全名
        'username': 'your_username_here',         # 替换为您的用户名
        'password': 'your_password_here'          # 替换为您的密码
    },
    # 您可以添加更多账户...
]

# ============================================
# Server酱配置（微信推送）
# ============================================
SERVERCHAN_SENDKEY = 'your_sendkey_here'  # 替换为您的 Server酱 SendKey
# 获取方式：访问 https://sctapi.ftqq.com/ 注册并获取 SendKey

# ============================================
# 日志配置
# ============================================
LOG_FILE = 'em_tracker.log'      # 日志文件名
LOG_LEVEL = 'INFO'              # 日志级别: DEBUG, INFO, WARNING, ERROR

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

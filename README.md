# Journal Manuscript Tracker

## 📋 功能说明

- 自动追踪学术期刊稿件状态（Editorial Manager 系统）
- 日志记录功能
- 微信消息推送（通过 Server酱 API）
- 支持 GitHub Actions 自动运行

## 🚀 快速开始

### 方式一：本地运行

#### 1. 创建配置文件
```bash
copy config_template.py config.py
```

#### 2. 编辑 `config.py`
```python
# 填入期刊账户信息
ACCOUNTS = [
    {
        'journal_short_name': 'GASTRO',
        'journal_full_name': 'Gastroenterology',
        'username': 'your_email@example.com',
        'password': 'your_password'
    },
]

# 填入 Server酱 SendKey（用于微信推送）
SERVERCHAN_SENDKEY = 'your_sendkey_here'
```

#### 3. 安装依赖
```bash
pip install -r requirements.txt
```

#### 4. 运行程序
```bash
python main.py
```

---

### 方式二：GitHub Actions 自动运行（推荐）

#### 1. Fork 本仓库到你的 GitHub 账户

#### 2. 配置 GitHub Secrets

进入你的仓库：`Settings` → `Secrets and variables` → `Actions` → `New repository secret`

添加以下 secrets：

| Secret 名称 | 说明 | 示例 |
|-------------|------|------|
| `ACCOUNTS_JSON` | 账户信息（JSON 格式） | `[{"journal_short_name":"GASTRO","journal_full_name":"Gastroenterology","username":"email@example.com","password":"pwd"}]` |
| `SERVERCHAN_SENDKEY` | Server酱 SendKey | `SCT123456xxxx` |

**ACCOUNTS_JSON 格式说明：**
```json
[
  {
    "journal_short_name": "GASTRO",
    "journal_full_name": "Gastroenterology",
    "username": "your_email@example.com",
    "password": "your_password"
  },
  {
    "journal_short_name": "GUT",
    "journal_full_name": "Gut",
    "username": "your_email@example.com",
    "password": "your_password"
  }
]
```

#### 3. 启用 GitHub Actions

- 进入 `Actions` 标签页
- 点击 `I understand my workflows, go ahead and enable them`

#### 4. 工作流配置

默认配置：
- **运行时间**：每天 UTC 0:00（北京时间 8:00）
- **支持手动触发**：在 Actions 页面点击 "Run workflow"

修改运行时间：
编辑 `.github/workflows/daily-tracker.yml` 中的 `cron` 表达式：
```yaml
schedule:
  # 格式：分 时 日 月 周
  # 每天 UTC 8:00 = 北京时间 16:00
  - cron: '0 8 * * *'
```

#### 5. 查看运行结果

- 进入 `Actions` 标签页查看工作流运行历史
- 可以下载运行日志文件（artifacts）

## 📊 输出示例

### 控制台输出
```
2024-01-22 08:00:00 - __main__ - INFO - ============================================================
2024-01-22 08:00:00 - __main__ - INFO - Journal Manuscript Tracker - 简化版
2024-01-22 08:00:00 - __main__ - INFO - 正在登录 'Gastroenterology'...
2024-01-22 08:00:05 - __main__ - INFO - 登录成功！账户: your@email.com
2024-01-22 08:00:06 - __main__ - INFO - 共发现 2 条稿件记录
2024-01-22 08:00:08 - __main__ - INFO - 微信推送成功
```

### 微信推送

**标题:** 📊 稿件追踪结果 (2024-01-22 08:00)

**内容:**
```
### Gastroenterology

📄 **Innovative Treatment Approach for IBD...**
• 编号: MS2024-001
• 状态: Under Review
• 日期: 2024-01-15
```

## 🔧 配置说明

### 本地运行配置

| 配置项 | 说明 | 必填 |
|--------|------|------|
| `journal_short_name` | 期刊简称（如 GASTRO） | ✅ |
| `journal_full_name` | 期刊全名 | ✅ |
| `username` | EM 账户用户名 | ✅ |
| `password` | EM 账户密码 | ✅ |
| `SERVERCHAN_SENDKEY` | Server酱 API Key | ✅ |
| `LOG_FILE` | 日志文件名 | ❌ |
| `LOG_LEVEL` | 日志级别 | ❌ |

### GitHub Actions 配置

| Secret 名称 | 说明 | 必填 |
|-------------|------|------|
| `ACCOUNTS_JSON` | 账户信息（JSON 格式） | ✅ |
| `SERVERCHAN_SENDKEY` | Server酱 SendKey | ✅ |

## 📦 依赖

- requests - HTTP 请求
- beautifulsoup4 - HTML 解析
- lxml - XML/HTML 解析器

## 📝 日志级别

- `DEBUG` - 详细调试信息
- `INFO` - 一般信息（默认）
- `WARNING` - 警告信息
- `ERROR` - 错误信息

## ⚠️ 注意事项

1. **时间时区**：GitHub Actions 使用 UTC 时间，请注意时区转换
2. **Secrets 安全**：GitHub Secrets 加密存储，不会在日志中显示
3. **手动触发**：如需立即运行，可在 Actions 页面手动触发工作流
4. **日志保留**：GitHub Actions 日志保留 90 天，artifacts 保留 7 天

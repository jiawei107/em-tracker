"""
Journal Manuscript Tracker - 简化版
从配置文件读取账户信息并追踪稿件状态
"""

import requests
import re
import time
import logging
from datetime import datetime
from bs4 import BeautifulSoup
from typing import Union, Dict, List, Any
from urllib.parse import urlparse, urlunparse, parse_qs, urlencode

# 配置导入
try:
    from config import (
        ACCOUNTS, BASE_URL, LOGIN_SUCCESS_FLAG, DEFAULT_RETRY_COUNT,
        RETRY_DELAY_SECONDS, DEFAULT_TIMEOUT, BROWSER_HEADERS,
        SERVERCHAN_SENDKEY, LOG_FILE, LOG_LEVEL
    )
except ImportError as e:
    print(f"[错误] 未找到 config.py 文件或配置不完整: {e}")
    print("请先复制 config_template.py 为 config.py 并填写配置信息。")
    exit(1)

# 配置日志
logging.basicConfig(
    level=getattr(logging, LOG_LEVEL.upper(), logging.INFO),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(LOG_FILE, encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


def send_to_serverchan(title: str, content: str) -> bool:
    """通过 Server酱 API 推送消息到微信"""
    if not SERVERCHAN_SENDKEY or SERVERCHAN_SENDKEY == 'your_sendkey_here':
        logger.warning("Server酱 SendKey 未配置，跳过微信推送")
        return False

    url = f"https://sctapi.ftqq.com/{SERVERCHAN_SENDKEY}.send"
    data = {
        'title': title,
        'desp': content
    }

    try:
        response = requests.post(url, data=data, timeout=10)
        result = response.json()

        if result.get('code') == 0:
            logger.info("微信推送成功")
            return True
        else:
            logger.error(f"微信推送失败: {result.get('message', '未知错误')}")
            return False

    except Exception as e:
        logger.error(f"微信推送异常: {e}")
        return False


def perform_login(account: dict) -> Union[requests.Session, None]:
    """执行登录操作并返回已认证的session"""
    journal_short = account['journal_short_name']
    login_url = f"{BASE_URL}/{journal_short}/LoginAction.ashx"
    login_payload = {'username': account['username'], 'password': account['password']}

    logger.info(f"正在登录 '{account['journal_full_name']}'...")

    for attempt in range(DEFAULT_RETRY_COUNT):
        try:
            session = requests.Session()
            session.headers.update(BROWSER_HEADERS)

            response = session.post(login_url, data=login_payload, timeout=DEFAULT_TIMEOUT)
            response.raise_for_status()

            if LOGIN_SUCCESS_FLAG in response.text:
                logger.info(f"登录成功！账户: {account['username']}")
                return session
            else:
                logger.error(f"登录失败。请检查账户信息: {account['username']}")
                return None

        except requests.exceptions.RequestException as e:
            logger.error(f"网络错误: {e}")

        if attempt < DEFAULT_RETRY_COUNT - 1:
            logger.info(f"{RETRY_DELAY_SECONDS} 秒后重试...")
            time.sleep(RETRY_DELAY_SECONDS)

    logger.error(f"所有登录尝试均失败: {account['username']}")
    return None


def fetch_manuscript_details(session: requests.Session, detail_url: str, referer_url: str) -> List[Dict[str, Any]]:
    """获取稿件详细信息"""
    page_name = detail_url.split('/')[-1].split('?')[0]

    try:
        headers = BROWSER_HEADERS.copy()
        headers['Referer'] = referer_url
        response = session.get(detail_url, headers=headers, timeout=DEFAULT_TIMEOUT)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'lxml')

        # 检查是否有分页器
        if soup.find('select', {'name': 'size1'}):
            parsed_url = urlparse(detail_url)
            query_params = parse_qs(parsed_url.query)
            query_params['size1'] = ['500']
            query_params['size2'] = ['500']
            full_data_url = urlunparse(parsed_url._replace(query=urlencode(query_params, doseq=True)))
            response = session.get(full_data_url, headers=headers, timeout=DEFAULT_TIMEOUT)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'lxml')

        manuscript_list = []
        table = soup.find('table', id='datatable') or soup.find('table', id='searchresults')
        if not table:
            return []

        thead = table.find('thead')
        tbody = table.find('tbody')
        if not thead or not tbody:
            return []

        original_headers = [th.get_text(strip=True) for th in thead.find_all('th')]
        data_rows = tbody.find_all('tr')

        for row in data_rows:
            cells = [child for child in row.children if child.name == 'td']
            if len(cells) == len(original_headers):
                manuscript_data = {original_headers[i]: cells[i].get_text(strip=True) for i in range(len(cells))}

                # 提取docid
                action_link = cells[0].find('a', href=re.compile(r'docid=(\d+)'))
                if action_link:
                    match = re.search(r'docid=(\d+)', action_link['href'])
                    if match:
                        manuscript_data['docid'] = match.group(1)

                manuscript_list.append(manuscript_data)

        logger.debug(f"成功获取 {len(manuscript_list)} 条稿件记录: {page_name}")
        return manuscript_list

    except Exception as e:
        logger.error(f"获取详情失败: {e}")
        return []


def fetch_submission_overview(session: requests.Session, account: dict) -> Union[List[Dict[str, Any]], None]:
    """获取投稿概览"""
    journal_short = account['journal_short_name']
    base_journal_url = f"{BASE_URL}/{journal_short}/"
    main_menu_url = f"{base_journal_url}AuthorMainMenu.aspx"

    logger.info("正在获取稿件列表...")

    try:
        headers = BROWSER_HEADERS.copy()
        headers['Referer'] = f'{base_journal_url}default2.aspx'
        response = session.get(main_menu_url, headers=headers, timeout=DEFAULT_TIMEOUT)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        logger.error(f"获取主菜单失败: {e}")
        return None

    try:
        soup = BeautifulSoup(response.text, 'html.parser')
        all_manuscripts = []

        for link in soup.select('fieldset.datatablecontainer div.main_menu_item a'):
            count_span = link.find_next_sibling('span', class_='count')
            if count_span and '(0)' not in count_span.get_text():
                full_detail_url = f"{base_journal_url}{link['href']}"
                details = fetch_manuscript_details(session, full_detail_url, main_menu_url)
                if details:
                    all_manuscripts.extend(details)

        logger.info(f"共发现 {len(all_manuscripts)} 条稿件记录")
        return all_manuscripts

    except Exception as e:
        logger.error(f"解析失败: {e}")
        return None


def find_value_by_partial_key(data: Dict[str, str], key_parts: List[str]) -> str:
    """通过部分关键词匹配字典中的值"""
    for key, value in data.items():
        normalized_key = ''.join(key.split()).lower()
        if any(part.lower() in normalized_key for part in key_parts):
            return value
    return ''


def format_manuscript_info(manuscript: Dict[str, Any]) -> str:
    """格式化单条稿件信息"""
    title = find_value_by_partial_key(manuscript, ['title']) or 'No-Title-Found'
    ms_number = find_value_by_partial_key(manuscript, ['manuscriptnumber'])
    submission_date = find_value_by_partial_key(manuscript, ['submissionbegan', 'initialdate', 'datesubmitted'])
    status_date = find_value_by_partial_key(manuscript, ['statusdate'])
    status = find_value_by_partial_key(manuscript, ['currentstatus'])

    return (
        f"📄 {title[:50]}...\n"
        f"   稿件编号: {ms_number}\n"
        f"   当前状态: {status}\n"
        f"   状态日期: {status_date}\n"
        f"   投稿日期: {submission_date}\n"
    )


def main():
    """主函数"""
    logger.info("=" * 60)
    logger.info("Journal Manuscript Tracker - 简化版")
    logger.info("=" * 60)

    all_results = []
    wechat_content = ""

    # 遍历所有账户
    for account in ACCOUNTS:
        if 'your_username' in account.get('username', '').lower():
            logger.warning(f"跳过未配置的账户: {account.get('username', '')}")
            continue

        logger.info("=" * 60)
        logger.info(f"期刊: {account['journal_full_name']} ({account['journal_short_name']})")
        logger.info(f"账户: {account['username']}")
        logger.info("=" * 60)

        # 登录
        session = perform_login(account)
        if not session:
            continue

        # 获取稿件信息
        manuscripts = fetch_submission_overview(session, account)
        if not manuscripts:
            logger.info("无稿件记录。")
            continue

        # 处理每条稿件记录
        wechat_content += f"\n### {account['journal_full_name']}\n\n"

        for manuscript in manuscripts:
            title = find_value_by_partial_key(manuscript, ['title']) or 'No-Title-Found'
            ms_number = find_value_by_partial_key(manuscript, ['manuscriptnumber'])
            submission_date = find_value_by_partial_key(manuscript, ['submissionbegan', 'initialdate', 'datesubmitted'])
            status_date = find_value_by_partial_key(manuscript, ['statusdate'])
            status = find_value_by_partial_key(manuscript, ['currentstatus'])

            result = {
                '时间戳': datetime.now().strftime('%Y-%m-%d %H:%M'),
                '投稿日期': submission_date,
                '状态日期': status_date,
                '当前状态': status,
                '稿件编号': ms_number
            }

            all_results.append(result)

            logger.info(f"稿件: {title[:50]}...")
            logger.info(f"  编号: {ms_number}")
            logger.info(f"  状态: {status}")
            logger.info(f"  状态日期: {status_date}")

            # 添加到微信推送内容
            wechat_content += f"📄 **{title[:40]}...**\n"
            wechat_content += f"• 编号: {ms_number}\n"
            wechat_content += f"• 状态: {status}\n"
            wechat_content += f"• 日期: {status_date}\n\n"

    # 输出汇总信息到日志
    if all_results:
        logger.info("=" * 60)
        logger.info("汇总结果")
        logger.info("=" * 60)

        for result in all_results:
            logger.info(
                f"时间戳: {result['时间戳']} | "
                f"稿件编号: {result['稿件编号']} | "
                f"状态: {result['当前状态']} | "
                f"状态日期: {result['状态日期']}"
            )

        logger.info(f"共处理 {len(all_results)} 条稿件记录")

        # 推送到微信
        wechat_title = f"📊 稿件追踪结果 ({datetime.now().strftime('%Y-%m-%d %H:%M')})"
        if wechat_content.strip():
            send_to_serverchan(wechat_title, wechat_content)
    else:
        logger.warning("未获取到任何稿件信息。")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        logger.info("程序被用户中断。")
    except Exception as e:
        logger.error(f"未处理的错误: {e}", exc_info=True)

<<<<<<< HEAD
"""
Journal Manuscript Tracker - 简化版
从配置文件读取账户信息并追踪稿件状态
=======
# main.py
"""
Journal Manuscript Tracker (v31.1 - The Open Source Release)
一个用于追踪学术期刊稿件状态的工具

Features:
1. 多期刊账户管理
2. 彩色命令行界面  
3. Excel格式历史记录
4. 临时账户查询模式
5. 智能错误处理和重试机制
>>>>>>> b9dafe607e64aa64da2259be10d19906969b2d0d
"""

import requests
import re
import time
<<<<<<< HEAD
import logging
=======
import os
import hashlib
import pandas as pd
>>>>>>> b9dafe607e64aa64da2259be10d19906969b2d0d
from datetime import datetime
from bs4 import BeautifulSoup
from typing import Union, Dict, List, Any
from urllib.parse import urlparse, urlunparse, parse_qs, urlencode

<<<<<<< HEAD
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

=======
# 彩色输出支持
try:
    import colorama
    from colorama import Fore, Style, init
    init(autoreset=True)
    C_GREEN = Fore.GREEN
    C_RED = Fore.RED
    C_YELLOW = Fore.YELLOW
    C_BLUE = Fore.BLUE
    C_CYAN = Fore.CYAN
    C_BOLD = Style.BRIGHT
    C_RESET = Style.RESET_ALL
except ImportError:
    print("[警告] 未找到 colorama 库。输出将不带颜色。请运行 'pip install colorama' 以获得最佳体验。")
    C_GREEN = C_RED = C_YELLOW = C_BLUE = C_CYAN = C_BOLD = C_RESET = ''

# 配置导入
try:
    from config import (
        ACCOUNTS, BASE_URL, LOGIN_SUCCESS_FLAG, DEFAULT_RETRY_COUNT, 
        RETRY_DELAY_SECONDS, DEFAULT_TIMEOUT, BROWSER_HEADERS
    )
except ImportError:
    print(C_RED + "[致命错误] 未找到 config.py 文件或文件内容不完整。")
    print(C_YELLOW + "请先运行 'python add_config.py' 创建配置文件。")
    exit(1)

>>>>>>> b9dafe607e64aa64da2259be10d19906969b2d0d

def perform_login(account: dict) -> Union[requests.Session, None]:
    """执行登录操作并返回已认证的session"""
    journal_short = account['journal_short_name']
    login_url = f"{BASE_URL}/{journal_short}/LoginAction.ashx"
    login_payload = {'username': account['username'], 'password': account['password']}
<<<<<<< HEAD

    logger.info(f"正在登录 '{account['journal_full_name']}'...")

=======
    
    print(C_BLUE + f"\n正在尝试登录 '{account['journal_full_name']}'...")
    
>>>>>>> b9dafe607e64aa64da2259be10d19906969b2d0d
    for attempt in range(DEFAULT_RETRY_COUNT):
        try:
            session = requests.Session()
            session.headers.update(BROWSER_HEADERS)
<<<<<<< HEAD

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
=======
            print(f"  - 第 {attempt + 1} 次尝试...")
            
            response = session.post(login_url, data=login_payload, timeout=DEFAULT_TIMEOUT)
            response.raise_for_status()
            
            if LOGIN_SUCCESS_FLAG in response.text:
                print(C_GREEN + C_BOLD + "\n[成功] " + C_GREEN + "登录成功！")
                return session
            else:
                print(C_RED + C_BOLD + "\n[失败] " + C_RED + "登录失败。请检查用户名、密码或期刊简称。")
                return None
                
        except requests.exceptions.RequestException as e:
            print(C_RED + f"  - 尝试失败: 发生网络错误: {e}")
            
        if attempt < DEFAULT_RETRY_COUNT - 1:
            print(C_YELLOW + f"  - {RETRY_DELAY_SECONDS} 秒后重试...")
            time.sleep(RETRY_DELAY_SECONDS)
    
    print(C_RED + C_BOLD + "\n[失败] " + C_RED + "所有登录尝试均告失败。")
>>>>>>> b9dafe607e64aa64da2259be10d19906969b2d0d
    return None


def fetch_manuscript_details(session: requests.Session, detail_url: str, referer_url: str) -> List[Dict[str, Any]]:
    """获取稿件详细信息"""
    page_name = detail_url.split('/')[-1].split('?')[0]
<<<<<<< HEAD

    try:
=======
    print(f"    -> 正在钻取详情: {page_name}")
    
    try:
        print("      - 步骤 1/2: 初步加载页面以检查分页...")
>>>>>>> b9dafe607e64aa64da2259be10d19906969b2d0d
        headers = BROWSER_HEADERS.copy()
        headers['Referer'] = referer_url
        response = session.get(detail_url, headers=headers, timeout=DEFAULT_TIMEOUT)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'lxml')

<<<<<<< HEAD
        # 检查是否有分页器
        if soup.find('select', {'name': 'size1'}):
=======
        # 检查是否有分页器，如果有则获取全量数据
        if soup.find('select', {'name': 'size1'}):
            print("      - 检测到分页器。正在尝试获取全量数据（每页500条）...")
>>>>>>> b9dafe607e64aa64da2259be10d19906969b2d0d
            parsed_url = urlparse(detail_url)
            query_params = parse_qs(parsed_url.query)
            query_params['size1'] = ['500']
            query_params['size2'] = ['500']
            full_data_url = urlunparse(parsed_url._replace(query=urlencode(query_params, doseq=True)))
<<<<<<< HEAD
            response = session.get(full_data_url, headers=headers, timeout=DEFAULT_TIMEOUT)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'lxml')
=======
            
            print("      - 步骤 2/2: 正在从新URL加载全量数据...")
            response = session.get(full_data_url, headers=headers, timeout=DEFAULT_TIMEOUT)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'lxml')
        else:
            print("      - 未检测到分页器，直接解析当前页面。")
>>>>>>> b9dafe607e64aa64da2259be10d19906969b2d0d

        manuscript_list = []
        table = soup.find('table', id='datatable') or soup.find('table', id='searchresults')
        if not table:
            return []
<<<<<<< HEAD

=======
            
>>>>>>> b9dafe607e64aa64da2259be10d19906969b2d0d
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
<<<<<<< HEAD

=======
                
>>>>>>> b9dafe607e64aa64da2259be10d19906969b2d0d
                # 提取docid
                action_link = cells[0].find('a', href=re.compile(r'docid=(\d+)'))
                if action_link:
                    match = re.search(r'docid=(\d+)', action_link['href'])
                    if match:
                        manuscript_data['docid'] = match.group(1)
<<<<<<< HEAD

                manuscript_list.append(manuscript_data)

        logger.debug(f"成功获取 {len(manuscript_list)} 条稿件记录: {page_name}")
        return manuscript_list

    except Exception as e:
        logger.error(f"获取详情失败: {e}")
=======
                        
                manuscript_list.append(manuscript_data)

        print(C_GREEN + f"      - 成功! 发现 {len(manuscript_list)} 条稿件记录。")
        return manuscript_list
        
    except Exception as e:
        print(C_RED + f"      - 钻取失败或依赖缺失: {e}")
>>>>>>> b9dafe607e64aa64da2259be10d19906969b2d0d
        return []


def fetch_submission_overview(session: requests.Session, account: dict) -> Union[List[Dict[str, Any]], None]:
    """获取投稿概览"""
    journal_short = account['journal_short_name']
    base_journal_url = f"{BASE_URL}/{journal_short}/"
    main_menu_url = f"{base_journal_url}AuthorMainMenu.aspx"
<<<<<<< HEAD

    logger.info("正在获取稿件列表...")

=======
    
    print(C_BLUE + C_BOLD + "\n[步骤 2] " + C_BLUE + "正在获取主菜单页面...")
    
>>>>>>> b9dafe607e64aa64da2259be10d19906969b2d0d
    try:
        headers = BROWSER_HEADERS.copy()
        headers['Referer'] = f'{base_journal_url}default2.aspx'
        response = session.get(main_menu_url, headers=headers, timeout=DEFAULT_TIMEOUT)
        response.raise_for_status()
<<<<<<< HEAD
    except requests.exceptions.RequestException as e:
        logger.error(f"获取主菜单失败: {e}")
        return None

    try:
        soup = BeautifulSoup(response.text, 'html.parser')
        all_manuscripts = []

=======
        print(C_GREEN + "  - 成功！已获取主菜单HTML。")
    except requests.exceptions.RequestException as e:
        print(C_RED + f"[错误] 获取主菜单页面失败: {e}")
        return None

    print(C_BLUE + C_BOLD + "\n[步骤 3] " + C_BLUE + "正在解析主菜单并钻取所有详情...")
    
    try:
        soup = BeautifulSoup(response.text, 'html.parser')
        all_manuscripts = []
        
>>>>>>> b9dafe607e64aa64da2259be10d19906969b2d0d
        for link in soup.select('fieldset.datatablecontainer div.main_menu_item a'):
            count_span = link.find_next_sibling('span', class_='count')
            if count_span and '(0)' not in count_span.get_text():
                full_detail_url = f"{base_journal_url}{link['href']}"
                details = fetch_manuscript_details(session, full_detail_url, main_menu_url)
                if details:
                    all_manuscripts.extend(details)
<<<<<<< HEAD

        logger.info(f"共发现 {len(all_manuscripts)} 条稿件记录")
        return all_manuscripts

    except Exception as e:
        logger.error(f"解析失败: {e}")
        return None


=======
                    
        print(C_GREEN + "  - 成功！所有非空类别的稿件详情均已获取。")
        return all_manuscripts
        
    except Exception as e:
        print(C_RED + f"[错误] 解析或钻取时发生致命错误: {e}")
        return None


def sanitize_filename(text: str, max_length: int = 80) -> str:
    """清理文件名中的非法字符"""
    sanitized = re.sub(r'[\\/*?:"<>|]', "", text)
    return re.sub(r'\s+', '-', sanitized.strip())[:max_length]


def safe_write_excel(df: pd.DataFrame, file_path: str) -> bool:
    """安全写入Excel文件，处理文件占用等异常"""
    try:
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
    except Exception as e:
        print(C_RED + f"  - [致命写入错误] 无法创建目录: {os.path.dirname(file_path)}. 错误: {e}")
        return False
        
    while True:
        try:
            with pd.ExcelWriter(file_path, engine='xlsxwriter') as writer:
                df.to_excel(writer, sheet_name='History', index=False, header=False, startrow=1)
                workbook = writer.book
                worksheet = writer.sheets['History']
                
                # 设置表头格式
                header_format = workbook.add_format({
                    'bold': True, 'top': 2, 'bottom': 1, 
                    'valign': 'vcenter', 'text_wrap': True
                })
                
                # 写入表头
                for col_num, value in enumerate(df.columns.values):
                    worksheet.write(0, col_num, value, header_format)
                
                # 自动调整列宽
                for i, col in enumerate(df.columns):
                    width = max(df[col].astype(str).map(len).max(), len(col)) + 2
                    worksheet.set_column(i, i, min(width, 70))
                    
            return True
            
        except PermissionError:
            print(C_YELLOW + f"\n  - [操作暂停] 文件 '{os.path.basename(file_path)}' 正被另一程序占用。")
            input(C_YELLOW + "    请关闭该Excel文件后，按 Enter键 继续...")
            print(C_YELLOW + "  - [重试] 正在尝试重新写入...")
            
        except Exception as e:
            print(C_RED + f"  - [写入失败] 发生未知错误: {e}")
            return False


>>>>>>> b9dafe607e64aa64da2259be10d19906969b2d0d
def find_value_by_partial_key(data: Dict[str, str], key_parts: List[str]) -> str:
    """通过部分关键词匹配字典中的值"""
    for key, value in data.items():
        normalized_key = ''.join(key.split()).lower()
        if any(part.lower() in normalized_key for part in key_parts):
            return value
    return ''


<<<<<<< HEAD
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
=======
def process_and_track_manuscripts(all_manuscripts: List[Dict[str, Any]], account: dict):
    """处理和追踪稿件状态"""
    if not all_manuscripts:
        print(C_YELLOW + "\n未发现任何需要追踪的稿件。")
        return
        
    print(C_BLUE + C_BOLD + "\n[步骤 4] " + C_BLUE + "开始处理和追踪稿件状态...")
    username_dir = os.path.join('data', account['username'])
    os.makedirs(username_dir, exist_ok=True)

    for manuscript in all_manuscripts:
        title = find_value_by_partial_key(manuscript, ['title']) or 'No-Title-Found'
        ms_number = find_value_by_partial_key(manuscript, ['manuscriptnumber'])
        docid = manuscript.get('docid')

        # 确定搜索前缀和标识符
        if ms_number:
            search_prefix = f"{ms_number}_"
            identifier_log = f"MS#: {ms_number}"
        elif docid:
            search_prefix = f"docid_{docid}_"
            identifier_log = f"DocID: {docid}"
        else:
            title_hash = hashlib.sha1(title.encode('utf-8')).hexdigest()[:10]
            search_prefix = f"hash_{title_hash}_"
            identifier_log = f"Title Hash: {title_hash}"

        print(C_CYAN + f"\n--- 正在处理: {title[:60]}... ({identifier_log}) ---")

        # 处理文件夹命名和重命名
        safe_folder_title = sanitize_filename(title)
        target_dir_name = f"{search_prefix}{safe_folder_title}"
        target_manuscript_dir = os.path.join(username_dir, target_dir_name)
        current_manuscript_dir = target_manuscript_dir

        # 检查是否需要重命名现有文件夹
        for item_name in os.listdir(username_dir):
            item_path = os.path.join(username_dir, item_name)
            if os.path.isdir(item_path) and item_name.startswith(search_prefix):
                existing_dir = item_path
                if existing_dir != target_manuscript_dir:
                    try:
                        os.rename(existing_dir, target_manuscript_dir)
                        print(C_GREEN + f"  - [标题更新] 已成功重命名文件夹 -> '{target_dir_name}'")
                    except Exception as e:
                        print(C_YELLOW + f"  - [重命名失败] {e}. 本次将使用旧文件夹。")
                        current_manuscript_dir = existing_dir
                break

        # 处理Excel历史记录
        excel_filename = f"{sanitize_filename(title)}_投稿追踪.xlsx"
        history_file = os.path.join(current_manuscript_dir, excel_filename)

        new_data = {
            'SubmissionBeganDate': find_value_by_partial_key(
                manuscript, ['submissionbegan', 'initialdate', 'datesubmitted']
            ),
            'StatusDate': find_value_by_partial_key(manuscript, ['statusdate']),
            'Status': find_value_by_partial_key(manuscript, ['currentstatus']),
            'ManuscriptNumber': ms_number,
            'Title': title
        }

        if not os.path.exists(history_file):
            print("  - 首次记录稿件历史。")
            new_record = pd.DataFrame([{
                'Timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                **new_data
            }])
            if safe_write_excel(new_record, history_file):
                print(C_GREEN + f"    - 已创建并格式化历史文件: {excel_filename}")
        else:
            try:
                df_history = pd.read_excel(history_file)
                last_record = df_history.iloc[-1]
                
                if (last_record['Status'] == new_data['Status'] and 
                    last_record['StatusDate'] == new_data['StatusDate']):
                    print(f"  - [状态未变] 当前状态与上次记录相同: {new_data['Status']}")
                else:
                    print(C_YELLOW + "  - [状态更新!] " + C_YELLOW + "发现新状态或状态日期变更。")
                    print(f"    - 旧状态: {last_record['Status']} ({last_record['StatusDate']})")
                    print(f"    - 新状态: {new_data['Status']} ({new_data['StatusDate']})")
                    
                    new_record = pd.DataFrame([{
                        'Timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                        **new_data
                    }])
                    updated_df = pd.concat([df_history, new_record], ignore_index=True)
                    
                    if safe_write_excel(updated_df, history_file):
                        print(C_GREEN + f"    - 历史记录已更新并重新格式化: {excel_filename}")
                        
            except Exception as e:
                print(C_RED + f"  - [读写错误] 无法处理历史文件 '{excel_filename}'。错误: {e}")


def get_temporary_account() -> dict:
    """获取临时账户信息"""
    print(C_BLUE + "\n请输入临时账户信息 (此信息不会被保存):")
    journal_full_name = input(f"  - {C_CYAN}期刊全名 (例如 'Gastroenterology'): {C_RESET}")
    journal_short_name = input(f"  - {C_CYAN}期刊简称 (例如 'GASTRO'): {C_RESET}")
    username = input(f"  - {C_CYAN}用户名: {C_RESET}")
    password = input(f"  - {C_CYAN}密码 (警告:输入可见): {C_RESET}")
    
    return {
        'journal_full_name': journal_full_name,
        'journal_short_name': journal_short_name.upper(),
        'username': username,
        'password': password
    }


def run_single_query(account: dict):
    """执行单次查询"""
    print(C_BLUE + C_BOLD + "\n[步骤 1] " + C_BLUE + "正在初始化登录流程...")
    logged_in_session = perform_login(account)
    if not logged_in_session:
        return

    all_manuscripts_data = fetch_submission_overview(logged_in_session, account)
    if all_manuscripts_data is not None:
        process_and_track_manuscripts(all_manuscripts_data, account)
    else:
        print(C_RED + "\n在数据抓取过程中发生错误，请检查上方的日志信息。")
    
    print("\n" + C_GREEN + "=" * 25 + " 本次查询完毕 " + "=" * 25)


def main():
    """主函数，程序入口"""
    while True:
        # 清屏并显示标题
        os.system('cls' if os.name == 'nt' else 'clear')
        print("\n" + C_CYAN + "=" * 60)
        print(C_CYAN + C_BOLD + " Journal Manuscript Tracker (v31.1)")
        print(C_CYAN + "=" * 60)

        # 组织账户数据
        accounts_by_user = {}
        valid_accounts = [acc for acc in ACCOUNTS if 'YOUR_USERNAME' not in acc.get('username', '')]
        
        for acc in valid_accounts:
            username = acc['username']
            if username not in accounts_by_user:
                accounts_by_user[username] = []
            accounts_by_user[username].append(acc)

        usernames = list(accounts_by_user.keys())

        # 显示用户选择菜单
        print(C_BLUE + "\n请选择要查询的用户:")
        if not usernames:
            print(C_YELLOW + "  -> config.py 中未配置任何有效账户。")
        else:
            for i, username in enumerate(usernames):
                journal_count = len(accounts_by_user[username])
                print(f"  {C_GREEN}[{i + 1}] {username} ({journal_count}本期刊)")

        temp_choice_num = len(usernames) + 1
        print(f"  {C_YELLOW}[{temp_choice_num}] 手动输入临时账户进行查询")
        print(f"  {C_RED}[Q] 退出程序")

        # 获取用户选择
        choice = input(C_BOLD + "\n请输入您的选择: ").strip().lower()

        # 处理退出
        if choice == 'q':
            break

        selected_account = None
        
        # 处理数字选择
        if choice.isdigit():
            try:
                choice_num = int(choice)
                
                # 选择预设用户
                if 1 <= choice_num <= len(usernames):
                    chosen_username = usernames[choice_num - 1]
                    journals_for_user = accounts_by_user[chosen_username]
                    
                    if len(journals_for_user) == 1:
                        selected_account = journals_for_user[0]
                        print(C_CYAN + f"  -> 已自动选择用户 '{chosen_username}' 的唯一期刊: {selected_account['journal_full_name']}")
                        time.sleep(1)
                    else:
                        print(f"\n{C_BLUE}用户 '{chosen_username}' 关联了多本期刊，请选择:")
                        for i, acc in enumerate(journals_for_user):
                            print(f"  {C_GREEN}[{i + 1}] {acc['journal_full_name']}")
                        print(f"  {C_RED}[B] 返回上级菜单")
                        
                        sub_choice_str = input(C_BOLD + "\n请选择期刊: ").strip().lower()
                        if sub_choice_str == 'b':
                            continue
                            
                        try:
                            sub_choice_num = int(sub_choice_str)
                            if 1 <= sub_choice_num <= len(journals_for_user):
                                selected_account = journals_for_user[sub_choice_num - 1]
                            else:
                                print(C_RED + "\n[错误] 无效的期刊选择。")
                                time.sleep(1.5)
                        except ValueError:
                            print(C_RED + "\n[错误] 请输入有效的数字。")
                            time.sleep(1.5)
                
                # 选择临时账户
                elif choice_num == temp_choice_num:
                    selected_account = get_temporary_account()
                else:
                    print(C_RED + "\n[错误] 无效的选择，请输入列表中的数字。")
                    time.sleep(1.5)
                    
            except ValueError:
                print(C_RED + "\n[错误] 无效的输入，请输入正确的数字或 'q'。")
                time.sleep(1.5)
        else:
            print(C_RED + "\n[错误] 无效的输入，请输入数字或 'q'。")
            time.sleep(1.5)

        # 执行查询
        if selected_account:
            run_single_query(selected_account)
            prompt = f"\n{C_YELLOW}>>> 操作完成。按 Enter 返回主菜单，或输入 'q' 退出: {C_RESET}"
            post_action_choice = input(prompt).lower()
            if post_action_choice == 'q':
                break

    print(C_BLUE + "\n感谢使用，再见！")
>>>>>>> b9dafe607e64aa64da2259be10d19906969b2d0d


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
<<<<<<< HEAD
        logger.info("程序被用户中断。")
    except Exception as e:
        logger.error(f"未处理的错误: {e}", exc_info=True)
=======
        print(C_YELLOW + "\n\n程序被用户中断。")
    except Exception as e:
        print(C_RED + C_BOLD + f"\n[未处理的致命错误] 发生了一个意外错误: {e}")
>>>>>>> b9dafe607e64aa64da2259be10d19906969b2d0d

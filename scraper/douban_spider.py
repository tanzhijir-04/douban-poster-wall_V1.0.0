import os
import re
import sys
import time
import json

# 支持直接运行：python scraper/douban_spider.py
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import requests
from bs4 import BeautifulSoup

from scraper.config import (
    COLLECT_URL, WISH_URL, POSTER_DIR, MAX_PAGES,
    REQUEST_DELAY, HEADERS,
)
from scraper.utils import logger

# 文件名不允许的字符
INVALID_CHARS = re.compile(r'[\\/:*?"<>|\x00-\x1f]')

# 保留扩展名映射
EXT_MAP = {
    "movie": ".jpg",
    "book": ".jpg",
    "music": ".jpg",
}


def safe_filename(title):
    """将标题转为安全的文件名"""
    name = INVALID_CHARS.sub("", title).strip()
    if not name:
        return None
    # Windows 保留名称
    if name.lower() in ("con", "prn", "aux", "nul", "com1", "lpt1"):
        name = f"_{name}"
    # 限制长度
    if len(name.encode("utf-8")) > 200:
        name = name[:60]
    return name


def deduplicate_name(name, used_names):
    """处理同名冲突：加序号"""
    if name not in used_names:
        used_names.add(name)
        return name
    counter = 2
    while f"{name}_{counter}" in used_names:
        counter += 1
    result = f"{name}_{counter}"
    used_names.add(result)
    return result


def download_poster(url, save_path):
    try:
        response = requests.get(url, headers=HEADERS, timeout=15)
        if response.status_code == 200:
            with open(save_path, "wb") as f:
                f.write(response.content)
            return True
        logger.warning("下载失败（%d）：%s", response.status_code, url)
        return False
    except Exception as e:
        logger.error("下载出错：%s，链接：%s", e, url)
        return False


def crawl_page(url, page_type, poster_dict):
    """爬取页面，返回 {海报URL: 作品标题} 字典"""
    page = 0
    consecutive_empty = 0
    logger.info("===== 开始爬取【%s】页面 =====", page_type)

    while consecutive_empty < 3 and page < MAX_PAGES:
        start = page * 20
        current_url = f"{url}?start={start}&sort=time&rating=all&filter=all&mode=grid"
        logger.info("爬取%s第%d页：%s", page_type, page + 1, current_url)

        try:
            response = requests.get(current_url, headers=HEADERS, timeout=15)
            response.encoding = "utf-8"

            if response.status_code == 403:
                logger.warning("收到 403，可能被反爬限制，等待 10 秒后重试")
                time.sleep(10)
                continue

            if response.status_code == 429:
                logger.warning("收到 429，请求过频，等待 15 秒后重试")
                time.sleep(15)
                continue

            soup = BeautifulSoup(response.text, "html.parser")

            current_count = 0
            for item in soup.select(".grid-view .item"):
                img = item.select_one("img")
                if not img or "src" not in img.attrs:
                    continue

                src = img["src"]
                if "doubanio.com" not in src and "douban.com" not in src:
                    continue
                if src in poster_dict:
                    continue

                # 提取标题：优先 .info .title，其次 .info a，最后 img alt
                title = None
                title_el = item.select_one(".info .title") or item.select_one(".info a")
                if title_el:
                    title = title_el.get_text(strip=True)
                if not title:
                    title = img.get("alt", "").strip()
                if not title:
                    title = f"poster_{abs(hash(src)) % 1000000}"

                poster_dict[src] = title
                current_count += 1

            logger.info("%s第%d页：新增%d张（累计：%d张）", page_type, page + 1, current_count, len(poster_dict))

            if current_count == 0:
                consecutive_empty += 1
            else:
                consecutive_empty = 0

            page += 1
            time.sleep(REQUEST_DELAY)

        except requests.exceptions.RequestException as e:
            logger.error("%s第%d页网络错误：%s", page_type, page + 1, e)
            page += 1
            time.sleep(REQUEST_DELAY * 2)
        except Exception as e:
            logger.error("%s第%d页解析错误：%s", page_type, page + 1, e)
            page += 1
            time.sleep(REQUEST_DELAY)

    logger.info("【%s】页面爬取完成，累计%d张", page_type, len(poster_dict))


def crawl_all_posters():
    os.makedirs(POSTER_DIR, exist_ok=True)
    all_posters = {}

    crawl_page(COLLECT_URL, "已看", all_posters)
    crawl_page(WISH_URL, "想看", all_posters)

    # 已有文件映射：先扫描已存在的文件，建立 {标题: 文件名} 映射
    used_names = set()
    for f in os.listdir(POSTER_DIR):
        if f.lower().endswith((".jpg", ".jpeg", ".webp", ".png")):
            name = os.path.splitext(f)[0]
            used_names.add(name)

    logger.info("===== 开始下载所有海报（共%d张） =====", len(all_posters))
    for idx, (url, title) in enumerate(all_posters.items(), 1):
        ext = os.path.splitext(url.split("?")[0])[1] or ".jpg"
        name = safe_filename(title)
        if not name:
            name = f"poster_{abs(hash(url)) % 1000000}"
        name = deduplicate_name(name, used_names)
        filename = f"{name}{ext}"
        save_path = os.path.join(POSTER_DIR, filename)

        if os.path.exists(save_path):
            logger.info("[%d] 已存在：%s", idx, filename)
            continue

        if download_poster(url, save_path):
            logger.info("[%d] 下载成功：%s", idx, filename)
        else:
            logger.warning("[%d] 下载失败：%s", idx, filename)

    poster_paths = [
        f"./posters/{f}" for f in os.listdir(POSTER_DIR)
        if f.lower().endswith((".jpg", ".jpeg", ".webp", ".png"))
    ]

    json_path = os.path.join(os.path.dirname(POSTER_DIR), "poster_paths.json")
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(poster_paths, f, indent=2, ensure_ascii=False)

    logger.info("===== 全部完成 =====")
    logger.info("已看+想看合计：%d张", len(all_posters))
    logger.info("成功下载到本地：%d张", len(poster_paths))


if __name__ == "__main__":
    crawl_all_posters()

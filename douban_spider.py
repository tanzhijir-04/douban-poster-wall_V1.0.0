import requests
import os
import time
import json
from bs4 import BeautifulSoup
from dotenv import load_dotenv  # 新增：用于加载.env文件

# 加载本地.env文件（关键：用户只需填ID）
load_dotenv()  # 自动读取项目根目录的.env文件

# 从.env获取豆瓣ID，自动生成链接（用户无需手动输入URL）
DOUBAN_ID = os.getenv("DOUBAN_ID")
if not DOUBAN_ID:
    print("错误：请在.env文件中填写DOUBAN_ID（豆瓣数字ID）")
    exit(1)

# 自动生成已看和想看页面的链接
COLLECT_URL = f"https://movie.douban.com/people/{DOUBAN_ID}/collect"  # 已看
WISH_URL = f"https://movie.douban.com/people/{DOUBAN_ID}/wish"        # 想看

POSTER_DIR = "posters"  # 统一保存所有海报
os.makedirs(POSTER_DIR, exist_ok=True)

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0.0.0 Safari/537.36",
    "Referer": "https://movie.douban.com/"
}


def download_poster(url, save_path):
    try:
        response = requests.get(url, headers=headers, timeout=15, stream=True)
        if response.status_code == 200:
            with open(save_path, "wb") as f:
                f.write(response.content)
            return True
        print(f"下载失败（{response.status_code}）：{url}")
        return False
    except Exception as e:
        print(f"下载出错：{e}，链接：{url}")
        return False


def crawl_page(url, page_type, poster_set):
    """爬取单个页面（已看/想看）的海报，添加到集合中"""
    page = 0
    consecutive_empty = 0
    print(f"\n===== 开始爬取【{page_type}】页面 =====")

    while consecutive_empty < 3:  # 连续3页空则停止
        start = page * 20
        current_url = f"{url}?start={start}&sort=time&rating=all&filter=all&mode=grid"
        print(f"爬取{page_type}第{page + 1}页：{current_url}")

        try:
            response = requests.get(current_url, headers=headers, timeout=15)
            response.encoding = "utf-8"
            soup = BeautifulSoup(response.text, "html.parser")

            # 提取当前页海报
            current_count = 0
            for item in soup.select(".grid-view .item"):
                img = item.select_one("img")
                if img and "src" in img.attrs:
                    src = img["src"]
                    if "doubanio.com" in src or "douban.com" in src:
                        if src not in poster_set:
                            poster_set.add(src)
                            current_count += 1

            print(f"{page_type}第{page + 1}页：新增{current_count}张（累计：{len(poster_set)}张）")

            # 判断是否空页
            if current_count == 0:
                consecutive_empty += 1
            else:
                consecutive_empty = 0

            page += 1
            time.sleep(2)

        except Exception as e:
            print(f"{page_type}第{page + 1}页出错：{e}，继续爬取")
            page += 1
            time.sleep(3)

    print(f"【{page_type}】页面爬取完成，累计{len(poster_set)}张")


def crawl_all_posters():
    all_posters = set()  # 用集合自动去重（已看和想看可能有重复）

    # 1. 先爬“已看”页面
    crawl_page(COLLECT_URL, "已看", all_posters)

    # 2. 再爬“想看”页面
    crawl_page(WISH_URL, "想看", all_posters)

    # 3. 下载所有海报
    print(f"\n===== 开始下载所有海报（共{len(all_posters)}张） =====")
    for idx, url in enumerate(all_posters, 1):
        # 处理带参数的链接（如 ?param=xxx）
        filename = url.split("/")[-1].split("?")[0]
        save_path = os.path.join(POSTER_DIR, filename)

        if os.path.exists(save_path):
            print(f"[{idx}] 已存在：{filename}")
            continue

        if download_poster(url, save_path):
            print(f"[{idx}] 下载成功：{filename}")
        else:
            print(f"[{idx}] 下载失败：{filename}")

    # 4. 生成前端路径列表
    poster_paths = [f"./{POSTER_DIR}/{f}" for f in os.listdir(POSTER_DIR)
                    if f.lower().endswith((".jpg", ".jpeg", ".webp", ".png"))]
    with open("poster_paths.json", "w", encoding="utf-8") as f:
        json.dump(poster_paths, f, indent=2)

    print(f"\n===== 全部完成 =====")
    print(f"已看+想看合计：{len(all_posters)}张")
    print(f"成功下载到本地：{len(poster_paths)}张")


if __name__ == "__main__":
    crawl_all_posters()
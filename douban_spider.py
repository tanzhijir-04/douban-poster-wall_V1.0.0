import requests
<<<<<<< HEAD
import os
import time
import json
from bs4 import BeautifulSoup

# 配置：已看和想看页面的链接
COLLECT_URL = "https://movie.douban.com/people/220645464/collect"  # 已看
WISH_URL = "https://movie.douban.com/people/220645464/wish"  # 想看

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
=======
import json
import os
import time

# 读取环境变量（必须配置正确）
DOUBAN_URL = os.getenv("DOUBAN_COLLECT_URL")
COOKIE = os.getenv("DOUBAN_COOKIE", "")

if not DOUBAN_URL:
    print("错误：未设置 DOUBAN_COLLECT_URL")
    exit(1)

# 关键：模拟真实浏览器请求头（包含Cookie）
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Cookie": COOKIE,
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    "Referer": "https://movie.douban.com/",
    "Connection": "keep-alive"
}

# 存储海报链接（去重）
posters = set()
>>>>>>> d80966fec88d1a9b587bbeac702c803dbbe38457

def crawl_all_posters():
    """循环爬取所有页面，直到没有新海报"""
    page = 0  # 从第0页开始（start=0, 20, 40...）
    while True:
        start = page * 20
        url = f"{DOUBAN_URL}?start={start}&sort=time&rating=all&filter=all&mode=grid"
        print(f"爬取页面：{url}")
        
        try:
            # 发送请求（带Cookie，允许重定向）
            response = requests.get(url, headers=headers, timeout=15, allow_redirects=True)
            response.raise_for_status()  # 检查请求是否成功
            html = response.text
            
            # 关键：从HTML中直接提取海报链接（豆瓣海报链接格式固定）
            # 海报链接格式：https://img9.doubanio.com/view/photo/s_ratio_poster/public/p1234567.jpg
            start_marker = 'src="https://img'
            end_marker = '" class="cover"'
            
            # 循环提取当前页所有海报
            page_posters = []
            index = 0
            while True:
                # 找到海报链接的起始位置
                index = html.find(start_marker, index)
                if index == -1:
                    break  # 没有更多海报了
                # 找到链接结束位置
                end_index = html.find(end_marker, index)
                if end_index == -1:
                    break
                # 提取完整链接
                poster_url = html[index + 5 : end_index]  # 去掉开头的 'src="'
                # 替换为中等清晰度
                poster_url = poster_url.replace("s_ratio_poster", "m_ratio_poster")
                page_posters.append(poster_url)
                index = end_index  # 继续查找下一个
            
            # 检查当前页是否有新海报
            if not page_posters:
                print(f"第{page+1}页未找到海报，停止爬取")
                break
            
            # 添加到集合（自动去重）
            posters.update(page_posters)
            print(f"第{page+1}页爬取成功，新增{len(page_posters)}张海报（累计：{len(posters)}）")
            
            # 翻页（最多爬50页，避免无限循环，可根据需要调整）
            page += 1
            if page >= 50:
                print("已爬取50页，自动停止")
                break
            
            time.sleep(3)  # 延迟3秒，降低反爬风险
            
        except Exception as e:
            print(f"爬取失败：{str(e)}，停止爬取")
            break

# 主逻辑
if __name__ == "__main__":
<<<<<<< HEAD
    crawl_all_posters()
=======
    crawl_all_posters()
    # 保存结果到posters.json
    with open("posters.json", "w", encoding="utf-8") as f:
        json.dump(list(posters), f, ensure_ascii=False, indent=2)
    print(f"\n爬取完成，共获取{len(posters)}张海报，已保存到posters.json")
>>>>>>> d80966fec88d1a9b587bbeac702c803dbbe38457

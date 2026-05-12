import os
import sys
from dotenv import load_dotenv

load_dotenv()

DOUBAN_ID = os.getenv("DOUBAN_ID")
DOUBAN_COOKIE = os.getenv("DOUBAN_COOKIE", "")

if not DOUBAN_ID:
    print("错误：请在 .env 文件中填写 DOUBAN_ID（豆瓣数字ID）")
    sys.exit(1)

COLLECT_URL = f"https://movie.douban.com/people/{DOUBAN_ID}/collect"
WISH_URL = f"https://movie.douban.com/people/{DOUBAN_ID}/wish"

POSTER_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "posters")
MAX_PAGES = 50
REQUEST_DELAY = 2

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0.0.0 Safari/537.36",
    "Referer": "https://movie.douban.com/",
}

if DOUBAN_COOKIE:
    HEADERS["Cookie"] = DOUBAN_COOKIE

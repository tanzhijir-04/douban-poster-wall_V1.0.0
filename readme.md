# 豆瓣观影海报墙 & 屏保

一个自动爬取你的豆瓣 "已看" 和 "想看" 电影海报，生成个性化海报墙和 3D 动态屏保的项目。支持本地、Nginx、Docker、Vercel 等多环境部署，适配电脑、手机和安卓电视。

### 您可以爱发电赞助我：https://afdian.com/a/tanz666
### 网页效果预览
 https://tanzhijir-04.github.io/douban-poster-wall_V1.0.0/

## 项目介绍

这个项目会自动爬取你在豆瓣上标记的电影海报，生成两种展示形式：
- **海报墙**：苹果风格的网格布局，展示所有海报，支持响应式设计。
- **3D 屏保**：海报自动 3D 翻滚动画，支持点击屏幕或按 `ESC` 退出，可在电视 / 电脑上作为屏保使用。

## 界面展示

- 屏保模式展示：![屏保截图](/pic_readme/screensaver.png)
- 海报墙展示：![海报墙截图](/pic_readme/poster-wall.png)

## 功能亮点

- **全自动爬取**：每天定时更新豆瓣海报，去重处理避免重复下载。
- **以作品命名**：海报文件以电影/图书/音乐名称命名，清晰直观。
- **多端适配**：电脑、手机、安卓电视均可访问，屏保模式支持全屏显示。
- **多部署方案**：支持本地运行、Nginx/Caddy、Docker、Vercel 等多种部署方式。
- **个性化配置**：仅需填写豆瓣 ID 即可使用，无需复杂设置。

## 技术栈

- **前端**：HTML5、CSS3（苹果风格动画）、JavaScript（3D 变换逻辑）
- **后端**：Python（爬虫脚本）、BeautifulSoup（页面解析）
- **部署**：Nginx、Caddy、Docker、Vercel
- **工具**：Git（版本控制）、python-dotenv（环境配置）

## 快速开始

### 准备工作

1. 获取你的豆瓣数字 ID：
   - 打开豆瓣个人主页（如`https://movie.douban.com/people/220645464/`），其中`220645464`即为数字 ID。

2. （可选）豆瓣 Cookie（用于私密列表爬取）：
   - 浏览器登录豆瓣，按 F12→Network→复制任意请求的`Cookie`字段。

3. 初始使用前，请将 `posters` 文件夹、`poster_paths.json` 清空，不然显示的就是我的内容。

### 本地运行

```bash
git clone https://github.com/你的用户名/豆瓣海报墙.git
cd 豆瓣海报墙

# 配置
cp .env.example .env
# 编辑 .env 填入你的豆瓣 ID

# 安装依赖
python -m venv .venv
.venv/Scripts/activate  # Windows
source .venv/bin/activate  # macOS/Linux
pip install -r requirements.txt

# 运行爬虫
python -m scraper.douban_spider

# 启动服务器
python -m http.server 8000
```

访问 `http://localhost:8000`

---

## 部署方案

### 方案 1：Nginx 部署（推荐生产环境）

适合自有服务器、VPS、云主机。

```bash
# 1. 在服务器上克隆项目并运行爬虫
git clone https://github.com/你的用户名/豆瓣海报墙.git
cd 豆瓣海报墙
cp .env.example .env  # 填入你的豆瓣 ID
pip install -r requirements.txt
python -m scraper.douban_spider

# 2. 配置 Nginx
sudo cp nginx.conf /etc/nginx/conf.d/poster-wall.conf
# 修改 root 路径指向你的项目目录
sudo sed -i 's|/usr/share/nginx/html|/你的项目路径|' /etc/nginx/conf.d/poster-wall.conf

# 3. 重载 Nginx
sudo nginx -t && sudo nginx -s reload
```

Nginx 配置已包含：
- 海报图片缓存 30 天
- CSS/JS 缓存 7 天
- `poster_paths.json` 不缓存（爬虫更新后立即生效）

### 方案 2：Caddy 部署（自动 HTTPS）

Caddy 自动申请和续签 SSL 证书，适合需要 HTTPS 的场景。

```bash
# 1. 运行爬虫生成数据（同上）

# 2. 修改 Caddyfile 中的域名
# 将 :80 改为你的域名，如 poster.example.com

# 3. 启动
docker run -d \
  -p 80:80 -p 443:443 \
  -v $(pwd):/srv:ro \
  -v caddy_data:/data \
  caddy caddy run --config /srv/Caddyfile
```

### 方案 3：Docker 部署（适合 NAS / 本地服务器）

```bash
# 构建并启动
docker-compose up -d

# 访问 http://localhost:8080
```

`docker-compose.yml` 已将 `posters/` 和 `poster_paths.json` 挂载为卷，爬虫在宿主机运行后数据自动同步到容器。

如需更新海报：
```bash
# 在宿主机运行爬虫
python -m scraper.douban_spider

# 重启容器（刷新 JSON 缓存）
docker-compose restart web
```

### 方案 4：Vercel 部署（静态托管）

1. 推送代码到 GitHub
2. 在 Vercel 导入仓库，Framework Preset 选 "Other"
3. 构建命令留空，Output Directory 填 `.`
4. 部署后通过 EasyCron 定时触发 Serverless 爬虫

> 注意：Vercel 适合纯静态展示。爬虫需配合 Serverless API 或在本地运行后推送 `posters/` 和 `poster_paths.json`。

### 方案 5：Synology NAS（Docker GUI）

1. 打开 Docker → 注册表 → 搜索 `nginx:alpine`，拉取镜像
2. 文件 station 中创建共享文件夹，放入项目文件
3. 创建容器：端口映射 `8080:80`，挂载项目目录到 `/usr/share/nginx/html`
4. 在容器内运行爬虫，或在宿主机 SSH 中运行

---

## 目录结构

```
豆瓣海报墙/
├── .env.example          # 环境变量模板
├── .env                  # 环境变量配置（用户填写，不入库）
├── requirements.txt      # Python 依赖
├── index.html            # 海报墙页面
├── screensaver.html      # 屏保页面
├── Dockerfile            # Docker 镜像定义
├── docker-compose.yml    # Docker Compose 配置
├── nginx.conf            # Nginx 配置
├── Caddyfile             # Caddy 配置
├── docs/
│   ├── design.md         # 设计规范
│   └── prd.md            # 产品需求文档
├── scraper/
│   ├── config.py         # 爬虫配置（环境变量、常量）
│   ├── utils.py          # 日志工具
│   └── douban_spider.py  # 核心爬虫逻辑
├── static/
│   ├── css/              # 样式文件
│   ├── js/               # 脚本文件
│   └── favicon.ico       # 网站图标
├── posters/              # 海报图片（自动生成，不入库）
├── poster_paths.json     # 海报路径索引（自动生成，不入库）
└── pic_readme/           # README 截图
```

## 常见问题

1. **爬不到海报？**
   - 检查 `.env` 中 `DOUBAN_ID` 是否正确。
   - 若列表为私密，需填写 `DOUBAN_COOKIE`。
   - 查看日志排除反爬拦截（可在 `scraper/config.py` 中增大 `REQUEST_DELAY`）。

2. **屏保动画卡顿？**
   - 减少海报数量（在 `scraper/config.py` 中修改 `MAX_PAGES`）。
   - 降低翻转频率（修改 `static/js/screensaver.js` 中的 `setInterval` 时间）。

3. **Docker 部署后图片不更新？**
   - 在宿主机重新运行爬虫后，重启 web 容器：`docker-compose restart web`

4. **Nginx 403 Forbidden？**
   - 检查 `nginx.conf` 中 `root` 路径是否正确
   - 确认 Nginx 用户（通常是 `www-data`）有权限读取项目目录

## 许可证

MIT License（开源免费，可自由修改和二次分发）

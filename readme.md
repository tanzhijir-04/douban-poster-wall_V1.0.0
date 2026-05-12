# 豆瓣观影海报墙 & 屏保

一个自动爬取你的豆瓣 "已看" 和 "想看" 电影海报，生成个性化海报墙和 3D 动态屏保的项目。支持本地、GitHub+Vercel、Docker 等多环境部署，适配电脑、手机和安卓电视。

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
- **多端适配**：电脑、手机、安卓电视均可访问，屏保模式支持全屏显示。
- **多部署方案**：支持本地运行、Vercel 静态部署、Docker 容器化（适合 NAS）。
- **个性化配置**：仅需填写豆瓣 ID 即可使用，无需复杂设置。

## 技术栈

- **前端**：HTML5、CSS3（苹果风格动画）、JavaScript（3D 变换逻辑）
- **后端**：Python（爬虫脚本）、BeautifulSoup（页面解析）
- **部署**：Vercel（静态页面 +Serverless 接口）、Docker（容器化部署）
- **工具**：Git（版本控制）、python-dotenv（环境配置）

## 快速开始

### 准备工作

1. 获取你的豆瓣数字 ID：
   - 打开豆瓣个人主页（如`https://movie.douban.com/people/220645464/`），其中`220645464`即为数字 ID。

2. （可选）豆瓣 Cookie（用于私密列表爬取）：
   - 浏览器登录豆瓣，按 F12→Network→复制任意请求的`Cookie`字段。

3. 初始使用前，请将 `posters` 文件夹、`poster_paths.json` 清空，不然显示的就是我的内容。

### 部署方案

#### 方案 1：本地运行（适合测试）

1. 克隆项目到本地：
   ```bash
   git clone https://github.com/你的用户名/豆瓣海报墙.git
   cd 豆瓣海报墙
   ```

2. 配置环境变量：
   ```bash
   cp .env.example .env
   ```
   编辑 `.env` 文件，填入你的豆瓣 ID。

3. 安装依赖并运行：
   ```bash
   python -m venv .venv
   .venv/Scripts/activate  # Windows
   source .venv/bin/activate  # macOS/Linux

   pip install -r requirements.txt

   # 运行爬虫
   python -m scraper.douban_spider

   # 启动本地服务器
   python -m http.server 8000
   ```

4. 访问：`http://localhost:8000` 查看海报墙，点击 "进入屏保模式" 体验屏保。

#### 方案 2：GitHub + Vercel 部署（适合公网访问）

1. 上传项目到 GitHub。
2. 部署到 Vercel：导入 GitHub 仓库，在 Environment Variables 中添加 `DOUBAN_ID`。
3. 配置自动更新：用 [EasyCron](https://easycron.com/) 定时访问 `https://xxx.vercel.app/api/crawl`。

#### 方案 3：Docker 部署（适合 NAS 或本地服务器）

```bash
docker-compose up -d
```

## 目录结构

```
豆瓣海报墙/
├── .env.example          # 环境变量模板
├── .env                  # 环境变量配置（用户填写，不入库）
├── requirements.txt      # Python 依赖
├── index.html            # 海报墙页面
├── screensaver.html      # 屏保页面
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
   - 查看日志排除反爬拦截（可延长爬取间隔）。

2. **屏保动画卡顿？**
   - 减少海报数量（在 `scraper/config.py` 中修改 `MAX_PAGES`）。
   - 降低翻转频率（修改 `static/js/screensaver.js` 中的 `setInterval` 时间）。

## 许可证

MIT License（开源免费，可自由修改和二次分发）

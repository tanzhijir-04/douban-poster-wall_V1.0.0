# 产品需求文档 — 豆瓣观影海报墙

## 产品概述

豆瓣观影海报墙是一个自动化工具，从用户的豆瓣"已看"和"想看"列表中爬取电影海报，生成两种展示形式：可浏览的海报墙和 3D 动态屏保。适配电脑、手机和安卓电视。

**目标用户**：豆瓣用户，希望将个人观影记录可视化展示。

---

## 用户故事

1. 作为用户，我只需填写豆瓣 ID，爬虫就能自动获取我的所有电影海报
2. 作为用户，我可以在浏览器中以网格墙的形式浏览所有海报
3. 作为用户，我可以进入屏保模式，在电视或显示器上作为环境展示
4. 作为用户，我可以通过点击屏幕、按 ESC 键或移动鼠标来退出屏保
5. 作为用户，我可以在本地、Vercel 或 Docker 环境中部署此项目

---

## 功能需求

### 爬虫模块

| 编号 | 需求 | 优先级 |
|---|---|---|
| FR-S1 | 从 .env 读取 DOUBAN_ID，自动生成已看/想看页面 URL | P0 |
| FR-S2 | 支持可选的 DOUBAN_COOKIE 用于访问私密列表 | P1 |
| FR-S3 | 分页爬取豆瓣列表页，自动去重海报 URL | P0 |
| FR-S4 | 下载海报图片到 posters/ 目录，跳过已存在文件 | P0 |
| FR-S5 | 生成 poster_paths.json 索引文件 | P0 |
| FR-S6 | 可配置的请求间隔（默认 2 秒），避免触发反爬 | P0 |
| FR-S7 | 最大页数限制（默认 50 页），防止无限爬取 | P1 |
| FR-S8 | 结构化日志输出（含时间戳），替代裸 print | P1 |
| FR-S9 | 异常退出使用 sys.exit()，非 exit() | P2 |
| FR-S10 | 优雅处理网络错误、HTTP 403/429、空响应 | P1 |

### 海报墙页面

| 编号 | 需求 | 优先级 |
|---|---|---|
| FR-W1 | 通过 fetch() 加载 poster_paths.json | P0 |
| FR-W2 | CSS Grid 响应式网格布局，自适应列数 | P0 |
| FR-W3 | 页面加载时交错渐入动画（Apple spring 曲线） | P0 |
| FR-W4 | 图片懒加载 loading="lazy" | P1 |
| FR-W5 | 图片加载失败显示本地占位图，防止 onerror 死循环 | P1 |
| FR-W6 | 语义化 HTML（main、header、figure） | P2 |
| FR-W7 | ARIA 属性（按钮 aria-label） | P2 |
| FR-W8 | Meta 标签（description、og:title） | P2 |
| FR-W9 | 深色模式（prefers-color-scheme: dark） | P2 |
| FR-W10 | DocumentFragment 批量渲染，避免逐个 reflow | P1 |

### 屏保页面

| 编号 | 需求 | 优先级 |
|---|---|---|
| FR-C1 | 全视口马赛克网格布局 | P0 |
| FR-C2 | 随机翻转 3D 动画（Apple spring 曲线） | P0 |
| FR-C3 | 点击任意位置退出 | P0 |
| FR-C4 | 鼠标静止 3 秒后自动隐藏光标 | P1 |
| FR-C5 | 鼠标移动时光标重新显示 | P1 |
| FR-C6 | ESC 键退出 | P0 |
| FR-C7 | 所有动效使用 Apple 非线性曲线 | P1 |
| FR-C8 | 翻转竞态防护：正在动画的格子不会被重复触发 | P1 |
| FR-C9 | 阻止页面滚动和文本选中 | P2 |

---

## 非功能需求

| 编号 | 需求 |
|---|---|
| NFR-1 | 无构建工具、无前端框架，纯原生 HTML/CSS/JS + Python |
| NFR-2 | 静态文件部署（python -m http.server、Nginx、Vercel） |
| NFR-3 | 所有界面文本使用中文 |
| NFR-4 | 支持 100+ 海报无性能问题 |
| NFR-5 | 本地服务器下页面加载时间 < 2 秒 |

---

## 部署方案

### 方案 1：本地运行
```bash
pip install -r requirements.txt
python -m scraper.douban_spider
python -m http.server 8000
```

### 方案 2：GitHub + Vercel
- 静态文件推送至 GitHub
- Vercel 部署为静态站点
- 通过 Serverless API + EasyCron 定时爬取

### 方案 3：Docker
- docker-compose 容器化部署，适合 NAS

---

## 不在范围内

- 前端构建流水线
- 后端 API（爬虫除外）
- Web UI 的用户认证
- 海报元数据（评分、评论）——仅展示图片

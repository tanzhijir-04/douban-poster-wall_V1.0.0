# 豆瓣观影海报墙 & 屏保

一个自动爬取你的豆瓣 “已看” 和 “想看” 电影海报，生成个性化海报墙和 3D 动态屏保的项目。支持本地、GitHub+Vercel、Docker 等多环境部署，适配电脑、手机和安卓电视。

### 您可以爱发电赞助我：https://afdian.com/a/tanz666
### 网页效果预览
 https://tanzhijir-04.github.io/douban-poster-wall_V1.0.0/



## 项目介绍

这个项目会自动爬取你在豆瓣上标记的电影海报，生成两种展示形式：
- **海报墙**：苹果风格的网格布局，展示所有海报，支持响应式设计。
- **3D 屏保**：海报自动 3D 翻滚动画，支持按`ESC`退出，可在电视 / 电脑上作为屏保使用。


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
   git clone https://github.com/ 你的用户名 / 豆瓣海报墙 .git
   cd 豆瓣海报墙
   ```

2. 配置环境变量：
   - 新建`.env`文件，填入：
     ```env
     DOUBAN_ID= 你的豆瓣数字 ID
     DOUBAN_COOKIE= 你的豆瓣 Cookie（可选）
     ```

3. 安装依赖并运行：
   ```bash
   # 创建虚拟环境（可选）
   python -m venv .venv
   .venv/Scripts/activate  # Windows
   source .venv/bin/activate  # macOS/Linux

   # 安装依赖
   pip install -r requirements.txt

   # 手动爬取海报
   python douban_spider.py

   # 启动本地服务器（推荐用 Python 内置服务器）
   python -m http.server 8000
   ```

4. 访问：`http://localhost:8000` 查看海报墙，点击 “进入屏保模式” 体验屏保。


#### 方案 2：GitHub + Vercel 部署（适合公网访问）

1. 上传项目到 GitHub：
   - 将本地项目推送到你的 GitHub 仓库（参考前文 “上传本地项目到 GitHub” 步骤）。

2. 部署到 Vercel：
   - 登录 Vercel，导入 GitHub 仓库。
   - 在 Vercel 项目设置→“Environment Variables” 中添加：
     ```
     DOUBAN_ID= 你的豆瓣数字 ID
     DOUBAN_COOKIE= 你的豆瓣 Cookie（可选）
     ```
   - 点击 “Deploy”，部署完成后获得访问域名（如`xxx.vercel.app`）。

3. 配置自动更新：
   - 用 [EasyCron](https://easycron.com/) 定时访问`https://xxx.vercel.app/api/crawl`（每天一次），自动爬取新海报。


#### 方案 3：Docker 部署（适合 NAS 或本地服务器）

1. 准备文件：
   - 确保项目包含`docker-compose.yml`和`.env`（配置方法同上）。

2. 启动容器：
   ```bash
   # 进入项目目录
   cd 豆瓣海报墙

   # 启动服务（后台运行）
   docker-compose up -d
   ```

3. 访问：
   - 局域网内访问`http://NAS 的 IP 地址:8080`（端口在`.env`中配置）。


## 目录结构

```
豆瓣海报墙 /
├── .env               # 环境变量配置（用户填写）
├── docker-compose.yml # Docker 部署配置
├── requirements.txt   # Python 依赖
├── index.html         # 海报墙页面
├── screensaver.html   # 屏保页面
├── douban_spider.py   # 核心爬虫脚本
├── api/
│   └── crawl.py       # Vercel Serverless 接口（自动爬取用）
├── posters/           # 海报图片存储目录（自动生成）
└── poster_paths.json  # 海报路径索引（自动生成）
```


## 常见问题

1. **爬不到海报？**
   - 检查`.env`中`DOUBAN_ID`是否正确。
   - 若列表为私密，需填写`DOUBAN_COOKIE`。
   - 查看日志排除反爬拦截（可延长爬取间隔）。

2. **屏保动画卡顿？**
   - 减少海报数量（爬虫脚本中限制最大页数）。
   - 降低`screensaver.html`中动画帧率（修改`setInterval`时间）。

3. **Vercel 部署后图片不显示？**
   - 确保`poster_paths.json`中路径为`posters/xxx.jpg`（相对路径）。
   - 检查爬虫接口是否正常（访问`/api/crawl`查看返回）。


## 许可证

MIT License（开源免费，可自由修改和二次分发）
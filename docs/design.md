# 设计规范 — 豆瓣观影海报墙

## 项目定位

个人豆瓣电影海报收藏展示工具。两种模式：可浏览的海报墙网格 + 环境氛围 3D 屏保。设计语言参考 Apple 官网风格。

---

## 配色

| Token | 值 | 用途 |
|---|---|---|
| `--color-bg` | `#f5f5f7` | 浅色模式海报墙背景 |
| `--color-bg-dark` | `#000000` | 屏保 / 深色模式背景 |
| `--color-surface` | `#ffffff` | 海报卡片背景 |
| `--color-text-primary` | `#1d1d1f` | 标题、主文本 |
| `--color-text-secondary` | `#6e6e73` | 统计信息、副文本 |
| `--color-glass-bg` | `rgba(255,255,255,0.25)` | 毛玻璃按钮背景 |
| `--color-glass-border` | `rgba(255,255,255,0.18)` | 毛玻璃按钮边框 |
| `--color-shadow` | `rgba(0,0,0,0.08)` | 海报卡片默认阴影 |
| `--color-shadow-hover` | `rgba(0,0,0,0.12)` | 海报卡片悬停阴影 |

### 深色模式

通过 `@media (prefers-color-scheme: dark)` 覆盖：

| Token | 深色值 |
|---|---|
| `--color-bg` | `#1d1d1f` |
| `--color-surface` | `#2d2d2f` |
| `--color-text-primary` | `#f5f5f7` |
| `--color-text-secondary` | `#a1a1a6` |

---

## 字体

| Token | 值 | 用途 |
|---|---|---|
| `--font-family` | `-apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif` | 全局字体 |
| `--font-size-title` | `2rem` | 页面标题 |
| `--font-size-body` | `1rem` | 正文、按钮 |
| `--font-size-loading` | `1.2rem` | 加载提示 |
| `--font-weight-semibold` | `600` | 标题 |
| `--font-weight-medium` | `500` | 按钮、标签 |

---

## 间距

基准单位 4px：

| Token | 值 | 用途 |
|---|---|---|
| `--space-xs` | `8px` | 小元素内间距 |
| `--space-sm` | `12px` | 按钮内间距 |
| `--space-md` | `16px` | 区块内部间距 |
| `--space-lg` | `20px` | 头部内边距、海报网格 gap |
| `--space-xl` | `24px` | 按钮水平内间距 |
| `--space-xxl` | `40px` | 页面底部间距 |

---

## Apple Spring 动效曲线

| Token | 值 | 用途 |
|---|---|---|
| `--ease-apple` | `cubic-bezier(0.16, 1, 0.3, 1)` | 主弹簧曲线 |
| `--ease-apple-out` | `cubic-bezier(0.33, 1, 0.68, 1)` | 入场动画 |
| `--ease-apple-in-out` | `cubic-bezier(0.65, 0, 0.35, 1)` | 平滑过渡 |

### 动画规范

| 动画 | 时长 | 曲线 | 细节 |
|---|---|---|---|
| 页面渐入 | 0.6s | `--ease-apple` | opacity 0→1, translateY 10px→0 |
| 海报卡片悬停 | 0.3s | `--ease-apple` | translateY(-6px) + 阴影加深 |
| 毛玻璃按钮悬停 | 0.3s | `--ease-apple` | translateY(-2px) + 阴影加深 |
| 屏保 3D 翻转 | 1.2s | `--ease-apple` | rotateY 0→90→0, scale 1→0.8→1 |
| 交错延迟序列 | — | — | 0.1s / 0.25s / 0.4s |

---

## 圆角

| Token | 值 | 用途 |
|---|---|---|
| `--radius-sm` | `8px` | 海报卡片 |
| `--radius-pill` | `30px` | 毛玻璃按钮 |

---

## 组件规范

### 海报卡片
- CSS Grid 单元格，`minmax(150px, 1fr)` 自适应列数
- 白色背景 + `--radius-sm` 圆角 + `--color-shadow` 阴影
- 悬停：上移 6px + 阴影加深
- 图片：`width: 100%; height: auto`，保持宽高比

### 毛玻璃按钮
- 胶囊形（`--radius-pill`）
- 半透明白色背景 + `backdrop-filter: blur(10px)`
- 1px 半透明边框
- 悬停：背景提亮 + 上移 2px + 深阴影

### 屏保马赛克
- 全视口 CSS Grid，`gap: 0`
- 单元格 `object-fit: cover` 裁剪填充
- 3D 翻转动画：`transform-style: preserve-3d; backface-visibility: hidden`
- 黑色背景，适合电视/显示器长时间展示

---

## 响应式断点

| 断点 | 宽度 | 行为 |
|---|---|---|
| 移动端 | < 640px | 海报 min-width 缩小至 120px |
| 平板 | 640–1024px | 默认网格 |
| 桌面 | > 1024px | 最大宽度 1600px 居中 |

---

## 无障碍

- 所有图片必须有 `alt` 属性
- 按钮必须有 `aria-label`
- 屏保支持 ESC 键和点击退出
- 最小触控目标 44x44px
- 支持键盘 Tab 导航

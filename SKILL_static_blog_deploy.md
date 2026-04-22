# SKILL: 纯静态个人博客从零建站并部署到 GitHub Pages

> 适用场景：为个人用户从零搭建纯静态 HTML/CSS/JS 博客网站，并部署到 GitHub Pages + 自定义域名。
> 无需框架，无需构建工具，适合内容驱动、不需要后端的个人品牌站点。

---

## 一、使用前需提供的信息

| 必填项 | 说明 |
|--------|------|
| 博主身份/职业 | 用于 Hero 文案、关于我页面、主题定位 |
| 博客主题/内容方向 | 例如"生命科学×人文"、"技术+旅行" |
| 板块划分 | 博客分几个板块，各叫什么名字，对应什么内容 |
| 视觉风格偏好 | 颜色偏好、正式/活泼/极简等 |
| GitHub 账号 | 用于创建仓库和部署 |
| GitHub Token | 需要 `repo` 权限，在 Settings → Developer Settings 生成 |
| 域名（可选）| 如已购买域名，提供域名和注册商（如阿里云）|
| 联系方式（可选）| 邮箱、社交账号等，用于 About 页 |

---

## 二、完整工作流程

### 阶段 1：设计决策（Design Planning）

**目标**：在写任何代码之前，确定视觉系统和信息架构。

**步骤：**

1. **收集用户背景**
   - 博主职业、博客主题、目标读者
   - 板块数量和各板块的内容属性
   - 风格偏好（正式/活泼，简约/丰富）

2. **制定颜色系统**
   - 主品牌色（CTA、Logo）：1个，与职业/主题相关
   - 各板块专属色：每个板块1个，颜色有逻辑（如：生活=暖土色，旅行=蓝色，科学=绿色）
   - 背景、正文、次要文字、分割线：用中性色
   - 将所有颜色定义为 CSS 变量（`:root { --brand: ...; --life: ...; }`）
   
   > 判断原则：颜色要有"情感逻辑"，不要随机搭配。比如与自然/科学相关用绿色，与探索/深度相关用蓝紫色。

3. **制定字体方案**
   - 标题用衬线体（如 Noto Serif SC），增加人文感
   - 正文用无衬线体（如 Noto Sans SC），保证可读性
   - 从 Google Fonts 引入，注意国内加载速度（可预连接）

4. **规划页面结构**
   - 首页：Hero → 板块导航卡片 → 精选内容 → 关于我 strip → 页脚
   - 各板块页：板块简介 + 内容卡片列表
   - 关于我：个人简介 + 时间轴 + 联系方式

---

### 阶段 2：基础框架搭建

**目标**：建立可复用的 HTML 模板和全站样式。

**步骤：**

1. **写 `css/main.css`**
   - 最顶部定义所有 CSS 变量
   - Reset（`* { box-sizing: border-box; margin: 0; padding: 0; }`）
   - 全局字体、颜色、行高
   - 通用组件：`.container`、`.card`、`.btn`、`.tag`、`.reveal`（滚动动画）
   - Header/Nav 样式（桌面+移动端响应式）
   - Footer 样式
   - 各板块专属强调色（`.nav-life { color: var(--life); }`等）

2. **写 `js/main.js`**
   需要包含以下功能模块：
   
   | 模块 | 实现要点 |
   |------|---------|
   | Sticky Header | `scroll` 事件，`scrollY > 20` 时加 `scrolled` class |
   | 汉堡菜单 | 点击展开/收起，三条横线动画变成 X |
   | 滚动揭示动画 | `IntersectionObserver`，元素进入视口时加 `visible` class |
   | 当前页高亮 | `window.location.pathname` 匹配 href |
   | 平滑滚动 | `scrollIntoView({ behavior: 'smooth' })` |
   | 中英切换（可选）| `data-zh`/`data-en` 属性批量替换，`localStorage` 持久化 |

3. **建立 HTML 模板结构**
   每个页面都复用相同的 Header 和 Footer 结构，方便统一修改。

---

### 阶段 3：页面开发

**顺序建议**：`index.html` → 各板块页 → `about.html`

**每个页面的开发要点：**

- Hero 区：大标题 + 副标题 + CTA 按钮，背景可用网格/渐变
- 卡片组件：统一用 `.card` class，hover 时上移阴影加深
- 给所有需要动画的元素加 `.reveal` class
- 图片用 `aspect-ratio` 固定比例，防止布局跳动
- 响应式断点：主要照顾 `≤768px`（移动端）

**中英切换（如需要）：**
- 每个翻译元素加 `data-zh="中文"` `data-en="English"` 属性
- 默认 `textContent` 写中文
- JS 统一遍历替换，不要针对单个元素写逻辑

---

### 阶段 4：部署到 GitHub Pages

**步骤与判断：**

1. **创建 GitHub 仓库**
   - 仓库名建议：`username.github.io`（自动成为主域名）或任意名（子路径访问）
   - 使用 GitHub API 创建（可编程操作，不依赖 GUI）：
     ```
     POST https://api.github.com/user/repos
     { "name": "repo-name", "private": false }
     ```

2. **上传文件**
   - 通过 GitHub Contents API 逐文件上传（Base64 编码）
   - 更新文件时需先 GET 获取当前 `sha`，否则报错
   - 跳过 `.workbuddy`、`__pycache__`、`.git` 等目录

3. **启用 GitHub Pages**
   ```
   POST https://api.github.com/repos/{owner}/{repo}/pages
   { "build_type": "legacy", "source": { "branch": "main", "path": "/" } }
   ```
   > ⚠️ 关键判断：Pages API 必须在仓库已有内容后才能成功调用；首次创建空仓库立即调用会失败（`404`）。正确顺序：建仓库 → 上传文件 → 启用 Pages。

4. **验证部署**
   - `GET https://api.github.com/repos/{owner}/{repo}/pages` 检查 `status` 字段
   - `status: "built"` 表示构建成功，约需 1-3 分钟
   - 访问 `https://username.github.io/repo-name/` 验证

---

### 阶段 5：绑定自定义域名

**前提条件：**
- 域名已购买并完成实名认证
- 域名在注册商控制台可以修改 DNS

**步骤：**

1. **在 GitHub 仓库设置自定义域名**
   - 在仓库 Settings → Pages → Custom domain 填写域名
   - GitHub 会自动在仓库根目录生成 `CNAME` 文件
   - 或通过 API 上传 `CNAME` 文件（内容为域名字符串，如 `xyx.show`）

2. **在 DNS 控制台添加解析记录**
   
   | 类型 | 主机记录 | 记录值 |
   |------|---------|-------|
   | A | @ | 185.199.108.153 |
   | A | @ | 185.199.109.153 |
   | A | @ | 185.199.110.153 |
   | A | @ | 185.199.111.153 |
   | CNAME | www | `username.github.io.` |

3. **等待 DNS 生效**
   - 通常 5-30 分钟，最长 48 小时
   - 用 `nslookup 域名` 或在线工具检查是否解析到上述 IP

4. **开启 HTTPS**
   - GitHub Pages 在 DNS 生效后自动申请 Let's Encrypt 证书
   - 在 Settings → Pages 勾选 "Enforce HTTPS"

> ⚠️ 常见问题：DNS 已生效但 HTTPS 仍报错，通常是证书还在申请中，等待 10-15 分钟即可。

---

### 阶段 6：后续维护

**日常修改文件的最简方式：**

```python
# deploy.py 核心逻辑
import requests, base64

def upload_file(token, owner, repo, path, content_bytes):
    url = f"https://api.github.com/repos/{owner}/{repo}/contents/{path}"
    headers = {"Authorization": f"token {token}"}
    # 必须先获取 sha（如果文件已存在）
    existing = requests.get(url, headers=headers)
    payload = {
        "message": f"Update {path}",
        "content": base64.b64encode(content_bytes).decode()
    }
    if existing.status_code == 200:
        payload["sha"] = existing.json()["sha"]
    requests.put(url, headers=headers, json=payload)
```

**触发重新构建（无文件改动时）：**
```
POST https://api.github.com/repos/{owner}/{repo}/pages/builds
```

---

## 三、踩坑记录 & 经验教训

| 问题 | 原因 | 解决方法 |
|------|------|---------|
| Pages API 返回 `404` | 仓库为空，Pages 无法初始化 | 先上传至少1个文件，再调用 Pages API |
| 更新文件返回 `422` | 没有传 `sha` 字段 | PUT 前先 GET 获取当前文件的 sha |
| 自定义域名访问正常，HTTPS 报错 | 证书尚未签发 | 等待 10-30 分钟，无需操作 |
| DNS 解析正确，但页面显示 404 | GitHub Pages 构建未完成 | 等待 2-5 分钟，或检查 Pages 构建状态 |
| 国内访问慢/超时 | GitHub 服务器在海外，无 CDN | 迁移到 Cloudflare Pages，或做 CF IP 优选分流 |
| `.show` 等非标后缀域名国内备案失败 | 工信部只支持通用后缀 | 无法备案，只能走境外加速方案 |
| 语言切换按钮在移动端溢出 | flex 容器未设 `flex-shrink: 0` | 给按钮加 `flex-shrink: 0; white-space: nowrap` |

---

## 四、可选增强功能

| 功能 | 技术方案 | 难度 |
|------|---------|------|
| 访问统计 | 不蒜子（无需注册，纯前端）| ⭐ 极简 |
| 评论系统 | Giscus（GitHub Discussions，免费）| ⭐⭐ |
| 暗色模式 | CSS `prefers-color-scheme` + CSS 变量覆写 | ⭐⭐ |
| 全文搜索 | Fuse.js（纯前端模糊搜索）| ⭐⭐⭐ |
| 国内加速 | Cloudflare Pages + IP 优选 | ⭐⭐⭐ |
| RSS Feed | 手写 `feed.xml`（纯静态）| ⭐⭐ |
| 文章分页 | 纯 JS 控制卡片显示隐藏 | ⭐⭐ |

---

## 五、关键判断树

```
用户想做个人博客
  ├── 需要后端（登录/数据库）？
  │     └── 是 → 考虑 Next.js + Vercel 或云开发
  └── 纯内容展示？
        └── 是 → 纯静态 HTML（本方案）
              ├── 有技术基础？
              │     ├── 是 → 可考虑 Hugo / Hexo 等静态生成器
              │     └── 否 → 手写 HTML（更易定制，AI 可直接操作）
              └── 部署平台
                    ├── 国内访问优先 → Cloudflare Pages（无需备案，自动 CDN）
                    ├── 最简单 → GitHub Pages（本方案当前选择）
                    └── 有备案域名 → 腾讯云 EdgeOne Pages（国内最快）
```

---

*此文档由实际项目经验总结生成，适用于同类静态博客建站任务。*

# XHS Poster

一个面向小红书图文发布的长文卡片排版工具。将 Markdown 文本粘贴到编辑器中，即可自动分页、切换视觉主题、调整排版，并导出为 3:4 PNG 卡片。

整个排版与导出流程均在浏览器本地完成，不需要后端服务，也不会上传正文内容。

## 在线使用

**GitHub Pages：** https://yingjinghuang.github.io/xhs-poster/

打开网页后即可直接使用，无需安装。

## 导出示例

<table>
  <tr>
    <td><img src="docs/images/export-main-01.png" alt="导出卡片示例 1" width="360" /></td>
    <td><img src="docs/images/export-main-02.png" alt="导出卡片示例 2" width="360" /></td>
  </tr>
</table>

## 主要功能

- **自动分页**：根据正文长度和当前排版参数自动拆分为多张卡片。
- **手动分页**：需要固定换页时，可使用 `---page---` 或 `<!-- pagebreak -->`。
- **Markdown 排版**：支持小标题、引用、分割线、加粗和高亮等常用格式。
- **多套视觉主题**：内置浅色、暖色、冷色和深色等多种卡片风格。
- **排版微调**：可调整标题字号、正文字号、行距、标题字体、小标题样式和高亮样式。
- **页脚设置**：可控制页脚显示、署名内容、页码或日期，以及卡片圆角。
- **自动保存**：正文、标题和当前样式自动保存到浏览器本地，刷新后继续编辑。
- **自定义预设**：可保存常用样式，并通过 JSON 导入或导出预设。
- **批量导出**：全部页面可一次生成并打包为 ZIP，也可以单独下载某一页 PNG。

## 支持的 Markdown

目前主要支持适合卡片排版的基础 Markdown 语法：

| 写法 | 用途 |
| --- | --- |
| `# 小标题` | 小标题 |
| `> 引用内容` | 引用块 |
| `---` | 分割线 |
| `**重点内容**` | 加粗 |
| `==重点内容==` | 高亮 |
| 空行 | 段落分隔 |
| `---page---` | 强制分页 |
| `<!-- pagebreak -->` | 强制分页 |

其中分割线 `---` 只负责绘制分隔元素；需要从下一张卡片开始时，请使用专门的分页标记。

## 视觉主题

<table>
  <tr>
    <td><img src="docs/images/theme-sample-01.png" alt="主题示例 1" width="220" /></td>
    <td><img src="docs/images/theme-sample-02.png" alt="主题示例 2" width="220" /></td>
    <td><img src="docs/images/theme-sample-03.png" alt="主题示例 3" width="220" /></td>
  </tr>
  <tr>
    <td><img src="docs/images/theme-sample-04.png" alt="主题示例 4" width="220" /></td>
    <td><img src="docs/images/theme-sample-05.png" alt="主题示例 5" width="220" /></td>
    <td><img src="docs/images/theme-sample-06.png" alt="主题示例 6" width="220" /></td>
  </tr>
  <tr>
    <td><img src="docs/images/theme-sample-07.png" alt="主题示例 7" width="220" /></td>
    <td></td>
    <td></td>
  </tr>
</table>

## 使用方式

1. 在左侧 **内容编辑** 中填写标题和正文。
2. 使用空行组织段落，并按需要加入 Markdown 格式。
3. 如果希望指定某处换页，在单独一行输入 `---page---`。
4. 切换到 **视觉样式**，选择主题并调整字体、字号、行距、页脚等参数。
5. 常用配置可以保存到 **我的预设**。
6. 点击 **下载 ZIP** 一次导出全部卡片，或在单张预览下方单独下载。

## 本地运行

### 环境要求

- Node.js 20 或更高版本
- npm

### 安装

```bash
git clone https://github.com/yingjinghuang/xhs-poster.git
cd xhs-poster
npm install
```

### 启动开发环境

```bash
npm run dev
```

默认访问：

```text
http://localhost:3000
```

### 构建生产版本

```bash
npm run build
npm run start
```

## 常用命令

| 命令 | 说明 |
| --- | --- |
| `npm run dev` | 启动本地开发服务器 |
| `npm run build` | 执行生产构建和 TypeScript 检查 |
| `npm run start` | 启动已构建的生产版本 |
| `npm test` | 运行项目的静态行为回归检查 |

## 项目结构

```text
xhs-poster/
├── app/
│   ├── layout.tsx       # 页面 metadata 与根布局
│   ├── page.tsx         # 编辑器、分页、预览与导出逻辑
│   ├── globals.css      # 界面样式
│   └── zip.ts           # 浏览器端 ZIP 生成
├── docs/images/         # README 示例图片
├── scripts/             # 回归检查脚本
├── package.json
└── next.config.mjs
```

## 本地数据与隐私

XHS Poster 是纯前端工具。

以下数据默认保存在当前浏览器的 `localStorage` 中：

- 当前正文与标题
- 主题和排版设置
- 页脚与卡片设置
- 用户自定义预设

这些内容不会由本项目主动上传到服务器。清除浏览器站点数据后，本地草稿和预设也会一并删除；如需跨设备保留自定义预设，可先导出 JSON 文件。

## 技术栈

- Next.js
- React
- TypeScript
- Canvas 2D
- GitHub Pages

项目不依赖服务端数据库，卡片渲染、PNG 生成和 ZIP 打包均在浏览器中完成。

## 致谢与许可证

本仓库基于 [LuKK351/lukk-xhs-poster-studio](https://github.com/LuKK351/lukk-xhs-poster-studio) 进行修改和扩展。

项目继续遵循原项目的 **MIT License**。具体版权与许可信息请参见 [`LICENSE`](LICENSE)。

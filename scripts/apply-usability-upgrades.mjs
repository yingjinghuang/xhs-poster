import fs from "node:fs";

function replaceOnce(source, before, after, label) {
  if (!source.includes(before)) {
    throw new Error(`Missing patch anchor: ${label}`);
  }
  return source.replace(before, after);
}

const pagePath = "app/page.tsx";
let page = fs.readFileSync(pagePath, "utf8");

page = replaceOnce(
  page,
  'import { useEffect, useMemo, useState, useTransition } from "react";\n',
  'import { useEffect, useMemo, useState, useTransition } from "react";\nimport { createStoredZip, dataUrlToBytes, downloadBlob } from "./zip";\n',
  "zip import"
);

page = replaceOnce(
  page,
  '\nconst THEMES: ThemeDefinition[] = [',
  `\ntype SavedWorkspace = {\n  content: string;\n  manualTitle: string;\n  themeId: string;\n  titleSize: number;\n  bodySize: number;\n  lineHeight: number;\n  titleFontMode: TitleFontMode;\n  subheadingStyle: SubheadingStyle;\n  highlightStyle: HighlightStyle;\n  footerEnabled: boolean;\n  footerLeft: string;\n  footerRightMode: FooterRightMode;\n  cardCornerMode: CardCornerMode;\n};\n\ntype UserPreset = SavedWorkspace & {\n  id: string;\n  name: string;\n  createdAt: string;\n};\n\ntype SaveState = "idle" | "saving" | "saved";\n\nconst THEMES: ThemeDefinition[] = [`,
  "workspace types"
);

page = replaceOnce(
  page,
  'const DEFAULT_SUBHEADING_STYLE: SubheadingStyle = "large";\n',
  'const DEFAULT_SUBHEADING_STYLE: SubheadingStyle = "large";\nconst WORKSPACE_STORAGE_KEY = "xhs-poster.workspace.v1";\nconst USER_PRESETS_STORAGE_KEY = "xhs-poster.user-presets.v1";\nconst PAGE_BREAK_TOKEN = "__XHS_POSTER_PAGE_BREAK__";\n',
  "storage constants"
);

page = replaceOnce(
  page,
  `function isMarkdownDividerLine(line: string) {\n  return line.trim() === "---";\n}\n\nfunction isStandaloneMarkdownBlockStart(line: string) {\n  return /^#{1,6}\\s+/.test(line) || /^>\\s?/.test(line) || isMarkdownDividerLine(line);\n}`,
  `function isMarkdownDividerLine(line: string) {\n  return line.trim() === "---";\n}\n\nfunction isPageBreakLine(line: string) {\n  const normalized = line.trim().toLowerCase();\n  return normalized === "---page---" || normalized === "<!-- pagebreak -->";\n}\n\nfunction isStandaloneMarkdownBlockStart(line: string) {\n  return /^#{1,6}\\s+/.test(line) || /^>\\s?/.test(line) || isMarkdownDividerLine(line) || isPageBreakLine(line);\n}`,
  "page break parser"
);

page = replaceOnce(
  page,
  `    if (isStandaloneMarkdownBlockStart(trimmed)) {\n      flushCurrentBlock();\n      blocks.push(trimmed);\n      continue;\n    }`,
  `    if (isStandaloneMarkdownBlockStart(trimmed)) {\n      flushCurrentBlock();\n      blocks.push(isPageBreakLine(trimmed) ? PAGE_BREAK_TOKEN : trimmed);\n      continue;\n    }`,
  "page break tokenization"
);

page = replaceOnce(
  page,
  `  const expandedParagraphs = sourceParagraphs.flatMap((paragraph) => {\n    const chunkSize = 180;`,
  `  const expandedParagraphs = sourceParagraphs.flatMap((paragraph) => {\n    if (paragraph === PAGE_BREAK_TOKEN) return [PAGE_BREAK_TOKEN];\n    const chunkSize = 180;`,
  "preserve page breaks"
);

page = replaceOnce(
  page,
  `      const wasCarryingParagraph = Boolean(carryParagraph);\n      const currentText = wasCarryingParagraph ? carryParagraph : expandedParagraphs[currentParagraph];\n      const block = getParagraphBlock(currentText);`,
  `      const wasCarryingParagraph = Boolean(carryParagraph);\n      const currentText = wasCarryingParagraph ? carryParagraph : expandedParagraphs[currentParagraph];\n      if (currentText === PAGE_BREAK_TOKEN) {\n        carryParagraph = "";\n        currentParagraph += 1;\n        if (page.paragraphs.length > 0) break;\n        continue;\n      }\n      const block = getParagraphBlock(currentText);`,
  "force page boundary"
);

page = page.replaceAll('"LuKK-小红书卡片"', '"XHS-Poster"');

page = replaceOnce(
  page,
  `function createExportFileName(manualTitle: string, index: number, exportTimestamp: string) {\n  const baseName = sanitizeDownloadName(manualTitle.trim() || "XHS-Poster") || "XHS-Poster";\n  const pageNumber = String(index + 1).padStart(2, "0");\n  return \`\${baseName}-\${pageNumber}-\${exportTimestamp}.png\`;\n}`,
  `function getExportBaseName(manualTitle: string) {\n  return sanitizeDownloadName(manualTitle.trim() || "XHS-Poster") || "XHS-Poster";\n}\n\nfunction createExportFileName(manualTitle: string, index: number, exportTimestamp: string) {\n  const baseName = getExportBaseName(manualTitle);\n  const pageNumber = String(index + 1).padStart(2, "0");\n  return \`\${baseName}-\${pageNumber}-\${exportTimestamp}.png\`;\n}\n\nfunction createZipEntryName(manualTitle: string, index: number) {\n  const baseName = getExportBaseName(manualTitle);\n  const pageNumber = String(index + 1).padStart(2, "0");\n  return \`\${baseName}-\${pageNumber}.png\`;\n}\n\nfunction createZipFileName(manualTitle: string, exportTimestamp: string) {\n  return \`\${getExportBaseName(manualTitle)}-\${exportTimestamp}.zip\`;\n}`,
  "export names"
);

page = replaceOnce(
  page,
  `  const [footerLeft, setFooterLeft] = useState("困困");`,
  `  const [footerLeft, setFooterLeft] = useState("");`,
  "neutral footer"
);

page = replaceOnce(
  page,
  `  const [previewUrls, setPreviewUrls] = useState<string[]>([]);\n  const [isExporting, startExportTransition] = useTransition();`,
  `  const [previewUrls, setPreviewUrls] = useState<string[]>([]);\n  const [userPresets, setUserPresets] = useState<UserPreset[]>([]);\n  const [presetName, setPresetName] = useState("");\n  const [hasHydrated, setHasHydrated] = useState(false);\n  const [saveState, setSaveState] = useState<SaveState>("idle");\n  const [isExporting, startExportTransition] = useTransition();`,
  "new state"
);

page = replaceOnce(
  page,
  `  useEffect(() => {\n    setContent((current) => (isLegacyDefaultContent(current) ? DEFAULT_CONTENT : current));\n  }, []);`,
  `  useEffect(() => {\n    try {\n      const rawWorkspace = window.localStorage.getItem(WORKSPACE_STORAGE_KEY);\n      if (rawWorkspace) {\n        const stored = JSON.parse(rawWorkspace) as Partial<SavedWorkspace>;\n        if (typeof stored.content === "string") setContent(isLegacyDefaultContent(stored.content) ? DEFAULT_CONTENT : stored.content);\n        if (typeof stored.manualTitle === "string") setManualTitle(stored.manualTitle);\n        if (typeof stored.themeId === "string" && THEMES.some((item) => item.id === stored.themeId)) setThemeId(stored.themeId);\n        if (typeof stored.titleSize === "number") setTitleSize(stored.titleSize);\n        if (typeof stored.bodySize === "number") setBodySize(stored.bodySize);\n        if (typeof stored.lineHeight === "number") setLineHeight(stored.lineHeight);\n        if (stored.titleFontMode && stored.titleFontMode in TITLE_FONT_MODES) setTitleFontMode(stored.titleFontMode);\n        if (stored.subheadingStyle === "large" || stored.subheadingStyle === "accent") setSubheadingStyle(stored.subheadingStyle);\n        if (stored.highlightStyle === "underline" || stored.highlightStyle === "marker" || stored.highlightStyle === "border") setHighlightStyle(stored.highlightStyle);\n        if (typeof stored.footerEnabled === "boolean") setFooterEnabled(stored.footerEnabled);\n        if (typeof stored.footerLeft === "string") setFooterLeft(stored.footerLeft);\n        if (stored.footerRightMode === "blank" || stored.footerRightMode === "page" || stored.footerRightMode === "date") setFooterRightMode(stored.footerRightMode);\n        if (stored.cardCornerMode === "rounded" || stored.cardCornerMode === "square") setCardCornerMode(stored.cardCornerMode);\n      } else {\n        setContent((current) => (isLegacyDefaultContent(current) ? DEFAULT_CONTENT : current));\n      }\n\n      const rawPresets = window.localStorage.getItem(USER_PRESETS_STORAGE_KEY);\n      if (rawPresets) {\n        const storedPresets = JSON.parse(rawPresets);\n        if (Array.isArray(storedPresets)) {\n          setUserPresets(storedPresets.filter((item) => item && typeof item.id === "string" && typeof item.name === "string"));\n        }\n      }\n    } catch (error) {\n      console.warn("无法恢复本地草稿，将使用默认内容。", error);\n    } finally {\n      setHasHydrated(true);\n    }\n  }, []);\n\n  useEffect(() => {\n    if (!hasHydrated) return;\n    setSaveState("saving");\n    const timer = window.setTimeout(() => {\n      const workspace: SavedWorkspace = {\n        content,\n        manualTitle,\n        themeId,\n        titleSize,\n        bodySize,\n        lineHeight,\n        titleFontMode,\n        subheadingStyle,\n        highlightStyle,\n        footerEnabled,\n        footerLeft,\n        footerRightMode,\n        cardCornerMode\n      };\n      window.localStorage.setItem(WORKSPACE_STORAGE_KEY, JSON.stringify(workspace));\n      setSaveState("saved");\n    }, 320);\n    return () => window.clearTimeout(timer);\n  }, [hasHydrated, content, manualTitle, themeId, titleSize, bodySize, lineHeight, titleFontMode, subheadingStyle, highlightStyle, footerEnabled, footerLeft, footerRightMode, cardCornerMode]);\n\n  useEffect(() => {\n    if (!hasHydrated) return;\n    window.localStorage.setItem(USER_PRESETS_STORAGE_KEY, JSON.stringify(userPresets));\n  }, [hasHydrated, userPresets]);`,
  "draft hydration and autosave"
);

page = replaceOnce(
  page,
  `  async function handleExportAll() {\n    startExportTransition(async () => {\n      const exportTimestamp = getExportTimestamp();\n      const exportPages = layoutPosterPages(content, manualTitle, typographySettings, theme, footerEnabled);\n      for (let index = 0; index < exportPages.length; index += 1) {\n        const dataUrl = await renderPosterToDataUrl(\n          exportPages[index],\n          theme,\n          typographySettings,\n          highlightStyle,\n          index,\n          exportPages.length,\n          footerLeft,\n          footerRightMode,\n          footerEnabled,\n          cardCornerMode\n        );\n        downloadDataUrl(dataUrl, createExportFileName(manualTitle, index, exportTimestamp));\n        await new Promise((resolve) => window.setTimeout(resolve, 120));\n      }\n    });\n  }`,
  `  function clearSavedDraft() {\n    window.localStorage.removeItem(WORKSPACE_STORAGE_KEY);\n    setContent(DEFAULT_CONTENT);\n    setManualTitle("");\n    setThemeId(INITIAL_THEME.id);\n    applyThemeEditorDefaults(INITIAL_THEME);\n    setFooterEnabled(true);\n    setFooterLeft("");\n    setFooterRightMode("page");\n    setCardCornerMode("square");\n    setSaveState("idle");\n  }\n\n  function saveCurrentPreset() {\n    const name = presetName.trim() || \`我的预设 \${userPresets.length + 1}\`;\n    const preset: UserPreset = {\n      id: typeof crypto !== "undefined" && "randomUUID" in crypto ? crypto.randomUUID() : \`preset-\${Date.now()}\`,\n      name,\n      createdAt: new Date().toISOString(),\n      content: "",\n      manualTitle: "",\n      themeId,\n      titleSize,\n      bodySize,\n      lineHeight,\n      titleFontMode,\n      subheadingStyle,\n      highlightStyle,\n      footerEnabled,\n      footerLeft,\n      footerRightMode,\n      cardCornerMode\n    };\n    setUserPresets((current) => [...current, preset]);\n    setPresetName("");\n  }\n\n  function applyUserPreset(preset: UserPreset) {\n    setThemeId(THEMES.some((item) => item.id === preset.themeId) ? preset.themeId : INITIAL_THEME.id);\n    setTitleSize(preset.titleSize);\n    setBodySize(preset.bodySize);\n    setLineHeight(preset.lineHeight);\n    setTitleFontMode(preset.titleFontMode);\n    setSubheadingStyle(preset.subheadingStyle);\n    setHighlightStyle(preset.highlightStyle);\n    setFooterEnabled(preset.footerEnabled);\n    setFooterLeft(preset.footerLeft);\n    setFooterRightMode(preset.footerRightMode);\n    setCardCornerMode(preset.cardCornerMode);\n  }\n\n  function deleteUserPreset(id: string) {\n    setUserPresets((current) => current.filter((preset) => preset.id !== id));\n  }\n\n  function exportUserPresets() {\n    const blob = new Blob([JSON.stringify(userPresets, null, 2)], { type: "application/json" });\n    downloadBlob(blob, "xhs-poster-presets.json");\n  }\n\n  async function importUserPresets(file: File | undefined) {\n    if (!file) return;\n    try {\n      const parsed = JSON.parse(await file.text());\n      if (!Array.isArray(parsed)) throw new Error("预设文件格式不正确");\n      const imported = parsed\n        .filter((item) => item && typeof item.name === "string" && typeof item.themeId === "string")\n        .map((item) => ({\n          ...item,\n          id: typeof item.id === "string" ? item.id : \`preset-\${Date.now()}-\${Math.random()}\`,\n          createdAt: typeof item.createdAt === "string" ? item.createdAt : new Date().toISOString(),\n          content: "",\n          manualTitle: ""\n        })) as UserPreset[];\n      setUserPresets((current) => {\n        const byId = new Map(current.map((item) => [item.id, item]));\n        imported.forEach((item) => byId.set(item.id, item));\n        return Array.from(byId.values());\n      });\n    } catch (error) {\n      window.alert(error instanceof Error ? error.message : "无法导入预设");\n    }\n  }\n\n  function handleExportSingle(index: number) {\n    const dataUrl = previewUrls[index];\n    if (!dataUrl) return;\n    downloadDataUrl(dataUrl, createExportFileName(manualTitle, index, getExportTimestamp()));\n  }\n\n  async function handleExportAll() {\n    startExportTransition(async () => {\n      const exportTimestamp = getExportTimestamp();\n      const exportPages = layoutPosterPages(content, manualTitle, typographySettings, theme, footerEnabled);\n      const zipEntries: { name: string; data: Uint8Array }[] = [];\n      for (let index = 0; index < exportPages.length; index += 1) {\n        const dataUrl = await renderPosterToDataUrl(\n          exportPages[index],\n          theme,\n          typographySettings,\n          highlightStyle,\n          index,\n          exportPages.length,\n          footerLeft,\n          footerRightMode,\n          footerEnabled,\n          cardCornerMode\n        );\n        zipEntries.push({\n          name: createZipEntryName(manualTitle, index),\n          data: dataUrlToBytes(dataUrl)\n        });\n      }\n      downloadBlob(createStoredZip(zipEntries), createZipFileName(manualTitle, exportTimestamp));\n    });\n  }`,
  "draft preset and zip handlers"
);

page = replaceOnce(
  page,
  `                  <textarea\n                    id="content-input"\n                    className="text-area text-area--content"\n                    value={content}\n                    onChange={(event) => setContent(event.target.value)}\n                    placeholder="直接贴正文内容，空行分段。"\n                  />`,
  `                  <textarea\n                    id="content-input"\n                    className="text-area text-area--content"\n                    value={content}\n                    onChange={(event) => setContent(event.target.value)}\n                    placeholder="直接贴正文内容，空行分段。"\n                  />\n                  <div className="editor-helper-row">\n                    <span className="editor-hint">手动分页：单独一行输入 <code>---page---</code></span>\n                    <div className="draft-tools">\n                      <span className={\`save-indicator save-indicator--\${saveState}\`}>\n                        {!hasHydrated ? "读取草稿..." : saveState === "saving" ? "保存中..." : saveState === "saved" ? "已自动保存" : "本地草稿"}\n                      </span>\n                      <button type="button" className="text-action-button" onClick={clearSavedDraft}>清空草稿</button>\n                    </div>\n                  </div>`,
  "draft helper UI"
);

const typographyAccordionAnchor = `                </details>\n\n                <details className="accordion-section">\n                  <summary className="accordion-summary">排版微调</summary>`;
page = replaceOnce(
  page,
  typographyAccordionAnchor,
  `                </details>\n\n                <details className="accordion-section">\n                  <summary className="accordion-summary">我的预设</summary>\n                  <div className="preset-manager">\n                    <div className="preset-save-row">\n                      <input\n                        className="text-input"\n                        value={presetName}\n                        onChange={(event) => setPresetName(event.target.value)}\n                        placeholder="给当前样式起个名字"\n                      />\n                      <button type="button" className="secondary-action-button" onClick={saveCurrentPreset}>保存当前样式</button>\n                    </div>\n                    {userPresets.length > 0 ? (\n                      <div className="saved-preset-list">\n                        {userPresets.map((preset) => (\n                          <div key={preset.id} className="saved-preset-item">\n                            <button type="button" className="saved-preset-apply" onClick={() => applyUserPreset(preset)}>\n                              <strong>{preset.name}</strong>\n                              <span>{THEMES.find((item) => item.id === preset.themeId)?.name ?? "自定义样式"}</span>\n                            </button>\n                            <button type="button" className="saved-preset-delete" onClick={() => deleteUserPreset(preset.id)} aria-label={\`删除\${preset.name}\`}>×</button>\n                          </div>\n                        ))}\n                      </div>\n                    ) : (\n                      <p className="preset-empty">把常用的主题、字号、页脚和卡片设置保存下来，下次一键恢复。</p>\n                    )}\n                    <div className="preset-transfer-row">\n                      <button type="button" className="text-action-button" onClick={exportUserPresets} disabled={userPresets.length === 0}>导出预设 JSON</button>\n                      <label className="text-action-button file-action-label">\n                        导入预设 JSON\n                        <input type="file" accept="application/json,.json" onChange={(event) => { void importUserPresets(event.target.files?.[0]); event.currentTarget.value = ""; }} />\n                      </label>\n                    </div>\n                  </div>\n                </details>\n\n                <details className="accordion-section">\n                  <summary className="accordion-summary">排版微调</summary>`,
  "custom presets UI"
);

page = replaceOnce(
  page,
  `<span className="export-tooltip" role="tooltip">{pages.length} 张卡片将按当前主题批量下载。也可以右键单击单张预览图片保存。</span>`,
  `<span className="export-tooltip" role="tooltip">{pages.length} 张卡片会打包成一个 ZIP 下载；每张卡片下方也可以单独下载。</span>`,
  "zip tooltip"
);

page = replaceOnce(
  page,
  `{isExporting ? "导出中..." : "生成并下载"}`,
  `{isExporting ? "打包中..." : "下载 ZIP"}`,
  "zip button label"
);

page = replaceOnce(
  page,
  `                <div className="poster-meta">\n                  <span>第 {index + 1} 页</span>\n                  <span>{page.paragraphs.length} 段</span>\n                </div>`,
  `                <div className="poster-meta">\n                  <div className="poster-meta-copy">\n                    <span>第 {index + 1} 页</span>\n                    <span>{page.paragraphs.length} 段</span>\n                  </div>\n                  <button type="button" className="poster-download-button" onClick={() => handleExportSingle(index)} disabled={!previewUrls[index]}>下载此页</button>\n                </div>`,
  "single page download"
);

fs.writeFileSync(pagePath, page);

const cssPath = "app/globals.css";
let css = fs.readFileSync(cssPath, "utf8");
const extraCss = `\n\n/* Usability upgrades: drafts, manual page breaks, saved presets and per-page export */\n.editor-helper-row {\n  display: flex;\n  align-items: center;\n  justify-content: space-between;\n  gap: 12px;\n  flex-wrap: wrap;\n  margin-top: 10px;\n}\n\n.editor-hint {\n  color: var(--muted, #6f777b);\n  font-size: 12px;\n  line-height: 1.5;\n}\n\n.editor-hint code {\n  padding: 2px 6px;\n  border-radius: 6px;\n  background: rgba(30, 41, 48, 0.06);\n  font-family: ui-monospace, SFMono-Regular, Menlo, monospace;\n}\n\n.draft-tools,\n.preset-transfer-row {\n  display: flex;\n  align-items: center;\n  gap: 8px;\n  flex-wrap: wrap;\n}\n\n.save-indicator {\n  font-size: 12px;\n  color: #7b858a;\n}\n\n.save-indicator--saved {\n  color: #3d7652;\n}\n\n.text-action-button,\n.secondary-action-button,\n.poster-download-button {\n  border: 1px solid rgba(36, 52, 70, 0.14);\n  background: rgba(255, 255, 255, 0.78);\n  color: #34434a;\n  border-radius: 10px;\n  padding: 7px 10px;\n  font: inherit;\n  font-size: 12px;\n  cursor: pointer;\n}\n\n.text-action-button:hover,\n.secondary-action-button:hover,\n.poster-download-button:hover {\n  border-color: rgba(36, 52, 70, 0.28);\n  background: #fff;\n}\n\n.text-action-button:disabled,\n.poster-download-button:disabled {\n  opacity: 0.45;\n  cursor: default;\n}\n\n.preset-manager {\n  display: grid;\n  gap: 12px;\n  padding-top: 8px;\n}\n\n.preset-save-row {\n  display: grid;\n  grid-template-columns: minmax(0, 1fr) auto;\n  gap: 8px;\n}\n\n.secondary-action-button {\n  padding-inline: 12px;\n  font-weight: 600;\n}\n\n.saved-preset-list {\n  display: grid;\n  gap: 8px;\n}\n\n.saved-preset-item {\n  display: grid;\n  grid-template-columns: minmax(0, 1fr) 32px;\n  align-items: stretch;\n  border: 1px solid rgba(36, 52, 70, 0.1);\n  border-radius: 12px;\n  overflow: hidden;\n  background: rgba(255, 255, 255, 0.52);\n}\n\n.saved-preset-apply {\n  display: grid;\n  gap: 2px;\n  padding: 10px 12px;\n  border: 0;\n  background: transparent;\n  text-align: left;\n  cursor: pointer;\n}\n\n.saved-preset-apply strong {\n  color: #26363d;\n  font-size: 13px;\n}\n\n.saved-preset-apply span,\n.preset-empty {\n  color: #7b858a;\n  font-size: 12px;\n}\n\n.saved-preset-delete {\n  border: 0;\n  border-left: 1px solid rgba(36, 52, 70, 0.08);\n  background: transparent;\n  color: #8c7777;\n  font-size: 18px;\n  cursor: pointer;\n}\n\n.preset-empty {\n  margin: 0;\n  line-height: 1.55;\n}\n\n.file-action-label {\n  position: relative;\n  display: inline-flex;\n  align-items: center;\n}\n\n.file-action-label input {\n  position: absolute;\n  width: 1px;\n  height: 1px;\n  opacity: 0;\n  pointer-events: none;\n}\n\n.poster-meta {\n  align-items: center;\n}\n\n.poster-meta-copy {\n  display: flex;\n  gap: 10px;\n}\n\n.poster-download-button {\n  padding: 5px 9px;\n}\n\n@media (max-width: 720px) {\n  .preset-save-row {\n    grid-template-columns: 1fr;\n  }\n}\n`;
if (!css.includes("Usability upgrades: drafts")) css += extraCss;
fs.writeFileSync(cssPath, css);

const readmePath = "README.md";
let readme = fs.readFileSync(readmePath, "utf8");
readme = readme
  .replace("# LuKK XHS Poster Studio", "# XHS Poster")
  .replaceAll("LuKK XHS Poster Studio", "XHS Poster")
  .replaceAll("LuKK-小红书卡片", "XHS-Poster")
  .replace("git clone https://github.com/LuKK351/lukk-xhs-poster-studio.git\\ncd lukk-xhs-poster-studio", "git clone https://github.com/yingjinghuang/xhs-poster.git\\ncd xhs-poster")
  .replace("- **批量导出**：逐张下载 PNG。文件名会带标题、页码和时间戳，避免多次导出时重名。", "- **自动保存**：标题、正文和样式会保存在当前浏览器，刷新后自动恢复。\\n- **手动分页**：单独一行输入 `---page---` 或 `<!-- pagebreak -->` 强制从下一张卡片开始。\\n- **自定义预设**：保存常用主题与排版设置，并可导入/导出 JSON。\\n- **ZIP 导出**：一次生成全部 PNG 并打包下载，也可单独下载某一页。")
  .replace("项目没有后端服务，不会上传你的内容。所有排版和导出都在浏览器本地完成。", "项目没有后端服务，不会上传你的内容。草稿、样式预设、排版和导出都只在浏览器本地完成。\\n\\n本仓库基于 [LuKK351/lukk-xhs-poster-studio](https://github.com/LuKK351/lukk-xhs-poster-studio) 修改并继续使用 MIT License；原作者署名与许可证信息保留在仓库历史和 LICENSE 中。")
  .replace("5. 点击“生成并下载”，每张卡片会按顺序下载成 PNG。", "5. 点击“下载 ZIP”，全部卡片会打包下载；也可以在单张预览下方单独下载。")
  .replace("## 导出命名规则", "## 草稿、分页与导出\\n\\n编辑内容和样式会自动保存到浏览器。需要固定换页时，在正文中单独一行写 `---page---`。\\n\\n## 导出命名规则");
fs.writeFileSync(readmePath, readme);

console.log("Usability upgrade patches applied successfully.");

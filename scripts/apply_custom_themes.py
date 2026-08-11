from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / "app" / "page.tsx"
CSS = ROOT / "app" / "globals.css"
README = ROOT / "README.md"
TEST = ROOT / "scripts" / "check-default-content.mjs"


def replace_once(path: Path, old: str, new: str):
    text = path.read_text(encoding="utf-8")
    count = text.count(old)
    if count != 1:
        raise RuntimeError(f"Expected exactly one match in {path}: {old[:80]!r}; found {count}")
    path.write_text(text.replace(old, new, 1), encoding="utf-8")


# 1) Persistable custom-palette shape.
replace_once(
    PAGE,
    'type SavedWorkspace = {\n',
    '''type CustomPalette = {\n  page: string;\n  pageAlt: string;\n  text: string;\n  muted: string;\n  accent: string;\n  highlight: string;\n};\n\ntype SavedWorkspace = {\n'''
)
replace_once(
    PAGE,
    '  cardCornerMode: CardCornerMode;\n};\n\ntype UserPreset = SavedWorkspace & {',
    '  cardCornerMode: CardCornerMode;\n  customThemeBaseId?: string;\n  customPalette?: CustomPalette;\n};\n\ntype UserPreset = SavedWorkspace & {'
)

# 2) Six additional curated palettes, each reusing a proven structural theme.
extra_themes = r'''

function createThemeVariant(
  baseId: string,
  definition: Pick<ThemeDefinition, "id" | "name" | "mood" | "preset" | "description" | "tags"> & {
    palette: ThemeDefinition["palette"];
  }
): ThemeDefinition {
  const base = THEMES.find((theme) => theme.id === baseId);
  if (!base) throw new Error(`Unknown base theme: ${baseId}`);
  return {
    ...base,
    ...definition,
    palette: { ...definition.palette },
    surface: { ...base.surface },
    components: { ...base.components },
    editor: { ...base.editor }
  };
}

const EXTRA_THEMES: ThemeDefinition[] = [
  createThemeVariant("peach-cloud", {
    id: "cream-coffee",
    name: "奶油咖啡",
    mood: "奶油纸面与咖啡棕",
    preset: "奶油咖啡",
    description: "温柔奶油底配咖啡棕，适合生活方式、书影音和日常记录",
    tags: ["奶油", "咖啡"],
    palette: {
      page: "#fbf6ed",
      pageAlt: "#f1e4d2",
      text: "#33261f",
      muted: "#7a685c",
      accent: "#9a5d3a",
      accentSoft: "rgba(154, 93, 58, 0.18)",
      border: "rgba(51, 38, 31, 0.12)",
      shadow: "rgba(51, 38, 31, 0.12)",
      glow: "rgba(206, 171, 132, 0.22)"
    }
  }),
  createThemeVariant("swiss-modern", {
    id: "glacier-blue",
    name: "冰川蓝",
    mood: "清冷蓝白与理性信息感",
    preset: "冰川蓝",
    description: "干净蓝白、低饱和冷色，适合知识、旅行和数据内容",
    tags: ["冷调", "清晰"],
    palette: {
      page: "#f5f9fc",
      pageAlt: "#e7f1f7",
      text: "#173041",
      muted: "#647987",
      accent: "#3a7ca5",
      accentSoft: "rgba(58, 124, 165, 0.18)",
      border: "rgba(23, 48, 65, 0.13)",
      shadow: "rgba(23, 48, 65, 0.09)",
      glow: "rgba(126, 186, 217, 0.18)"
    }
  }),
  createThemeVariant("swiss-modern", {
    id: "wine-gray",
    name: "酒红灰",
    mood: "暖灰纸面与克制酒红",
    preset: "酒红灰",
    description: "低饱和酒红配暖灰，适合观点、文化与较正式的长文",
    tags: ["酒红", "克制"],
    palette: {
      page: "#f5f2f1",
      pageAlt: "#ebe4e3",
      text: "#2b2325",
      muted: "#75686b",
      accent: "#8f3f4d",
      accentSoft: "rgba(143, 63, 77, 0.16)",
      border: "rgba(43, 35, 37, 0.13)",
      shadow: "rgba(43, 35, 37, 0.09)",
      glow: "rgba(173, 108, 119, 0.14)"
    }
  }),
  createThemeVariant("sage-dawn", {
    id: "lavender-mist",
    name: "薰衣草雾",
    mood: "浅紫灰与柔和雾面",
    preset: "薰衣草雾",
    description: "轻柔紫灰、安静不甜腻，适合随笔、审美和情绪内容",
    tags: ["紫灰", "柔和"],
    palette: {
      page: "#f6f3fa",
      pageAlt: "#e9e2f2",
      text: "#2e2738",
      muted: "#746c80",
      accent: "#7b5ca8",
      accentSoft: "rgba(123, 92, 168, 0.18)",
      border: "rgba(46, 39, 56, 0.12)",
      shadow: "rgba(46, 39, 56, 0.1)",
      glow: "rgba(184, 164, 211, 0.2)"
    }
  }),
  createThemeVariant("peach-cloud", {
    id: "cherry-cream",
    name: "樱桃奶霜",
    mood: "奶白粉底与樱桃红",
    preset: "樱桃奶霜",
    description: "奶白粉调配清晰樱桃红，适合美食、生活与轻快表达",
    tags: ["樱桃", "轻快"],
    palette: {
      page: "#fff5f2",
      pageAlt: "#fbe4df",
      text: "#362022",
      muted: "#806064",
      accent: "#c83f55",
      accentSoft: "rgba(200, 63, 85, 0.17)",
      border: "rgba(54, 32, 34, 0.12)",
      shadow: "rgba(84, 40, 47, 0.11)",
      glow: "rgba(231, 140, 154, 0.18)"
    }
  }),
  createThemeVariant("moss-paper", {
    id: "ink-rice-paper",
    name: "宣纸朱印",
    mood: "米白宣纸、墨色与朱印",
    preset: "宣纸朱印",
    description: "东方纸张感与克制朱红，适合读书、历史、人文和长文摘记",
    tags: ["东方", "纸墨"],
    palette: {
      page: "#f4f0e6",
      pageAlt: "#e8e1d2",
      text: "#292823",
      muted: "#6f6b62",
      accent: "#a24a3a",
      accentSoft: "rgba(162, 74, 58, 0.16)",
      border: "rgba(41, 40, 35, 0.12)",
      shadow: "rgba(41, 40, 35, 0.11)",
      glow: "rgba(190, 154, 126, 0.18)"
    }
  })
];

THEMES.push(...EXTRA_THEMES);
'''
replace_once(PAGE, ']\n;\n\nconst DEFAULT_CONTENT', ']\n;'+extra_themes+'\n\nconst DEFAULT_CONTENT') if False else None
# Use the exact array terminator present in the source.
replace_once(PAGE, '  }\n];\n\nconst DEFAULT_CONTENT', '  }\n];' + extra_themes + '\n\nconst DEFAULT_CONTENT')

# 3) Keep the original 8-theme order intact for compatibility, then append 6 new presets.
replace_once(
    PAGE,
    '''const THEME_PRESETS = THEME_PRESET_ORDER\n  .map((themeId) => THEMES.find((theme) => theme.id === themeId))\n  .filter((theme): theme is ThemeDefinition => Boolean(theme));''',
    '''const EXTRA_THEME_PRESET_ORDER = [\n  "cream-coffee",\n  "glacier-blue",\n  "wine-gray",\n  "lavender-mist",\n  "cherry-cream",\n  "ink-rice-paper"\n];\nconst THEME_PRESETS = [...THEME_PRESET_ORDER, ...EXTRA_THEME_PRESET_ORDER]\n  .map((themeId) => THEMES.find((theme) => theme.id === themeId))\n  .filter((theme): theme is ThemeDefinition => Boolean(theme));'''
)
replace_once(
    PAGE,
    'const PAGE_BREAK_TOKEN = "__XHS_POSTER_PAGE_BREAK__";\n\nfunction getTitleFontWeight',
    r'''const PAGE_BREAK_TOKEN = "__XHS_POSTER_PAGE_BREAK__";
const CUSTOM_THEME_ID = "custom";
const CUSTOM_PALETTE_FIELDS: Array<{ key: keyof CustomPalette; label: string; hint: string }> = [
  { key: "page", label: "卡片背景", hint: "主背景色" },
  { key: "pageAlt", label: "背景渐变", hint: "第二背景色" },
  { key: "text", label: "主文字", hint: "标题与正文" },
  { key: "muted", label: "次文字", hint: "辅助信息" },
  { key: "accent", label: "强调色", hint: "标题、引用与重点" },
  { key: "highlight", label: "柔和高亮", hint: "标记与氛围色" }
];

function normalizeHexColor(value: string, fallback: string) {
  const candidate = value.trim();
  return /^#[0-9a-f]{6}$/i.test(candidate) ? candidate.toUpperCase() : fallback.toUpperCase();
}

function getCustomPaletteFromTheme(theme: ThemeDefinition): CustomPalette {
  return {
    page: theme.palette.page,
    pageAlt: theme.palette.pageAlt,
    text: theme.palette.text,
    muted: theme.palette.muted,
    accent: theme.palette.accent,
    highlight: theme.palette.accent
  };
}

function normalizeCustomPalette(value: unknown, fallback: CustomPalette): CustomPalette {
  const source = value && typeof value === "object" ? value as Partial<CustomPalette> : {};
  return {
    page: normalizeHexColor(typeof source.page === "string" ? source.page : fallback.page, fallback.page),
    pageAlt: normalizeHexColor(typeof source.pageAlt === "string" ? source.pageAlt : fallback.pageAlt, fallback.pageAlt),
    text: normalizeHexColor(typeof source.text === "string" ? source.text : fallback.text, fallback.text),
    muted: normalizeHexColor(typeof source.muted === "string" ? source.muted : fallback.muted, fallback.muted),
    accent: normalizeHexColor(typeof source.accent === "string" ? source.accent : fallback.accent, fallback.accent),
    highlight: normalizeHexColor(typeof source.highlight === "string" ? source.highlight : fallback.highlight, fallback.highlight)
  };
}

function buildCustomTheme(baseTheme: ThemeDefinition, paletteInput: CustomPalette): ThemeDefinition {
  const fallback = getCustomPaletteFromTheme(baseTheme);
  const palette = normalizeCustomPalette(paletteInput, fallback);
  return {
    ...baseTheme,
    id: CUSTOM_THEME_ID,
    name: "自定义配色",
    mood: `基于 ${baseTheme.name} 的自定义配色`,
    preset: "自定义配色",
    description: "保留当前版式结构，自定义背景、文字和强调颜色",
    tags: ["自定义", "配色"],
    palette: {
      page: palette.page,
      pageAlt: palette.pageAlt,
      text: palette.text,
      muted: palette.muted,
      accent: palette.accent,
      accentSoft: hexToRgba(palette.highlight, 0.2),
      border: hexToRgba(palette.text, 0.14),
      shadow: hexToRgba(palette.text, 0.12),
      glow: hexToRgba(palette.highlight, 0.16)
    },
    surface: {
      ...baseTheme.surface,
      previewShadow: `0 24px 52px ${hexToRgba(palette.text, 0.12)}`
    },
    components: { ...baseTheme.components },
    editor: { ...baseTheme.editor }
  };
}

function getRelativeLuminance(hex: string) {
  const normalized = normalizeHexColor(hex, "#000000").slice(1);
  const channels = [0, 2, 4].map((offset) => parseInt(normalized.slice(offset, offset + 2), 16) / 255);
  const linear = channels.map((channel) => channel <= 0.03928 ? channel / 12.92 : Math.pow((channel + 0.055) / 1.055, 2.4));
  return 0.2126 * linear[0] + 0.7152 * linear[1] + 0.0722 * linear[2];
}

function getContrastRatio(background: string, foreground: string) {
  const a = getRelativeLuminance(background);
  const b = getRelativeLuminance(foreground);
  const lighter = Math.max(a, b);
  const darker = Math.min(a, b);
  return (lighter + 0.05) / (darker + 0.05);
}

function getTitleFontWeight'''
)

# 4) State + memoized custom theme.
replace_once(
    PAGE,
    '  const [themeId, setThemeId] = useState(INITIAL_THEME.id);\n  const [titleSize, setTitleSize] = useState(INITIAL_THEME.editor.titleSize);',
    '  const [themeId, setThemeId] = useState(INITIAL_THEME.id);\n  const [customThemeBaseId, setCustomThemeBaseId] = useState(INITIAL_THEME.id);\n  const [customPalette, setCustomPalette] = useState<CustomPalette>(() => getCustomPaletteFromTheme(INITIAL_THEME));\n  const [titleSize, setTitleSize] = useState(INITIAL_THEME.editor.titleSize);'
)
replace_once(
    PAGE,
    '  const theme = useMemo(() => THEMES.find((item) => item.id === themeId) ?? THEMES[0], [themeId]);\n  const characterCount',
    '''  const customBaseTheme = useMemo(\n    () => THEMES.find((item) => item.id === customThemeBaseId) ?? INITIAL_THEME,\n    [customThemeBaseId]\n  );\n  const customThemePreview = useMemo(\n    () => buildCustomTheme(customBaseTheme, customPalette),\n    [customBaseTheme, customPalette]\n  );\n  const theme = useMemo(\n    () => themeId === CUSTOM_THEME_ID ? customThemePreview : THEMES.find((item) => item.id === themeId) ?? THEMES[0],\n    [themeId, customThemePreview]\n  );\n  const customContrastRatio = useMemo(\n    () => getContrastRatio(customPalette.page, customPalette.text),\n    [customPalette.page, customPalette.text]\n  );\n  const characterCount'''
)

# Preserve selectThemePreset exactly, add separate custom-theme actions after it.
replace_once(
    PAGE,
    '''  function selectThemePreset(targetTheme: ThemeDefinition) {\n    setThemeId(targetTheme.id);\n  }\n\n  useEffect(() => {''',
    r'''  function selectThemePreset(targetTheme: ThemeDefinition) {
    setThemeId(targetTheme.id);
  }

  function startCustomThemeFromCurrent() {
    if (themeId === CUSTOM_THEME_ID) return;
    setCustomThemeBaseId(theme.id);
    setCustomPalette(getCustomPaletteFromTheme(theme));
    setThemeId(CUSTOM_THEME_ID);
  }

  function updateCustomPaletteColor(key: keyof CustomPalette, value: string) {
    let next = value.trim();
    if (!next.startsWith("#")) next = `#${next}`;
    if (!/^#[0-9a-f]{0,6}$/i.test(next)) return;
    setCustomPalette((current) => ({ ...current, [key]: next.toUpperCase() }));
  }

  function commitCustomPaletteColor(key: keyof CustomPalette) {
    const fallback = getCustomPaletteFromTheme(customBaseTheme)[key];
    setCustomPalette((current) => ({
      ...current,
      [key]: normalizeHexColor(current[key], fallback)
    }));
  }

  function resetCustomPalette() {
    setCustomPalette(getCustomPaletteFromTheme(customBaseTheme));
  }

  useEffect(() => {'''
)

# 5) Workspace hydration and autosave.
replace_once(
    PAGE,
    '        if (typeof stored.themeId === "string" && THEMES.some((item) => item.id === stored.themeId)) setThemeId(stored.themeId);',
    '''        if (typeof stored.themeId === "string" && (stored.themeId === CUSTOM_THEME_ID || THEMES.some((item) => item.id === stored.themeId))) setThemeId(stored.themeId);\n        if (typeof stored.customThemeBaseId === "string" && THEMES.some((item) => item.id === stored.customThemeBaseId)) setCustomThemeBaseId(stored.customThemeBaseId);\n        if (stored.customPalette) setCustomPalette(normalizeCustomPalette(stored.customPalette, getCustomPaletteFromTheme(INITIAL_THEME)));'''
)
replace_once(
    PAGE,
    '        cardCornerMode\n      };',
    '        cardCornerMode,\n        customThemeBaseId,\n        customPalette\n      };'
)
replace_once(
    PAGE,
    '  }, [hasHydrated, content, manualTitle, themeId, titleSize, bodySize, lineHeight, titleFontMode, subheadingStyle, highlightStyle, footerEnabled, footerLeft, footerRightMode, cardCornerMode]);',
    '  }, [hasHydrated, content, manualTitle, themeId, customThemeBaseId, customPalette, titleSize, bodySize, lineHeight, titleFontMode, subheadingStyle, highlightStyle, footerEnabled, footerLeft, footerRightMode, cardCornerMode]);'
)
replace_once(
    PAGE,
    '    setThemeId(INITIAL_THEME.id);\n    applyThemeEditorDefaults(INITIAL_THEME);',
    '    setThemeId(INITIAL_THEME.id);\n    setCustomThemeBaseId(INITIAL_THEME.id);\n    setCustomPalette(getCustomPaletteFromTheme(INITIAL_THEME));\n    applyThemeEditorDefaults(INITIAL_THEME);'
)
replace_once(
    PAGE,
    '      cardCornerMode\n    };\n    setUserPresets',
    '      cardCornerMode,\n      customThemeBaseId,\n      customPalette\n    };\n    setUserPresets'
)

# 6) Applying saved presets remains backward-compatible with old JSON.
old_apply = '''  function applyUserPreset(preset: UserPreset) {\n    setThemeId(THEMES.some((item) => item.id === preset.themeId) ? preset.themeId : INITIAL_THEME.id);\n    setTitleSize(preset.titleSize);\n    setBodySize(preset.bodySize);\n    setLineHeight(preset.lineHeight);\n    setTitleFontMode(preset.titleFontMode);\n    setSubheadingStyle(preset.subheadingStyle);\n    setHighlightStyle(preset.highlightStyle);\n    setFooterEnabled(preset.footerEnabled);\n    setFooterLeft(preset.footerLeft);\n    setFooterRightMode(preset.footerRightMode);\n    setCardCornerMode(preset.cardCornerMode);\n  }'''
new_apply = r'''  function applyUserPreset(preset: UserPreset) {
    if (preset.themeId === CUSTOM_THEME_ID) {
      const baseId = typeof preset.customThemeBaseId === "string" && THEMES.some((item) => item.id === preset.customThemeBaseId)
        ? preset.customThemeBaseId
        : INITIAL_THEME.id;
      const baseTheme = THEMES.find((item) => item.id === baseId) ?? INITIAL_THEME;
      setCustomThemeBaseId(baseId);
      setCustomPalette(normalizeCustomPalette(preset.customPalette, getCustomPaletteFromTheme(baseTheme)));
      setThemeId(CUSTOM_THEME_ID);
    } else {
      setThemeId(THEMES.some((item) => item.id === preset.themeId) ? preset.themeId : INITIAL_THEME.id);
    }
    setTitleSize(preset.titleSize);
    setBodySize(preset.bodySize);
    setLineHeight(preset.lineHeight);
    setTitleFontMode(preset.titleFontMode);
    setSubheadingStyle(preset.subheadingStyle);
    setHighlightStyle(preset.highlightStyle);
    setFooterEnabled(preset.footerEnabled);
    setFooterLeft(preset.footerLeft);
    setFooterRightMode(preset.footerRightMode);
    setCardCornerMode(preset.cardCornerMode);
  }'''
replace_once(PAGE, old_apply, new_apply)
replace_once(
    PAGE,
    '<span>{THEMES.find((item) => item.id === preset.themeId)?.name ?? "自定义样式"}</span>',
    '<span>{preset.themeId === CUSTOM_THEME_ID ? "自定义配色" : THEMES.find((item) => item.id === preset.themeId)?.name ?? "自定义样式"}</span>'
)

# 7) Custom palette card and editor under built-in themes.
old_theme_end = '''                          <span className="theme-card-check" style={{ background: item.palette.accent }} aria-hidden="true">{isActive ? "✓" : ""}</span>\n                        </button>\n                      );\n                    })}\n                  </div>\n                </details>'''
new_theme_end = r'''                          <span className="theme-card-check" style={{ background: item.palette.accent }} aria-hidden="true">{isActive ? "✓" : ""}</span>
                        </button>
                      );
                    })}
                    <button
                      type="button"
                      className={`theme-card theme-card--custom${themeId === CUSTOM_THEME_ID ? " active" : ""}`}
                      onClick={() => setThemeId(CUSTOM_THEME_ID)}
                      title="使用并继续编辑自定义配色"
                      style={themeId === CUSTOM_THEME_ID ? { borderColor: customThemePreview.palette.accent, boxShadow: `0 16px 32px ${hexToRgba(customThemePreview.palette.accent, 0.14)}` } : undefined}
                    >
                      <span
                        className="theme-swatch"
                        aria-hidden="true"
                        style={{
                          background: getThemeSwatchBackground(customThemePreview),
                          boxShadow: `inset 0 0 0 1px ${customThemePreview.palette.border}`
                        }}
                      >
                        <span className="theme-swatch-mark" style={{ color: customThemePreview.palette.text }}>自</span>
                        <span className="theme-swatch-lines" aria-hidden="true">
                          <span style={{ backgroundColor: customThemePreview.palette.accent }} />
                          <span style={{ backgroundColor: hexToRgba(customThemePreview.palette.text, 0.28) }} />
                          <span style={{ backgroundColor: customThemePreview.palette.accentSoft }} />
                        </span>
                      </span>
                      <span className="theme-card-copy">
                        <strong>自定义配色</strong>
                        <span className="theme-card-tags">
                          <span className="theme-card-tag">自由配色</span>
                          <span className="theme-card-tag">本地保存</span>
                        </span>
                      </span>
                      <span className="theme-card-check" style={{ background: customThemePreview.palette.accent }} aria-hidden="true">{themeId === CUSTOM_THEME_ID ? "✓" : ""}</span>
                    </button>
                  </div>

                  <div className="custom-theme-actions">
                    {themeId !== CUSTOM_THEME_ID ? (
                      <button type="button" className="secondary-action-button" onClick={startCustomThemeFromCurrent}>
                        复制当前主题并自定义
                      </button>
                    ) : (
                      <span className="custom-theme-base-label">版式基底：{customBaseTheme.name}</span>
                    )}
                  </div>

                  {themeId === CUSTOM_THEME_ID ? (
                    <div className="custom-theme-editor">
                      <div className="custom-theme-editor-head">
                        <div>
                          <strong>自定义配色</strong>
                          <p>只改颜色，版式、纹理和引用样式继续沿用 {customBaseTheme.name}。</p>
                        </div>
                        <button type="button" className="text-action-button" onClick={resetCustomPalette}>恢复基底配色</button>
                      </div>
                      <div className="custom-color-grid">
                        {CUSTOM_PALETTE_FIELDS.map((field) => {
                          const fallback = getCustomPaletteFromTheme(customBaseTheme)[field.key];
                          const pickerValue = normalizeHexColor(customPalette[field.key], fallback);
                          return (
                            <label key={field.key} className="custom-color-field">
                              <span className="custom-color-label">
                                <strong>{field.label}</strong>
                                <small>{field.hint}</small>
                              </span>
                              <span className="custom-color-controls">
                                <input
                                  type="color"
                                  value={pickerValue}
                                  onChange={(event) => updateCustomPaletteColor(field.key, event.target.value)}
                                  aria-label={`${field.label}颜色选择器`}
                                />
                                <input
                                  className="custom-hex-input"
                                  value={customPalette[field.key]}
                                  onChange={(event) => updateCustomPaletteColor(field.key, event.target.value)}
                                  onBlur={() => commitCustomPaletteColor(field.key)}
                                  spellCheck={false}
                                  aria-label={`${field.label} HEX`}
                                />
                              </span>
                            </label>
                          );
                        })}
                      </div>
                      <div className={`contrast-note${customContrastRatio < 4.5 ? " warning" : ""}`}>
                        <strong>正文对比度 {customContrastRatio.toFixed(1)}:1</strong>
                        <span>{customContrastRatio < 4.5 ? "当前文字与背景对比偏低，建议调深文字或调浅背景。" : "文字与主背景的可读性良好。"}</span>
                      </div>
                    </div>
                  ) : null}
                </details>'''
replace_once(PAGE, old_theme_end, new_theme_end)

# 8) CSS for custom palette editor.
css_addition = r'''

/* Curated and custom color themes */
.theme-card--custom {
  background: linear-gradient(145deg, rgba(255, 255, 255, 0.74), rgba(246, 242, 236, 0.72));
}

.custom-theme-actions {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 10px;
  margin-top: 12px;
}

.custom-theme-base-label {
  color: #746a60;
  font-size: 12px;
  font-weight: 650;
}

.custom-theme-editor {
  display: grid;
  gap: 14px;
  margin-top: 12px;
  padding: 14px;
  border: 1px solid rgba(72, 64, 56, 0.12);
  border-radius: 14px;
  background: rgba(255, 255, 255, 0.58);
}

.custom-theme-editor-head {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 12px;
}

.custom-theme-editor-head > div {
  display: grid;
  gap: 4px;
}

.custom-theme-editor-head strong {
  color: #2b261f;
  font-size: 13px;
}

.custom-theme-editor-head p {
  margin: 0;
  color: #80766c;
  font-size: 11px;
  line-height: 1.5;
}

.custom-color-grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 9px;
}

.custom-color-field {
  display: grid;
  gap: 7px;
  padding: 10px;
  border: 1px solid rgba(72, 64, 56, 0.1);
  border-radius: 11px;
  background: rgba(255, 255, 255, 0.7);
}

.custom-color-label {
  display: flex;
  align-items: baseline;
  justify-content: space-between;
  gap: 8px;
}

.custom-color-label strong {
  color: #3a342e;
  font-size: 12px;
}

.custom-color-label small {
  color: #968b80;
  font-size: 10px;
}

.custom-color-controls {
  display: grid;
  grid-template-columns: 34px minmax(0, 1fr);
  gap: 7px;
  align-items: center;
}

.custom-color-controls input[type="color"] {
  width: 34px;
  height: 34px;
  padding: 2px;
  border: 1px solid rgba(72, 64, 56, 0.14);
  border-radius: 9px;
  background: #fff;
  cursor: pointer;
}

.custom-hex-input {
  width: 100%;
  min-width: 0;
  border: 1px solid #e4e4e7;
  border-radius: 9px;
  padding: 8px 9px;
  background: #fff;
  color: #3a342e;
  font-family: ui-monospace, SFMono-Regular, Menlo, monospace;
  font-size: 11px;
  text-transform: uppercase;
}

.custom-hex-input:focus {
  outline: none;
  border-color: #a8a09a;
  box-shadow: 0 0 0 2px rgba(36, 32, 28, 0.08);
}

.contrast-note {
  display: grid;
  gap: 3px;
  padding: 10px 11px;
  border-radius: 10px;
  background: rgba(61, 118, 82, 0.08);
  color: #426550;
  font-size: 11px;
  line-height: 1.45;
}

.contrast-note.warning {
  background: rgba(178, 118, 42, 0.1);
  color: #815d2f;
}

@media (max-width: 760px) {
  .custom-color-grid {
    grid-template-columns: 1fr;
  }

  .custom-theme-editor-head,
  .custom-theme-actions {
    align-items: stretch;
    flex-direction: column;
  }
}
'''
css_text = CSS.read_text(encoding="utf-8")
if "/* Curated and custom color themes */" in css_text:
    raise RuntimeError("Custom theme CSS already present")
CSS.write_text(css_text.rstrip() + css_addition + "\n", encoding="utf-8")

# 9) README: standard documentation for the new color system.
replace_once(
    README,
    '- **多套视觉主题**：内置浅色、暖色、冷色和深色等多种卡片风格。',
    '- **14 套内置主题**：覆盖纸书、冷调、暖调、极简、深色、奶油、酒红、紫灰、东方纸墨等不同配色。\n- **自定义配色**：可从任一内置主题复制版式，自定义背景、文字、强调与柔和高亮颜色，并实时检查正文对比度。'
)
replace_once(
    README,
    '## 使用方式\n',
    '''## 自定义配色\n\n在 **视觉样式 → 排版风格预设** 中可以直接选择 14 套内置主题。需要自己的配色时：\n\n1. 先选择一个版式接近需求的内置主题。\n2. 点击 **复制当前主题并自定义**。\n3. 分别调整卡片背景、背景渐变、主文字、次文字、强调色和柔和高亮。\n4. 每个颜色既支持系统颜色选择器，也可以直接输入 HEX。\n5. 工具会实时计算正文与主背景的对比度；低于 4.5:1 时给出提醒，但不会强制阻止使用。\n6. 调整完成后，可在 **我的预设** 中保存当前样式；自定义颜色会随预设一起保存在本地，也支持 JSON 导入/导出。\n\n自定义主题只替换颜色层，原主题的版式、纸张纹理、引用块、高亮方式等视觉结构会继续保留。\n\n## 使用方式\n'''
)

# 10) Regression checks for the new built-ins and custom theme workflow.
test_text = TEST.read_text(encoding="utf-8")
checks = r'''

// Curated + custom theme system
assert.match(pageSource, /const EXTRA_THEME_PRESET_ORDER = \[[\s\S]*?"cream-coffee"[\s\S]*?"glacier-blue"[\s\S]*?"wine-gray"[\s\S]*?"lavender-mist"[\s\S]*?"cherry-cream"[\s\S]*?"ink-rice-paper"/, "six additional curated theme presets should be registered");
assert.match(pageSource, /id:\s*"cream-coffee"/, "cream coffee theme should be available");
assert.match(pageSource, /id:\s*"glacier-blue"/, "glacier blue theme should be available");
assert.match(pageSource, /id:\s*"wine-gray"/, "wine gray theme should be available");
assert.match(pageSource, /id:\s*"lavender-mist"/, "lavender mist theme should be available");
assert.match(pageSource, /id:\s*"cherry-cream"/, "cherry cream theme should be available");
assert.match(pageSource, /id:\s*"ink-rice-paper"/, "ink rice paper theme should be available");
assert.match(pageSource, /const CUSTOM_THEME_ID = "custom";/, "custom theme should have a stable id");
assert.match(pageSource, /const CUSTOM_PALETTE_FIELDS/, "custom theme should expose a bounded set of meaningful color controls");
assert.match(pageSource, /function buildCustomTheme/, "custom colors should reuse an existing structural theme");
assert.match(pageSource, /function getContrastRatio/, "custom colors should include a readability contrast check");
assert.match(pageSource, /复制当前主题并自定义/, "users should be able to fork a built-in palette into a custom theme");
assert.match(pageSource, /type="color"/, "custom theme editor should provide native color pickers");
assert.match(pageSource, /customThemeBaseId,[\s\S]*?customPalette/, "custom colors should be included in local workspace persistence");
assert.match(pageSource, /preset\.themeId === CUSTOM_THEME_ID/, "saved presets should restore custom colors");
assert.match(cssSource, /\.custom-theme-editor/, "custom theme editor should have dedicated UI styling");
assert.match(readmeSource, /14 套内置主题/, "README should document the expanded built-in theme library");
assert.match(readmeSource, /## 自定义配色/, "README should document custom palette editing");
'''
if "// Curated + custom theme system" in test_text:
    raise RuntimeError("Custom theme checks already present")
TEST.write_text(test_text.rstrip() + checks + "\n", encoding="utf-8")

print("Applied curated and custom theme upgrades.")

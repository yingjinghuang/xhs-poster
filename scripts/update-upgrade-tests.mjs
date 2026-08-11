import fs from "node:fs";

const path = "scripts/check-default-content.mjs";
let source = fs.readFileSync(path, "utf8");

const readmeAnchor = 'const readmeSource = readFileSync(join(root, "README.md"), "utf8");\n';
if (!source.includes(readmeAnchor)) throw new Error("Missing README test anchor");
source = source.replace(
  readmeAnchor,
  `${readmeAnchor}const zipSource = readFileSync(join(root, "app/zip.ts"), "utf8");\n`
);

const oldExportAssertions = `assert.match(pageSource, /manualTitle\\.trim\\(\\) \\|\\| "LuKK-小红书卡片"/, "untitled exports should use a LuKK-branded default name");\nassert.match(pageSource, /createExportFileName\\(manualTitle, index, exportTimestamp\\)/, "bulk export should name each single image from the user title and page number");`;

const newExportAssertions = `assert.match(pageSource, /manualTitle\\.trim\\(\\) \\|\\| "XHS-Poster"/, "untitled exports should use a neutral XHS-Poster default name");\nassert.doesNotMatch(pageSource, /LuKK-小红书卡片/, "visible export branding should not fall back to the upstream LuKK name");\nassert.match(pageSource, /createZipEntryName\\(manualTitle, index\\)/, "bulk export should name each image inside the ZIP by title and page number");\nassert.match(pageSource, /downloadBlob\\(createStoredZip\\(zipEntries\\), createZipFileName\\(manualTitle, exportTimestamp\\)\\)/, "bulk export should download one ZIP archive");\nassert.match(zipSource, /export function createStoredZip/, "ZIP creation should stay in a browser-only helper");\nassert.match(pageSource, /const WORKSPACE_STORAGE_KEY = "xhs-poster\\.workspace\\.v1";/, "workspace auto-save should use a versioned localStorage key");\nassert.match(pageSource, /window\\.localStorage\\.setItem\\(WORKSPACE_STORAGE_KEY/, "workspace changes should be auto-saved locally");\nassert.match(pageSource, /function isPageBreakLine/, "manual page-break syntax should have an explicit parser helper");\nassert.match(pageSource, /normalized === "---page---" \\|\\| normalized === "<!-- pagebreak -->"/, "manual page breaks should support both documented markers");\nassert.match(pageSource, /currentText === PAGE_BREAK_TOKEN/, "pagination should honor manual page-break tokens");\nassert.match(pageSource, /const USER_PRESETS_STORAGE_KEY = "xhs-poster\\.user-presets\\.v1";/, "saved style presets should use a versioned localStorage key");\nassert.match(pageSource, /function saveCurrentPreset/, "users should be able to save the current style as a preset");\nassert.match(pageSource, /function applyUserPreset/, "saved presets should be reusable");\nassert.match(pageSource, /导出预设 JSON/, "saved presets should support JSON export");`;

if (!source.includes(oldExportAssertions)) throw new Error("Missing legacy export assertions");
source = source.replace(oldExportAssertions, newExportAssertions);

fs.writeFileSync(path, source);

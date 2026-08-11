import fs from "node:fs";

const path = "app/page.tsx";
let source = fs.readFileSync(path, "utf8");
const before = `    if (isStandaloneMarkdownBlockStart(trimmed)) {\n      flushCurrentBlock();\n      blocks.push(isPageBreakLine(trimmed) ? PAGE_BREAK_TOKEN : trimmed);\n      continue;\n    }`;
const after = `    if (isStandaloneMarkdownBlockStart(trimmed)) {\n      flushCurrentBlock();\n      if (isPageBreakLine(trimmed)) {\n        blocks.push(PAGE_BREAK_TOKEN);\n      } else {\n        blocks.push(trimmed);\n      }\n      continue;\n    }`;
if (!source.includes(before)) throw new Error("Expected parser output was not found");
source = source.replace(before, after);
fs.writeFileSync(path, source);

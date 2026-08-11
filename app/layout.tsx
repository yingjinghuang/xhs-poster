import "./globals.css";
import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "XHS Poster｜小红书长文卡片排版工具",
  description: "将 Markdown 长文自动分页、排版并导出为可发布的 3:4 PNG 小红书卡片。"
};

export default function RootLayout({ children }: Readonly<{ children: React.ReactNode }>) {
  return (
    <html lang="zh-CN">
      <body>{children}</body>
    </html>
  );
}

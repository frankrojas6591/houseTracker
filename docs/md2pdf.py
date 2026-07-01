#!/usr/bin/env python3
import argparse
import sys
from pathlib import Path

import markdown
from weasyprint import HTML

CSS = """
@page  { margin: 12mm 14mm 12mm 22mm; size: letter; }
body    { font-family: Georgia, serif; font-size: 8.5pt; max-width: none;
          margin: 0; line-height: 1.4; color: #1a1a1a; }
h1      { font-size: 14pt; border-bottom: 2px solid #333; padding-bottom: 4px;
          margin-top: 10px; }
h2      { font-size: 11pt; border-bottom: 1px solid #aaa; padding-bottom: 3px;
          margin-top: 14px; color: #222; }
h3      { font-size: 9.5pt; margin-top: 10px; color: #333; }
table   { border-collapse: collapse; width: 100%; margin: 8px 0; font-size: 7.5pt; }
th      { background: #333; color: #fff; padding: 3px 7px; text-align: left; }
td      { border: 1px solid #ccc; padding: 3px 7px; vertical-align: top; }
tr:nth-child(even) td { background: #f7f7f7; }
blockquote { border-left: 3px solid #aaa; margin: 8px 0; padding: 2px 12px;
             color: #555; font-style: italic; }
code    { font-family: monospace; background: #f0f0f0; padding: 1px 3px;
          border-radius: 2px; font-size: 7.5pt; }
pre     { background: #f0f0f0; padding: 6px 10px; border-radius: 3px;
          overflow-x: auto; font-size: 7pt; line-height: 1.3; }
pre code { background: none; padding: 0; }
ul, ol  { margin: 4px 0; padding-left: 18px; }
li      { margin-bottom: 2px; }
hr      { border: none; border-top: 1px solid #ccc; margin: 12px 0; }
img     { max-width: 100%; height: auto; display: block; margin: 8px 0; }
"""

NEWPAGE_MD  = r'\newpage'
NEWPAGE_HTML = '<div style="page-break-after: always;"></div>'


def convert(md_path: Path) -> Path:
    pdf_path = md_path.with_suffix('.pdf')

    raw = md_path.read_text(encoding='utf-8').replace(NEWPAGE_MD, NEWPAGE_HTML)
    body = markdown.markdown(raw, extensions=['tables', 'fenced_code', 'nl2br'])

    html = (
        '<!DOCTYPE html><html><head><meta charset="utf-8">'
        f'<style>{CSS}</style></head><body>{body}</body></html>'
    )

    # base_url tells WeasyPrint where to resolve relative image paths (SVGs, etc.)
    HTML(string=html, base_url=md_path.parent.as_uri()).write_pdf(str(pdf_path))
    return pdf_path


def main():
    parser = argparse.ArgumentParser(
        description='Convert a Markdown file to PDF using weasyprint.')
    parser.add_argument('md_file', help='Path to the .md file')
    args = parser.parse_args()

    md_path = Path(args.md_file).resolve()
    if not md_path.exists():
        sys.exit(f'error: file not found: {md_path}')
    if md_path.suffix.lower() != '.md':
        sys.exit(f'error: expected a .md file, got: {md_path.name}')

    pdf_path = convert(md_path)
    print(f'wrote {pdf_path}')


if __name__ == '__main__':
    main()

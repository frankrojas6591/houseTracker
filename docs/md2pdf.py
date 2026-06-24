#!/usr/bin/env python3
import argparse
import sys
import tempfile
from pathlib import Path

import markdown
from weasyprint import HTML

CSS = """
body    { font-family: Georgia, serif; font-size: 11pt; max-width: 800px;
          margin: 40px auto; line-height: 1.6; color: #1a1a1a; }
h1      { font-size: 22pt; border-bottom: 2px solid #333; padding-bottom: 6px; }
h2      { font-size: 16pt; border-bottom: 1px solid #aaa; padding-bottom: 4px;
          margin-top: 28px; color: #222; }
h3      { font-size: 13pt; margin-top: 20px; color: #333; }
table   { border-collapse: collapse; width: 100%; margin: 12px 0; font-size: 10pt; }
th      { background: #333; color: #fff; padding: 6px 10px; text-align: left; }
td      { border: 1px solid #ccc; padding: 6px 10px; vertical-align: top; }
tr:nth-child(even) td { background: #f7f7f7; }
blockquote { border-left: 3px solid #aaa; margin: 12px 0; padding: 4px 16px;
             color: #555; font-style: italic; }
code    { font-family: monospace; background: #f0f0f0; padding: 1px 4px;
          border-radius: 2px; font-size: 9.5pt; }
pre     { background: #f0f0f0; padding: 10px 14px; border-radius: 4px;
          overflow-x: auto; font-size: 9pt; line-height: 1.4; }
pre code { background: none; padding: 0; }
ul, ol  { margin: 6px 0; padding-left: 24px; }
li      { margin-bottom: 4px; }
hr      { border: none; border-top: 1px solid #ccc; margin: 20px 0; }
@media print { body { margin: 20mm; max-width: none; } }
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

    with tempfile.NamedTemporaryFile(suffix='.html', mode='w',
                                    encoding='utf-8', delete=False) as f:
        f.write(html)
        tmp = f.name

    HTML(filename=tmp).write_pdf(str(pdf_path))
    Path(tmp).unlink(missing_ok=True)
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

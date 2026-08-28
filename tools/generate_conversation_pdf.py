"""Convert a manually copied conversation in Markdown/text into a PDF.

This program deliberately does not download or invent conversation content.  The
input file must contain the submitter's real exported or copied conversation.
"""
from __future__ import annotations

import argparse
import html
import re
import sys
from pathlib import Path

from pypdf import PdfReader
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    ListFlowable,
    ListItem,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
    XPreformatted,
)

DEFAULT_INPUT = Path("conversation_input.md")
DEFAULT_OUTPUT = Path("chatgpt_conversation.pdf")
HEADING = re.compile(r"^(#{1,6})\s+(.+?)\s*$")
LIST_ITEM = re.compile(r"^\s*(?:[-*+]\s+|\d+[.)]\s+)(.+?)\s*$")


def find_font(candidates: list[Path]) -> str | None:
    """Register the first installed TrueType font, if available."""
    for candidate in candidates:
        if candidate.is_file():
            font_name = f"ConversationFont{len(pdfmetrics.getRegisteredFontNames())}"
            pdfmetrics.registerFont(TTFont(font_name, str(candidate)))
            return font_name
    return None


def register_unicode_fonts() -> tuple[str, str]:
    """Prefer local TrueType fonts so Unicode characters render correctly."""
    sans = find_font([
        Path("C:/Windows/Fonts/arial.ttf"),
        Path("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"),
        Path("/Library/Fonts/Arial Unicode.ttf"),
    ]) or "Helvetica"
    mono = find_font([
        Path("C:/Windows/Fonts/consola.ttf"),
        Path("/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"),
        Path("/Library/Fonts/Menlo.ttc"),
    ]) or "Courier"
    return sans, mono


def inline_markup(text: str, mono_font: str) -> str:
    """Escape source text, then apply small safe Markdown inline formatting."""
    escaped = html.escape(text)
    escaped = re.sub(r"`([^`]+)`", rf'<font face="{mono_font}">\1</font>', escaped)
    escaped = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", escaped)
    return escaped


def table_from_lines(lines: list[str], style: ParagraphStyle) -> Table:
    rows = []
    for line in lines:
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        # Markdown table separator, such as | --- | --- |.
        if all(re.fullmatch(r":?-{3,}:?", cell.replace(" ", "")) for cell in cells):
            continue
        rows.append([Paragraph(inline_markup(cell, style.fontName), style) for cell in cells])
    if not rows:
        raise ValueError("A table must contain at least one non-separator row.")
    column_count = max(len(row) for row in rows)
    for row in rows:
        row.extend([Paragraph("", style)] * (column_count - len(row)))
    table = Table(rows, repeatRows=1, hAlign="LEFT")
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#E8EEF7")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.HexColor("#172B4D")),
        ("GRID", (0, 0), (-1, -1), 0.35, colors.HexColor("#AAB7C4")),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("RIGHTPADDING", (0, 0), (-1, -1), 6),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
    ]))
    return table


def build_story(content: str, sans_font: str, mono_font: str):
    styles = getSampleStyleSheet()
    body = ParagraphStyle("ConversationBody", parent=styles["BodyText"], fontName=sans_font, fontSize=10, leading=14, spaceAfter=7)
    title = ParagraphStyle("ConversationTitle", parent=styles["Title"], fontName=sans_font, alignment=TA_CENTER, textColor=colors.HexColor("#172B4D"), spaceAfter=14)
    headings = {
        level: ParagraphStyle(f"Heading{level}", parent=styles[f"Heading{min(level, 3)}"], fontName=sans_font, textColor=colors.HexColor("#172B4D"), spaceBefore=12, spaceAfter=6)
        for level in range(1, 7)
    }
    code = ParagraphStyle("ConversationCode", fontName=mono_font, fontSize=8.5, leading=11, backColor=colors.HexColor("#F4F6F8"), borderColor=colors.HexColor("#D5DDE5"), borderWidth=0.5, borderPadding=7)

    story, lines, index = [], content.replace("\r\n", "\n").split("\n"), 0
    first_heading = True
    while index < len(lines):
        line = lines[index]
        if not line.strip() or line.lstrip().startswith("<!--"):
            index += 1
            continue
        if line.strip().startswith("```"):
            index += 1
            block = []
            while index < len(lines) and not lines[index].strip().startswith("```"):
                block.append(lines[index])
                index += 1
            if index == len(lines):
                raise ValueError("Unclosed code block in input.")
            story.extend([XPreformatted("\n".join(block), code), Spacer(1, 8)])
            index += 1
            continue
        heading = HEADING.match(line)
        if heading:
            level, text = len(heading.group(1)), heading.group(2)
            style = title if level == 1 and first_heading else headings[level]
            story.append(Paragraph(inline_markup(text, mono_font), style))
            first_heading = False
            index += 1
            continue
        if "|" in line and line.strip().startswith("|"):
            table_lines = []
            while index < len(lines) and "|" in lines[index] and lines[index].strip().startswith("|"):
                table_lines.append(lines[index])
                index += 1
            story.extend([table_from_lines(table_lines, body), Spacer(1, 8)])
            continue
        if LIST_ITEM.match(line):
            items = []
            while index < len(lines) and (match := LIST_ITEM.match(lines[index])):
                items.append(ListItem(Paragraph(inline_markup(match.group(1), mono_font), body)))
                index += 1
            story.extend([ListFlowable(items, bulletType="bullet", leftIndent=18), Spacer(1, 6)])
            continue
        paragraph = [line.strip()]
        index += 1
        while index < len(lines) and lines[index].strip() and not HEADING.match(lines[index]) and not lines[index].strip().startswith("```") and not LIST_ITEM.match(lines[index]) and not lines[index].strip().startswith("|"):
            paragraph.append(lines[index].strip())
            index += 1
        story.append(Paragraph(inline_markup(" ".join(paragraph), mono_font), body))
    return story


def page_number(canvas, document):
    canvas.saveState()
    canvas.setFont("Helvetica", 8)
    canvas.setFillColor(colors.HexColor("#5E6C84"))
    canvas.drawRightString(A4[0] - 2 * cm, 1.25 * cm, f"Page {document.page}")
    canvas.restoreState()


def validate_pdf(output_path: Path) -> None:
    if not output_path.is_file() or output_path.stat().st_size < 1000:
        raise ValueError("PDF generation failed: output is missing or unexpectedly small.")
    with output_path.open("rb") as pdf_file:
        if not pdf_file.read(4) == b"%PDF":
            raise ValueError("PDF generation failed: output does not have a valid PDF header.")
    reader = PdfReader(str(output_path))
    if not reader.pages or not any(page.extract_text().strip() for page in reader.pages):
        raise ValueError("PDF generation failed: output contains no readable conversation text.")


def generate_pdf(input_path: Path, output_path: Path) -> None:
    if not input_path.is_file():
        raise FileNotFoundError(f"Input file not found: {input_path}")
    content = input_path.read_text(encoding="utf-8").strip()
    if not content:
        raise ValueError("Input is empty. Paste the real conversation into the input file first.")
    sans_font, mono_font = register_unicode_fonts()
    story = build_story(content, sans_font, mono_font)
    if not story:
        raise ValueError("Input has no printable conversation content.")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    document = SimpleDocTemplate(str(output_path), pagesize=A4, rightMargin=2 * cm, leftMargin=2 * cm, topMargin=2 * cm, bottomMargin=2 * cm, title="ChatGPT Conversation")
    document.build(story, onFirstPage=page_number, onLaterPages=page_number)
    validate_pdf(output_path)


def main() -> int:
    parser = argparse.ArgumentParser(description="Create a PDF from a manually copied real conversation.")
    parser.add_argument("--input", type=Path, default=DEFAULT_INPUT, help="UTF-8 Markdown/text file containing the real conversation.")
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT, help="PDF file to create (default: chatgpt_conversation.pdf).")
    arguments = parser.parse_args()
    try:
        generate_pdf(arguments.input, arguments.output)
    except (FileNotFoundError, ValueError) as error:
        print(f"Error: {error}", file=sys.stderr)
        return 1
    print(f"Created and validated: {arguments.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

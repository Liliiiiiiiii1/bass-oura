from pathlib import Path
import re
from xml.sax.saxutils import escape

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Image,
    Table, TableStyle, PageBreak
)

ROOT = Path(__file__).resolve().parent
SOURCE = ROOT / "report" / "report_source.md"
OUTPUT = ROOT / "report" / "report.pdf"

styles = getSampleStyleSheet()
styles.add(ParagraphStyle(
    name="ReportTitle", parent=styles["Title"],
    fontSize=22, leading=27, alignment=TA_CENTER,
    spaceAfter=18
))
styles.add(ParagraphStyle(
    name="HeadingOne", parent=styles["Heading1"],
    fontSize=16, leading=20, spaceBefore=14, spaceAfter=8
))
styles.add(ParagraphStyle(
    name="HeadingTwo", parent=styles["Heading2"],
    fontSize=12, leading=15, spaceBefore=10, spaceAfter=6
))
styles.add(ParagraphStyle(
    name="BodyTextCustom", parent=styles["BodyText"],
    fontSize=9, leading=13, spaceAfter=7
))
styles.add(ParagraphStyle(
    name="SmallCustom", parent=styles["BodyText"],
    fontSize=7.5, leading=10
))

def inline(text):
    text = escape(text)
    text = re.sub(r"\[([^\]]+)\]\((https?://[^)]+)\)",
                  r'<link href="\2" color="blue">\1</link>', text)
    text = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", text)
    text = re.sub(r"(?<!\*)\*([^*]+)\*(?!\*)", r"<i>\1</i>", text)
    text = re.sub(r"`([^`]+)`", r"<font name='Courier'>\1</font>", text)
    text = text.replace("$", "")
    return text

def footer(canvas, doc):
    canvas.saveState()
    canvas.setFont("Helvetica", 8)
    canvas.setFillColor(colors.grey)
    canvas.drawCentredString(A4[0] / 2, 1.1 * cm, f"{doc.page}")
    canvas.restoreState()

if not SOURCE.exists():
    raise FileNotFoundError(f"Cannot find {SOURCE}")

lines = SOURCE.read_text(encoding="utf-8").splitlines()
story = []
paragraph_lines = []
i = 0

def flush_paragraph():
    global paragraph_lines
    if paragraph_lines:
        text = " ".join(line.strip() for line in paragraph_lines)
        story.append(Paragraph(inline(text), styles["BodyTextCustom"]))
        paragraph_lines = []

while i < len(lines):
    line = lines[i].strip()

    if not line:
        flush_paragraph()
        i += 1
        continue

    # Insert the actual graph immediately after its figure description
    figure_images = {
        "Figure 1": ROOT / "img" / "fitbit_bass_fit.png",
        "Figure 2": ROOT / "img" / "oura_us_forecast.png",
    }
    figure_match = re.match(r"\*\*(Figure [12]):\*\*", line)
    if figure_match:
        flush_paragraph()
        story.append(Paragraph(inline(line), styles["BodyTextCustom"]))
        image_path = figure_images[figure_match.group(1)]
        if image_path.exists():
            img = Image(str(image_path))
            max_width = 16.5 * cm
            max_height = 15 * cm
            scale = min(max_width / img.imageWidth,
                        max_height / img.imageHeight, 1)
            img.drawWidth = img.imageWidth * scale
            img.drawHeight = img.imageHeight * scale
            story.extend([Spacer(1, 4), img, Spacer(1, 8)])
        else:
            raise FileNotFoundError(f"Missing figure: {image_path}")
        i += 1
        continue

    # Standard Markdown image syntax, if used elsewhere
    image_match = re.match(r"!\[(.*?)\]\((.*?)\)", line)
    if image_match:
        flush_paragraph()
        image_path = (SOURCE.parent / image_match.group(2)).resolve()
        if not image_path.exists():
            image_path = (ROOT / image_match.group(2)).resolve()
        if image_path.exists():
            img = Image(str(image_path))
            max_width = 16.5 * cm
            max_height = 15 * cm
            scale = min(max_width / img.imageWidth,
                        max_height / img.imageHeight, 1)
            img.drawWidth = img.imageWidth * scale
            img.drawHeight = img.imageHeight * scale
            story.extend([Spacer(1, 5), img, Spacer(1, 8)])
        else:
            raise FileNotFoundError(f"Missing image: {image_path}")
        i += 1
        continue

    # Markdown table
    if line.startswith("|") and i + 1 < len(lines) and re.match(
        r"^\s*\|?\s*:?-{3,}", lines[i + 1]
    ):
        flush_paragraph()
        raw_rows = []
        while i < len(lines) and lines[i].strip().startswith("|"):
            cells = [c.strip() for c in lines[i].strip().strip("|").split("|")]
            raw_rows.append(cells)
            i += 1
        if len(raw_rows) >= 2:
            data = []
            for row_index, row in enumerate(raw_rows):
                if row_index == 1:
                    continue
                data.append([
                    Paragraph(inline(cell), styles["SmallCustom"])
                    for cell in row
                ])
            if data:
                col_count = max(len(row) for row in data)
                widths = [16.5 * cm / col_count] * col_count
                table = Table(data, colWidths=widths, repeatRows=1,
                              hAlign="LEFT")
                table.setStyle(TableStyle([
                    ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#E8EEF5")),
                    ("TEXTCOLOR", (0, 0), (-1, 0), colors.HexColor("#172B4D")),
                    ("GRID", (0, 0), (-1, -1), 0.4, colors.grey),
                    ("VALIGN", (0, 0), (-1, -1), "TOP"),
                    ("LEFTPADDING", (0, 0), (-1, -1), 5),
                    ("RIGHTPADDING", (0, 0), (-1, -1), 5),
                    ("TOPPADDING", (0, 0), (-1, -1), 5),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
                ]))
                story.extend([table, Spacer(1, 8)])
        continue

    if line.startswith("# "):
        flush_paragraph()
        story.append(Paragraph(inline(line[2:]), styles["ReportTitle"]))
    elif line.startswith("## "):
        flush_paragraph()
        story.append(Paragraph(inline(line[3:]), styles["HeadingOne"]))
    elif line.startswith("### "):
        flush_paragraph()
        story.append(Paragraph(inline(line[4:]), styles["HeadingTwo"]))
    elif line.startswith("- ") or line.startswith("* "):
        flush_paragraph()
        story.append(Paragraph("• " + inline(line[2:]),
                               styles["BodyTextCustom"]))
    elif re.match(r"^\d+\.\s", line):
        flush_paragraph()
        story.append(Paragraph(inline(line), styles["BodyTextCustom"]))
    elif line in ("---", "***"):
        flush_paragraph()
        story.append(Spacer(1, 8))
    else:
        paragraph_lines.append(line)
    i += 1

flush_paragraph()

doc = SimpleDocTemplate(
    str(OUTPUT), pagesize=A4,
    rightMargin=2 * cm, leftMargin=2 * cm,
    topMargin=1.8 * cm, bottomMargin=1.8 * cm,
    title="Oura Ring 4 Bass Diffusion Analysis"
)
doc.build(story, onFirstPage=footer, onLaterPages=footer)

print(f"PDF created: {OUTPUT}")
print(f"Size: {OUTPUT.stat().st_size:,} bytes")

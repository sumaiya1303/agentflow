from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, HRFlowable, Table, TableStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER
from io import BytesIO
import re
from datetime import datetime

def clean_text(text: str) -> str:
    """Remove markdown symbols for PDF rendering."""
    text = re.sub(r'\*\*(.*?)\*\*', r'\1', text)
    text = re.sub(r'\*(.*?)\*', r'\1', text)
    text = re.sub(r'#{1,6}\s*', '', text)
    text = re.sub(r'={3,}', '', text)
    text = re.sub(r'-{3,}', '', text)
    text = text.strip()
    return text

def generate_pdf(company: str, research: str, analysis: str, report: str, duration: float) -> bytes:
    """
    Takes the three agent outputs and generates a professional PDF.
    Returns the PDF as bytes.
    """
    buffer = BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=0.75 * inch,
        leftMargin=0.75 * inch,
        topMargin=0.75 * inch,
        bottomMargin=0.75 * inch
    )

    # Define styles
    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        "TitleStyle",
        parent=styles["Title"],
        fontSize=22,
        textColor=colors.HexColor("#1a1d2e"),
        spaceAfter=6,
        alignment=TA_CENTER,
        fontName="Helvetica-Bold"
    )

    subtitle_style = ParagraphStyle(
        "SubtitleStyle",
        parent=styles["Normal"],
        fontSize=10,
        textColor=colors.HexColor("#6b7280"),
        spaceAfter=4,
        alignment=TA_CENTER
    )

    section_header_style = ParagraphStyle(
        "SectionHeader",
        parent=styles["Heading1"],
        fontSize=13,
        textColor=colors.HexColor("#1e40af"),
        spaceBefore=16,
        spaceAfter=6,
        fontName="Helvetica-Bold"
    )

    body_style = ParagraphStyle(
        "BodyStyle",
        parent=styles["Normal"],
        fontSize=10,
        textColor=colors.HexColor("#1f2937"),
        spaceAfter=6,
        leading=16
    )

    meta_style = ParagraphStyle(
        "MetaStyle",
        parent=styles["Normal"],
        fontSize=9,
        textColor=colors.HexColor("#6b7280"),
        spaceAfter=4
    )

    # Build PDF content
    content = []

    # Header
    content.append(Spacer(1, 0.2 * inch))
    content.append(Paragraph("AgentFlow", title_style))
    content.append(Paragraph("Multi-Agent Financial Due Diligence Platform", subtitle_style))
    content.append(Spacer(1, 0.1 * inch))
    content.append(HRFlowable(width="100%", thickness=2, color=colors.HexColor("#1e40af")))
    content.append(Spacer(1, 0.1 * inch))

    # Report title
    content.append(Paragraph(f"Due Diligence Report: {company.upper()}", section_header_style))

    # Metadata table
    meta_data = [
        ["Generated:", datetime.now().strftime("%B %d, %Y at %H:%M")],
        ["Processing Time:", f"{duration} seconds"],
        ["Architecture:", "Zero Data Egress — All inference ran locally via Ollama + LLaMA3"],
        ["Agents Used:", "Researcher → Analyst → Reporter"],
    ]

    meta_table = Table(meta_data, colWidths=[1.5 * inch, 5 * inch])
    meta_table.setStyle(TableStyle([
        ("FONTSIZE", (0, 0), (-1, -1), 9),
        ("TEXTCOLOR", (0, 0), (0, -1), colors.HexColor("#6b7280")),
        ("TEXTCOLOR", (1, 0), (1, -1), colors.HexColor("#1f2937")),
        ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
    ]))

    content.append(meta_table)
    content.append(Spacer(1, 0.2 * inch))
    content.append(HRFlowable(width="100%", thickness=0.5, color=colors.HexColor("#e5e7eb")))

    # Full Report Section
    content.append(Paragraph("FULL DUE DILIGENCE REPORT", section_header_style))
    for line in report.split("\n"):
        cleaned = clean_text(line)
        if cleaned:
            content.append(Paragraph(cleaned, body_style))

    content.append(Spacer(1, 0.2 * inch))
    content.append(HRFlowable(width="100%", thickness=0.5, color=colors.HexColor("#e5e7eb")))

    # Research Section
    content.append(Paragraph("RESEARCH DATA", section_header_style))
    for line in research.split("\n"):
        cleaned = clean_text(line)
        if cleaned:
            content.append(Paragraph(cleaned, body_style))

    content.append(Spacer(1, 0.2 * inch))
    content.append(HRFlowable(width="100%", thickness=0.5, color=colors.HexColor("#e5e7eb")))

    # Analysis Section
    content.append(Paragraph("RISK ANALYSIS", section_header_style))
    for line in analysis.split("\n"):
        cleaned = clean_text(line)
        if cleaned:
            content.append(Paragraph(cleaned, body_style))

    content.append(Spacer(1, 0.3 * inch))
    content.append(HRFlowable(width="100%", thickness=2, color=colors.HexColor("#1e40af")))
    content.append(Spacer(1, 0.1 * inch))
    content.append(Paragraph("Generated by AgentFlow — Local-first Multi-Agent AI Platform", meta_style))
    content.append(Paragraph("Zero Data Egress — No data left this machine during generation", meta_style))

    doc.build(content)
    return buffer.getvalue()
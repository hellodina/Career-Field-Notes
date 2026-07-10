from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
from reportlab.lib.enums import TA_LEFT, TA_CENTER
from datetime import datetime
from io import BytesIO

def generate_pdf(student, entries):
    """Generate PDF of all entries + journey recap."""
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter, topMargin=0.5*inch, bottomMargin=0.5*inch)
    
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor='#2c3e50',
        spaceAfter=12,
        alignment=TA_CENTER
    )
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=14,
        textColor='#34495e',
        spaceAfter=8,
        spaceBefore=8
    )
    normal_style = ParagraphStyle(
        'CustomBody',
        parent=styles['BodyText'],
        fontSize=10,
        spaceAfter=6
    )
    
    story = []
    
    # Title page
    story.append(Paragraph("Career Field Notes", title_style))
    story.append(Spacer(1, 0.2*inch))
    story.append(Paragraph(f"<b>{student.display_name}</b>", heading_style))
    story.append(Paragraph(f"Internship: {student.internship_date}", normal_style))
    story.append(Paragraph(f"Generated: {datetime.now().strftime('%B %d, %Y')}", normal_style))
    story.append(Spacer(1, 0.3*inch))
    
    # Journey recap (Entry 1 vs Entry 6)
    story.append(Paragraph("Your Journey: First Contact → Version 1.0", heading_style))
    
    e1 = entries[1]
    e6 = entries[6]
    
    story.append(Paragraph("<b>Entry 1: First Contact</b>", ParagraphStyle('SubHead', parent=styles['Heading3'], fontSize=11)))
    if e1:
        for prompt, answer in e1.fields.items():
            story.append(Paragraph(f"<b>{prompt}:</b> {answer[:200]}", normal_style))
            story.append(Spacer(1, 0.1*inch))
    story.append(Spacer(1, 0.2*inch))
    
    story.append(Paragraph("<b>Entry 6: Your Version 1.0 Plan</b>", ParagraphStyle('SubHead', parent=styles['Heading3'], fontSize=11)))
    if e6:
        for prompt, answer in e6.fields.items():
            story.append(Paragraph(f"<b>{prompt}:</b> {answer[:200]}", normal_style))
            story.append(Spacer(1, 0.1*inch))
    
    story.append(PageBreak())
    
    # All entries
    story.append(Paragraph("Full Field Notes", heading_style))
    
    for entry_num in range(1, 7):
        entry = entries[entry_num]
        if entry:
            story.append(Paragraph(f"<b>Entry {entry_num}: {entry.fields.get('title', 'Untitled')}</b>", heading_style))
            for prompt, answer in entry.fields.items():
                if prompt != 'title':
                    story.append(Paragraph(f"<i>{prompt}</i>", normal_style))
                    story.append(Paragraph(answer, normal_style))
                    story.append(Spacer(1, 0.08*inch))
            story.append(Spacer(1, 0.2*inch))
    
    doc.build(story)
    buffer.seek(0)
    return buffer.getvalue()

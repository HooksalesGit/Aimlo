from reportlab.lib.pagesizes import LETTER
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from datetime import datetime
import textwrap
def build_prequal_pdf(filename, deal, summary, warnings, checklist, disclaimer):
    c=canvas.Canvas(filename, pagesize=LETTER); w,h=LETTER; y=h-0.75*inch
    def line(txt, size=10, dy=14):
        nonlocal y; c.setFont('Helvetica', size); c.drawString(0.75*inch, y, txt); y-=dy
    line('Aimlo Prequalification Summary',14,18); line(datetime.now().strftime('%Y-%m-%d %H:%M'),9,14); line(' ')
    line('Deal Snapshot',12,16)
    for k in ['Scenario','Program','Rate','TermYears','PurchasePrice','BaseLoan','AdjustedLoan','LTV']: line(f"{k}: {deal.get(k,'')}")
    line(' '); line('Income & DTI',12,16)
    for k in ['TotalIncome','PITIA','OtherDebts','FE','BE']:
        v=summary.get(k,0.0); line(f"{k}: {v:.2%}" if k in ['FE','BE'] else f"{k}: ${v:,.2f}")
    line(' '); line('Warnings',12,16)
    if not warnings: line('None')
    else:
        for r in warnings: line(f"[{r.get('code')}] {r.get('message')}")
    line(' '); line('Documentation Checklist',12,16)
    for item in checklist: line(f"[ ] {item}")
    line(' '); line('Disclaimer',12,16)
    for chunk in textwrap.wrap(disclaimer, 95): line(chunk,8,10)
    c.showPage(); c.save()

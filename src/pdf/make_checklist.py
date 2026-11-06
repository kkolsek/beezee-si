#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Zgradi PDF »Kontrolni seznam pred prenovo spletne strani« v SL/EN/HR.
Uporaba: python3 src/pdf/make_checklist.py   → dist/assets/pdf/beezee-kontrolni-seznam-{sl,en,hr}.pdf
Potrebuje: reportlab, fonttools, brotli (pip install reportlab fonttools brotli)."""
import os, sys, tempfile
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib.colors import HexColor, white
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT
from reportlab.platypus import (BaseDocTemplate, PageTemplate, Frame, Paragraph, Spacer, Table, TableStyle, Flowable, KeepTogether)
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from fontTools.ttLib import TTFont as FTFont
from fontTools.merge import Merger

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
FONTS = os.path.join(ROOT, "dist", "assets", "fonts")
IMG = os.path.join(ROOT, "dist", "assets", "img")
OUT = os.path.join(ROOT, "dist", "assets", "pdf")
sys.path.insert(0, HERE)
from checklist_content import CHECKLIST

HONEY, INK, CREAM, AMBER, GREY, PALE = HexColor("#FFDD55"), HexColor("#141414"), HexColor("#FFF8E7"), HexColor("#E8B92E"), HexColor("#6B6459"), HexColor("#FFF1C2")
W, H = A4
M = 20 * mm

# ---------- pisave: woff2 (latin + latin-ext) -> ttf ----------
def font(name, w):
    tmp = tempfile.mkdtemp()
    parts = []
    for sub in ("latin", "latin-ext"):
        f = FTFont(os.path.join(FONTS, f"{name}-{sub}-{w}-normal.woff2")); f.flavor = None
        p = os.path.join(tmp, f"{sub}.ttf"); f.save(p); parts.append(p)
    merged = Merger().merge(parts); out = os.path.join(tmp, f"{name}-{w}.ttf"); merged.save(out)
    return out

pdfmetrics.registerFont(TTFont("Baloo", font("baloo-2", "700")))
pdfmetrics.registerFont(TTFont("Body", font("dm-sans", "400")))
pdfmetrics.registerFont(TTFont("BodyB", font("dm-sans", "700")))
pdfmetrics.registerFont(TTFont("Hand", font("caveat", "700")))

sTitle = ParagraphStyle("t", fontName="Baloo", fontSize=30, leading=34, textColor=INK)
sSub = ParagraphStyle("s", fontName="Hand", fontSize=20, leading=24, textColor=GREY)
sBody = ParagraphStyle("b", fontName="Body", fontSize=10.5, leading=15, textColor=INK)
sHow = ParagraphStyle("h", parent=sBody, textColor=GREY, fontSize=9.5, leading=13.5)
sH2 = ParagraphStyle("h2", fontName="Baloo", fontSize=17, leading=20, textColor=INK)
sItem = ParagraphStyle("i", fontName="Body", fontSize=10.5, leading=14, textColor=INK)
sOutroT = ParagraphStyle("ot", fontName="Baloo", fontSize=22, leading=26, textColor=INK)
sContact = ParagraphStyle("c", fontName="BodyB", fontSize=11, leading=14, textColor=INK)

def hexagon(c, cx, cy, w, h, fill, stroke=None):
    p = c.beginPath()
    pts = [(cx, cy + h/2), (cx + w/2, cy + h/4), (cx + w/2, cy - h/4), (cx, cy - h/2), (cx - w/2, cy - h/4), (cx - w/2, cy + h/4)]
    p.moveTo(*pts[0])
    for x, y in pts[1:]: p.lineTo(x, y)
    p.close()
    c.setFillColor(fill)
    if stroke: c.setStrokeColor(stroke); c.setLineWidth(1.2)
    c.drawPath(p, fill=1, stroke=1 if stroke else 0)

class Checkbox(Flowable):
    def __init__(self, size=4.2*mm): super().__init__(); self.size = size
    def wrap(self, aw, ah): return self.size, self.size
    def draw(self):
        c = self.canv; s = self.size
        c.setStrokeColor(INK); c.setLineWidth(1.3); c.setFillColor(white)
        c.roundRect(0, 0, s, s, 1.2*mm, fill=1, stroke=1)

class HexNumber(Flowable):
    def __init__(self, n): super().__init__(); self.n = n; self.w = 11*mm; self.h = 12.5*mm
    def wrap(self, aw, ah): return self.w, self.h
    def draw(self):
        c = self.canv; hexagon(c, self.w/2, self.h/2, self.w, self.h, HONEY)
        c.setFillColor(INK); c.setFont("Hand", 18); c.drawCentredString(self.w/2, self.h/2 - 6, str(self.n))

def on_page(lang):
    t = CHECKLIST[lang]
    def _draw(c, doc):
        # ozadje zgoraj + dekoracija
        c.saveState()
        if doc.page == 1:
            c.setFillColor(CREAM); c.rect(0, H - 78*mm, W, 78*mm, fill=1, stroke=0)
            hexagon(c, W - 22*mm, H - 20*mm, 46*mm, 53*mm, HONEY)
            hexagon(c, W - 52*mm, H - 58*mm, 22*mm, 25*mm, PALE)
            c.drawImage(os.path.join(IMG, "logo-black.png"), W - 31*mm, H - 30*mm, 18*mm, 18*mm, mask="auto")
            c.setFillColor(INK); c.setFont("Baloo", 13); c.drawString(M, H - 16*mm, "BEEZEE")
            c.setFont("Hand", 15); c.setFillColor(GREY)
            c.saveState(); c.translate(W - 78*mm, H - 49*mm); c.rotate(-5); c.drawString(0, 0, t["sticker"]); c.restoreState()
        else:
            hexagon(c, W - 10*mm, H - 8*mm, 24*mm, 28*mm, PALE)
        # noga
        c.setStrokeColor(HexColor("#E6DCC4")); c.setLineWidth(0.8); c.setDash(3, 3); c.line(M, 16*mm, W - M, 16*mm); c.setDash()
        c.setFont("Body", 8); c.setFillColor(GREY); c.drawString(M, 10.5*mm, t["footer"])
        c.setFont("Baloo", 9); c.setFillColor(INK); c.drawRightString(W - M, 10.5*mm, f"{doc.page}")
        c.restoreState()
    return _draw

def build(lang):
    t = CHECKLIST[lang]
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, f"beezee-kontrolni-seznam-{lang}.pdf")
    doc = BaseDocTemplate(path, pagesize=A4, leftMargin=M, rightMargin=M, topMargin=M, bottomMargin=22*mm,
                          title=t["title"], author="Katja Kolšek – BEEZEE", subject=t["subtitle"], creator="beezee.si")
    first = Frame(M, 22*mm, W - 2*M, H - 22*mm - 24*mm, id="first", leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0)
    rest = Frame(M, 22*mm, W - 2*M, H - 22*mm - M, id="rest", leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0)
    doc.addPageTemplates([PageTemplate(id="First", frames=[first], onPage=on_page(lang)),
                          PageTemplate(id="Rest", frames=[rest], onPage=on_page(lang))])
    from reportlab.platypus import NextPageTemplate
    story = [NextPageTemplate("Rest")]
    story += [Spacer(1, 6*mm), Paragraph(t["title"], ParagraphStyle("tt", parent=sTitle, rightIndent=62*mm)), Spacer(1, 2*mm),
              Paragraph(t["subtitle"], sSub), Spacer(1, 10*mm),
              Paragraph(t["intro"], ParagraphStyle("in", parent=sBody, rightIndent=10*mm)), Spacer(1, 3*mm),
              Paragraph(t["how"], ParagraphStyle("hw", parent=sHow, rightIndent=10*mm)), Spacer(1, 8*mm)]
    for n, (title, items) in enumerate(t["sections"], 1):
        head = Table([[HexNumber(n), Paragraph(title, sH2)]], colWidths=[14*mm, None], rowHeights=[13*mm])
        head.setStyle(TableStyle([("VALIGN", (0, 0), (-1, -1), "MIDDLE"), ("LEFTPADDING", (0, 0), (-1, -1), 0), ("BOTTOMPADDING", (0, 0), (-1, -1), 0), ("TOPPADDING", (0, 0), (-1, -1), 0)]))
        rows = [[Checkbox(), Paragraph(it, sItem)] for it in items]
        tbl = Table(rows, colWidths=[9*mm, None])
        tbl.setStyle(TableStyle([("VALIGN", (0, 0), (-1, -1), "TOP"), ("LEFTPADDING", (0, 0), (-1, -1), 2), ("RIGHTPADDING", (0, 0), (-1, -1), 4),
                                 ("TOPPADDING", (0, 0), (-1, -1), 3), ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
                                 ("LINEBELOW", (1, 0), (1, -2), 0.5, HexColor("#EEDFB8"))]))
        story += [KeepTogether([head, Spacer(1, 1.5*mm), tbl]), Spacer(1, 7*mm)]
    outro = Table([[Paragraph(t["outro_title"], sOutroT)], [Paragraph(t["outro"], sBody)], [Paragraph(t["contact"], sContact)]], colWidths=[W - 2*M])
    outro.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, -1), HONEY), ("BOX", (0, 0), (-1, -1), 1.2, INK), ("ROUNDEDCORNERS", [10, 10, 10, 10]),
                               ("LEFTPADDING", (0, 0), (-1, -1), 8*mm), ("RIGHTPADDING", (0, 0), (-1, -1), 8*mm), ("TOPPADDING", (0, 0), (0, 0), 6*mm),
                               ("BOTTOMPADDING", (0, -1), (0, -1), 6*mm), ("TOPPADDING", (0, 1), (0, -1), 1.5*mm), ("BOTTOMPADDING", (0, 0), (0, -2), 1.5*mm)]))
    story += [KeepTogether([outro])]
    doc.build(story)
    return path

if __name__ == "__main__":
    for lang in ("sl", "en", "hr"):
        print(build(lang))

"""
PDF Resume & Cover Letter Generator Module — NY DataMind
100% Native PDF Generator using fpdf2 & qrcode.
"""

import io
import os
import qrcode
from datetime import datetime
from fpdf import FPDF
from typing import Dict, Any, List

# Custom Color Accents Map
COLOR_ACCENTS = {
    "Navy Blue": (30, 58, 138),
    "Emerald Teal": (13, 148, 136),
    "Royal Purple": (88, 28, 135),
    "Slate Charcoal": (51, 65, 85),
    "Crimson Red": (185, 28, 28),
    "Midnight Black": (15, 23, 42)
}

class Executive_PDF(FPDF):
    def __init__(self, accent_color=(30, 58, 138)):
        super().__init__(orientation='P', unit='mm', format='A4')
        self.set_margins(12, 12, 12)
        self.set_auto_page_break(auto=True, margin=12)
        self.accent_color = accent_color

    def sanitize_text(self, text: str) -> str:
        if not text:
            return ""
        replacements = {
            '•': '-', '–': '-', '—': '-', '“': '"', '”': '"', '‘': "'", '’': "'",
            '✓': '[v]', '⚡': '*', '🟢': '', '🔵': '', '🟡': '', '🔴': '', '🎯': ''
        }
        for k, v in replacements.items():
            text = text.replace(k, v)
        return text.encode('latin-1', 'replace').decode('latin-1')

    def add_section_header(self, title: str):
        self.set_x(12)
        self.set_font('Helvetica', 'B', 11.5)
        self.set_text_color(*self.accent_color)
        self.cell(0, 6, self.sanitize_text(title.upper()), ln=True)
        self.set_x(12)
        self.set_draw_color(*self.accent_color)
        self.set_line_width(0.5)
        self.line(12, self.get_y(), 198, self.get_y())
        self.ln(2.5)
        self.set_x(12)
        self.set_text_color(30, 41, 59)


def generate_qr_code(url: str, filename="temp_qr.png") -> str:
    """Generates QR Code image for LinkedIn/GitHub links."""
    if not url:
        return ""
    try:
        qr = qrcode.QRCode(version=1, box_size=3, border=1)
        qr.add_data(url)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")
        img.save(filename)
        return filename
    except Exception:
        return ""


def generate_pdf(template_key: str, d: Dict[str, Any], custom_color_name="Navy Blue") -> bytes:
    """Generates ultra-professional PDF binary bytes for given template style and accent color."""

    accent = COLOR_ACCENTS.get(custom_color_name, (30, 58, 138))

    pdf = Executive_PDF(accent_color=accent)
    pdf.add_page()

    full_name = pdf.sanitize_text(d.get("full_name", "Alex Morgan"))
    target_role = pdf.sanitize_text(d.get("target_role", "Senior Software Engineer"))
    email = pdf.sanitize_text(d.get("email", "alex@example.com"))
    phone = pdf.sanitize_text(d.get("phone", "+1 555-0199"))
    location = pdf.sanitize_text(d.get("location", "San Francisco, CA"))
    linkedin = pdf.sanitize_text(d.get("linkedin", "linkedin.com/in/alex"))

    photo_fn = d.get("photo_filename", "")
    has_photo = (template_key in ["2", "4"]) and photo_fn and os.path.exists(photo_fn)

    # Generate QR Code image
    qr_fn = generate_qr_code(d.get("linkedin", "")) if d.get("linkedin") else ""

    # HEADER SECTION
    if has_photo:
        try:
            pdf.image(photo_fn, x=168, y=12, w=28)
        except Exception:
            pass
        pdf.set_font('Helvetica', 'B', 20)
        pdf.set_text_color(*accent)
        pdf.cell(150, 8, full_name, ln=True); pdf.set_x(12)
        pdf.set_font('Helvetica', 'B', 11)
        pdf.set_text_color(71, 85, 105)
        pdf.cell(150, 5.5, target_role, ln=True); pdf.set_x(12)
        pdf.set_font('Helvetica', '', 9)
        pdf.set_text_color(100, 116, 139)
        pdf.cell(150, 4.5, f"{email}  |  {phone}  |  {location}  |  {linkedin}", ln=True); pdf.set_x(12)
        pdf.ln(3); pdf.set_x(12)
    else:
        pdf.set_font('Helvetica', 'B', 22)
        pdf.set_text_color(*accent)
        pdf.cell(0, 9, full_name, ln=True, align='C'); pdf.set_x(12)
        pdf.set_font('Helvetica', 'B', 11)
        pdf.set_text_color(71, 85, 105)
        pdf.cell(0, 5.5, target_role, ln=True, align='C'); pdf.set_x(12)
        pdf.set_font('Helvetica', '', 9)
        pdf.set_text_color(100, 116, 139)
        pdf.cell(0, 4.5, f"{email}  |  {phone}  |  {location}  |  {linkedin}", ln=True, align='C'); pdf.set_x(12)
        pdf.ln(3); pdf.set_x(12)

    # 1. SUMMARY
    summary_text = pdf.sanitize_text(d.get("summary", ""))
    if summary_text:
        pdf.add_section_header("Professional Summary")
        pdf.set_font('Helvetica', '', 9.5)
        pdf.set_text_color(30, 41, 59)
        pdf.multi_cell(0, 4.6, summary_text); pdf.set_x(12)
        pdf.ln(3); pdf.set_x(12)

    # 2. SKILLS
    skills_text = pdf.sanitize_text(d.get("skills", ""))
    if skills_text:
        pdf.add_section_header("Technical & Core Skills")
        pdf.set_font('Helvetica', '', 9.5)
        pdf.set_text_color(30, 41, 59)
        pdf.multi_cell(0, 4.6, f"Core Proficiencies: {skills_text}"); pdf.set_x(12)
        pdf.ln(3); pdf.set_x(12)

    # 3. WORK EXPERIENCE
    experiences = d.get("experience", [])
    if experiences:
        pdf.add_section_header("Professional Experience")
        for exp in experiences:
            title = pdf.sanitize_text(exp.get("title", ""))
            company = pdf.sanitize_text(exp.get("company", ""))
            dates = pdf.sanitize_text(exp.get("dates", ""))
            loc = pdf.sanitize_text(exp.get("location", ""))

            pdf.set_font('Helvetica', 'B', 10.5)
            pdf.set_text_color(15, 23, 42)
            pdf.cell(0, 5, f"{title} - {company} ({dates} | {loc})", ln=True); pdf.set_x(12)

            pdf.set_font('Helvetica', '', 9)
            pdf.set_text_color(51, 65, 85)
            for bullet in exp.get("bullets", []):
                clean_b = pdf.sanitize_text(bullet)
                if clean_b:
                    pdf.multi_cell(0, 4.5, f"-  {clean_b}"); pdf.set_x(12)
            pdf.ln(2); pdf.set_x(12)

    # 4. PROJECTS
    projects = d.get("projects", [])
    if projects:
        pdf.add_section_header("Key Engineering & Analytical Projects")
        for proj in projects:
            p_name = pdf.sanitize_text(proj.get("name", ""))
            p_tech = pdf.sanitize_text(proj.get("tech", ""))
            p_desc = pdf.sanitize_text(proj.get("description", ""))

            pdf.set_font('Helvetica', 'B', 10)
            pdf.set_text_color(15, 23, 42)
            pdf.cell(0, 5, f"{p_name} [{p_tech}]", ln=True); pdf.set_x(12)
            pdf.set_font('Helvetica', '', 9)
            pdf.set_text_color(51, 65, 85)
            pdf.multi_cell(0, 4.5, p_desc); pdf.set_x(12)
            pdf.ln(1.5); pdf.set_x(12)

    # 5. EDUCATION
    education = d.get("education", [])
    if education:
        pdf.add_section_header("Education & Credentials")
        for edu in education:
            degree = pdf.sanitize_text(edu.get("degree", ""))
            inst = pdf.sanitize_text(edu.get("institution", ""))
            dates = pdf.sanitize_text(edu.get("dates", ""))

            pdf.set_font('Helvetica', 'B', 10)
            pdf.set_text_color(15, 23, 42)
            pdf.cell(0, 5, f"{degree}, {inst} ({dates})", ln=True); pdf.set_x(12)

    # Cleanup temp QR image
    if qr_fn and os.path.exists(qr_fn):
        try:
            os.remove(qr_fn)
        except Exception:
            pass

    return bytes(pdf.output())


def generate_cover_letter_pdf(d: Dict[str, Any], custom_color_name="Navy Blue") -> bytes:
    """Generates matching Cover Letter PDF binary bytes."""
    accent = COLOR_ACCENTS.get(custom_color_name, (30, 58, 138))

    pdf = Executive_PDF(accent_color=accent)
    pdf.add_page()

    name = pdf.sanitize_text(d.get("full_name", "Alex Morgan"))
    role = pdf.sanitize_text(d.get("target_role", "Software Engineer"))
    email = pdf.sanitize_text(d.get("email", "alex@example.com"))
    phone = pdf.sanitize_text(d.get("phone", "+1 555-0199"))
    location = pdf.sanitize_text(d.get("location", "San Francisco, CA"))
    skills = pdf.sanitize_text(d.get("skills", "Python, SQL, React, AWS"))

    # HEADER
    pdf.set_font('Helvetica', 'B', 22)
    pdf.set_text_color(*accent)
    pdf.cell(0, 10, name, ln=True); pdf.set_x(12)
    pdf.set_font('Helvetica', 'B', 11)
    pdf.set_text_color(71, 85, 105)
    pdf.cell(0, 6, f"Target Position: {role}", ln=True); pdf.set_x(12)
    pdf.set_font('Helvetica', '', 9.5)
    pdf.set_text_color(100, 116, 139)
    pdf.cell(0, 5, f"Contact: {email} | {phone} | {location}", ln=True); pdf.set_x(12)
    pdf.ln(4); pdf.set_x(12)

    # DIVIDER LINE
    pdf.set_draw_color(*accent)
    pdf.set_line_width(0.5)
    pdf.line(12, pdf.get_y(), 198, pdf.get_y())
    pdf.ln(6); pdf.set_x(12)

    # BODY
    body_paragraphs = [
        "Dear Hiring Manager,",
        f"I am writing to express my strong interest in the {role} position. With a proven track record in technical innovation, system design, and delivering scalable solutions, I am excited about the opportunity to contribute to your team.",
        f"Throughout my career, I have specialized in leveraging core technologies including {skills}. In my previous engineering roles, I have spearheaded critical projects, optimized operational pipelines, and delivered measurable business value.",
        "What drives me is solving complex technical challenges and collaborating with cross-functional teams to build impactful products. I am dedicated to continuous learning, data-driven execution, and modern engineering standards.",
        "I am confident that my technical expertise, problem-solving mindset, and passion for quality make me a strong candidate. I look forward to discussing how my background aligns with your team's goals.",
        f"Thank you for your time and consideration.\n\nSincerely,\n{name}\n{email} | {phone}"
    ]

    pdf.set_font('Helvetica', '', 10)
    pdf.set_text_color(30, 41, 59)
    for p in body_paragraphs:
        pdf.multi_cell(0, 5.2, p); pdf.set_x(12)
        pdf.ln(3); pdf.set_x(12)

    return bytes(pdf.output())


# ==============================================================================
# ATS SCORE REPORT PDF (Recruiter-Facing — Executive Score Benchmark Report)
# ==============================================================================

def _score_verdict(score: int):
    """Returns (label, rgb_color, description) verdict badge matching the app's tiering."""
    if score >= 85:
        return (
            "EXCELLENT — SHORTLIST READY",
            (16, 150, 100),
            "Candidate profile demonstrates high ATS keyword alignment, robust action verb usage, and strong quantified business metrics. Highly recommended for top recruiter shortlist."
        )
    elif score >= 70:
        return (
            "STRONG — PASSES ATS SCREENER",
            (37, 99, 235),
            "Profile successfully passes corporate ATS filtering algorithms. Incorporating recommended missing domain keywords will further elevate recruiter ranking."
        )
    elif score >= 50:
        return (
            "MODERATE — OPTIMIZATION NEEDED",
            (217, 119, 6),
            "Moderate ATS match. Core foundational experience is visible, but several critical domain keywords or measurable metrics are missing, reducing automated match rank."
        )
    else:
        return (
            "AT RISK — HIGH FILTER RISK",
            (220, 38, 38),
            "Elevated risk of automated ATS screener rejection. Critical technical keywords, standard structural headings, or measurable achievements require immediate revision."
        )


class Report_PDF(FPDF):
    def __init__(self, accent_color=(37, 99, 235)):
        super().__init__(orientation='P', unit='mm', format='A4')
        self.set_margins(12, 12, 12)
        self.set_auto_page_break(auto=True, margin=14)
        self.accent_color = accent_color
        self.report_id = "NYDM-" + datetime.now().strftime("%Y%m%d-%H%M%S")

    def sanitize_text(self, text: str) -> str:
        if not text:
            return ""
        replacements = {
            '•': '-', '–': '-', '—': '-', '“': '"', '”': '"', '‘': "'", '’': "'",
            '✓': '[v]', '✗': '[x]', '⚡': '*', '🟢': '', '🔵': '', '🟡': '', '🔴': '',
            '🎯': '', '📊': '', '🛠️': '', '🚀': '', '📄': '', '✓': '[v]'
        }
        for k, v in replacements.items():
            text = text.replace(k, v)
        return text.encode('latin-1', 'replace').decode('latin-1')

    def footer(self):
        self.set_y(-13)
        self.set_draw_color(226, 232, 240)
        self.set_line_width(0.3)
        self.line(12, self.get_y(), 198, self.get_y())
        self.ln(2)
        self.set_x(12)
        self.set_font('Helvetica', '', 7.5)
        self.set_text_color(148, 163, 184)
        self.cell(100, 4, f"NY DATAMIND CAREER INTELLIGENCE  |  AUDIT ID: {self.report_id}", new_x="RIGHT", new_y="TOP")
        self.set_x(112)
        self.cell(86, 4, f"CONFIDENTIAL  |  Page {self.page_no()}", align='R', new_x="LMARGIN", new_y="NEXT")

    def section_header(self, title: str, badge: str = ""):
        y = self.get_y()
        self.set_xy(12, y)
        self.set_fill_color(*self.accent_color)
        self.rect(12, y + 0.8, 3, 5.2, style='F', round_corners=True, corner_radius=1)

        self.set_xy(17, y)
        self.set_font('Helvetica', 'B', 10)
        self.set_text_color(15, 23, 42)
        clean_title = self.sanitize_text(title.upper())
        self.cell(self.get_string_width(clean_title) + 2, 6.8, clean_title, new_x="RIGHT", new_y="TOP")

        if badge:
            badge_text = self.sanitize_text(badge)
            self.set_font('Helvetica', 'B', 7)
            bw = self.get_string_width(badge_text) + 7
            bx = 198 - bw
            self.set_fill_color(239, 246, 255)
            self.set_draw_color(191, 219, 254)
            self.rect(bx, y + 1.2, bw, 4.5, style='DF', round_corners=True, corner_radius=1)
            self.set_xy(bx, y + 1.2)
            self.set_text_color(37, 99, 235)
            self.cell(bw, 4.5, badge_text, align='C', new_x="LMARGIN", new_y="NEXT")

        self.set_xy(12, y + 7.5)
        self.set_draw_color(241, 245, 249)
        self.set_line_width(0.4)
        self.line(12, self.get_y(), 198, self.get_y())
        self.ln(2.5)

    def draw_progress_bar(self, x: float, y: float, w: float, h: float, pct: float, fill_color, bg_color=(241, 245, 249)):
        self.set_fill_color(*bg_color)
        self.rect(x, y, w, h, style='F', round_corners=True, corner_radius=1.2)
        if pct > 0:
            filled_w = max(2.5, min(w, w * pct))
            self.set_fill_color(*fill_color)
            self.rect(x, y, filled_w, h, style='F', round_corners=True, corner_radius=1.2)

    def render_chips_grid(self, items: List[str], fill_color, text_color, border_color, prefix=""):
        if not items:
            self.set_font('Helvetica', 'I', 8)
            self.set_text_color(148, 163, 184)
            self.cell(0, 5, "None detected for this domain criteria.", new_x="LMARGIN", new_y="NEXT")
            self.set_x(12)
            return

        self.set_font('Helvetica', 'B', 7.5)
        x_cursor = 12
        y_cursor = self.get_y()
        max_x = 198
        chip_h = 5.4

        for item in items:
            label = self.sanitize_text(f"{prefix}{item}")
            text_w = self.get_string_width(label) + 6.0
            if x_cursor + text_w > max_x:
                x_cursor = 12
                y_cursor += chip_h + 1.6
            if y_cursor > 275:
                self.add_page()
                x_cursor, y_cursor = 12, self.get_y()

            self.set_fill_color(*fill_color)
            self.set_draw_color(*border_color)
            self.set_line_width(0.2)
            self.rect(x_cursor, y_cursor, text_w, chip_h, style='DF', round_corners=True, corner_radius=1.5)

            self.set_xy(x_cursor, y_cursor)
            self.set_text_color(*text_color)
            self.cell(text_w, chip_h, label, align='C', new_x="RIGHT", new_y="TOP")
            x_cursor += text_w + 2.0

        self.set_xy(12, y_cursor + chip_h + 2.5)


def generate_ats_report_pdf(results: Dict[str, Any], domain_target: str, candidate: Dict[str, Any] = None) -> bytes:
    """
    Generates a smart, executive-grade ATS Compatibility Score Report PDF.
    Features:
    - High-impact executive masthead with domain metadata
    - Candidate identity card
    - Hero score benchmark card with recruiter verdict & screener readiness
    - 3-card summary KPI stats (Skill Coverage, Action Verbs, Impact Metrics)
    - 5-Pillar Score Breakdown with visual progress bars
    - Skill Match & Keyword Intelligence chips matrix
    - ATS Structural/Formatting audit and high-ROI optimization checklist
    """
    candidate = candidate or {}
    accent = COLOR_ACCENTS.get("Navy Blue", (37, 99, 235))
    pdf = Report_PDF(accent_color=accent)
    pdf.add_page()

    score = results.get("overall_score", 0)
    verdict_label, verdict_color, verdict_desc = _score_verdict(score)
    gen_date = datetime.now().strftime("%d %b %Y, %I:%M %p")

    candidate_name = pdf.sanitize_text(candidate.get("full_name", "") or "Executive Candidate")
    target_role = pdf.sanitize_text(candidate.get("target_role", "") or "Professional Candidate")
    email = pdf.sanitize_text(candidate.get("email", ""))
    phone = pdf.sanitize_text(candidate.get("phone", ""))
    linkedin = pdf.sanitize_text(candidate.get("linkedin", ""))

    # =========================================================================
    # 1. TOP DUAL STRIPE & MASTHEAD
    # =========================================================================
    pdf.set_fill_color(15, 23, 42)
    pdf.rect(0, 0, 210, 3.2, style='F')
    pdf.set_fill_color(37, 99, 235)
    pdf.rect(0, 3.2, 210, 1.2, style='F')

    pdf.set_xy(12, 7.5)
    logo_path = "logo_decagon.png" if os.path.exists("logo_decagon.png") else ("logo.jpg" if os.path.exists("logo.jpg") else None)
    if logo_path:
        try:
            pdf.image(logo_path, x=12, y=8.0, h=11)
            pdf.set_xy(26, 7.5)
        except Exception:
            pdf.set_xy(12, 7.5)

    text_start_x = pdf.get_x()
    pdf.set_font('Helvetica', 'B', 7.5)
    pdf.set_text_color(37, 99, 235)
    pdf.cell(100, 3.8, "NY DATAMIND CAREER PLATFORM  |  ATS BENCHMARK ENGINE", new_x="LMARGIN", new_y="NEXT")
    pdf.set_x(text_start_x)
    pdf.set_font('Helvetica', 'B', 15)
    pdf.set_text_color(15, 23, 42)
    pdf.cell(100, 6.0, "ATS Compatibility Score Report", new_x="LMARGIN", new_y="NEXT")
    pdf.set_x(text_start_x)
    pdf.set_font('Helvetica', '', 8)
    pdf.set_text_color(100, 116, 139)
    pdf.cell(100, 3.8, f"Automated Screener Audit  |  Generated: {gen_date}", new_x="LMARGIN", new_y="NEXT")

    # Right side meta badge
    badge_x = 136.0
    badge_y = 7.5
    pdf.set_fill_color(248, 250, 252)
    pdf.set_draw_color(226, 232, 240)
    pdf.rect(badge_x, badge_y, 62, 14.0, style='DF', round_corners=True, corner_radius=1.5)
    pdf.set_xy(badge_x + 3, badge_y + 2.0)
    pdf.set_font('Helvetica', 'B', 7)
    pdf.set_text_color(100, 116, 139)
    pdf.cell(56, 3.2, "TARGET DOMAIN FIELD:", new_x="LMARGIN", new_y="NEXT")
    pdf.set_xy(badge_x + 3, badge_y + 5.8)
    pdf.set_font('Helvetica', 'B', 8.5)
    pdf.set_text_color(37, 99, 235)
    pdf.cell(56, 4.2, pdf.sanitize_text(domain_target)[:29], new_x="LMARGIN", new_y="NEXT")

    pdf.set_xy(12, 24.5)
    pdf.set_draw_color(226, 232, 240)
    pdf.set_line_width(0.3)
    pdf.line(12, pdf.get_y(), 198, pdf.get_y())
    pdf.ln(2.5)

    # =========================================================================
    # 2. CANDIDATE IDENTITY STRIP (NAME ONLY - BIG FONT)
    # =========================================================================
    cand_y = pdf.get_y()
    cand_h = 13.0
    pdf.set_fill_color(248, 250, 252)
    pdf.set_draw_color(226, 232, 240)
    pdf.rect(12, cand_y, 186, cand_h, style='DF', round_corners=True, corner_radius=2)
    pdf.set_fill_color(37, 99, 235)
    pdf.rect(12, cand_y, 2.5, cand_h, style='F', round_corners=True, corner_radius=1)

    pdf.set_xy(18, cand_y + 2.8)
    pdf.set_font('Helvetica', 'B', 16)
    pdf.set_text_color(15, 23, 42)
    pdf.cell(0, 7.5, candidate_name, new_x="LMARGIN", new_y="NEXT")

    pdf.set_xy(12, cand_y + cand_h + 2.5)

    # =========================================================================
    # 3. EXECUTIVE HERO SCORE CARD
    # =========================================================================
    hero_y = pdf.get_y()
    hero_h = 30.5
    pdf.set_fill_color(248, 250, 252)
    pdf.set_draw_color(226, 232, 240)
    pdf.rect(12, hero_y, 186, hero_h, style='DF', round_corners=True, corner_radius=2.5)

    # Left score box indicator
    pdf.set_fill_color(*verdict_color)
    pdf.rect(12, hero_y, 3, hero_h, style='F', round_corners=True, corner_radius=1)

    score_str = str(score)
    pdf.set_font('Helvetica', 'B', 28)
    pdf.set_text_color(15, 23, 42)
    pdf.set_xy(18, hero_y + 2.5)
    sw = pdf.get_string_width(score_str)
    pdf.cell(sw, 11, score_str, new_x="RIGHT", new_y="TOP")

    pdf.set_font('Helvetica', 'B', 9.5)
    pdf.set_text_color(148, 163, 184)
    pdf.set_xy(18 + sw + 1.5, hero_y + 8.5)
    pdf.cell(16, 5, "/ 100", new_x="RIGHT", new_y="TOP")

    # Verdict pill under score
    pill_y = hero_y + 17.5
    pill_w = 48.0
    pill_h = 6.2
    if verdict_color == (16, 150, 100):
        pdf.set_fill_color(236, 253, 245)
        pdf.set_draw_color(167, 243, 208)
    elif verdict_color == (37, 99, 235):
        pdf.set_fill_color(239, 246, 255)
        pdf.set_draw_color(191, 219, 254)
    elif verdict_color == (217, 119, 6):
        pdf.set_fill_color(254, 243, 199)
        pdf.set_draw_color(253, 230, 138)
    else:
        pdf.set_fill_color(254, 242, 242)
        pdf.set_draw_color(254, 202, 202)

    pdf.rect(18, pill_y, pill_w, pill_h, style='DF', round_corners=True, corner_radius=1.5)
    pdf.set_xy(18, pill_y)
    pdf.set_font('Helvetica', 'B', 7)
    pdf.set_text_color(*verdict_color)
    pdf.cell(pill_w, pill_h, pdf.sanitize_text(verdict_label.split('—')[0].strip()), align='C', new_x="RIGHT", new_y="TOP")

    # Right side: Executive explanation
    pdf.set_xy(70, hero_y + 3.0)
    pdf.set_font('Helvetica', 'B', 8.5)
    pdf.set_text_color(15, 23, 42)
    pdf.cell(124, 4.2, "EXECUTIVE RECRUITER VERDICT & SCREENER READINESS", new_x="LMARGIN", new_y="NEXT")

    pdf.set_xy(70, hero_y + 7.8)
    pdf.set_font('Helvetica', '', 8)
    pdf.set_text_color(71, 85, 105)
    pdf.multi_cell(124, 3.7, pdf.sanitize_text(verdict_desc))

    # Bottom scale bar inside hero card
    scale_y = hero_y + 23.5
    pdf.set_xy(70, scale_y)
    pdf.set_font('Helvetica', 'B', 6.8)
    pdf.set_text_color(148, 163, 184)
    pdf.cell(124, 3.2, "BENCHMARK TIERS:   [ <50 At Risk ]   [ 50-69 Moderate ]   [ 70-84 Strong ]   [ 85-100 Elite Shortlist ]", new_x="LMARGIN", new_y="NEXT")

    pdf.set_xy(12, hero_y + hero_h + 3.2)

    # =========================================================================
    # 4. THREE STAT CARDS GRID
    # =========================================================================
    matched = results.get("hard_skills_matched", [])
    missing = results.get("hard_skills_missing", [])
    total_skills = len(matched) + len(missing)
    skills_pct = int(round((len(matched) / total_skills) * 100)) if total_skills > 0 else 0
    verbs_count = len(results.get("action_verbs_found", []))
    quant_count = results.get("quantified_metrics_count", 0)

    card_y = pdf.get_y()
    card_w = 59.5
    card_h = 15.0
    cards_data = [
        ("SKILL COVERAGE", f"{len(matched)} / {total_skills} Matched", f"{skills_pct}% Target Alignment", (16, 150, 100) if skills_pct >= 70 else (217, 119, 6)),
        ("ACTION VERBS", f"{verbs_count} Power Verbs", "Leadership & Impact Voice", (37, 99, 235) if verbs_count >= 6 else (217, 119, 6)),
        ("IMPACT METRICS", f"{quant_count} Quantified Signals", "Data-Backed Business ROI", (16, 150, 100) if quant_count >= 3 else (220, 38, 38))
    ]

    for i, (ctitle, cval, csub, ccol) in enumerate(cards_data):
        cx = 12 + i * (card_w + 3.8)
        pdf.set_fill_color(248, 250, 252)
        pdf.set_draw_color(226, 232, 240)
        pdf.rect(cx, card_y, card_w, card_h, style='DF', round_corners=True, corner_radius=2)
        pdf.set_fill_color(*ccol)
        pdf.rect(cx, card_y, 2, card_h, style='F', round_corners=True, corner_radius=1)

        pdf.set_xy(cx + 4.5, card_y + 1.6)
        pdf.set_font('Helvetica', 'B', 6.8)
        pdf.set_text_color(100, 116, 139)
        pdf.cell(card_w - 6, 3.0, ctitle, new_x="LMARGIN", new_y="NEXT")

        pdf.set_xy(cx + 4.5, card_y + 4.8)
        pdf.set_font('Helvetica', 'B', 9.5)
        pdf.set_text_color(15, 23, 42)
        pdf.cell(card_w - 6, 4.6, cval, new_x="LMARGIN", new_y="NEXT")

        pdf.set_xy(cx + 4.5, card_y + 9.8)
        pdf.set_font('Helvetica', '', 6.8)
        pdf.set_text_color(*ccol)
        pdf.cell(card_w - 6, 3.2, csub, new_x="LMARGIN", new_y="NEXT")

    pdf.set_xy(12, card_y + card_h + 4.0)

    # =========================================================================
    # 5. 5-PILLAR SCORE BREAKDOWN MATRIX
    # =========================================================================
    pdf.section_header("5-Pillar Score Breakdown", badge="Weighted Screener Model")

    pillars = [
        ("Technical Skill Depth", results.get("skills_score", 0), 30, "Industry & domain technical keywords"),
        ("Action Verb Power", results.get("verbs_score", 0), 25, "Strong active leadership & execution verbs"),
        ("Quantified Impact Metrics", results.get("metrics_score", 0), 20, "Measurable ROI, percentages & performance"),
        ("ATS Section Structure", results.get("section_score", 0), 15, "Standard headings (Experience, Skills, Education)"),
        ("Readability & Word Count", results.get("readability_score", 0), 10, "Target 400-850 words & bullet conciseness")
    ]

    p_y = pdf.get_y()
    for name, p_score, p_max, desc in pillars:
        pct = max(0.0, min(1.0, p_score / p_max if p_max else 0))
        if pct >= 0.8:
            bar_color = (16, 150, 100)
            status_text = "OPTIMAL"
        elif pct >= 0.5:
            bar_color = (37, 99, 235)
            status_text = "STRONG"
        elif pct >= 0.3:
            bar_color = (217, 119, 6)
            status_text = "ATTENTION"
        else:
            bar_color = (220, 38, 38)
            status_text = "CRITICAL GAP"

        pdf.set_xy(12, p_y)
        pdf.set_font('Helvetica', 'B', 8)
        pdf.set_text_color(15, 23, 42)
        pdf.cell(52, 4.0, pdf.sanitize_text(name), new_x="RIGHT", new_y="TOP")

        pdf.set_font('Helvetica', '', 6.8)
        pdf.set_text_color(148, 163, 184)
        pdf.set_xy(12, p_y + 3.8)
        pdf.cell(52, 3.0, pdf.sanitize_text(desc)[:38], new_x="RIGHT", new_y="TOP")

        # Progress bar (w=72mm)
        bar_x = 66.0
        bar_w = 72.0
        bar_h = 3.8
        pdf.draw_progress_bar(bar_x, p_y + 1.6, bar_w, bar_h, pct, fill_color=bar_color)

        # Score numbers (x=142 to 164)
        pdf.set_xy(bar_x + bar_w + 3.0, p_y + 1.0)
        pdf.set_font('Helvetica', 'B', 8)
        pdf.set_text_color(15, 23, 42)
        pdf.cell(20, 4.2, f"{p_score:g} / {p_max:g}", new_x="RIGHT", new_y="TOP")

        # Status badge (x=165 to 198)
        pdf.set_xy(165, p_y + 1.0)
        pdf.set_font('Helvetica', 'B', 7)
        pdf.set_text_color(*bar_color)
        pdf.cell(33, 4.2, f"({int(round(pct*100))}%) {status_text}", align='R', new_x="LMARGIN", new_y="NEXT")

        p_y += 7.8

    pdf.set_xy(12, p_y + 1.0)

    # =========================================================================
    # 6. SKILL MATCH INTELLIGENCE (CHIPS)
    # =========================================================================
    pdf.section_header(f"Skill Intelligence Matrix", badge=f"Target: {domain_target[:24]}")

    pdf.set_xy(12, pdf.get_y())
    pdf.set_font('Helvetica', 'B', 7.5)
    pdf.set_text_color(16, 150, 100)
    pdf.cell(0, 3.8, pdf.sanitize_text(f"MATCHED DOMAIN KEYWORDS ({len(matched)})"), new_x="LMARGIN", new_y="NEXT")
    pdf.ln(0.4)
    pdf.render_chips_grid(
        matched,
        fill_color=(236, 253, 245),
        text_color=(6, 95, 70),
        border_color=(167, 243, 208),
        prefix="[v] "
    )

    pdf.set_font('Helvetica', 'B', 7.5)
    pdf.set_text_color(185, 28, 28)
    pdf.cell(0, 3.8, pdf.sanitize_text(f"RECOMMENDED MISSING KEYWORDS ({len(missing)})"), new_x="LMARGIN", new_y="NEXT")
    pdf.ln(0.4)
    pdf.render_chips_grid(
        missing,
        fill_color=(254, 242, 242),
        text_color=(153, 27, 27),
        border_color=(254, 202, 202),
        prefix="+ "
    )

    # =========================================================================
    # 7. FORMATTING AUDIT & RECOMMENDATIONS
    # =========================================================================
    warnings = results.get("formatting_warnings", [])
    recs = results.get("recommendations", [])

    if warnings or recs:
        if pdf.get_y() > 230:
            pdf.add_page()

        pdf.section_header("Recruiter Audit & Actionable Next Steps")

        if warnings:
            pdf.set_font('Helvetica', 'B', 7.5)
            pdf.set_text_color(217, 119, 6)
            pdf.cell(0, 3.8, "FORMATTING & STRUCTURAL AUDIT:", new_x="LMARGIN", new_y="NEXT")
            pdf.ln(0.4)
            for w in warnings:
                wy = pdf.get_y()
                pdf.set_fill_color(254, 243, 199)
                pdf.set_draw_color(253, 230, 138)
                pdf.rect(12, wy, 186, 5.4, style='DF', round_corners=True, corner_radius=1.2)
                pdf.set_fill_color(217, 119, 6)
                pdf.rect(12, wy, 1.8, 5.4, style='F', round_corners=True, corner_radius=1)

                pdf.set_xy(16, wy + 0.8)
                pdf.set_font('Helvetica', '', 7.5)
                pdf.set_text_color(120, 53, 15)
                pdf.cell(180, 3.8, pdf.sanitize_text(w), new_x="LMARGIN", new_y="NEXT")
                pdf.set_xy(12, wy + 6.6)

        if recs:
            pdf.ln(0.8)
            pdf.set_font('Helvetica', 'B', 7.5)
            pdf.set_text_color(37, 99, 235)
            pdf.cell(0, 3.8, "STRATEGIC OPTIMIZATION RECOMMENDATIONS:", new_x="LMARGIN", new_y="NEXT")
            pdf.ln(0.4)
            for i, r in enumerate(recs, 1):
                ry = pdf.get_y()
                pdf.set_fill_color(239, 246, 255)
                pdf.set_draw_color(191, 219, 254)
                pdf.rect(12, ry, 186, 5.4, style='DF', round_corners=True, corner_radius=1.2)
                pdf.set_fill_color(37, 99, 235)
                pdf.rect(12, ry, 1.8, 5.4, style='F', round_corners=True, corner_radius=1)

                pdf.set_xy(16, ry + 0.8)
                pdf.set_font('Helvetica', '', 7.5)
                pdf.set_text_color(30, 58, 138)
                pdf.cell(180, 3.8, pdf.sanitize_text(f"{i}.  {r}"), new_x="LMARGIN", new_y="NEXT")
                pdf.set_xy(12, ry + 6.6)

    return bytes(pdf.output())

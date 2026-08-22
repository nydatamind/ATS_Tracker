"""
LaTeX Resume Templates Generator Module
Provides 6 production-grade LaTeX resume templates with dynamic data injection,
Photo & Non-Photo layouts, LaTeX character escaping, and downloadable source generator.
"""

import re
from typing import Dict, Any, List

def escape_latex(text: str) -> str:
    """Escapes special LaTeX characters in text strings."""
    if not isinstance(text, str):
        return str(text)
    
    replacements = [
        ('\\', r'\textbackslash{}'),
        ('&', r'\&'),
        ('%', r'\%'),
        ('$', r'\$'),
        ('#', r'\#'),
        ('_', r'\_'),
        ('{', r'\{'),
        ('}', r'\}'),
        ('~', r'\textasciitilde{}'),
        ('^', r'\textasciicircum{}'),
    ]
    for char, replacement in replacements:
        text = text.replace(char, replacement)
    return text


def clean_dict_for_latex(data: Dict[str, Any]) -> Dict[str, Any]:
    """Recursively escapes strings in dictionary for safe LaTeX rendering."""
    cleaned = {}
    for k, v in data.items():
        if isinstance(v, str):
            cleaned[k] = escape_latex(v)
        elif isinstance(v, list):
            new_list = []
            for item in v:
                if isinstance(item, str):
                    new_list.append(escape_latex(item))
                elif isinstance(item, dict):
                    new_list.append(clean_dict_for_latex(item))
                else:
                    new_list.append(item)
            cleaned[k] = new_list
        elif isinstance(v, dict):
            cleaned[k] = clean_dict_for_latex(v)
        else:
            cleaned[k] = v
    return cleaned


# ==========================================
# 1. CLASSIC ATS TEMPLATE (JAKE'S STYLE) - NO PHOTO
# ==========================================
def template_classic_ats(d: Dict[str, Any]) -> str:
    exp_code = ""
    for exp in d.get("experience", []):
        bullets = "\n".join([f"    \\resumeItem{{{b}}}" for b in exp.get("bullets", [])])
        exp_code += f"""
  \\resumeSubheading
    {{{exp.get('title', '')}}}{{{exp.get('dates', '')}}}
    {{{exp.get('company', '')}}}{{{exp.get('location', '')}}}
    \\resumeItemListStart
{bullets}
    \\resumeItemListEnd
"""

    edu_code = ""
    for edu in d.get("education", []):
        edu_code += f"""
  \\resumeSubheading
    {{{edu.get('institution', '')}}}{{{edu.get('dates', '')}}}
    {{{edu.get('degree', '')}}}{{GPA: {edu.get('gpa', 'N/A')}}}
"""

    proj_code = ""
    for proj in d.get("projects", []):
        proj_code += f"""
  \\resumeProjectHeading
    {{\\textbf{{{proj.get('name', '')}}} $|$ \\emph{{{proj.get('tech', '')}}}}}{{}}
    \\resumeItemListStart
      \\resumeItem{{{proj.get('description', '')}}}
    \\resumeItemListEnd
"""

    return f"""\\documentclass[letterpaper,11pt]{{article}}

\\usepackage{{latexsym}}
\\usepackage[empty]{{fullpage}}
\\usepackage{{titlesec}}
\\usepackage{{marvosym}}
\\usepackage[usenames,dvipsnames]{{color}}
\\usepackage{{verbatim}}
\\usepackage{{enumitem}}
\\usepackage[hidelinks]{{hyperref}}
\\usepackage{{fancyhdr}}
\\usepackage[english]{{babel}}
\\usepackage{{tabularx}}

\\pagestyle{{fancy}}
\\fancyhf{{}}
\\fancyfoot{{}}
\\renewcommand{{\\headrulewidth}}{{0pt}}
\\renewcommand{{\\footrulewidth}}{{0pt}}

\\addtolength{{\\oddsidemargin}}{{-0.5in}}
\\addtolength{{\\evensidemargin}}{{-0.5in}}
\\addtolength{{\\textwidth}}{{1.0in}}
\\addtolength{{\\topmargin}}{{-0.5in}}
\\addtolength{{\\textheight}}{{1.0in}}

\\urlstyle{{same}}
\\raggedbottom
\\raggedright
\\setlength{{\\tabcolsep}}{{0pt}}

\\titleformat{{\\section}}{{\\vspace{{-4pt}}\\scshape\\raggedright\\large}}{{}}{{0em}}{{}}[\\color{{black}}\\vspace{{-5pt}}\\hline]

\\newcommand{{\\resumeItem}}[1]{{\\item\\small{{#1 \\vspace{{-2pt}}}}}}
\\newcommand{{\\resumeSubheading}}[4]{{
  \\vspace{{-2pt}}\\item
    \\begin{{tabularx}}{{0.97\\textwidth}}[t]{{X r}}
      \\textbf{{#1}} & #2 \\\\
      \\italic{{#3}} & \\small #4 \\\\
    \\end{{tabularx}}\\vspace{{-7pt}}
}}
\\newcommand{{\\resumeProjectHeading}}[2]{{
    \\item
    \\begin{{tabularx}}{{0.97\\textwidth}}{{X r}}
      \\small#1 & #2 \\\\
    \\end{{tabularx}}\\vspace{{-7pt}}
}}
\\newcommand{{\\resumeSubItem}}[1]{{\\resumeItem{{#1}}\\vspace{{-4pt}}}}
\\renewcommand\\labelitemii{{$\\vcenter{{\\hbox{{\\tiny$\\bullet$}}}}$}}
\\newcommand{{\\resumeSubHeadingListStart}}{{\\begin{{itemize}}[leftmargin=0.15in, label={{}}]}}
\\newcommand{{\\resumeSubHeadingListEnd}}{{\\end{{itemize}}}}
\\newcommand{{\\resumeItemListStart}}{{\\begin{{itemize}}}}
\\newcommand{{\\resumeItemListEnd}}{{\\end{{itemize}}\\vspace{{-5pt}}}}

\\begin{{document}}

%----------HEADING----------
\\begin{{center}}
    \\textbf{{\\Huge \\scshape {d.get('full_name', '')}}} \\\\ \\vspace{{1pt}}
    \\small {d.get('phone', '')} $|$ \\href{{mailto:{d.get('email', '')}}}{{{d.get('email', '')}}} $|$ 
    \\href{{{d.get('linkedin', '')}}}{{LinkedIn}} $|$
    \\href{{{d.get('github', '')}}}{{GitHub}}
\\end{{center}}

%-----------SUMMARY-----------
\\section{{Professional Summary}}
\\small{{{d.get('summary', '')}}}

%-----------SKILLS-----------
\\section{{Technical Skills}}
 \\begin{{itemize}}[leftmargin=0.15in, label={{}}]
    \\small{{\\item{{
     \\textbf{{Skills:}} {{{d.get('skills', '')}}}
    }}}}
 \\end{{itemize}}

%-----------EXPERIENCE-----------
\\section{{Experience}}
  \\resumeSubHeadingListStart
{exp_code}
  \\resumeSubHeadingListEnd

%-----------PROJECTS-----------
\\section{{Projects}}
  \\resumeSubHeadingListStart
{proj_code}
  \\resumeSubHeadingListEnd

%-----------EDUCATION-----------
\\section{{Education}}
  \\resumeSubHeadingListStart
{edu_code}
  \\resumeSubHeadingListEnd

\\end{{document}}
"""


# ==========================================
# 2. MODERN TECH DEVELOPER - WITH PROFILE PHOTO
# ==========================================
def template_modern_tech_photo(d: Dict[str, Any]) -> str:
    exp_code = ""
    for exp in d.get("experience", []):
        bullets = "\n".join([f"    \\item \\small{{{b}}}" for b in exp.get("bullets", [])])
        exp_code += f"""
\\noindent \\textbf{{{exp.get('title', '')}}} \\hfill \\textbf{{{exp.get('dates', '')}}}\\\\
\\textit{{{exp.get('company', '')} --- {exp.get('location', '')}}}\\\\
\\begin{{itemize}}[leftmargin=1.2em, topsep=2pt, itemsep=2pt]
{bullets}
\\end{{itemize}}
\\vspace{{4pt}}
"""

    proj_code = ""
    for proj in d.get("projects", []):
        proj_code += f"""
\\noindent \\textbf{{{proj.get('name', '')}}} $|$ \\textit{{{proj.get('tech', '')}}}\\\\
\\small{{{proj.get('description', '')}}}\\\\
\\vspace{{3pt}}
"""

    photo_cmd = ""
    if d.get("photo_filename"):
        photo_cmd = f"\\includegraphics[width=2.5cm,height=2.5cm,keepaspectratio]{{{d.get('photo_filename')}}}"
    else:
        photo_cmd = "% [Candidate Photo Placeholder]\n\\framebox[2.5cm]{\\rule{0pt}{2.5cm}\\small Photo}"

    return f"""\\documentclass[11pt,a4paper]{{article}}
\\usepackage[utf8]{{utf8}}
\\usepackage[margin=0.6in]{{geometry}}
\\usepackage{{enumitem}}
\\usepackage{{hyperref}}
\\usepackage{{xcolor}}
\\usepackage{{graphicx}}
\\usepackage{{tabularx}}

\\definecolor{{accentcolor}}{{HTML}}{{1E3A8A}}

\\hypersetup{{colorlinks=true, linkcolor=accentcolor, urlcolor=accentcolor}}
\\urlstyle{{same}}

\\begin{{document}}

\\begin{{center}}
\\begin{{tabularx}}{{\\textwidth}}{{@{{}}X c@{{}}}}
\\begin{{minipage}}[t]{{0.75\\textwidth}}
    {{\\Huge \\textbf{{\\color{{accentcolor}}{d.get('full_name', '')}}}}}\\\\ \\vspace{{3pt}}
    {{\\large \\textit{{{d.get('target_role', '')}}}}}\\\\ \\vspace{{4pt}}
    \\small {d.get('email', '')} $\\cdot$ {d.get('phone', '')} $\\cdot$ {d.get('location', '')}\\\\
    \\small \\href{{{d.get('linkedin', '')}}}{{LinkedIn}} $\\cdot$ \\href{{{d.get('github', '')}}}{{GitHub}}
\\end{{minipage}} &
\\begin{{minipage}}[t]{{0.22\\textwidth}}
    \\raggedleft
    {photo_cmd}
\\end{{minipage}}
\\end{{tabularx}}
\\end{{center}}

\\vspace{{-6pt}}
\\color{{accentcolor}}\\hrule height 1.2pt \\color{{black}}
\\vspace{{6pt}}

\\section*{{\\color{{accentcolor}}Technical Stack}}
\\textbf{{Core Skills:}} {d.get('skills', '')}

\\section*{{\\color{{accentcolor}}Professional Experience}}
{exp_code}

\\section*{{\\color{{accentcolor}}Key Engineering Projects}}
{proj_code}

\\section*{{\\color{{accentcolor}}Education}}
""" + "\n".join([f"\\noindent \\textbf{{{edu.get('degree', '')}}} \\hfill {edu.get('dates', '')}\\\\ \\textit{{{edu.get('institution', '')}}} (GPA: {edu.get('gpa', '')})\\\\" for edu in d.get("education", [])]) + """

\\end{{document}}
"""


# ==========================================
# 3. EXECUTIVE & SENIOR LEADERSHIP - NO PHOTO
# ==========================================
def template_executive(d: Dict[str, Any]) -> str:
    exp_code = ""
    for exp in d.get("experience", []):
        bullets = "\n".join([f"  \\item {b}" for b in exp.get("bullets", [])])
        exp_code += f"""
\\subsection*{{{exp.get('title', '')} --- \\textit{{{exp.get('company', '')}}}}}
\\textbf{{{exp.get('dates', '')}}} $|$ {exp.get('location', '')}
\\begin{{itemize}}[leftmargin=1.5em]
{bullets}
\\end{{itemize}}
"""

    return f"""\\documentclass[11pt]{{article}}
\\usepackage[margin=0.75in]{{geometry}}
\\usepackage{{titlesec}}
\\usepackage{{enumitem}}
\\usepackage{{hyperref}}

\\titleformat{{\\section}}{{\\Large\\bfseries\\scshape}}{{}}{{0pt}}{{}}
\\titleformat{{\\subsection}}{{\\large\\bfseries}}{{}}{{0pt}}{{}}

\\begin{{document}}

\\begin{{center}}
    {{\\Huge \\textbf{{{d.get('full_name', '')}}}}}\\\\ \\vspace{{4pt}}
    {{\\Large \\textbf{{{d.get('target_role', '')}}}}}\\\\ \\vspace{{6pt}}
    \\small {d.get('email', '')} $|$ {d.get('phone', '')} $|$ {d.get('location', '')}\\\\
    \\small \\url{{{d.get('linkedin', '')}}}
\\end{{center}}

\\hrule
\\vspace{{10pt}}

\\section*{{Executive Profile}}
{d.get('summary', '')}

\\section*{{Leadership \\& Core Competencies}}
{d.get('skills', '')}

\\section*{{Professional Career History}}
{exp_code}

\\section*{{Education \\& Credentials}}
""" + "\n".join([f"\\textbf{{{edu.get('degree', '')}}}, {edu.get('institution', '')} ({edu.get('dates', '')})\\\\" for edu in d.get("education", [])]) + """

\\end{{document}}
"""


# ==========================================
# 4. DATA SCIENCE & AI SPECIALIST - WITH PROFILE PHOTO
# ==========================================
def template_data_science_photo(d: Dict[str, Any]) -> str:
    exp_code = ""
    for exp in d.get("experience", []):
        bullets = "\n".join([f"  \\item {b}" for b in exp.get("bullets", [])])
        exp_code += f"""
\\textbf{{{exp.get('title', '')}}} \\hfill \\textbf{{{exp.get('dates', '')}}}\\\\
\\textit{{{exp.get('company', '')}}} --- \\small{{{exp.get('location', '')}}}
\\begin{{itemize}}[leftmargin=1.2em, itemsep=1pt]
{bullets}
\\end{{itemize}}
\\vspace{{3pt}}
"""

    proj_code = ""
    for proj in d.get("projects", []):
        proj_code += f"""
\\textbf{{{proj.get('name', '')}}} [\\textit{{{proj.get('tech', '')}}}]\\\\
\\small{{{proj.get('description', '')}}}\\\\
\\vspace{{2pt}}
"""

    photo_cmd = ""
    if d.get("photo_filename"):
        photo_cmd = f"\\includegraphics[width=2.4cm,height=2.4cm,keepaspectratio]{{{d.get('photo_filename')}}}"
    else:
        photo_cmd = "% [Candidate Photo Placeholder]\n\\framebox[2.4cm]{\\rule{0pt}{2.4cm}\\small Photo}"

    return f"""\\documentclass[10pt,a4paper]{{article}}
\\usepackage[margin=0.6in]{{geometry}}
\\usepackage{{enumitem}}
\\usepackage{{hyperref}}
\\usepackage{{xcolor}}
\\usepackage{{graphicx}}
\\usepackage{{tabularx}}

\\definecolor{{darkteal}}{{HTML}}{{0D9488}}

\\begin{{document}}

\\begin{{center}}
\\begin{{tabularx}}{{\\textwidth}}{{@{{}}X c@{{}}}}
\\begin{{minipage}}[t]{{0.75\\textwidth}}
    {{\\Huge \\textbf{{\\color{{darkteal}}{d.get('full_name', '')}}}}}\\\\ \\vspace{{2pt}}
    {{\\large \\textbf{{{d.get('target_role', '')}}}}}\\\\ \\vspace{{3pt}}
    \\small Contact: {d.get('email', '')} $|$ {d.get('phone', '')} $|$ GitHub: \\url{{{d.get('github', '')}}}
\\end{{minipage}} &
\\begin{{minipage}}[t]{{0.22\\textwidth}}
    \\raggedleft
    {photo_cmd}
\\end{{minipage}}
\\end{{tabularx}}
\\end{{center}}

\\vspace{{-4pt}}
\\color{{darkteal}}\\hrule height 1pt \\color{{black}}
\\vspace{{6pt}}

\\section*{{\\color{{darkteal}}Summary}}
\\small{{{d.get('summary', '')}}}

\\section*{{\\color{{darkteal}}Technical \\& AI Stack}}
\\textbf{{Machine Learning, Tools \\& Frameworks:}} {d.get('skills', '')}

\\section*{{\\color{{darkteal}}Work Experience}}
{exp_code}

\\section*{{\\color{{darkteal}}AI \\& Data Science Projects}}
{proj_code}

\\section*{{\\color{{darkteal}}Education}}
""" + "\n".join([f"\\textbf{{{edu.get('degree', '')}}} \\hfill {edu.get('dates', '')}\\\\ \\textit{{{edu.get('institution', '')}}}\\\\" for edu in d.get("education", [])]) + """

\\end{{document}}
"""


# ==========================================
# 5. MINIMALIST CLEAN PROFESSIONAL - NO PHOTO
# ==========================================
def template_minimalist(d: Dict[str, Any]) -> str:
    exp_code = ""
    for exp in d.get("experience", []):
        bullets = "\n".join([f"  \\item {b}" for b in exp.get("bullets", [])])
        exp_code += f"""
\\noindent \\textbf{{{exp.get('title', '')}}}, \\textit{{{exp.get('company', '')}}} \\hfill \\small{{{exp.get('dates', '')}}}
\\begin{{itemize}}[leftmargin=1.0em, itemsep=1pt]
{bullets}
\\end{{itemize}}
\\vspace{{2pt}}
"""

    return f"""\\documentclass[10pt]{{article}}
\\usepackage[margin=0.5in]{{geometry}}
\\usepackage{{enumitem}}
\\usepackage{{hyperref}}

\\begin{{document}}

\\begin{{center}}
    {{\\LARGE \\textbf{{{d.get('full_name', '')}}}}}\\\\ \\vspace{{2pt}}
    \\small {d.get('target_role', '')} $\\cdot$ {d.get('email', '')} $\\cdot$ {d.get('phone', '')} $\\cdot$ {d.get('location', '')}
\\end{{center}}

\\vspace{{-8pt}}
\\hrule
\\vspace{{6pt}}

\\noindent \\textbf{{SKILLS:}} {d.get('skills', '')}

\\vspace{{6pt}}
\\noindent \\textbf{{EXPERIENCE}}
{exp_code}

\\vspace{{4pt}}
\\noindent \\textbf{{PROJECTS}}
""" + "\n".join([f"\\noindent \\textbf{{{p.get('name', '')}}} ({p.get('tech', '')}): {p.get('description', '')}\\\\" for p in d.get("projects", [])]) + """

\\vspace{{4pt}}
\\noindent \\textbf{{EDUCATION}}
""" + "\n".join([f"\\noindent \\textbf{{{edu.get('degree', '')}}}, {edu.get('institution', '')} \\hfill {edu.get('dates', '')}\\\\" for edu in d.get("education", [])]) + """

\\end{{document}}
"""


# ==========================================
# 6. ACADEMIC & RESEARCH CV - NO PHOTO
# ==========================================
def template_academic(d: Dict[str, Any]) -> str:
    exp_code = ""
    for exp in d.get("experience", []):
        bullets = "\n".join([f"  \\item {b}" for b in exp.get("bullets", [])])
        exp_code += f"""
\\subsection*{{{exp.get('title', '')} --- \\textit{{{exp.get('company', '')}}}}}
\\textbf{{{exp.get('dates', '')}}} \\hfill {exp.get('location', '')}
\\begin{{itemize}}[leftmargin=1.2em]
{bullets}
\\end{{itemize}}
"""

    return f"""\\documentclass[11pt]{{article}}
\\usepackage[margin=0.7in]{{geometry}}
\\usepackage{{enumitem}}
\\usepackage{{hyperref}}

\\begin{{document}}

\\begin{{center}}
    {{\\Huge \\textbf{{{d.get('full_name', '')}}}}}\\\\ \\vspace{{4pt}}
    \\textit{{Curriculum Vitae}}\\\\ \\vspace{{4pt}}
    \\small {d.get('email', '')} $|$ {d.get('phone', '')} $|$ {d.get('location', '')}\\\\
    \\small \\url{{{d.get('linkedin', '')}}} $|$ \\url{{{d.get('github', '')}}}
\\end{{center}}

\\hrule
\\vspace{{8pt}}

\\section*{{Research Summary \\& Objective}}
{d.get('summary', '')}

\\section*{{Education}}
""" + "\n".join([f"\\textbf{{{edu.get('degree', '')}}} \\hfill {edu.get('dates', '')}\\\\ \\textit{{{edu.get('institution', '')}}} (GPA: {edu.get('gpa', '')})\\\\" for edu in d.get("education", [])]) + """

\\section*{{Technical Expertise}}
{d.get('skills', '')}

\\section*{{Research \\& Industry Experience}}
{exp_code}

\\section*{{Selected Projects \\& Publications}}
""" + "\n".join([f"\\textbf{{{p.get('name', '')}}} ({p.get('tech', '')})\\\\ \\small{{{p.get('description', '')}}}\\\\" for p in d.get("projects", [])]) + """

\\end{{document}}
"""


TEMPLATES = {
    "1": ("Classic ATS Standard (Jake's Resume) — [No Photo, 100% ATS Compliant]", template_classic_ats),
    "2": ("Modern Tech & Developer — [With Profile Photo]", template_modern_tech_photo),
    "3": ("Executive & Senior Leadership — [No Photo]", template_executive),
    "4": ("Data Science & AI Specialist — [With Profile Photo]", template_data_science_photo),
    "5": ("Minimalist Clean Professional — [No Photo]", template_minimalist),
    "6": ("Academic & Research CV — [No Photo]", template_academic),
}


def render_latex(template_key: str, user_data: Dict[str, Any]) -> str:
    """Renders the selected LaTeX template with escaped user profile data."""
    cleaned_data = clean_dict_for_latex(user_data)
    if template_key in TEMPLATES:
        return TEMPLATES[template_key][1](cleaned_data)
    return TEMPLATES["1"][1](cleaned_data)

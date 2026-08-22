"""
NY DataMind — Single-Page Animated ATS Resume & Career Suite
Developed by Nitin Yadav
100% Native Python — NO API REQUIRED
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import json
import os

from ats_engine import (
    evaluate_ats_score, DOMAIN_TAXONOMY
)
from parser import parse_resume_file, extract_structured_resume_data
from pdf_generator import generate_ats_report_pdf

# Page Configuration
st.set_page_config(
    page_title="NY DataMind — ATS Resume & Career Suite",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom Glassmorphism Theme & Fluid CSS Animations
st.markdown("""
<style>
    /* Hide Default Streamlit Branding & Menus */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stDeployButton {display:none;}
    
    /* Main Background */
    .stApp {
        background-color: #0F172A;
        color: #F8FAFC;
    }

    /* CSS Keyframe Animations */
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(12px); }
        to { opacity: 1; transform: translateY(0); }
    }

    @keyframes pulseGlow {
        0% { box-shadow: 0 0 10px rgba(59, 130, 246, 0.2); }
        50% { box-shadow: 0 0 25px rgba(59, 130, 246, 0.5); }
        100% { box-shadow: 0 0 10px rgba(59, 130, 246, 0.2); }
    }

    .animated-card {
        animation: fadeIn 0.6s cubic-bezier(0.16, 1, 0.3, 1) forwards;
    }

    .app-title {
        background: linear-gradient(135deg, #3B82F6 0%, #8B5CF6 50%, #EC4899 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 2.6rem;
        font-weight: 800;
        margin: 0;
    }

    .developer-badge {
        color: #94A3B8;
        font-size: 0.95rem;
        font-weight: 600;
    }
    
    .developer-badge span {
        color: #60A5FA;
        font-weight: 700;
    }

    .metric-card {
        background: rgba(15, 23, 42, 0.7);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 12px;
        padding: 1.1rem;
        text-align: center;
        transition: transform 0.3s ease, border-color 0.3s ease;
    }

    .metric-card:hover {
        transform: translateY(-4px);
        border-color: rgba(59, 130, 246, 0.5);
    }
    
    .metric-val {
        font-size: 2rem;
        font-weight: 800;
        color: #60A5FA;
    }
    
    .metric-label {
        color: #94A3B8;
        font-size: 0.78rem;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }

    .score-badge-excellent {
        background-color: rgba(16, 185, 129, 0.2);
        color: #34D399;
        border: 1px solid #10B981;
        padding: 8px 18px;
        border-radius: 20px;
        font-weight: 700;
        display: inline-block;
        animation: pulseGlow 3s infinite;
    }
    
    .score-badge-good {
        background-color: rgba(59, 130, 246, 0.2);
        color: #60A5FA;
        border: 1px solid #3B82F6;
        padding: 8px 18px;
        border-radius: 20px;
        font-weight: 700;
        display: inline-block;
    }

    .score-badge-warning {
        background-color: rgba(245, 158, 11, 0.2);
        color: #FBBF24;
        border: 1px solid #F59E0B;
        padding: 8px 18px;
        border-radius: 20px;
        font-weight: 700;
        display: inline-block;
    }

    .score-badge-poor {
        background-color: rgba(239, 68, 68, 0.2);
        color: #F87171;
        border: 1px solid #EF4444;
        padding: 8px 18px;
        border-radius: 20px;
        font-weight: 700;
        display: inline-block;
    }

    .skill-tag-match {
        display: inline-block;
        background: rgba(16, 185, 129, 0.15);
        color: #34D399;
        border: 1px solid rgba(16, 185, 129, 0.3);
        padding: 4px 10px;
        border-radius: 6px;
        margin: 3px;
        font-size: 0.85rem;
    }

    .skill-tag-missing {
        display: inline-block;
        background: rgba(239, 68, 68, 0.15);
        color: #F87171;
        border: 1px solid rgba(239, 68, 68, 0.3);
        padding: 4px 10px;
        border-radius: 6px;
        margin: 3px;
        font-size: 0.85rem;
        transition: transform 0.2s ease;
    }

    .skill-tag-match:hover, .skill-tag-missing:hover {
        transform: scale(1.08);
    }

    /* Smooth Global Transitions */
    * {
        transition: background-color 0.25s ease, border-color 0.25s ease, box-shadow 0.25s ease;
    }

    @keyframes slideDown {
        from { opacity: 0; transform: translateY(-10px); }
        to { opacity: 1; transform: translateY(0); }
    }

    .app-title {
        animation: slideDown 0.7s cubic-bezier(0.16, 1, 0.3, 1);
    }

    .developer-badge {
        animation: fadeIn 0.9s cubic-bezier(0.16, 1, 0.3, 1);
    }

    /* Domain Selector Card Wrapper */
    .domain-selector-wrap {
        animation: fadeIn 0.6s cubic-bezier(0.16, 1, 0.3, 1);
    }

    div[data-baseweb="select"] > div {
        border-radius: 10px !important;
        transition: box-shadow 0.3s ease, border-color 0.3s ease !important;
    }

    div[data-baseweb="select"] > div:hover {
        border-color: rgba(59, 130, 246, 0.6) !important;
        box-shadow: 0 0 14px rgba(59, 130, 246, 0.25) !important;
    }

    .stButton > button, .stDownloadButton > button {
        border-radius: 10px !important;
        transition: transform 0.25s cubic-bezier(0.16, 1, 0.3, 1), box-shadow 0.25s ease !important;
    }

    .stButton > button:hover, .stDownloadButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 20px rgba(59, 130, 246, 0.3);
    }

    /* Primary Analyze Button — Blue/Purple Gradient */
    .stButton > button[kind="primary"] {
        background: linear-gradient(135deg, #3B82F6 0%, #8B5CF6 100%) !important;
        border: none !important;
        color: #FFFFFF !important;
        font-weight: 700 !important;
    }

    .stButton > button[kind="primary"]:hover {
        background: linear-gradient(135deg, #2563EB 0%, #7C3AED 100%) !important;
        box-shadow: 0 10px 24px rgba(139, 92, 246, 0.4) !important;
    }

    /* Download Report Button — Emerald/Teal Gradient */
    .stDownloadButton > button[kind="primary"] {
        background: linear-gradient(135deg, #10B981 0%, #0D9488 100%) !important;
        border: none !important;
        color: #FFFFFF !important;
        font-weight: 700 !important;
        letter-spacing: 0.02em;
    }

    .stDownloadButton > button[kind="primary"]:hover {
        background: linear-gradient(135deg, #059669 0%, #0F766E 100%) !important;
        box-shadow: 0 10px 24px rgba(16, 185, 129, 0.45) !important;
    }

    .stProgress > div > div > div {
        transition: width 0.8s cubic-bezier(0.16, 1, 0.3, 1) !important;
    }
</style>
""", unsafe_allow_html=True)

# Initialize Session State
if "resume_text" not in st.session_state:
    st.session_state.resume_text = ""
if "domain_target" not in st.session_state:
    st.session_state.domain_target = "All Domains (General Tech Standard)"
if "parsed_data" not in st.session_state:
    st.session_state.parsed_data = extract_structured_resume_data("")

# HEADER WITH LOGO & DEVELOPER CREDIT
col_logo, col_head = st.columns([1, 4])
with col_logo:
    if os.path.exists("logo_decagon.png"):
        st.image("logo_decagon.png", width=150)
    elif os.path.exists("logo.jpg"):
        st.image("logo.jpg", width=150)
    else:
        st.markdown("## 🎯")

with col_head:
    st.markdown('<div class="app-title">NY DataMind — ATS Resume & Career Suite</div>', unsafe_allow_html=True)
    st.markdown('<div class="developer-badge">DATA | INSIGHTS | INTELLIGENCE &nbsp;•&nbsp; <span>Developed by Nitin Yadav</span></div>', unsafe_allow_html=True)

st.divider()

# ==============================================================================
# TOOLBAR: TARGET INDUSTRY DOMAIN SELECTOR (SEARCHABLE)
# ==============================================================================
st.markdown('<div class="domain-selector-wrap">', unsafe_allow_html=True)
st.session_state.domain_target = st.selectbox(
    "🎯 Target Industry Field — start typing to search:",
    options=list(DOMAIN_TAXONOMY.keys()),
    index=list(DOMAIN_TAXONOMY.keys()).index(st.session_state.domain_target) if st.session_state.domain_target in DOMAIN_TAXONOMY else 0
)
st.markdown('</div>', unsafe_allow_html=True)

# INPUT AREA: FILE UPLOAD OR TEXT PASTING
col_u1, col_u2 = st.columns([1, 1])
with col_u1:
    uploaded_file = st.file_uploader("Upload Resume File (PDF, DOCX, TXT)", type=["pdf", "docx", "txt"])
    if uploaded_file is not None:
        file_bytes = uploaded_file.read()
        extracted_text = parse_resume_file(file_bytes, uploaded_file.name)
        if extracted_text.strip():
            st.session_state.resume_text = extracted_text
            st.session_state.parsed_data = extract_structured_resume_data(extracted_text)
            st.success(f"Successfully extracted text from '{uploaded_file.name}'!")

with col_u2:
    resume_input = st.text_area(
        "Or Paste Resume Text Here:",
        value=st.session_state.resume_text,
        height=140,
        placeholder="Paste your full resume text here..."
    )
    st.session_state.resume_text = resume_input

# ANALYZE BUTTON
if st.button("🚀 Calculate High-Precision ATS Score", type="primary", use_container_width=True):
    if not st.session_state.resume_text.strip():
        st.warning("⚠️ Please upload or paste your resume text to calculate the ATS Score.")
    else:
        with st.spinner("Analyzing 200+ skill taxonomy, action verb density, impact metrics, and structural compliance..."):
            results = evaluate_ats_score(st.session_state.resume_text, st.session_state.domain_target)
            st.session_state.ats_results = results
            st.session_state.parsed_data = extract_structured_resume_data(st.session_state.resume_text)

# ==============================================================================
# SEAMLESS FLUID SINGLE-PAGE DASHBOARD
# ==============================================================================
if "ats_results" in st.session_state:
    res = st.session_state.ats_results
    score = res["overall_score"]

    st.divider()
    st.markdown('<div class="animated-card">', unsafe_allow_html=True)
    st.subheader(f"📊 5-Pillar High-Precision ATS Score ({st.session_state.domain_target})")

    # Score Gauge Header
    col_score, col_badge = st.columns([1, 2])
    with col_score:
        st.metric("Overall ATS Score", f"{score} / 100")
        st.progress(score / 100.0)
    with col_badge:
        if score >= 85:
            st.markdown('<br><span class="score-badge-excellent">🟢 EXCELLENT ATS SCORE — Ready for Top Recruiter Shortlist!</span>', unsafe_allow_html=True)
        elif score >= 70:
            st.markdown('<br><span class="score-badge-good">🔵 STRONG ATS SCORE — Passes standard automated ATS screeners.</span>', unsafe_allow_html=True)
        elif score >= 50:
            st.markdown('<br><span class="score-badge-warning">🟡 MODERATE ATS SCORE — Inject missing keywords below to reach 85+.</span>', unsafe_allow_html=True)
        else:
            st.markdown('<br><span class="score-badge-poor">🔴 POOR ATS SCORE — High rejection risk. Add missing skills below.</span>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # 5 Pillar Cards
    p1, p2, p3, p4, p5 = st.columns(5)
    with p1:
        st.markdown(f'<div class="metric-card"><div class="metric-val">{res["skills_score"]}/30</div><div class="metric-label">Technical Skills</div></div>', unsafe_allow_html=True)
    with p2:
        st.markdown(f'<div class="metric-card"><div class="metric-val">{res["verbs_score"]}/25</div><div class="metric-label">Action Verbs</div></div>', unsafe_allow_html=True)
    with p3:
        st.markdown(f'<div class="metric-card"><div class="metric-val">{res["metrics_score"]}/20</div><div class="metric-label">Impact Metrics</div></div>', unsafe_allow_html=True)
    with p4:
        st.markdown(f'<div class="metric-card"><div class="metric-val">{res["section_score"]}/15</div><div class="metric-label">ATS Sections</div></div>', unsafe_allow_html=True)
    with p5:
        st.markdown(f'<div class="metric-card"><div class="metric-val">{res["readability_score"]}/10</div><div class="metric-label">Readability</div></div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # PLOTLY 5-PILLAR SCORE RADAR CHART & SKILL GAP
    col_chart, col_sk = st.columns([1, 1])
    with col_chart:
        st.markdown("### 🕸️ 5-Pillar Score Radar Chart")
        categories = ['Technical Skills', 'Action Verbs', 'Impact Metrics', 'Section Structure', 'Readability']
        values = [
            (res['skills_score'] / 30.0) * 100,
            (res['verbs_score'] / 25.0) * 100,
            (res['metrics_score'] / 20.0) * 100,
            (res['section_score'] / 15.0) * 100,
            (res['readability_score'] / 10.0) * 100
        ]
        
        fig = go.Figure()
        fig.add_trace(go.Scatterpolar(
            r=values + [values[0]],
            theta=categories + [categories[0]],
            fill='toself',
            name='Candidate Profile',
            line_color='#3B82F6',
            fillcolor='rgba(59, 130, 246, 0.25)'
        ))
        fig.add_trace(go.Scatterpolar(
            r=[90, 85, 80, 100, 90, 90],
            theta=categories + [categories[0]],
            name='Target Benchmark',
            line_color='#10B981',
            line_dash='dash'
        ))
        fig.update_layout(
            polar=dict(
                radialaxis=dict(visible=True, range=[0, 100], color="#94A3B8"),
                bgcolor="rgba(15, 23, 42, 0.6)"
            ),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#F8FAFC"),
            margin=dict(l=40, r=40, t=20, b=20),
            height=320
        )
        st.plotly_chart(fig, use_container_width=True)

    with col_sk:
        st.markdown(f"### 🛠️ {st.session_state.domain_target} Skill Gap")
        st.write("**Detected Skills:**")
        if res["hard_skills_matched"]:
            tags_html = "".join([f'<span class="skill-tag-match">✓ {s}</span>' for s in res["hard_skills_matched"]])
            st.markdown(tags_html, unsafe_allow_html=True)
        else:
            st.info("No technical skills detected.")

        st.write("<br>**Recommended Missing Keywords:**", unsafe_allow_html=True)
        if res["hard_skills_missing"]:
            tags_html = "".join([f'<span class="skill-tag-missing">✗ {s}</span>' for s in res["hard_skills_missing"]])
            st.markdown(tags_html, unsafe_allow_html=True)
        else:
            st.success("All technical skills present!")

    st.markdown('</div>', unsafe_allow_html=True)

    # ==============================================================================
    # EXPORT ATS SCORE REPORT — recruiter-facing PDF (score report only, not the resume)
    # ==============================================================================
    st.markdown("<br>", unsafe_allow_html=True)
    st.divider()
    st.markdown('<div class="export-report-wrap">', unsafe_allow_html=True)
    st.markdown(
        '<div style="text-align:center; margin-bottom: 0.6rem;">'
        '<span style="color:#94A3B8; font-size:0.9rem;">Share a clean, recruiter-friendly summary of this score — no resume content included.</span>'
        '</div>', unsafe_allow_html=True
    )
    report_pdf_bytes = generate_ats_report_pdf(
        res, st.session_state.domain_target,
        candidate=st.session_state.parsed_data
    )
    col_dl1, col_dl2, col_dl3 = st.columns([1, 2, 1])
    with col_dl2:
        st.download_button(
            label="📄 Download ATS Score Report (PDF)",
            data=report_pdf_bytes,
            file_name="ATS_Score_Report.pdf",
            mime="application/pdf",
            use_container_width=True,
            type="primary"
        )
    st.markdown('</div>', unsafe_allow_html=True)

# (Footer credit intentionally removed per user preference)

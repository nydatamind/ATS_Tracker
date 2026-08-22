# 🎯 ATS Resume Score Predictor & 6 LaTeX Resume Builder

A high-precision **Applicant Tracking System (ATS) Resume Score Predictor** and **6-Template LaTeX Resume Builder** built with Python and Streamlit.

---

## 🔥 Features

- 🎯 **100% Precision ATS Match Scoring**: Uses TF-IDF cosine similarity, skill taxonomy matching, action verb frequency, and quantified metrics audit.
- 📱 **2-Step Streamlined User Interface**:
  - **Step 1**: Upload Resume (PDF, DOCX, TXT) + Job Description -> Calculates high-precision ATS score, skill gaps, and recommendations.
  - **Step 2**: Auto-extracted fields editor with **1-Click Keyword Booster**, **Profile Photo upload**, and **6 LaTeX Templates** (With Photo & Without Photo options).
- 🖼️ **Photo & Non-Photo LaTeX Templates**:
  1. `Classic ATS Standard (Jake's Resume)` — [No Photo, 100% ATS Compliant]
  2. `Modern Tech & Developer` — [With Profile Photo]
  3. `Executive Leadership` — [No Photo]
  4. `Data Science & AI Specialist` — [With Profile Photo]
  5. `Minimalist Clean Professional` — [No Photo]
  6. `Academic & Research CV` — [No Photo]
- ⚡ **1-Click Keyword Booster**: Dynamically injects missing JD keywords into skills to increase ATS match score live.
- 📥 **1-Click LaTeX Export**: Download `.tex` files or copy source code for Overleaf.com.
- 🚀 **1-Click Streamlit Community Cloud Deployment**: Native Python application ready for direct GitHub-to-Streamlit deployment.

---

## 🛠️ Local Installation & Running

```bash
# 1. Clone repository
git clone <your-github-repo-url>
cd SusheelTEDS

# 2. Install Python dependencies
pip install -r requirements.txt

# 3. Launch Streamlit server
python -m streamlit run app.py
```

---

## 🚀 How to Deploy on Streamlit Community Cloud

1. Commit and push this directory to your **GitHub** account (`git push origin main`).
2. Go to **[share.streamlit.io](https://share.streamlit.io)** and log in with your GitHub account.
3. Click **"New App"**.
4. Select your repository, set branch to `main`, and main file path to `app.py`.
5. Click **Deploy!** Your app will be live with a free HTTPS URL.

"""
ATS Scoring Engine & Career Intelligence Module — NY DataMind
100% Native Python — NO API REQUIRED
Evaluates 5-pillar ATS scores, 100-domain taxonomies, random sample resumes pool,
native bullet enhancers, matching cover letters, LinkedIn profiles, interview Q&A prep, and salary estimators.
"""

import re
import math
import random
from typing import Dict, Any, List, Tuple

# Expanded 100 Domain Priority Pools
DOMAIN_TAXONOMY = {
    "All Domains (General Tech Standard)": ["python", "sql", "react", "docker", "aws", "git", "rest api", "ci/cd", "postgresql", "agile", "kubernetes", "system design", "pandas"],
    "Data Analytics & Business Intelligence": ["sql", "python", "power bi", "tableau", "excel", "postgresql", "bigquery", "snowflake", "data analysis", "data modeling", "statistics", "r", "etl"],
    "Software & Full Stack Web Development": ["javascript", "typescript", "python", "react", "node.js", "java", "c++", "c#", "html", "css", "docker", "postgresql", "git", "rest api", "microservices"],
    "Cloud Engineering & DevOps": ["aws", "azure", "gcp", "docker", "kubernetes", "terraform", "ansible", "jenkins", "github actions", "ci/cd", "linux", "bash", "python", "system design"],
    "AI, Machine Learning & Data Science": ["python", "machine learning", "deep learning", "nlp", "tensorflow", "pytorch", "scikit-learn", "pandas", "numpy", "spacy", "huggingface", "llm", "genai", "sql"],
    "Cybersecurity & Network Security": ["cybersecurity", "network security", "python", "bash", "linux", "siem", "firewall", "wireshark", "penetration testing", "cissp", "cryptography", "incident response"],
    "Mobile App Development (iOS / Android)": ["react native", "swift", "kotlin", "flutter", "ios", "android", "javascript", "typescript", "rest api", "xcode", "mobile app", "git"],
    "Product & Project Management": ["agile", "scrum", "kanban", "jira", "confluence", "product management", "leadership", "stakeholder management", "strategic planning", "user research", "roadmapping"],
    "UI/UX Design & Frontend Engineering": ["javascript", "typescript", "react", "html", "css", "tailwindcss", "bootstrap", "figma", "ui/ux", "responsive design", "web design", "frontend"],
    "Finance, Accounting & Quant Tech": ["excel", "sql", "python", "financial modeling", "financial analysis", "accounting", "risk management", "r", "statistics", "forecasting", "data analysis"],
    "Healthcare & Bioinformatics Tech": ["python", "r", "bioinformatics", "data analysis", "sql", "machine learning", "statistics", "hipaa", "genomics", "clinical data"],
    "Sales, Marketing & Growth Tech": ["seo", "google analytics", "hubspot", "crm", "digital marketing", "data analysis", "content strategy", "salesforce", "lead generation", "growth marketing"],
    "Backend Engineering & API Development": ["python", "java", "node.js", "rest api", "graphql", "microservices", "postgresql", "mongodb", "redis", "docker", "system design", "unit testing"],
    "Data Engineering & Big Data": ["python", "sql", "spark", "pyspark", "hadoop", "airflow", "etl", "kafka", "snowflake", "bigquery", "data pipelines", "aws"],
    "Data Science & Predictive Analytics": ["python", "r", "machine learning", "statistics", "pandas", "numpy", "scikit-learn", "sql", "data visualization", "hypothesis testing", "predictive modeling"],
    "Natural Language Processing & LLM Engineering": ["python", "nlp", "llm", "transformers", "huggingface", "spacy", "langchain", "prompt engineering", "genai", "pytorch", "vector databases", "rag"],
    "Computer Vision & Image Processing": ["python", "opencv", "computer vision", "pytorch", "tensorflow", "image processing", "deep learning", "cnn", "yolo", "object detection"],
    "MLOps & AI Infrastructure": ["mlops", "docker", "kubernetes", "mlflow", "airflow", "aws sagemaker", "ci/cd", "python", "model deployment", "monitoring", "feature store"],
    "Site Reliability Engineering (SRE)": ["linux", "kubernetes", "terraform", "prometheus", "grafana", "python", "bash", "incident response", "monitoring", "aws", "system design", "on-call"],
    "Platform Engineering": ["kubernetes", "docker", "terraform", "aws", "ci/cd", "internal developer platform", "golang", "python", "infrastructure as code", "observability"],
    "Blockchain & Web3 Development": ["solidity", "ethereum", "web3.js", "smart contracts", "blockchain", "rust", "cryptography", "defi", "nft", "hardhat"],
    "Game Development": ["unity", "unreal engine", "c#", "c++", "game design", "3d modeling", "physics engine", "opengl", "directx", "multiplayer networking"],
    "Embedded Systems & IoT": ["c", "c++", "embedded systems", "rtos", "microcontrollers", "arduino", "raspberry pi", "iot", "firmware", "uart", "spi", "i2c"],
    "Robotics Engineering": ["ros", "python", "c++", "robotics", "control systems", "kinematics", "slam", "sensor fusion", "embedded systems", "matlab"],
    "Quality Assurance & Test Automation": ["selenium", "test automation", "python", "java", "cypress", "junit", "test cases", "regression testing", "qa", "jira", "ci/cd"],
    "Database Administration": ["sql", "postgresql", "mysql", "oracle", "database tuning", "backup and recovery", "replication", "database security", "indexing", "nosql"],
    "Network Engineering": ["cisco", "networking", "tcp/ip", "routing and switching", "firewall", "vpn", "ccna", "network security", "dns", "load balancing"],
    "IT Support & Systems Administration": ["windows server", "active directory", "linux", "troubleshooting", "help desk", "itil", "networking", "powershell", "office 365", "system administration"],
    "Enterprise Architecture": ["enterprise architecture", "togaf", "system design", "cloud strategy", "integration", "business process modeling", "stakeholder management", "governance"],
    "Solutions Architecture": ["aws", "azure", "system design", "microservices", "api design", "cloud architecture", "integration patterns", "scalability", "security architecture"],
    "Technical Writing & Documentation": ["technical writing", "documentation", "markdown", "api documentation", "confluence", "editing", "content management", "user guides", "developer docs"],
    "Digital Marketing & SEO": ["seo", "sem", "google analytics", "google ads", "content marketing", "keyword research", "digital marketing", "ppc", "conversion optimization"],
    "Content Strategy & Copywriting": ["content strategy", "copywriting", "seo writing", "editorial calendar", "brand voice", "content marketing", "proofreading", "storytelling"],
    "Social Media Marketing": ["social media marketing", "content creation", "instagram", "facebook ads", "community management", "analytics", "influencer marketing", "brand strategy"],
    "E-commerce & Retail Tech": ["shopify", "e-commerce", "magento", "inventory management", "payment gateways", "retail analytics", "supply chain", "crm", "merchandising"],
    "Supply Chain & Logistics Tech": ["supply chain management", "logistics", "inventory management", "sap", "erp", "procurement", "demand forecasting", "warehouse management"],
    "Human Resources & HR Tech": ["hris", "recruitment", "talent acquisition", "performance management", "workday", "payroll", "employee relations", "hr analytics", "onboarding"],
    "Legal Tech & Compliance": ["contract management", "legal research", "compliance", "regulatory affairs", "risk assessment", "legal writing", "gdpr", "corporate law"],
    "EdTech & Learning Design": ["instructional design", "lms", "curriculum development", "e-learning", "learning analytics", "content authoring", "assessment design"],
    "Insurance & Actuarial Tech": ["actuarial science", "underwriting", "risk assessment", "insurance claims", "statistics", "excel", "regulatory compliance", "pricing models"],
    "Real Estate & PropTech": ["real estate", "property management", "crm", "market analysis", "valuation", "mls", "leasing", "real estate law"],
    "Banking & Investment Technology": ["financial modeling", "banking operations", "risk management", "bloomberg terminal", "trading systems", "compliance", "kyc/aml", "investment analysis"],
    "Risk Management & Compliance": ["risk assessment", "regulatory compliance", "internal controls", "audit", "governance", "sox compliance", "enterprise risk management"],
    "Audit & Internal Controls": ["internal audit", "sox compliance", "financial reporting", "risk assessment", "gaap", "audit planning", "internal controls", "excel"],
    "Manufacturing & Industrial Engineering": ["lean manufacturing", "six sigma", "process improvement", "production planning", "quality control", "cad", "supply chain", "plc programming"],
    "Automotive Engineering": ["cad", "automotive systems", "vehicle dynamics", "matlab", "embedded systems", "cae", "quality standards", "product design"],
    "Aerospace Engineering": ["aerodynamics", "cad", "matlab", "structural analysis", "avionics", "systems engineering", "propulsion", "flight testing"],
    "Civil Engineering": ["autocad", "structural analysis", "civil 3d", "project management", "construction management", "surveying", "building codes", "geotechnical engineering"],
    "Mechanical Engineering": ["solidworks", "autocad", "cad", "finite element analysis", "thermodynamics", "product design", "manufacturing processes", "gd&t"],
    "Electrical Engineering": ["circuit design", "matlab", "pcb design", "power systems", "control systems", "embedded systems", "autocad electrical", "electrical testing"],
    "Chemical Engineering": ["process engineering", "chemical process design", "matlab", "process simulation", "aspen plus", "quality control", "safety compliance", "plant operations"],
    "Environmental Science & Sustainability": ["environmental compliance", "sustainability reporting", "gis", "environmental impact assessment", "esg", "data analysis", "regulatory compliance"],
    "Energy & Renewable Tech": ["renewable energy", "solar pv design", "energy analysis", "grid systems", "matlab", "sustainability", "project management", "energy efficiency"],
    "Telecommunications Engineering": ["telecommunications", "5g", "network protocols", "rf engineering", "signal processing", "fiber optics", "network design"],
    "Biotechnology & Life Sciences": ["biotechnology", "molecular biology", "lab techniques", "pcr", "cell culture", "research methodology", "data analysis", "genomics"],
    "Pharmaceutical R&D": ["drug development", "clinical research", "gmp", "regulatory affairs", "formulation", "pharmacology", "quality assurance", "fda regulations"],
    "Clinical Research & Trials": ["clinical trials", "gcp", "protocol development", "regulatory submissions", "clinical data management", "patient recruitment", "ich guidelines"],
    "Public Health & Epidemiology": ["epidemiology", "biostatistics", "public health policy", "data analysis", "program evaluation", "health surveillance", "sas", "spss"],
    "Nursing & Patient Care": ["patient care", "clinical documentation", "ehr systems", "nursing assessment", "medication administration", "patient safety", "hipaa compliance"],
    "Medical Devices Engineering": ["medical device design", "fda regulations", "iso 13485", "product development", "risk analysis", "biocompatibility", "cad", "quality systems"],
    "Agriculture & AgriTech": ["precision agriculture", "gis", "crop management", "agronomy", "data analysis", "farm management systems", "sustainability practices"],
    "Food Science & Technology": ["food safety", "haccp", "quality control", "product development", "food chemistry", "regulatory compliance", "sensory evaluation"],
    "Hospitality & Tourism Management": ["hospitality management", "customer service", "revenue management", "event planning", "property management systems", "guest relations"],
    "Event Management & Planning": ["event planning", "vendor management", "budget management", "logistics coordination", "project management", "stakeholder communication"],
    "Media & Entertainment Production": ["video production", "adobe premiere", "final cut pro", "content production", "project management", "post-production", "storytelling"],
    "Journalism & Broadcasting": ["journalism", "news writing", "editing", "investigative reporting", "broadcast production", "interviewing", "media law", "fact checking"],
    "Graphic Design & Visual Arts": ["adobe photoshop", "adobe illustrator", "graphic design", "typography", "branding", "layout design", "indesign", "visual communication"],
    "Animation & VFX": ["maya", "blender", "after effects", "3d animation", "vfx", "rigging", "motion graphics", "rendering"],
    "Photography & Videography": ["photography", "photo editing", "lightroom", "videography", "cinematography", "lighting techniques", "adobe premiere"],
    "Architecture & Urban Planning": ["autocad", "revit", "urban planning", "architectural design", "building codes", "sketchup", "sustainable design", "zoning regulations"],
    "Interior Design": ["interior design", "autocad", "sketchup", "space planning", "material selection", "3d rendering", "color theory"],
    "Fashion Design & Merchandising": ["fashion design", "adobe illustrator", "trend forecasting", "merchandising", "pattern making", "textile knowledge", "retail buying"],
    "Sports Management & Analytics": ["sports analytics", "data analysis", "athlete performance", "sports marketing", "event management", "statistics", "python"],
    "Nonprofit & NGO Management": ["grant writing", "fundraising", "program management", "nonprofit management", "donor relations", "volunteer coordination", "impact reporting"],
    "Public Policy & Government Affairs": ["policy analysis", "public administration", "legislative research", "stakeholder engagement", "government relations", "program evaluation"],
    "Diplomacy & International Relations": ["international relations", "diplomacy", "policy analysis", "negotiation", "foreign affairs", "cross-cultural communication"],
    "Education Administration": ["education administration", "curriculum development", "staff management", "budget management", "student affairs", "policy compliance"],
    "Library & Information Science": ["cataloging", "information retrieval", "digital archiving", "library management systems", "research assistance", "metadata management"],
    "Psychology & Counseling": ["counseling", "psychological assessment", "therapy techniques", "case management", "dsm-5", "patient confidentiality", "crisis intervention"],
    "Social Work": ["case management", "social work", "client advocacy", "crisis intervention", "community resources", "documentation", "counseling"],
    "Customer Success & Support": ["customer success", "crm", "zendesk", "customer retention", "account management", "onboarding", "salesforce", "communication skills"],
    "Business Development": ["business development", "lead generation", "partnership development", "sales strategy", "market research", "negotiation", "crm"],
    "Operations Management": ["operations management", "process improvement", "supply chain", "budget management", "kpi tracking", "project management", "erp systems"],
    "Strategy & Management Consulting": ["strategic planning", "management consulting", "market analysis", "business analysis", "financial modeling", "stakeholder management", "powerpoint"],
    "Investment Banking & Private Equity": ["financial modeling", "valuation", "m&a", "due diligence", "excel", "bloomberg terminal", "deal structuring", "private equity"],
    "Venture Capital & Startups": ["startup evaluation", "market research", "financial modeling", "due diligence", "pitch deck analysis", "networking", "term sheets"],
    "Economics & Financial Research": ["econometrics", "statistical analysis", "financial research", "stata", "r", "economic modeling", "data analysis"],
    "Actuarial Science": ["actuarial modeling", "statistics", "risk assessment", "excel", "sas", "probability theory", "exam fm", "exam p"],
    "Accounting & Bookkeeping": ["quickbooks", "accounts payable", "accounts receivable", "reconciliation", "gaap", "financial statements", "bookkeeping", "excel"],
    "Taxation & Corporate Finance": ["tax preparation", "corporate finance", "tax compliance", "financial analysis", "excel", "gaap", "tax planning"],
    "Procurement & Vendor Management": ["procurement", "vendor management", "contract negotiation", "supply chain", "cost analysis", "erp systems", "purchasing"],
    "Quality Control & Six Sigma": ["six sigma", "quality control", "process improvement", "root cause analysis", "statistical process control", "lean manufacturing"],
    "Construction Management": ["construction management", "project scheduling", "autocad", "budget management", "contract administration", "site supervision", "osha compliance"],
    "Facilities & Property Management": ["facilities management", "property management", "vendor coordination", "maintenance planning", "budget management", "lease administration"],
    "Transportation & Fleet Management": ["fleet management", "logistics", "route optimization", "dot compliance", "transportation management systems", "budget management"],
    "Marine & Naval Engineering": ["marine engineering", "naval architecture", "cad", "ship systems", "structural analysis", "propulsion systems"],
    "Mining & Metallurgy": ["mining engineering", "metallurgy", "mineral processing", "geology", "safety compliance", "autocad", "resource estimation"],
    "Textile Engineering": ["textile engineering", "fabric technology", "quality control", "production planning", "textile testing", "material science"],
    "Culinary Arts & Food Service": ["culinary arts", "menu development", "food safety", "kitchen management", "cost control", "haccp", "inventory management"],
    "General Business & Administrative Professional": ["microsoft office", "communication", "project coordination", "scheduling", "data entry", "customer service", "organization", "problem solving"],
}

# Master 200+ Skill Taxonomy
FULL_SKILL_TAXONOMY = {
    "Languages & Core Tech": [
        "python", "javascript", "typescript", "java", "c++", "c#", "go", "golang", "rust", "ruby",
        "php", "swift", "kotlin", "sql", "html", "html5", "css", "css3", "bash", "shell", "r", "scala"
    ],
    "Frameworks & Web": [
        "react", "react.js", "react native", "next.js", "vue", "vue.js", "angular", "node.js", "express",
        "express.js", "django", "flask", "fastapi", "spring", "spring boot", "asp.net", "laravel",
        "tailwindcss", "bootstrap", "graphql", "rest api", "restful api", "microservices", "web sockets"
    ],
    "Cloud, DevOps & Infrastructure": [
        "aws", "amazon web services", "azure", "gcp", "google cloud", "docker", "kubernetes", "k8s",
        "terraform", "ansible", "jenkins", "github actions", "ci/cd", "git", "github", "gitlab",
        "linux", "unix", "nginx", "apache", "system design", "distributed systems", "serverless"
    ],
    "Data Science, AI & Databases": [
        "postgresql", "postgres", "mysql", "mongodb", "redis", "elasticsearch", "sqlite", "oracle",
        "snowflake", "bigquery", "machine learning", "deep learning", "artificial intelligence", "nlp",
        "computer vision", "tensorflow", "pytorch", "scikit-learn", "sklearn", "pandas", "numpy",
        "spacy", "huggingface", "llm", "genai", "generative ai", "spark", "pyspark", "hadoop",
        "airflow", "power bi", "tableau", "excel", "data analysis", "data engineering", "etl"
    ],
    "Management & Methodologies": [
        "agile", "scrum", "kanban", "jira", "confluence", "project management", "product management",
        "leadership", "teamwork", "communication", "problem solving", "critical thinking",
        "stakeholder management", "cross-functional", "strategic planning", "mentorship"
    ]
}

ALL_TAXONOMY_SKILLS = [skill for cat in FULL_SKILL_TAXONOMY.values() for skill in cat]

POWER_ACTION_VERBS = [
    "accelerated", "achieved", "architected", "automated", "built", "spearheaded", "engineered",
    "optimized", "designed", "implemented", "developed", "increased", "reduced", "decreased",
    "streamlined", "delivered", "led", "managed", "created", "formulated", "transformed",
    "negotiated", "launched", "deployed", "scaled", "expanded", "generated", "pioneered",
    "improved", "overhauled", "mentored", "maximized", "minimized", "resolved", "executed"
]

REQUIRED_SECTIONS = {
    "Contact Information": [r"email", r"phone", r"linkedin", r"github", r"contact", r"location"],
    "Summary / Objective": [r"summary", r"profile", r"objective", r"about me"],
    "Work Experience": [r"experience", r"work history", r"employment", r"professional experience"],
    "Education": [r"education", r"academic", r"qualification", r"degree", r"university"],
    "Technical Skills": [r"skill", r"technologies", r"technical proficiency", r"competencies"],
    "Key Projects": [r"project", r"key projects", r"personal projects"]
}

# ==========================================
# RICH RANDOM SAMPLE RESUMES POOL (10 PROFILES)
# ==========================================
SAMPLE_RESUMES_POOL = [
    {
        "domain": "Data Analytics & Business Intelligence",
        "text": """Nitin Yadav
Senior Data Analyst
nitin.yadav@email.com | +1 (555) 019-2834 | New York, NY | linkedin.com/in/nitinyadav

Professional Summary:
Results-driven Data Analyst with 5+ years of experience transforming complex datasets into actionable business intelligence. Proficient in SQL, Python, Power BI, Tableau, PostgreSQL, and Snowflake. Demonstrated track record of optimizing ETL data pipelines and building executive analytics dashboards.

Technical Skills:
SQL, Python, Power BI, Tableau, PostgreSQL, Snowflake, Excel, Data Analysis, Data Modeling, R, ETL, Statistics

Work Experience:
Senior Data Analyst - DataMind Analytics (2022 - Present)
• Spearheaded automated ETL data pipelines in SQL and Python, reducing manual reporting overhead by 45%.
• Architected 15+ executive Power BI & Tableau dashboards monitoring $10M+ annual revenue KPIs.
• Optimized PostgreSQL query performance and data warehousing models, cutting query latency from 180s to 12s.

Data Analyst - Insight Tech Corp (2020 - 2022)
• Analyzed customer churn datasets using Python, Pandas, and R, identifying key churn drivers with 92% precision.
• Collaborated with cross-functional product teams to deliver weekly A/B test analytics reports.

Education:
B.S. in Data Analytics - State University (2016 - 2020) (GPA: 3.8 / 4.0)

Projects:
Cloud Data Warehouse & BI Dashboard [SQL, Snowflake, Power BI]
• Designed end-to-end cloud data warehouse architecture integrating sales streams with real-time BI reports."""
    },
    {
        "domain": "Software & Full Stack Web Development",
        "text": """Alex Morgan
Senior Full Stack Developer
alex.morgan@email.com | +1 (555) 234-5678 | San Francisco, CA | linkedin.com/in/alexmorgan

Professional Summary:
High-performance Software Developer with 6+ years of expertise building scalable cloud applications, microservices, and web platforms. Proficient in Python, JavaScript, TypeScript, React, Node.js, Docker, AWS, and PostgreSQL. Proven track record of scaling systems to handle millions of requests.

Technical Skills:
Python, JavaScript, TypeScript, React, Node.js, SQL, PostgreSQL, Docker, AWS, Git, REST API, CI/CD, Microservices

Work Experience:
Senior Software Engineer - Tech Solutions Inc. (2021 - Present)
• Architected scalable microservices using Python and FastAPI, boosting system throughput by 35%.
• Automated CI/CD deployment pipelines using Docker, Kubernetes, and GitHub Actions, cutting deployment build times by 40%.
• Mentored junior developers and instituted rigorous peer code review practices across engineering.

Software Developer - Innovate Web Labs (2018 - 2021)
• Developed responsive web applications using React, TypeScript, and Redux serving 500k+ monthly active users.
• Optimized database indexing and query caching in PostgreSQL, cutting latency by 55ms.

Education:
B.S. in Computer Science - University of Technology (2014 - 2018)

Projects:
AI Resume ATS Score Optimizer [Python, Streamlit, Scikit-learn]
• Built an intelligent ATS resume predictor and multi-format document builder with 100% precision scoring."""
    },
    {
        "domain": "AI, Machine Learning & Data Science",
        "text": """Dr. Elena Rostova
Lead AI & Machine Learning Scientist
elena.rostova@email.com | +1 (555) 987-6543 | Boston, MA | linkedin.com/in/elenarostova

Professional Summary:
Accomplished AI & ML Scientist with 7+ years of experience developing deep learning models, natural language processing (NLP) pipelines, and generative AI systems. Expert in Python, PyTorch, TensorFlow, Scikit-Learn, HuggingFace, LLMs, and PySpark.

Technical Skills:
Python, Machine Learning, Deep Learning, NLP, PyTorch, TensorFlow, Scikit-Learn, Pandas, NumPy, HuggingFace, LLM, GenAI, SQL, PySpark

Work Experience:
Lead Machine Learning Engineer - NeuralAI Systems (2021 - Present)
• Architected large language model (LLM) fine-tuning pipelines using PyTorch and HuggingFace, improving domain sentiment accuracy by 28%.
• Deployed real-time computer vision models for automated defect detection, handling 2,000+ images per second with 99.4% accuracy.
• Spearheaded scalable distributed ML training on AWS GPU clusters.

Machine Learning Researcher - DataVision Labs (2017 - 2021)
• Formulated novel recommendation system algorithms using PySpark and TensorFlow, increasing user conversion by $2.4M annually.

Education:
Ph.D. in Computer Science (Artificial Intelligence) - MIT (2013 - 2017)

Projects:
Generative AI Contextual Summarizer [Python, PyTorch, LLM]
• Engineered a multi-modal RAG search pipeline indexing 500k+ enterprise documents with sub-second retrieval times."""
    },
    {
        "domain": "Cloud Engineering & DevOps",
        "text": """Marcus Vance
Senior DevOps & Cloud Architect
marcus.vance@email.com | +1 (555) 345-6789 | Austin, TX | linkedin.com/in/marcusvance

Professional Summary:
Cloud & DevOps Engineer with 6+ years of experience automating infrastructure, zero-downtime CI/CD pipelines, and Kubernetes clusters across AWS, GCP, and Azure. Expert in Terraform, Docker, Kubernetes, Ansible, Jenkins, and Linux.

Technical Skills:
AWS, Azure, GCP, Docker, Kubernetes, Terraform, Ansible, Jenkins, GitHub Actions, CI/CD, Linux, Bash, Python, System Design

Work Experience:
Senior DevOps Engineer - CloudScale Operations (2021 - Present)
• Architected multi-region Kubernetes clusters on AWS EKS using Terraform, maintaining 99.99% infrastructure uptime.
• Automated enterprise CI/CD deployment workflows via GitHub Actions and Docker, reducing software release cycles from 2 weeks to 15 minutes.
• Implemented infrastructure security scanning and cost optimization strategies, saving $120,000 annually.

Infrastructure Engineer - DataCloud Corp (2018 - 2021)
• Managed Linux server fleets using Ansible and Bash scripts across 400+ virtual machines.

Education:
B.S. in Information Technology - Texas A&M University (2014 - 2018)

Projects:
GitOps Kubernetes Automation Pipeline [Terraform, Kubernetes, ArgoCD]
• Built an automated GitOps deployment system synchronizing microservice infrastructure changes live."""
    },
    {
        "domain": "Cybersecurity & Network Security",
        "text": """Samantha Reed
Cybersecurity Analyst & Threat Hunter
samantha.reed@email.com | +1 (555) 678-9012 | Washington, DC | linkedin.com/in/samanthareed

Professional Summary:
Dedicated Cybersecurity Analyst with 5+ years of expertise in threat detection, SIEM log monitoring, penetration testing, and incident response. Proficient in Python, Bash, Linux, Wireshark, Splunk, and Network Security protocols.

Technical Skills:
Cybersecurity, Network Security, Python, Bash, Linux, SIEM, Firewall, Wireshark, Penetration Testing, CISSP, Cryptography, Incident Response

Work Experience:
Senior Security Analyst - CyberGuard Defense (2021 - Present)
• Spearheaded 24/7 SIEM monitoring using Splunk, detecting and mitigating over 1,500 security incidents annually.
• Executed internal penetration testing and vulnerability assessments across corporate infrastructure, remediating 45+ high-risk vulnerabilities.
• Automated incident response triage scripts in Python and Bash, reducing mean time to detect (MTTD) by 60%.

Information Security Specialist - Federal Defense Systems (2018 - 2021)
• Conducted network packet inspection using Wireshark and configured enterprise firewalls.

Education:
B.S. in Cybersecurity - George Mason University (2014 - 2018) (CISSP Certified)

Projects:
Automated Threat Intelligence Scanner [Python, SIEM, API]
• Developed a custom threat intelligence parser aggregating malicious IP indicators in real time."""
    },
    {
        "domain": "Product & Project Management",
        "text": """David Kim
Senior Technical Product Manager
david.kim@email.com | +1 (555) 456-7890 | Seattle, WA | linkedin.com/in/davidkim

Professional Summary:
Strategic Technical Product Manager with 6+ years of experience leading cross-functional engineering teams to ship enterprise SaaS products. Skilled in Agile, Scrum, Kanban, Jira, Roadmap Strategy, Product Analytics, and Stakeholder Management.

Technical Skills:
Agile, Scrum, Kanban, Jira, Confluence, Product Management, Leadership, Stakeholder Management, Strategic Planning, User Research, Roadmapping

Work Experience:
Senior Product Manager - SaaS Cloud Inc. (2021 - Present)
• Spearheaded product vision and roadmap execution for enterprise SaaS analytics platform, driving $4.5M in ARR growth.
• Led 3 cross-functional Agile engineering teams through bi-weekly sprint cycles, achieving 98% sprint velocity predictability.
• Conducted user research interviews and A/B test experiments, improving onboarding conversion by 34%.

Technical Project Manager - Agile Dynamics (2018 - 2021)
• Managed product releases and Jira sprint backlogs across mobile and web engineering initiatives.

Education:
B.A. in Business Administration & Computer Science - University of Washington (2014 - 2018)

Projects:
Customer Journey Analytics Dashboard [Jira, Mixpanel, Agile]
• Designed end-to-end telemetry product spec tracking user drop-off across key funnel workflows."""
    }
]


def get_random_sample_resume() -> Dict[str, str]:
    """Returns a random candidate profile from the sample resumes pool."""
    return random.choice(SAMPLE_RESUMES_POOL)


def clean_text(text: str) -> str:
    if not text:
        return ""
    text = text.lower()
    text = re.sub(r'[\r\n\t]+', ' ', text)
    text = re.sub(r'[^a-z0-9\s#+\.-]', ' ', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text


def extract_detected_skills(text: str, domain_target="All Domains (General Tech Standard)") -> Tuple[List[str], List[str]]:
    cleaned = clean_text(text)
    matched = []
    
    for skill in ALL_TAXONOMY_SKILLS:
        pattern = r'(?:\b|_)' + re.escape(skill) + r'(?:\b|_)'
        if re.search(pattern, cleaned):
            matched.append(skill)
            
    matched_unique = list(set(matched))
    priority_pool = DOMAIN_TAXONOMY.get(domain_target, DOMAIN_TAXONOMY["All Domains (General Tech Standard)"])
    missing = [s for s in priority_pool if s not in matched_unique]
    
    return matched_unique, missing


def extract_skills_and_terms(text: str):
    matched, _ = extract_detected_skills(text)
    verbs = extract_action_verbs(text)
    return matched, [], verbs


def extract_action_verbs(text: str) -> List[str]:
    cleaned = clean_text(text)
    found = []
    for verb in POWER_ACTION_VERBS:
        pattern = r'\b' + re.escape(verb) + r'\b'
        if re.search(pattern, cleaned):
            found.append(verb)
    return list(set(found))


def calculate_quantified_metrics(text: str) -> int:
    if not text:
        return 0
    patterns = [
        r'\b\d+%',
        r'\$\d+(?:\.\d+)?(?:k|m|b)?\b',
        r'\b\d+(?:\.\d+)?\s*(?:x|xfold|ms|s|hr|hours|days|k|m)\b',
        r'\b\d+\+\b',
        r'\b(?:increased|decreased|reduced|grew|improved|saved)\s+by\s+\d+',
    ]
    matches = 0
    for p in patterns:
        matches += len(re.findall(p, text, re.IGNORECASE))
    return matches


def check_sections(text: str) -> dict:
    cleaned = clean_text(text)
    sections_status = {}
    for section, keywords in REQUIRED_SECTIONS.items():
        found = False
        for kw in keywords:
            if re.search(r'\b' + re.escape(kw) + r'\b', cleaned):
                found = True
                break
        sections_status[section] = found
    return sections_status


def evaluate_ats_score(resume_text: str, domain_target="All Domains (General Tech Standard)") -> dict:
    if not resume_text or not resume_text.strip():
        return {
            "overall_score": 0,
            "skills_score": 0,
            "verbs_score": 0,
            "metrics_score": 0,
            "section_score": 0,
            "readability_score": 0,
            "hard_skills_matched": [],
            "hard_skills_missing": [],
            "action_verbs_found": [],
            "quantified_metrics_count": 0,
            "sections_status": {},
            "formatting_warnings": ["Please upload or paste your resume text."],
            "recommendations": ["Upload or paste your resume to get a full ATS score analysis."]
        }

    clean_res = clean_text(resume_text)
    words = clean_res.split()
    word_count = len(words)

    # 1. Technical Skill Depth (30 points)
    matched_skills, missing_skills = extract_detected_skills(resume_text, domain_target)
    skills_score = min(30.0, (len(matched_skills) / 9.0) * 30.0)

    # 2. Action Verb Power (25 points)
    found_action_verbs = extract_action_verbs(resume_text)
    verbs_score = min(25.0, (len(found_action_verbs) / 6.0) * 25.0)

    # 3. Quantified Achievement Ratio (20 points)
    quant_metrics_count = calculate_quantified_metrics(resume_text)
    metrics_score = min(20.0, (quant_metrics_count / 4.0) * 20.0)

    # 4. ATS Section Structure (15 points)
    sections_status = check_sections(resume_text)
    found_sections = sum(1 for v in sections_status.values() if v)
    section_score = (found_sections / len(REQUIRED_SECTIONS)) * 15.0

    # 5. Readability & Length Audit (10 points)
    if 400 <= word_count <= 850:
        readability_score = 10.0
    elif 300 <= word_count < 400 or 850 < word_count <= 1100:
        readability_score = 7.0
    else:
        readability_score = 4.0

    overall_score = int(round(skills_score + verbs_score + metrics_score + section_score + readability_score))
    overall_score = min(100, max(15, overall_score))

    formatting_warnings = []
    if word_count < 350:
        formatting_warnings.append("Resume is too short (< 350 words). Expand details on technical projects & impact.")
    elif word_count > 1000:
        formatting_warnings.append("Resume is long (> 1000 words). Keep it concise (1-2 pages).")

    if quant_metrics_count < 3:
        formatting_warnings.append("Low measurable impact: Include more numbers, %, or dollar figures (e.g., 'Improved performance by 35%').")

    missing_sec = [k for k, v in sections_status.items() if not v]
    if missing_sec:
        formatting_warnings.append(f"Missing standard section headers: {', '.join(missing_sec)}")

    recommendations = []
    if missing_skills:
        recommendations.append(f"Inject targeted {domain_target} skills: {', '.join([s.title() for s in missing_skills[:5]])}.")

    if len(found_action_verbs) < 5:
        recommendations.append("Begin work bullets with strong action verbs like 'Architected', 'Spearheaded', 'Optimized', 'Engineered'.")

    if quant_metrics_count < 3:
        recommendations.append("Add measurable outcomes to experience bullet points (e.g., 'Reduced processing latency by 40%').")

    if not recommendations:
        recommendations.append("Outstanding resume! Passes top automated ATS screeners with high compliance.")

    return {
        "overall_score": overall_score,
        "skills_score": round(skills_score, 1),
        "verbs_score": round(verbs_score, 1),
        "metrics_score": round(metrics_score, 1),
        "section_score": round(section_score, 1),
        "readability_score": round(readability_score, 1),
        "hard_skills_matched": sorted([s.title() for s in matched_skills]),
        "hard_skills_missing": sorted([s.title() for s in missing_skills]),
        "action_verbs_found": sorted([s.title() for s in found_action_verbs]),
        "quantified_metrics_count": quant_metrics_count,
        "sections_status": sections_status,
        "formatting_warnings": formatting_warnings,
        "recommendations": recommendations
    }


def enhance_bullet_point(bullet: str) -> str:
    bullet = bullet.strip()
    if not bullet:
        return bullet

    bullet = re.sub(r'^[•\-\*]\s*', '', bullet)
    words = bullet.split()
    first_word = words[0].lower() if words else ""

    verb_map = {
        "worked": "Engineered",
        "created": "Architected",
        "built": "Developed",
        "made": "Formulated",
        "helped": "Spearheaded",
        "assisted": "Collaborated on",
        "handled": "Managed",
        "did": "Executed",
        "used": "Leveraged",
        "wrote": "Authored",
        "fixed": "Resolved",
        "changed": "Optimized"
    }

    if first_word in verb_map:
        words[0] = verb_map[first_word]
        bullet = " ".join(words)
    elif first_word not in [v.lower() for v in POWER_ACTION_VERBS]:
        bullet = f"Spearheaded {bullet[0].lower() + bullet[1:]}"

    if not re.search(r'\d', bullet):
        bullet += ", improving operational efficiency by 25% and reducing processing latency."

    return bullet


def generate_cover_letter_text(d: Dict[str, Any]) -> str:
    name = d.get("full_name", "Alex Morgan")
    role = d.get("target_role", "Senior Software Engineer")
    email = d.get("email", "alex@example.com")
    phone = d.get("phone", "+1 555-0199")
    skills = d.get("skills", "Python, SQL, React, AWS")
    location = d.get("location", "San Francisco, CA")

    return f"""Dear Hiring Manager,

I am writing to express my strong interest in the {role} position. With a proven track record in technical innovation, system design, and delivering scalable solutions, I am excited about the opportunity to contribute to your team.

Throughout my career, I have specialized in building robust architectures and leveraging technologies including {skills}. In my previous roles, I have spearheaded critical engineering initiatives, optimized complex systems, and consistently delivered measurable business value.

What drives me is solving complex technical challenges and collaborating with cross-functional teams to build impactful products. My background in {location} has equipped me with a strong foundation in system architecture, data-driven execution, and modern development best practices.

I am confident that my technical expertise, problem-solving mindset, and dedication to excellence make me a strong candidate for this role. I look forward to discussing how my experience aligns with your team's goals.

Thank you for your time and consideration.

Sincerely,
{name}
{email} | {phone} | {location}"""


def generate_linkedin_content(d: Dict[str, Any]) -> Dict[str, Any]:
    name = d.get("full_name", "Alex Morgan")
    role = d.get("target_role", "Software Engineer")
    skills_list = [s.strip() for s in d.get("skills", "Python, SQL, AWS, React").split(",") if s.strip()][:4]
    top_skills = " | ".join(skills_list)

    headlines = [
        f"{role} | Specializing in {top_skills} | Driving Scalable Technical Impact",
        f"Results-Driven {role} | {top_skills} | High-Performance System Architect",
        f"{role} @ Tech | {top_skills} | Passionate about Innovation & Data-Driven Solutions"
    ]

    about_text = f"""Hi! I'm {name}, a results-driven {role} dedicated to building high-performance software systems and driving business growth.

💡 Core Expertise:
{top_skills}

🚀 What I Do:
• Architect scalable software architectures and cloud-native solutions.
• Optimize system performance, reducing latency and operational overhead.
• Collaborate with cross-functional teams to deliver end-to-end technical products.

📫 Let's Connect:
Feel free to reach out for technical discussions, engineering collaborations, or professional opportunities!"""

    return {"headlines": headlines, "about": about_text}


def generate_interview_qa(skills_str: str) -> List[Dict[str, str]]:
    skills = [s.strip().lower() for s in skills_str.split(",") if s.strip()]

    qa_pool = [
        {
            "q": "How do you optimize system performance and query latency in production?",
            "a": "I analyze bottleneck metrics using profiling tools, implement database indexing, leverage Redis caching layers, and optimize asynchronous I/O execution, resulting in 30-50% latency reduction."
        },
        {
            "q": "Explain your approach to designing scalable microservices or component architectures.",
            "a": "I follow domain-driven design, enforcing single responsibility, decoupled RESTful/gRPC API contracts, stateless service deployment with Docker/Kubernetes, and circuit breaker patterns."
        },
        {
            "q": "How do you ensure zero-downtime CI/CD deployments?",
            "a": "Using automated GitHub Actions/Jenkins pipelines with containerization, blue-green or canary deployment strategies, automated unit/integration test suites, and rollback triggers."
        },
        {
            "q": "Describe a challenging technical problem you solved recently.",
            "a": "Describe the situation, technical complexity, your specific architectural choice (e.g. switching to asynchronous queues/caching), and the measurable result (e.g. 40% speed boost)."
        },
        {
            "q": "How do you handle data consistency and concurrency in distributed systems?",
            "a": "By using atomic database transactions, optimistic locking, idempotent API design, and event-driven architectures with Kafka/RabbitMQ."
        }
    ]
    return qa_pool


def estimate_market_salary(d: Dict[str, Any]) -> Dict[str, str]:
    exp_list = d.get("experience", [])
    exp_years = len(exp_list) * 2
    skills_count = len(d.get("skills", "").split(","))

    if exp_years >= 6 or skills_count >= 12:
        tier = "Senior / Executive Lead"
        usd_range = "$120,000 - $185,000 / yr"
        inr_range = "₹22,00,000 - ₹38,00,000 / yr"
    elif exp_years >= 3 or skills_count >= 7:
        tier = "Mid-Level Professional"
        usd_range = "$85,000 - $130,000 / yr"
        inr_range = "₹12,00,000 - ₹22,00,000 / yr"
    else:
        tier = "Associate / Junior Specialist"
        usd_range = "$60,000 - $90,000 / yr"
        inr_range = "₹6,00,000 - ₹12,00,000 / yr"

    return {"tier": tier, "usd": usd_range, "inr": inr_range}

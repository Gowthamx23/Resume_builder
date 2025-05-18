from sklearn.feature_extraction.text import TfidfVectorizer
import re

def analyze_posting(posting):
    """
    Extract keywords from job posting using TF-IDF.s
    """
    try:
        # Clean text
        posting = re.sub(r'[^\w\s]', '', posting.lower())
        vectorizer = TfidfVectorizer(stop_words='english', max_features=20)
        tfidf_matrix = vectorizer.fit_transform([posting])
        keywords = vectorizer.get_feature_names_out()
        return keywords.tolist()
    except Exception as e:
        print(f"Posting analysis failed: {e}")
        return []

def generate_resume(profile, keywords):
    """
    Generate a LaTeX resume tailored to the job posting.
    """
    skills = ", ".join([s.strip() for s in profile["skills"] if s.strip()])
    matched_skills = [s for s in profile["skills"] if any(k.lower() in s.lower() for k in keywords)]
    matched_skills_str = ", ".join(matched_skills) if matched_skills else skills

    # LaTeX resume template
    template = r"""
\documentclass[a4paper,11pt]{article}
\usepackage{geometry}
\geometry{left=1.5cm,right=1.5cm,top=2cm,bottom=2cm}
\usepackage{titlesec}
\usepackage{enumitem}
\usepackage[utf8]{inputenc}
\usepackage[T1]{fontenc}
\usepackage{helvet}
\renewcommand{\familydefault}{\sfdefault}

\begin{document}

\begin{center}
    {\LARGE \textbf{Your name}} \\
    \vspace{0.2cm}
    Your email \,|\, Your phone
\end{center}

\section*{Education}
Your education

\section*{Skills}
Your skills

\section*{Experience}
Your experience

\end{document}
"""
    # Replace placeholders
    resume = template.replace("Your name", profile["name"]) \
                    .replace("Your email", profile["email"]) \
                    .replace("Your phone", profile["phone"]) \
                    .replace("Your education", profile["education"]) \
                    .replace("Your skills", matched_skills_str) \
                    .replace("Your experience", profile["experience"])
    return resume
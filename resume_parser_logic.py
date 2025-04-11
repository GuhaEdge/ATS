import fitz  # PyMuPDF
import spacy
import re

nlp = spacy.load("en_core_web_sm")

def extract_text_from_pdf(file_bytes):
    text = ""
    doc = fitz.open(stream=file_bytes, filetype="pdf")
    for page in doc:
        text += page.get_text()
    return text

def extract_email(text):
    match = re.search(r"[\w\.-]+@[\w\.-]+", text)
    return match.group(0) if match else ""

def extract_phone(text):
    match = re.search(r"\+?\d[\d\s\-]{7,}\d", text)
    return match.group(0) if match else ""

def extract_dob(text):
    match = re.search(r"\b\d{2}[\/\-\.]\d{2}[\/\-\.]\d{4}\b", text)
    return match.group(0) if match else ""

def extract_location(text):
    locations = ["Bangalore", "Delhi", "Mumbai", "Chennai", "Hyderabad", "Pune"]
    for loc in locations:
        if loc.lower() in text.lower():
            return {"city": loc, "state": "", "country": "India"}
    return {}

def extract_name(text):
    lines = text.split("\n")
    first_line = lines[0].strip()
    if len(first_line.split()) <= 4:
        return first_line
    return ""

def extract_skills(text):
    skill_keywords = ["Python", "Java", "SQL", "AWS", "Azure", "Docker", "Kubernetes"]
    return [kw for kw in skill_keywords if kw.lower() in text.lower()]

def extract_certifications(text):
    certs = ["PMP", "AWS Certified", "Azure Fundamentals", "Scrum Master", "CCNA"]
    return [cert for cert in certs if cert.lower() in text.lower()]

def summarize(text):
    doc = nlp(text)
    sentences = list(doc.sents)
    return " ".join([sent.text for sent in sentences[:3]])

def score_candidate(skills):
    return min(100, len(skills) * 15)

def process_resume(file_bytes):
    text = extract_text_from_pdf(file_bytes)
    return {
        "name": extract_name(text),
        "email": extract_email(text),
        "phone": extract_phone(text),
        "dob": extract_dob(text),
        "location": extract_location(text),
        "skills": extract_skills(text),
        "certifications": extract_certifications(text),
        "summary": summarize(text),
        "score": score_candidate(extract_skills(text))
    }
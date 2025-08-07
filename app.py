import streamlit as st
import pdfplumber
import re

def extract_text_from_pdf(pdf_file):
    with pdfplumber.open(pdf_file) as pdf:
        text = ''
        for page in pdf.pages:
            text += page.extract_text() or ''
    return text

def parse_resume(text):
    parsed_data = {}

    # Extract Name (first line)
    name = text.strip().split('\n')[0]
    parsed_data['Name'] = name

    # Extract Email
    email_match = re.search(r'[\w\.-]+@[\w\.-]+', text)
    parsed_data['Email'] = email_match.group(0) if email_match else "Not found"

    # Extract Phone
    phone_match = re.search(r'\+?\d[\d\s()-]{7,}\d', text)
    parsed_data['Phone'] = phone_match.group(0) if phone_match else "Not found"

    return parsed_data

st.set_page_config(page_title="AI Resume Parser")
st.title("📄 AI Resume Parser")

uploaded_file = st.file_uploader("Upload your resume (PDF only)", type="pdf")

if uploaded_file:
    with st.spinner("Reading resume..."):
        text = extract_text_from_pdf(uploaded_file)
        parsed_data = parse_resume(text)

    st.subheader("📌 Extracted Details")
    st.json(parsed_data)

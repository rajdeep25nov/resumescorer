import streamlit as st
from dotenv import load_dotenv
import base64
import os
import io
from PIL import Image
import pdf2image
import google.generativeai as genai
from fpdf import FPDF
import PyPDF2
import time  # For simulating loading

# Set page config (make sure it's at the very top)
st.set_page_config(
    page_title="ATS Resume Expert",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Add custom CSS for enhanced UI
st.markdown("""
    <style>
        /* General Page Styling */
        body {
            font-family: 'Arial', sans-serif;
            background: linear-gradient(135deg, #f5f7fa, #c3cfe2);
            color: #333;
        }

        /* Colorful Buttons */
        .stButton>button {
            background: linear-gradient(135deg, #6a11cb, #2575fc);
            color: white;
            border: none;
            border-radius: 25px;
            padding: 10px 20px;
            font-size: 16px;
            font-weight: bold;
            cursor: pointer;
            transition: all 0.3s ease;
        }

        .stButton>button:hover {
            background: linear-gradient(135deg, #2575fc, #6a11cb);
            transform: scale(1.05);
        }

        /* Loading Spinner */
        .loading-spinner {
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100px;
        }

        .spinner {
            border: 8px solid #f3f3f3;
            border-top: 8px solid #6a11cb;
            border-radius: 50%;
            width: 60px;
            height: 60px;
            animation: spin 1s linear infinite;
        }

        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }

        /* Responsive Design */
        @media (max-width: 768px) {
            .stButton>button {
                width: 100%;
                margin-bottom: 10px;
            }
        }

        /* Footer Styling */
        .footer {
            position: fixed;
            bottom: 0;
            left: 0;
            right: 0;
            padding: 10px;
            background: linear-gradient(135deg, #6a11cb, #2575fc);
            color: white;
            text-align: center;
        }
    </style>
""", unsafe_allow_html=True)

# Hide Streamlit's default menu and footer
hide_menu_style = """
    <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
    </style>
"""
st.markdown(hide_menu_style, unsafe_allow_html=True)

# Streamlit app setup
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Define prompts
input_prompt1 = """
You are an experienced HR with Tech Experience in the field of any one job role from Data Science, Full stack 
Web Development, Big Data Engineering, DEVOPS, Data Analyst. Your task is to review 
the provided resume against the job description for these profiles.
Please share your professional evaluation on whether the candidate's profile aligns with the role.
Highlight the strengths and weaknesses of the applicant in relation to the specified job requirements.
"""

input_prompt3 = """
You are a skilled ATS (Application Tracking System) scanner with deep understanding of any one job role from Data Science, Full stack 
Web Development, Big Data Engineering, DEVOPS, Data Analyst, and deep ATS functionality.
Your task is to evaluate the resume against the provided job description. Give me the percentage match if the resume matches
the job description. First, the output should come as a percentage and then keywords missing, and last, final thoughts.
"""

def get_gemini_response(input, pdf_content, prompt):
    model = genai.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content([input, pdf_content[0], prompt])
    return response.text

def input_pdf_setup(uploaded_file):
    if uploaded_file is not None:
        images = pdf2image.convert_from_bytes(uploaded_file.read())
        first_page = images[0]
        
        img_byte_arr = io.BytesIO()
        first_page.save(img_byte_arr, format='JPEG')
        img_byte_arr = img_byte_arr.getvalue()

        pdf_parts = [
            {
                "mime_type": "image/jpeg",
                "data": base64.b64encode(img_byte_arr).decode()
            }
        ]
        return pdf_parts
    else:
        raise FileNotFoundError("No file Uploaded")

# Function to extract text from PDF
def extract_text_from_pdf(uploaded_file):
    try:
        reader = PyPDF2.PdfReader(uploaded_file)
        text = ""
        for page in reader.pages:
            text += page.extract_text()
        return text
    except Exception as e:
        st.error(f"Error extracting text from PDF: {e}")
        return ""

# Function to generate interview questions
def generate_interview_questions(job_description, prompt_type="JD"):
    model = genai.GenerativeModel("gemini-pro")
    if prompt_type == "JD":
        prompt = f"Generate 10 most asked interview questions based on the following job description:\n{job_description}"
    else:
        prompt = "Generate 10 commonly asked interview questions for warmup."

    response = model.generate_content(prompt)
    return response.text.strip().split("\n")

# Function to generate a cover letter
def generate_cover_letter(resume_text, job_description):
    model = genai.GenerativeModel("gemini-pro")
    prompt = f"""
    Generate a professional cover letter based on the following resume and job description:
    
    Resume:
    {resume_text}
    
    Job Description:
    {job_description}
    """
    response = model.generate_content(prompt)
    return response.text

# Function to calculate resume scorecard
def calculate_scorecard(resume_text, job_description):
    model = genai.GenerativeModel("gemini-pro")
    prompt = f"""
    Analyze the following resume and job description to calculate a scorecard:
    
    Resume:
    {resume_text}
    
    Job Description:
    {job_description}
    
    Provide the following metrics:
    1. Skills Match: Percentage of skills in the resume that match the job description.
    2. Experience Match: How well the candidate's experience aligns with the job requirements.
    3. Education Match: Whether the candidate's education meets the job's requirements.
    
    Return the results in the following format:
    Skills Match: X%
    Experience Match: Y%
    Education Match: Z%
    """
    response = model.generate_content(prompt)
    return response.text

# Function to generate a PDF report
def generate_pdf(resume_evaluation, percentage_match, jd_questions, warmup_questions, cover_letter, scorecard):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    
    # Add Resume Evaluation
    pdf.cell(200, 10, txt="Resume Evaluation", ln=True)
    pdf.multi_cell(0, 10, txt=resume_evaluation)
    
    # Add Percentage Match
    pdf.cell(200, 10, txt="Percentage Match", ln=True)
    pdf.multi_cell(0, 10, txt=percentage_match)
    
    # Add JD-Specific Questions
    pdf.cell(200, 10, txt="Most Asked Interview Questions (JD-Specific):", ln=True)
    for question in jd_questions:
        pdf.multi_cell(0, 10, txt=f"- {question}")
    
    # Add Warmup Questions
    pdf.cell(200, 10, txt="Warmup Questions (General):", ln=True)
    for question in warmup_questions:
        pdf.multi_cell(0, 10, txt=f"- {question}")
    
    # Add Cover Letter
    pdf.cell(200, 10, txt="Cover Letter", ln=True)
    pdf.multi_cell(0, 10, txt=cover_letter)
    
    # Add Scorecard
    pdf.cell(200, 10, txt="Resume Scorecard", ln=True)
    pdf.multi_cell(0, 10, txt=scorecard)
    
    # Return the PDF as bytes
    return pdf.output(dest="S").encode("latin1")

# Streamlit app UI
st.title("📄 ATS Resume Expert")
st.markdown("Welcome to the ATS Resume Expert! Upload your resume and job description to get started.")

# Input for Job Description
with st.container():
    st.header("Job Description")
    input_text = st.text_area("Paste Job Description Here", key="input", height=150)

# Input for Resume
with st.container():
    st.header("Resume")
    uploaded_file = st.file_uploader("Upload your Resume (PDF)...", type=["pdf"])

if uploaded_file is not None:
    st.success("PDF uploaded successfully!")

# Buttons for actions
col1, col2, col3, col4 = st.columns(4)
with col1:
    submit1 = st.button("Tell me About the Resume")
with col2:
    submit3 = st.button("Percentage Match")
with col3:
    submit_questions = st.button("Generate Interview Questions")
with col4:
    submit_cover_letter = st.button("Generate Cover Letter")

# Handle Resume Scorecard Generation
submit_scorecard = st.button("Generate Resume Scorecard")

# Variables to store results
resume_evaluation = ""
percentage_match = ""
jd_questions = []
warmup_questions = []
cover_letter = ""
scorecard = ""

# Loading Spinner
def show_loading_spinner():
    st.markdown("""
        <div class="loading-spinner">
            <div class="spinner"></div>
        </div>
    """, unsafe_allow_html=True)

# Handle Button Clicks
if submit1 or submit3 or submit_questions or submit_cover_letter or submit_scorecard:
    if uploaded_file is not None and input_text:
        with st.spinner("Generating insights..."):
            # Simulate loading for 2 seconds
            time.sleep(2)

            if submit1:
                pdf_content = input_pdf_setup(uploaded_file)
                resume_evaluation = get_gemini_response(input_prompt1, pdf_content, input_text)
                st.subheader("Resume Evaluation")
                st.write(resume_evaluation)

            if submit3:
                pdf_content = input_pdf_setup(uploaded_file)
                percentage_match = get_gemini_response(input_prompt3, pdf_content, input_text)
                st.subheader("Percentage Match")
                st.write(percentage_match)

            if submit_questions:
                jd_questions = generate_interview_questions(input_text, prompt_type="JD")
                st.subheader("Most Asked Interview Questions (JD-Specific):")
                for question in jd_questions:
                    st.write(f"- {question}")

                warmup_questions = generate_interview_questions(input_text, prompt_type="Warmup")
                st.subheader("Warmup Questions (General):")
                for question in warmup_questions:
                    st.write(f"- {question}")

            if submit_cover_letter:
                resume_text = extract_text_from_pdf(uploaded_file)
                if resume_text:
                    cover_letter = generate_cover_letter(resume_text, input_text)
                    st.subheader("Generated Cover Letter")
                    st.write(cover_letter)
                else:
                    st.error("Failed to extract text from the uploaded PDF.")

            if submit_scorecard:
                resume_text = extract_text_from_pdf(uploaded_file)
                if resume_text:
                    scorecard = calculate_scorecard(resume_text, input_text)
                    st.subheader("Resume Scorecard")
                    st.write(scorecard)
                else:
                    st.error("Failed to extract text from the uploaded PDF.")
    else:
        st.warning("Please upload a resume and provide a job description.")

# Add PDF Download Button
if resume_evaluation or percentage_match or jd_questions or warmup_questions or cover_letter or scorecard:
    pdf = generate_pdf(resume_evaluation, percentage_match, jd_questions, warmup_questions, cover_letter, scorecard)
    st.download_button(
        label="Download Results as PDF",
        data=pdf,
        file_name="results.pdf",
        mime="application/pdf",
    )

# Footer with credit text
st.markdown("""
    <div class="footer">
        <p>Created by Rajdeep Jaiswal</p>
    </div>
""", unsafe_allow_html=True)

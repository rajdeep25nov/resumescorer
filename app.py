import streamlit as st
from dotenv import load_dotenv
import base64
import os
import io
from PIL import Image
import pdf2image
import google.generativeai as genai

# Set page config (make sure it's at the very top)
st.set_page_config(page_title="ATS Resume Expert", layout="wide")

# Add custom CSS to enhance UI, hide Streamlit UI elements, and add colorful bubble animation
st.markdown("""
    <style>
        /* General Page Styling */
        body {
            font-family: Arial, sans-serif;
            background: #f0f8ff; /* Light background for better visibility */
            overflow: hidden; /* Hide overflow to keep the animation smooth */
        }

        /* Colorful Bubbles animation styles */
        .bubble {
            position: absolute;
            bottom: -100px; /* Start bubbles off-screen */
            width: 50px;
            height: 50px;
            border-radius: 50%; /* Ensures the bubble is perfectly round */
            background: #ff7f7f; /* Default light bubble color */
            animation: bubble 10s infinite ease-in-out;
        }

        /* Light pastel colors for different bubbles */
        .bubble:nth-child(odd) {
            background: #ffb3b3; /* Light pink */
        }

        .bubble:nth-child(even) {
            background: #b3e0ff; /* Light blue */
        }

        .bubble:nth-child(3) {
            background: #d9f7a6; /* Light yellow */
        }

        .bubble:nth-child(4) {
            background: #ffcc99; /* Light peach */
        }

        @keyframes bubble {
            0% {
                transform: translateX(0) translateY(0);
                opacity: 1;
            }
            100% {
                transform: translateX(300px) translateY(-1000px); /* Moving upwards */
                opacity: 0;
            }
        }

        /* Styling the header */
        .css-1v3fvcr {
            font-size: 2rem;
            color: #00bfae;
        }

        /* Button Styling */
        .css-1n8z0g6 {
            background-color: #00bfae;
            color: white;
        }

        /* Hide the Streamlit Footer */
        .css-18e3th9 {visibility: hidden;}

        /* Hide the settings menu in the top-right corner */
        .css-1r6wz6s {visibility: hidden;}

        /* Optionally, hide the hamburger menu (three-dot menu) */
        .css-1gb49t5 {display: none;}

        /* Hide the sidebar */
        .css-1d391kg {display: none;}

        /* Hide the deploy button (on Streamlit Cloud) */
        .css-1d391kg button[title="Deploy"] {display: none;}

        /* Hide the top-right corner elements including "Settings" and "Deploy" buttons */
        .css-1c1z2hu {display: none;}

        /* Footer Styling */
        .footer {
            position: fixed;
            bottom: 0;
            left: 0;
            right: 0;
            padding: 10px;
            background-color: #00bfae;
            color: white;
            text-align: center;
        }

        /* Adjust layout for wide view */
        .css-1xv4szo {max-width: 1200px;}
    </style>
""", unsafe_allow_html=True)

hide_menu_style = """<style>#MainMenu {visibility: hidden;} footer {visibility: hidden;}</style>"""
st.markdown(hide_menu_style, unsafe_allow_html=True)


st.markdown(
        r"""
        <style>
        .stAppDeployButton {
                visibility: hidden;
            }
        </style>
        """, unsafe_allow_html=True
    )


# Streamlit app setup
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

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

# Streamlit app UI
st.header("ATS Resume Scanner")
input_text = st.text_area("Job Description: ", key="input")
uploaded_file = st.file_uploader("Upload your Resume(PDF)...", type=["pdf"])

if uploaded_file is not None:
    st.write("PDF uploaded Successfully")

submit1 = st.button("Tell me About the Resume")
submit3 = st.button("Percentage match")

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

if submit1:
    if uploaded_file is not None:
        pdf_content = input_pdf_setup(uploaded_file)
        response = get_gemini_response(input_prompt1, pdf_content, input_text)
        st.subheader("The Response is")
        st.write(response)
    else:
        st.write("Please upload a pdf")
elif submit3:
    if uploaded_file is not None:
        pdf_content = input_pdf_setup(uploaded_file)
        response = get_gemini_response(input_prompt3, pdf_content, input_text)
        st.subheader("The Response is")
        st.write(response)
    else:
        st.write("Please upload a pdf")

# Footer with credit text
st.markdown("""
    <div class="footer">
        <p>Created by Rajdeep Jaiswal</p>
    </div>
""", unsafe_allow_html=True)

# Adding animated colorful bubbles to the page
import random

# Add 30 colorful bubbles with randomized sizes and animations
for i in range(30):
    st.markdown(f"""
        <div class="bubble" style="left: {random.randint(0, 100)}%; width: {random.randint(30, 60)}px; height: {random.randint(30, 60)}px; animation-duration: {random.randint(6, 12)}s; animation-delay: {random.randint(0, 3)}s;"></div>
    """, unsafe_allow_html=True)

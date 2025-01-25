

Overview

This ATS Resume Scanner web application allows users to upload their resumes (in PDF format) and compare them against a job description. It utilizes Google's Generative AI model to provide insights and feedback on whether a candidate's resume matches the provided job description. The application evaluates resumes in multiple aspects, including the percentage match and missing keywords, making it an essential tool for job seekers and HR professionals


Features

Job Description Input: Users can input the job description for a specific role.
Resume Upload: Users can upload a resume (PDF format) for analysis.
ATS Evaluation: The app evaluates the resume using Google's generative AI model and provides detailed feedback.
Keyword Match: The app evaluates the percentage match of the resume to the job description and highlights missing keywords.
Image-based PDF Parsing: Uses pdf2image and Pillow for converting PDF resumes into images for better processing.
Interactive UI: Built using Streamlit, making it easy to interact with.


Technologies Used

Streamlit: A framework to build the web application.
Google Generative AI: For analyzing and generating insights on resumes.
Pillow: For image processing and manipulation.
pdf2image: For converting PDF files into images for better text extraction.
Python-dotenv: For securely storing environment variables like API keys.



Usage

Input the Job Description: Paste the job description for the role you're applying for in the provided text area.
Upload the Resume: Upload your resume in PDF format.
Click "Tell me About the Resume" to get an analysis of how well your resume matches the job description.
Click "Percentage Match" to see the percentage of keyword match between your resume and the job description.
The application will return:

A professional evaluation of the resume.
The percentage match between the resume and job description.
Missing keywords or skills in the resume.



Running the Application

streamlit run app.py



License

This project is licensed under the MIT License - see the LICENSE file for details.

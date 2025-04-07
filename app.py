import streamlit as st
import re
from langchain_groq import ChatGroq
import json

# Setup ChatGroq LLM with model and API key
llm = ChatGroq(
    temperature=0,
    groq_api_key='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',  # Replace with your secure API key
    model_name="llama-3.3-70b-versatile"
)

# Preprocessing function (optional, could be enhanced)
def preprocess_text(text):
    text = text.lower()
    text = re.sub(r'[^a-z0-9\s@.:]', '', text)  # Keep useful characters
    return text.strip()

# Improved classification function with prompt engineering
def classify_text_with_chatgroq(sender, subject, body):
    clean_sender = preprocess_text(sender)
    clean_subject = preprocess_text(subject)
    clean_body = preprocess_text(body)

    prompt = f"""
You are a language model trained to classify emails as "Spam" or "Not Spam".
Analyze the following email and respond with exactly one word: "Spam" or "Not Spam".

--- EMAIL START ---
Sender: {clean_sender}
Subject: {clean_subject}
Body: {clean_body}
--- EMAIL END ---
"""

    response = llm.invoke(prompt)
    result = response.content.strip().lower()

    if "not spam" in result:
        return "Not Spam"
    else:
        return "Spam"

# Streamlit Page Config
st.set_page_config(page_title="Spam Mail Detection with ChatGroq", page_icon="📧", layout="wide")

# Custom CSS Styling
st.markdown("""
    <style>
        .title {
            text-align: center;
            color: #1E3A8A;
            font-size: 50px;
            font-weight: bold;
            margin-top: 40px;
        }
        .subheader {
            text-align: center;
            color: #4B5563;
            font-size: 24px;
            margin-bottom: 30px;
        }
        .prediction {
            font-size: 30px;
            font-weight: bold;
            color: #10B981;
            text-align: center;
            margin-top: 30px;
        }
    </style>
""", unsafe_allow_html=True)

# Header
st.markdown('<div class="title">Spam Mail Detection with ChatGroq</div>', unsafe_allow_html=True)
st.markdown('<div class="subheader">Enter the sender, subject, and body of the email to predict whether it is spam or not.</div>', unsafe_allow_html=True)

# Input Form
with st.form(key='email_form', clear_on_submit=True):
    sender_email = st.text_input("Sender Email ID", placeholder="e.g., spammer@example.com")
    email_subject = st.text_input("Email Subject", placeholder="e.g., Congratulations! You've won")
    email_body = st.text_area("Email Body", height=200, placeholder="Paste the email content here...")
    submit_button = st.form_submit_button(label="Predict", use_container_width=True)

# Result
if submit_button:
    if sender_email and email_subject and email_body:
        result = classify_text_with_chatgroq(sender_email, email_subject, email_body)
        st.markdown(f'<div class="prediction">{result}</div>', unsafe_allow_html=True)
    else:
        st.warning("Please fill in all fields: Sender Email, Subject, and Body.")

# Contact Info
st.markdown("""
    <hr style="margin-top: 50px; margin-bottom: 20px;">
    <div style="text-align: center;">
        <h3>📬 Contact Us</h3>
        <p>If you have any questions, feedback, or suggestions, feel free to reach out!</p>
        <p>📧 Email: <a href="mailto:yourname@example.com">yourname@example.com</a></p>
        <p>💻 GitHub: <a href="https://github.com/your-github" target="_blank">your-github</a></p>
    </div>
""", unsafe_allow_html=True)

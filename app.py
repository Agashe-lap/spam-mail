import streamlit as st
import re
from langchain_groq import ChatGroq
import json

# Setup ChatGroq LLM with model and API key
llm = ChatGroq(
    temperature=0,
    groq_api_key='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',  # Replace with your API key
    model_name="llama-3.3-70b-versatile"
)

# Function to preprocess the email text
def preprocess_text(text):
    text = text.lower()
    text = re.sub(r'[^a-z\s]', '', text)  # Removing non-alphabet characters
    return text

# Function to classify the text using the ChatGroq LLM
def classify_text_with_chatgroq(sender, subject, body):
    combined_text = f"Sender: {sender}\nSubject: {subject}\nBody: {body}"
    clean_text = preprocess_text(combined_text)
    
    # Query the ChatGroq model to check if the email is spam
    response = llm.invoke(f"Is this email spam? {clean_text}")
    
    # Debug print
    print(response)
    
    # Return classification
    if "spam" in response.content.lower():
        return "Spam"
    else:
        return "Not Spam"

# Set up the Streamlit UI
st.set_page_config(page_title="Spam Mail Detection with ChatGroq", page_icon="📧", layout="wide")

# Custom CSS for styling
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
        .input-box {
            font-size: 18px;
            padding: 15px;
            border-radius: 10px;
            width: 100%;
            max-width: 800px;
            margin-top: 10px;
        }
        .button {
            background-color: #2563EB;
            color: white;
            font-weight: bold;
            border-radius: 12px;
            padding: 20px 40px;
            cursor: pointer;
            font-size: 22px;
            display: block;
            margin-left: auto;
            margin-right: auto;
            width: 50%;
            margin-top: 20px;
        }
        .button:hover {
            background-color: #1D4ED8;
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

# UI components
st.markdown('<div class="title">Spam Mail Detection with ChatGroq</div>', unsafe_allow_html=True)
st.markdown('<div class="subheader">Enter the sender, subject, and body of the email to predict whether it is spam or not.</div>', unsafe_allow_html=True)

# Input form
with st.form(key='email_form', clear_on_submit=True):
    sender_email = st.text_input("Sender Email ID", placeholder="e.g., spammer@example.com")
    email_subject = st.text_input("Email Subject", placeholder="e.g., Congratulations! You've won")
    email_body = st.text_area("Email Body", height=200, placeholder="Paste the email content here...")
    submit_button = st.form_submit_button(label="Predict", use_container_width=True)

# Display result
if submit_button:
    if sender_email and email_subject and email_body:
        result = classify_text_with_chatgroq(sender_email, email_subject, email_body)
        st.markdown(f'<div class="prediction">{result}</div>', unsafe_allow_html=True)
    else:
        st.warning("Please fill in all fields: Sender Email, Subject, and Body.")

# Contact Us Section
st.markdown("""
    <hr style="margin-top: 50px; margin-bottom: 20px;">
    <div style="text-align: center;">
        <h3>📬 Contact Us</h3>
        <p>If you have any questions, feedback, or suggestions, feel free to reach out!</p>
        <p>📧 Email: <a href="mailto:yourname@example.com">yourname@example.com</a></p>
        <p>💻 GitHub: <a href="https://github.com/your-github" target="_blank">your-github</a></p>
    </div>
""", unsafe_allow_html=True)

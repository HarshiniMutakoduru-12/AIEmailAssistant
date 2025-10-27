# model_utils.py
import re
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import google.generativeai as genai
from config import GEMINI_API_KEY, SENDER_EMAIL, EMAIL_PASSWORD, SMTP_HOST, SMTP_PORT, MODEL_NAME
import streamlit as st

@st.cache_resource
def init_model():
    """Initialize and return the Gemini model."""
    genai.configure(api_key=GEMINI_API_KEY)
    return genai.GenerativeModel(MODEL_NAME)

def send_email(recipient: str, subject: str, body: str):
    """Send an email using SMTP."""
    msg = MIMEMultipart()
    msg['From'] = SENDER_EMAIL
    msg['To'] = recipient
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
        server.starttls()
        server.login(SENDER_EMAIL, EMAIL_PASSWORD)
        server.send_message(msg)

def process_message(prompt: str, model):
    """Process user input and return Gemini or email response."""
    try:
        # Email sending logic
        if "send" in prompt.lower() and "@" in prompt and st.session_state.current_email:
            emails = re.findall(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", prompt)
            if emails:
                recipient = emails[0]
                subject_match = re.search(r"Subject:\s*(.+)", st.session_state.current_email)
                subject = subject_match.group(1) if subject_match else "Email"
                body = re.sub(r"Subject:\s*.+\n", "", st.session_state.current_email)

                send_email(recipient, subject, body)
                return f'<div class="status success">✅ Email sent to {recipient}</div>'

        # Context
        context = "\n".join([f"{m['role']}: {m['content'][:100]}" for m in st.session_state.messages[-4:]])

        # Check if it’s an email request
        is_email = any(kw in prompt.lower() for kw in ["email", "mail", "letter", "application"])
        if is_email:
            prompt_text = f"""Generate a professional email for: {prompt}

Include:
- Subject: [subject line]
- Greeting
- Body
- Closing
- [Your Name]"""
        else:
            prompt_text = f"Context: {context}\n\nUser: {prompt}\n\nProvide a helpful response:"

        # Get Gemini response
        response = model.generate_content(prompt_text)
        result = response.text

        # Format email output
        if "Subject:" in result:
            st.session_state.current_email = result
            subject = re.search(r"Subject:\s*(.+)", result)
            if subject:
                return f"""
                <div class="email-preview">
                    <div class="email-header">
                        <div class="email-icon">📧</div>
                        <div class="email-title">{subject.group(1)}</div>
                    </div>
                    <div class="email-content">{re.sub(r"Subject:.+", "", result).strip()}</div>
                </div>
                """
        return result.replace('\n', '<br>')

    except Exception as e:
        return f'<div class="status error">Error: {str(e)}</div>'

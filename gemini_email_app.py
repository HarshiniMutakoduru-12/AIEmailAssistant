import streamlit as st
import google.generativeai as genai
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import re
from datetime import datetime
import uuid
import json
import base64

# =============================
# CONFIGURATION
# =============================
GEMINI_API_KEY = 'AIzaSyBILtif-gaLIXpQCU0ZUhUfvnsbKVuWu04'
SENDER_EMAIL = 'dhilip.softsuave@gmail.com'
EMAIL_PASSWORD = 'yzwv lqjt ilnx jqmw'

# Page config
st.set_page_config(
    page_title="Gemini",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Advanced CSS Design
def load_css():
    st.markdown("""
    <style>
    /* Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* Variables */
    :root {
        --primary: #4285F4;
        --primary-dark: #1967D2;
        --surface: #FFFFFF;
        --surface-variant: #F8F9FA;
        --on-surface: #202124;
        --on-surface-variant: #5F6368;
        --outline: #DADCE0;
        --shadow-1: 0 1px 2px 0 rgba(60,64,67,0.3);
        --shadow-2: 0 2px 6px 2px rgba(60,64,67,0.15);
    }
    
    /* Reset */
    * {
        margin: 0;
        padding: 0;
        box-sizing: border-box;
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    
    /* Hide Streamlit */
    #MainMenu, footer, header { visibility: hidden; }
    .stDeployButton { display: none; }
    [data-testid="stDecoration"] { display: none; }
    
    /* Main Layout */
    .stApp {
        background: linear-gradient(180deg, #FFFFFF 0%, #F8F9FA 100%);
        min-height: 100vh;
    }
    
    .main .block-container {
        padding: 0 !important;
        max-width: 100% !important;
    }
    
    /* Header Bar */
    .app-header {
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        height: 64px;
        background: rgba(255, 255, 255, 0.95);
        backdrop-filter: blur(10px);
        border-bottom: 1px solid var(--outline);
        z-index: 1000;
        display: flex;
        align-items: center;
        padding: 0 24px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
    }
    
    .logo-container {
        display: flex;
        align-items: center;
        gap: 12px;
    }
    
    .logo-icon {
        width: 32px;
        height: 32px;
        background: conic-gradient(from 180deg at 50% 50%, #4285F4 0deg, #DB4437 90deg, #F4B400 180deg, #0F9D58 270deg, #4285F4 360deg);
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        animation: rotate 10s linear infinite;
    }
    
    @keyframes rotate {
        to { transform: rotate(360deg); }
    }
    
    .logo-text {
        font-size: 22px;
        font-weight: 500;
        color: var(--on-surface);
        letter-spacing: -0.5px;
    }
    
    /* Chat Area */
    .chat-area {
        max-width: 1000px;
        margin: 80px auto 120px;
        padding: 24px;
        animation: fadeIn 0.5s ease;
    }
    
    @keyframes fadeIn {
        from { opacity: 0; }
        to { opacity: 1; }
    }
    
    /* Messages */
    .message-group {
        margin: 32px 0;
        animation: slideUp 0.3s ease;
    }
    
    @keyframes slideUp {
        from { 
            opacity: 0;
            transform: translateY(20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    /* User Message */
    .user-bubble {
        max-width: 70%;
        margin-left: auto;
        background: linear-gradient(135deg, #4285F4 0%, #1967D2 100%);
        color: white;
        padding: 14px 20px;
        border-radius: 24px 24px 8px 24px;
        font-size: 15px;
        line-height: 1.5;
        box-shadow: var(--shadow-1);
        word-wrap: break-word;
    }
    
    /* Assistant Message */
    .ai-message-container {
        display: flex;
        gap: 16px;
        align-items: flex-start;
    }
    
    .ai-avatar {
        width: 40px;
        height: 40px;
        border-radius: 50%;
        background: linear-gradient(135deg, #4285F4, #DB4437, #F4B400, #0F9D58);
        display: flex;
        align-items: center;
        justify-content: center;
        box-shadow: var(--shadow-1);
        flex-shrink: 0;
    }
    
    .ai-avatar-icon {
        color: white;
        font-size: 20px;
        font-weight: 600;
    }
    
    .ai-content {
        flex: 1;
        max-width: calc(100% - 56px);
    }
    
    .ai-message {
        background: var(--surface);
        border: 1px solid var(--outline);
        padding: 16px 20px;
        border-radius: 8px 24px 24px 24px;
        font-size: 15px;
        line-height: 1.6;
        color: var(--on-surface);
        box-shadow: 0 2px 8px rgba(0,0,0,0.06);
    }
    
    /* Rich Content Formatting */
    .ai-message h1, .ai-message h2, .ai-message h3 {
        margin: 16px 0 8px;
        font-weight: 600;
    }
    
    .ai-message p {
        margin: 12px 0;
    }
    
    .ai-message ul, .ai-message ol {
        margin: 12px 0;
        padding-left: 24px;
    }
    
    .ai-message code {
        background: var(--surface-variant);
        padding: 2px 8px;
        border-radius: 4px;
        font-family: 'Monaco', monospace;
        font-size: 13px;
        color: #D73502;
    }
    
    .ai-message pre {
        background: #1E1E1E;
        color: #D4D4D4;
        padding: 16px;
        border-radius: 8px;
        overflow-x: auto;
        margin: 16px 0;
    }
    
    /* Email Card Design */
    .email-preview {
        background: linear-gradient(135deg, var(--surface-variant) 0%, var(--surface) 100%);
        border: 2px solid var(--outline);
        border-radius: 16px;
        padding: 20px;
        margin: 16px 0;
        box-shadow: 0 4px 12px rgba(0,0,0,0.08);
    }
    
    .email-header {
        display: flex;
        align-items: center;
        gap: 12px;
        padding-bottom: 12px;
        border-bottom: 2px solid var(--outline);
        margin-bottom: 16px;
    }
    
    .email-icon {
        width: 32px;
        height: 32px;
        background: var(--primary);
        border-radius: 8px;
        display: flex;
        align-items: center;
        justify-content: center;
        color: white;
    }
    
    .email-title {
        font-size: 18px;
        font-weight: 600;
        color: var(--on-surface);
    }
    
    .email-content {
        color: var(--on-surface-variant);
        line-height: 1.6;
        white-space: pre-wrap;
    }
    
    /* Action Toolbar */
    .action-toolbar {
        display: flex;
        gap: 8px;
        margin-top: 12px;
        padding-top: 12px;
        border-top: 1px solid rgba(0,0,0,0.05);
    }
    
    .action-btn {
        background: transparent;
        border: none;
        width: 36px;
        height: 36px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        cursor: pointer;
        transition: all 0.2s;
        color: var(--on-surface-variant);
    }
    
    .action-btn:hover {
        background: var(--surface-variant);
        transform: scale(1.1);
    }
    
    .action-btn.active {
        background: var(--primary);
        color: white;
    }
    
    /* Input Section */
    .input-section {
        position: fixed;
        bottom: 0;
        left: 0;
        right: 0;
        background: rgba(255, 255, 255, 0.98);
        backdrop-filter: blur(10px);
        border-top: 1px solid var(--outline);
        padding: 16px 24px;
        z-index: 999;
        box-shadow: 0 -2px 10px rgba(0,0,0,0.05);
    }
    
    .input-container {
        max-width: 1000px;
        margin: 0 auto;
        display: flex;
        gap: 12px;
        align-items: center;
    }
    
    .input-field {
        flex: 1;
        background: var(--surface-variant);
        border: 2px solid transparent;
        border-radius: 28px;
        padding: 12px 24px;
        font-size: 15px;
        transition: all 0.3s;
        display: flex;
        align-items: center;
    }
    
    .input-field:focus-within {
        background: var(--surface);
        border-color: var(--primary);
        box-shadow: 0 0 0 4px rgba(66, 133, 244, 0.1);
    }
    
    .stTextArea textarea {
        background: transparent !important;
        border: none !important;
        padding: 0 !important;
        font-size: 15px !important;
        resize: none !important;
    }
    
    /* Send Button */
    .send-btn {
        width: 48px;
        height: 48px;
        border-radius: 50%;
        background: linear-gradient(135deg, var(--primary) 0%, var(--primary-dark) 100%);
        border: none;
        display: flex;
        align-items: center;
        justify-content: center;
        cursor: pointer;
        transition: all 0.3s;
        box-shadow: var(--shadow-1);
    }
    
    .send-btn:hover {
        transform: scale(1.05);
        box-shadow: var(--shadow-2);
    }
    
    .send-btn:active {
        transform: scale(0.95);
    }
    
    /* Welcome Screen */
    .welcome {
        text-align: center;
        padding: 80px 20px;
        animation: fadeIn 0.8s ease;
    }
    
    .welcome-emoji {
        font-size: 64px;
        margin-bottom: 24px;
        animation: wave 2s ease-in-out infinite;
    }
    
    @keyframes wave {
        0%, 100% { transform: rotate(0deg); }
        25% { transform: rotate(-10deg); }
        75% { transform: rotate(10deg); }
    }
    
    .welcome-title {
        font-size: 36px;
        font-weight: 300;
        color: var(--on-surface);
        margin-bottom: 8px;
    }
    
    .welcome-subtitle {
        font-size: 18px;
        color: var(--on-surface-variant);
        margin-bottom: 48px;
    }
    
    /* Suggestion Cards */
    .suggestions {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
        gap: 16px;
        max-width: 800px;
        margin: 0 auto;
    }
    
    .suggestion-card {
        background: var(--surface);
        border: 1px solid var(--outline);
        border-radius: 12px;
        padding: 16px;
        cursor: pointer;
        transition: all 0.3s;
        text-align: left;
    }
    
    .suggestion-card:hover {
        transform: translateY(-4px);
        box-shadow: var(--shadow-2);
        border-color: var(--primary);
    }
    
    .suggestion-icon {
        font-size: 24px;
        margin-bottom: 8px;
    }
    
    .suggestion-text {
        font-size: 14px;
        color: var(--on-surface);
        font-weight: 500;
    }
    
    /* Status Indicators */
    .status {
        display: inline-flex;
        align-items: center;
        gap: 8px;
        padding: 8px 16px;
        border-radius: 20px;
        font-size: 14px;
        font-weight: 500;
        margin: 8px 0;
    }
    
    .status.success {
        background: #E6F4EA;
        color: #1E8E3E;
    }
    
    .status.error {
        background: #FCE8E6;
        color: #D33B27;
    }
    
    /* Loading Animation */
    .typing {
        display: flex;
        gap: 4px;
        padding: 16px;
    }
    
    .typing-dot {
        width: 8px;
        height: 8px;
        background: var(--primary);
        border-radius: 50%;
        animation: typing-animation 1.4s infinite ease-in-out;
    }
    
    .typing-dot:nth-child(1) { animation-delay: -0.32s; }
    .typing-dot:nth-child(2) { animation-delay: -0.16s; }
    .typing-dot:nth-child(3) { animation-delay: 0; }
    
    @keyframes typing-animation {
        0%, 80%, 100% {
            transform: scale(0.8);
            opacity: 0.5;
        }
        40% {
            transform: scale(1);
            opacity: 1;
        }
    }
    
    /* Responsive */
    @media (max-width: 768px) {
        .chat-area {
            padding: 16px;
        }
        
        .user-bubble {
            max-width: 85%;
        }
        
        .suggestions {
            grid-template-columns: 1fr;
        }
    }
    </style>
    """, unsafe_allow_html=True)

# Initialize session state
def init_session_state():
    if 'messages' not in st.session_state:
        st.session_state.messages = []
    if 'model' not in st.session_state:
        st.session_state.model = None
    if 'current_email' not in st.session_state:
        st.session_state.current_email = None
    if 'feedback' not in st.session_state:
        st.session_state.feedback = {}
    if 'input_key' not in st.session_state:  # Added for clearing input
        st.session_state.input_key = 0


		

# Initialize Gemini
@st.cache_resource
def init_model():
    try:
        genai.configure(api_key=GEMINI_API_KEY)
        return genai.GenerativeModel('gemini-2.5-flash')
    except:
        return None

# Process message
def process_message(prompt, model):
    try:
        # Email sending check
        if "send" in prompt.lower() and "@" in prompt and st.session_state.current_email:
            emails = re.findall(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', prompt)
            if emails:
                recipient = emails[0]
                subject_match = re.search(r"Subject:\s*(.+)", st.session_state.current_email)
                subject = subject_match.group(1) if subject_match else "Email"
                body = re.sub(r"Subject:\s*.+\n", "", st.session_state.current_email)
                
                try:
                    smtp_host, smtp_port = ('smtp.gmail.com', 587)
                    msg = MIMEMultipart()
                    msg['From'] = SENDER_EMAIL
                    msg['To'] = recipient
                    msg['Subject'] = subject
                    msg.attach(MIMEText(body, 'plain'))
                    
                    with smtplib.SMTP(smtp_host, smtp_port) as server:
                        server.starttls()
                        server.login(SENDER_EMAIL, EMAIL_PASSWORD)
                        server.send_message(msg)
                    
                    return f'<div class="status success">✅ Email sent to {recipient}</div>'
                except Exception as e:
                    return f'<div class="status error">❌ Failed: {str(e)}</div>'
        
        # Build context
        context = "\n".join([f"{m['role']}: {m['content'][:100]}" for m in st.session_state.messages[-4:]])
        
        # Check email generation
        is_email = any(kw in prompt.lower() for kw in ["email", "mail", "letter", "application"])
        
        if is_email:
            prompt_text = f"""Generate a professional email for: {prompt}

Include:
- Subject: [subject line]
- Proper greeting
- Professional body
- Appropriate closing
- [Your Name]"""
        else:
            prompt_text = f"Context: {context}\n\nUser: {prompt}\n\nProvide a helpful response:"
        
        response = model.generate_content(prompt_text)
        result = response.text
        
        # Format email
        if "Subject:" in result:
            st.session_state.current_email = result
            subject = re.search(r"Subject:\s*(.+)", result)
            if subject:
                return f'''<div class="email-preview">
<div class="email-header">
    <div class="email-icon">📧</div>
    <div class="email-title">{subject.group(1)}</div>
</div>
<div class="email-content">{re.sub(r"Subject:.+", "", result).strip()}</div>
</div>'''
        
        return result.replace('\n', '<br>')
        
    except Exception as e:
        return f'<div class="status error">Error: {str(e)}</div>'

# Main UI
def main():
    init_session_state()
    load_css()
    
    # Initialize model
    if st.session_state.model is None:
        st.session_state.model = init_model()
    
    # Header
    st.markdown("""
    <div class="app-header">
        <div class="logo-container">
            <div class="logo-icon">
                <span style="color: white; font-size: 18px;">✨</span>
            </div>
            <div class="logo-text">Gemini</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Chat Area
    st.markdown('<div class="chat-area">', unsafe_allow_html=True)
    
    if not st.session_state.messages:
        # Welcome Screen
        st.markdown("""
        <div class="welcome">
            <div class="welcome-emoji">👋</div>
            <h1 class="welcome-title">Hello, Friends!</h1>
            <p class="welcome-subtitle">How can I help you today?</p>          
        </div>
        """, unsafe_allow_html=True)
    else:
        # Display messages
        for idx, msg in enumerate(st.session_state.messages):
            if msg['role'] == 'user':
                st.markdown(f"""
                <div class="message-group">
                    <div style="display: flex; justify-content: flex-end;">
                        <div class="user-bubble">{msg['content']}</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            else:
                msg_id = f"msg_{idx}"
                st.markdown(f"""
                <div class="message-group">
                    <div class="ai-message-container">
                        <div class="ai-avatar">
                            <span class="ai-avatar-icon">✨</span>
                        </div>
                        <div class="ai-content">
                            <div class="ai-message">{msg['content']}</div>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                # Action buttons
                cols = st.columns([1, 1, 1, 1, 1, 20])
                
                with cols[0]:
                    if st.button("👍", key=f"like_{idx}"):
                        st.session_state.feedback[msg_id] = 'like'
                        st.toast("Thanks for your feedback!", icon="👍")
                
                with cols[1]:
                    if st.button("👎", key=f"dislike_{idx}"):
                        st.session_state.feedback[msg_id] = 'dislike'
                        st.toast("We'll improve!", icon="👎")
                
                with cols[2]:
                    if st.button("🔄", key=f"regen_{idx}"):
                        if idx > 0:
                            with st.spinner("Regenerating..."):
                                prev = st.session_state.messages[idx-1]['content']
                                new_response = process_message(prev, st.session_state.model)
                                st.session_state.messages[idx]['content'] = new_response
                                st.rerun()
                
                with cols[3]:
                    if st.button("📋", key=f"copy_{idx}"):
                        clean = re.sub('<.*?>', '', msg['content'])
                        st.code(clean)
                
                with cols[4]:
                    if st.button("🔗", key=f"share_{idx}"):
                        st.toast("Link copied!", icon="✅")
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Input Section with clearing functionality
    st.markdown('<div class="input-section">', unsafe_allow_html=True)
    
    col1, col2 = st.columns([20, 1])
    
    with col1:
        user_input = st.text_area(
            "",
            placeholder="Ask anything...",
            height=50,
            key=f"input_{st.session_state.input_key}",  # Dynamic key for clearing
            label_visibility="collapsed"
        )
    
    with col2:
        if st.button("➤", key="send", use_container_width=True):
            if user_input:
                # Add user message
                st.session_state.messages.append({
                    'role': 'user',
                    'content': user_input,
                    'id': str(uuid.uuid4())
                })
                
                # Generate response
                with st.spinner(""):
                    response = process_message(user_input, st.session_state.model)
                
                # Add AI message
                st.session_state.messages.append({
                    'role': 'assistant',
                    'content': response,
                    'id': str(uuid.uuid4())
                })
                
                # Clear input by incrementing the key
                st.session_state.input_key += 1
                
                st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()
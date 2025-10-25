# Gemini Email Assistant - Full Chatbot with Email Features

A sophisticated Streamlit application that mimics Gemini's UI with complete chatbot functionality, email generation, translation, and automatic sending capabilities.

## ✨ Features

### Core Capabilities
- **Full Gemini-like Chatbot**: Natural conversation with context retention
- **Email Generation**: Professional emails from simple prompts
- **Multi-language Translation**: Translate emails to any language
- **Automatic Email Sending**: Send emails with natural commands
- **Message History**: Complete chat history with timestamps
- **Edit & Regenerate**: Edit past messages and regenerate responses
- **Smart SMTP Detection**: Automatically configures based on email domain

### UI Features (Gemini-style)
- **Modern Chat Interface**: Beautiful gradient messages
- **Live Email Preview**: See and edit generated emails
- **Message Actions**: Edit, regenerate, copy any message
- **Quick Actions**: Example prompts for easy start
- **Export Chat**: Download conversation history
- **Responsive Design**: Clean, modern interface

## 🚀 Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements_gemini.txt
```

### 2. Configuration
The app is **pre-configured** with your credentials:
- ✅ Gemini API Key: Already set
- ✅ Email: dhilip.softsuave@gmail.com
- ✅ App Password: Already configured
- ✅ SMTP: Auto-detected (Gmail)

### 3. Run the Application
```bash
streamlit run gemini_email_app.py
```

The app will open at `http://localhost:8501`

## 💬 How to Use

### Email Generation
Type naturally, just like chatting with Gemini:
- "Generate a sick leave email for 2 days"
- "Write a resignation letter with 30 days notice"
- "Create a job application for software developer"
- "Draft a meeting request for next Monday"

### Translation
After generating an email:
- "Translate to Spanish"
- "Convert this to French"
- "Make it in Hindi"
- "Translate to Japanese"
- Works with ANY language!

### Sending Emails
Natural language commands:
- "Send the email to manager@company.com"
- "Email this to hr@example.com"
- "Forward to john.doe@gmail.com"

Or use the Quick Send panel on the right.

### Chat Features

#### Edit Messages
- Hover over any user message
- Click "✏️ Edit" to modify
- Save changes to regenerate response

#### Regenerate Responses
- Click "🔄 Regenerate" on any assistant message
- Get a fresh response for the same query

#### Message Actions
- **Copy**: Copy any message to clipboard
- **Set as Current**: Set any email as the active one
- **Export**: Download entire conversation

### General Chatbot
Ask anything, just like Gemini:
- "What's the weather like?"
- "Explain quantum computing"
- "Help me with Python code"
- "Tell me a joke"

## 🎯 Example Workflows

### Complete Email Workflow
1. **Generate**: "Create a leave application for tomorrow"
2. **Review**: Email appears in preview panel
3. **Translate**: "Translate to Hindi"
4. **Send**: "Send to manager@office.com"

### Edit and Regenerate
1. Type your request
2. If not satisfied, click "🔄 Regenerate"
3. Or edit your message and save for new response

### Multi-turn Conversation
```
You: Generate a project update email
Gemini: [Creates email]
You: Make it more detailed
Gemini: [Adds details]
You: Add budget information
Gemini: [Includes budget]
You: Perfect, send to team@company.com
Gemini: ✅ Email sent successfully!
```

## 🔧 Technical Details

### Automatic SMTP Configuration
The app automatically detects SMTP settings:
- Gmail → smtp.gmail.com:587
- Outlook → smtp-mail.outlook.com:587
- Yahoo → smtp.mail.yahoo.com:587
- Corporate Gmail → Uses Gmail SMTP

### Session Management
- Maintains complete chat history
- Preserves context across messages
- Remembers current email for modifications
- Tracks message timestamps

### Security
- Uses app passwords (not regular passwords)
- Secure SMTP with TLS encryption
- No credentials stored in browser

## 🎨 UI Features

### Chat Interface
- **Gradient user messages**: Purple gradient bubbles
- **Clean assistant messages**: Light gray with border
- **Hover actions**: Edit/regenerate on hover
- **Smooth animations**: Fade-in effects

### Email Preview Panel
- **Live preview**: See email as you chat
- **Editable content**: Modify before sending
- **Quick send**: One-click sending
- **Subject extraction**: Automatic subject detection

### Status Indicators
- ✅ Success messages in green
- ❌ Error messages in red
- 🔄 Loading animations
- Timestamps on all messages

## 📝 Commands Reference

### Email Commands
- `generate [type] email` - Create emails
- `translate to [language]` - Translate content
- `send to [email]` - Send to recipient
- `make it [formal/shorter/longer]` - Modify

### Chat Commands
- Ask any question naturally
- Request explanations
- Get help with tasks
- Have conversations

## 🐛 Troubleshooting

### Email Not Sending
- Check internet connection
- Verify app password is correct
- Ensure recipient email is valid

### Translation Issues
- Be specific about target language
- Use standard language names

### Regeneration
- Previous context is maintained
- Click regenerate for fresh response

## 🔑 Keyboard Shortcuts
- `Enter` - New line in message
- `Ctrl/Cmd + Enter` - Send message (when focused)
- `Ctrl/Cmd + C` - Copy selected text

## 📊 Features Summary

| Feature | Status | Description |
|---------|--------|-------------|
| Email Generation | ✅ | Professional emails from prompts |
| Translation | ✅ | Any language supported |
| Email Sending | ✅ | Direct SMTP sending |
| Chat History | ✅ | Complete conversation log |
| Edit Messages | ✅ | Modify and regenerate |
| Export Chat | ✅ | Download conversations |
| Auto-SMTP | ✅ | Automatic configuration |
| Context Retention | ✅ | Remembers conversation |

## 🌟 Pro Tips

1. **Chain Commands**: Generate → Translate → Send in one flow
2. **Edit for Perfection**: Edit messages to refine responses
3. **Use Examples**: Click example prompts to start quickly
4. **Export Important Chats**: Save conversations for reference
5. **Natural Language**: Talk naturally, like with Gemini

## 📄 License

This application is ready to use with your configured credentials.

---

**Note**: Your credentials are already configured in the code. The app works immediately upon running!
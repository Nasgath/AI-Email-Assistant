# AI Email Assistant

This is a professional AI Email Assistant built with **Streamlit** and **OpenRouter API (LLaMA 3 8B Instruct model)**.  
It understands email instructions, drafts emails, follow-ups, acknowledgments, or provides step-by-step guidance based on user input.

## Features
- Draft professional emails based on instructions
- Provide step-by-step guidance or clarification requests
- Maintains session history
- Download conversation history as CSV
- Sample instructions and demo-ready UI

## Requirements
- Python 3.9+
- Streamlit
- Requests library

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/Nasgath/AI-Email-Assistant.git


# ================================
# AI Email Assistant - Full Setup
# ================================

# 1. Navigate to the folder where you want the project
cd C:\Users\hp\Documents\Projects   # change path if needed

# 2. Clone the GitHub repository
git clone https://github.com/Nasgath/AI-Email-Assistant.git
cd AI-Email-Assistant

# 3. (Optional) Create and activate a clean virtual environment
conda create -n ai_email python=3.11 -y
conda activate ai_email

# 4. Install required Python packages
pip install streamlit requests

# 5. Open the project file to add your API key
# Open 'email_assistant_app3.py' in any editor
# Find the line: API_KEY = ""
# Replace with your API key: API_KEY = "YOUR_API_KEY_HERE"
# Save the file

# 6. Run the Streamlit app
streamlit run email_assistant_app3.py

# ================================
# Using the AI Email Assistant
# ================================

# Type instructions such as:
# - "Send acknowledgment for submitted files"
# - "Follow up with manager on pending approval"
# - "Reply to client about project status"
# Click "Generate Email" to see professional responses.

# Clear session button removes all current generated emails.
# Download Chat History button saves emails to CSV.

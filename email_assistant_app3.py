# email_assistant_app2.py
import streamlit as st
import requests
import csv
import os

# -----------------------
# Configuration
# -----------------------
API_KEY = ""  # <-- Replace with your OpenRouter API key
URL = "https://openrouter.ai/api/v1/chat/completions"

# Folder to store CSV
DATA_FOLDER = "data"
if not os.path.exists(DATA_FOLDER):
    os.makedirs(DATA_FOLDER)

HISTORY_FILE = os.path.join(DATA_FOLDER, "email_history.csv")

# -----------------------
# Functions
# -----------------------

def ask_ai(messages):
    """Send conversation messages to AI and return assistant response"""
    data = {
        "model": "meta-llama/llama-3-8b-instruct",
        "messages": messages
    }
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    response = requests.post(URL, headers=headers, json=data)
    if response.status_code == 200:
        try:
            return response.json()["choices"][0]["message"]["content"]
        except:
            return "Error: Unexpected response format"
    else:
        return f"Error: {response.status_code} - {response.text}"

def save_to_csv(user_input, assistant_reply):
    """Save instruction and assistant response to CSV"""
    try:
        file_exists = os.path.isfile(HISTORY_FILE)
        with open(HISTORY_FILE, mode='a', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=["Instruction", "Assistant"])
            if not file_exists:
                writer.writeheader()
            writer.writerow({"Instruction": user_input, "Assistant": assistant_reply})
    except Exception as e:
        st.error(f"Error saving CSV: {e}")

# -----------------------
# Streamlit UI
# -----------------------
st.set_page_config(page_title="AI Email Assistant", page_icon="📧")
st.title("📧 DataZoic Email Assistant")
st.write("""
This assistant reads your email or instruction carefully, understands the intent, and provides a **clear, relevant, professional response**.
It will not generate generic emails. You can also ask for **step-by-step guidance, acknowledgment emails, follow-ups, or draft replies**.
""")
st.write("Example instructions you can try:")
st.markdown("""
**Sample Instructions to Try:**
- Acknowledgment: "Send acknowledgment for submitted files"
- Follow-up: "Follow up with manager on pending approval"
- Draft reply: "Reply to client about project status"
- Clarification: "Ask sender for missing details politely"
""")


# Initialize conversation and history
if "conversation" not in st.session_state:
    st.session_state.conversation = []
if "history" not in st.session_state:
    st.session_state.history = []

# User input
user_input = st.text_input("Your Instruction / Email Content:")

# Generate AI response
if st.button("Get AI Response"):
    if user_input.strip() != "":
        # Professional assistant prompt: understand intent, give relevant response
        prompt = f"""
You are a professional AI Email Assistant. 

Requirements:
1. Understand the user's request in detail.
2. Provide a clear, specific, and relevant response.
3. Maintain a professional tone.
4. Do not generate generic responses.
5. If needed, provide step-by-step instructions or draft emails.
6. If clarification is required, politely ask the user.

User said: {user_input}
"""

        # Append user message
        st.session_state.conversation.append({"role": "user", "content": prompt})

        # Ask AI
        with st.spinner("Analyzing request..."):
            reply = ask_ai(st.session_state.conversation)
            st.session_state.conversation.append({"role": "assistant", "content": reply})
            st.session_state.history.append({"Instruction": user_input, "Assistant": reply})
            save_to_csv(user_input, reply)
    else:
        st.warning("Please enter your instruction or email content!")

# Clear session
if st.button("Clear Session"):
    st.session_state.conversation = []
    st.session_state.history = []
    st.success("Session cleared! Previous responses removed from view.")

# Display history
if st.session_state.history:
    st.subheader("AI Email Assistant History")
    for idx, item in enumerate(reversed(st.session_state.history), 1):
        st.markdown(f"**{idx}. Instruction / Email:** {item['Instruction']}")
        st.markdown(f"**Assistant Response:**\n{item['Assistant']}")
        st.markdown("---")

# Download CSV button
if os.path.isfile(HISTORY_FILE):
    with open(HISTORY_FILE, "r", encoding="utf-8") as f:
        csv_data = f.read()
    st.download_button(
        label="Download Full Chat History",
        data=csv_data,
        file_name="email_history.csv",
        mime="text/csv"
    )

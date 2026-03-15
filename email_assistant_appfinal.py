# email_assistant_appfinal.py
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
def ask_ai(prompt):
    """Call the AI API and return the response."""
    data = {
        "model": "meta-llama/llama-3-8b-instruct",
        "messages": [{"role": "user", "content": prompt}]
    }
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    response = requests.post(URL, headers=headers, json=data)
    if response.status_code == 200:
        try:
            return response.json()["choices"][0]["message"]["content"]
        except (KeyError, IndexError):
            return "Error: Unexpected response format"
    else:
        return f"Error: {response.status_code} - {response.text}"

def generate_email(instruction):
    """Generate professional email from user instruction."""
    # Strict prompt: generate ready-to-use draft, no extra questions
    prompt = f"""
You are an AI professional email assistant.
Read this instruction carefully and generate 2-3 professional email drafts exactly as requested.
Do NOT ask the user for more information.
Keep the tone professional and concise.
Instruction: {instruction}
"""
    return ask_ai(prompt)

def save_to_csv(instruction, email):
    """Append a new email to CSV file safely."""
    try:
        file_exists = os.path.isfile(HISTORY_FILE)
        with open(HISTORY_FILE, mode='a', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=["Instruction", "Email"])
            if not file_exists:
                writer.writeheader()
            writer.writerow({"Instruction": instruction, "Email": email})
    except Exception as e:
        st.error(f"Error saving CSV: {e}")

# -----------------------
# Streamlit UI
# -----------------------
st.set_page_config(page_title="📧 DataZoic Email Assistant", page_icon="📧")
st.title("📧 DataZoic Email Assistant")
st.write("This assistant reads your email or instruction carefully, understands the intent, and provides a clear, relevant, professional response. It will not generate generic emails. You can ask for step-by-step guidance, acknowledgment emails, follow-ups, or draft replies.")

st.markdown("""
**Sample Instructions to Try:**
- Acknowledgment: "Send acknowledgment for submitted files"
- Follow-up: "Follow up with manager on pending approval"
- Draft reply: "Reply to client about project status"
- Clarification: "Ask sender for missing details politely"
""")

# Initialize session state (fresh on every startup)
if "history" not in st.session_state:
    st.session_state.history = []

# Input box
user_input = st.text_input("Your Instruction / Email Content:")

# Generate email button
if st.button("Generate Email"):
    if user_input.strip() != "":
        with st.spinner("Generating email drafts..."):
            email = generate_email(user_input)
            st.session_state.history.append({"Instruction": user_input, "Email": email})
            save_to_csv(user_input, email)
    else:
        st.warning("Please enter an instruction!")

# Clear session button
if st.button("Clear Current Session"):
    st.session_state.history = []
    st.success("Session cleared! Generated emails removed from display.")

# Display current session history
if st.session_state.history:
    st.subheader("AI Email Assistant History")
    for idx, item in enumerate(reversed(st.session_state.history), 1):
        st.markdown(f"**{idx}. Instruction / Email:** {item['Instruction']}")
        st.markdown(f"**Assistant Response:** {item['Email']}")
        st.markdown("---")

# Download CSV button if file exists
if os.path.isfile(HISTORY_FILE):
    with open(HISTORY_FILE, "r", encoding="utf-8") as f:
        csv_data = f.read()
    st.download_button(
        label="Download Chat History as CSV",
        data=csv_data,
        file_name="email_history.csv",
        mime="text/csv"
    )

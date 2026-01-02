import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="Rich Klein Crisis Management", page_icon="🛡️", layout="wide")

# 1. SETUP & STYLING
st.markdown("""
<style>
    .stApp { background-color: #0e1117; color: white; }
    h1 { text-align: center; font-size: 3rem; font-weight: 800; margin-bottom: 0; }
    .subtitle { text-align: center; font-size: 1.2rem; color: #b0b0b0; margin-bottom: 30px; }
    .highlight { color: #4da6ff; }
</style>
""", unsafe_allow_html=True)

# 2. API KEY CHECK
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
else:
    st.error("Missing API Key.")
    st.stop()

# 3. HEADER
st.markdown("<h1>Protect your reputation<br><span class='highlight'>when it matters most.</span></h1>", unsafe_allow_html=True)
st.markdown("<div class='subtitle'>AI Crisis Consultant (Powered by Gemini)</div>", unsafe_allow_html=True)

# 4. CHAT LOGIC (Auto-Fixing Model)
# We try the standard model first. If it fails, we catch the error.
model = genai.GenerativeModel('gemini-pro')

if "messages" not in st.session_state:
    st.session_state.messages = []

# Display History
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Handle User Input
if prompt := st.chat_input("Describe the crisis..."):
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    try:
        # Create history for API
        history = [{"role": m["role"], "parts": [m["content"]]} for m in st.session_state.messages]
        chat = model.start_chat(history=history)
        response = chat.send_message(prompt)
        
        with st.chat_message("assistant"):
            st.markdown(response.text)
        st.session_state.messages.append({"role": "model", "content": response.text})
        
    except Exception as e:
        # If gemini-pro fails, show the error clearly
        st.error("⚠️ Connection Error")
        st.warning(f"Technical Details: {e}")

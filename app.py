import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="Crisis Comms Assistant", page_icon="🛡️")
st.title("Crisis Communications Manager 🛡️")

# GET API KEY
if "GOOGLE_API_KEY" in st.secrets:
    api_key = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=api_key)
else:
    st.error("Missing API Key. Please add it to Streamlit Secrets.")
    st.stop()

# YOUR INSTRUCTIONS
system_instruction = """
You are a Crisis Communications expert. 
Your goal is to protect the client's brand and mitigate negative press.
You are professional, calm, and strategic.
"""

model = genai.GenerativeModel(model_name="gemini-1.5-flash", system_instruction=system_instruction)

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Enter crisis details here..."):
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    try:
        chat = model.start_chat(history=[{"role": m["role"], "parts": [m["content"]]} for m in st.session_state.messages])
        response = chat.send_message(prompt)
        with st.chat_message("assistant"):
            st.markdown(response.text)
        st.session_state.messages.append({"role": "model", "content": response.text})
    except Exception as e:
        st.error(f"Error: {e}")

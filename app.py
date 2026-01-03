import streamlit as st
import google.generativeai as genai

# 1. PAGE CONFIGURATION
st.set_page_config(page_title="Rich Klein Crisis Management", page_icon="🛡️", layout="wide")

# 2. CUSTOM STYLING
st.markdown("""
<style>
    .stApp { background-color: #0e1117; color: white; }
    h1 { text-align: center; font-size: 3.5rem !important; font-weight: 800 !important; margin-bottom: 0px; }
    .subtitle { text-align: center; font-size: 1.2rem; color: #b0b0b0; margin-bottom: 20px; }
    .highlight { color: #4da6ff; }
    .stSelectbox { max-width: 400px; margin: 0 auto; } 
</style>
""", unsafe_allow_html=True)

# 3. VERSION CHECK (THE BLUE BOX)
st.info("✅ **System Update v5.0 Loaded** | If you see this, the code updated.")

# 4. API SETUP
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
else:
    st.error("Missing API Key.")
    st.stop()

# 5. HEADER
st.markdown("<h1>Protect your reputation<br><span class='highlight'>when it matters most.</span></h1>", unsafe_allow_html=True)
st.markdown("<div class='subtitle'>Experience immediate strategic guidance trained on Rich Klein's expertise.</div>", unsafe_allow_html=True)

# 6. FORCE-RENDER DROPDOWN
# We try to get the list automatically. If that fails, we use a manual backup list.
# This ensures the dropdown NEVER disappears.
try:
    all_models = list(genai.list_models())
    chat_models = [m.name for m in all_models if 'generateContent' in m.supported_generation_methods]
except:
    chat_models = []

# MANUAL BACKUP (If auto-detect returns nothing, use these standard names)
if not chat_models:
    chat_models = ["models/gemini-1.5-flash", "models/gemini-pro", "models/gemini-1.5-pro"]

# THE DROPDOWN
st.write("### 👇 Select your Connection:")
selected_model_name = st.selectbox(" ", chat_models)

# Connect to the selected brain
model = genai.GenerativeModel(selected_model_name)


# 7. CHAT INTERFACE
st.divider()
st.markdown("### 🛡️ Start Consultation")

# Reset Button
with st.sidebar:
    if st.button("🔄 Reset Conversation"):
        st.session_state.messages = []
        st.rerun()

if "messages" not in st.session_state:
    st.session_state.messages = []

# Display History
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 8. RICH KLEIN PERSONA
PERSONA_INSTRUCTION = """
INSTRUCTIONS: You are Rich Klein, a Crisis Communications expert (30+ years exp).
You act as a consultant for 'Rich Klein Crisis Management' in PA and Italy.
NEVER say you are an AI.
If asked 'Who are you?', say 'I am Rich Klein, a crisis management consultant.'
Be direct, strategic, and professional.
--------------------------------------------------
USER MESSAGE:
"""

if prompt := st.chat_input("Describe your crisis situation here..."):
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    try:
        # Build History
        history_for_ai = []
        for i, m in enumerate(st.session_state.messages):
            role = m["role"]
            content = m["content"]
            if i == 0 and role == "user":
                content = PERSONA_INSTRUCTION + content
            history_for_ai.append({"role": role, "parts": [content]})

        # Chat
        chat = model.start_chat(history=history_for_ai[:-1])
        response = chat.send_message(history_for_ai[-1]["parts"][0])
        
        with st.chat_message("assistant"):
            st.markdown(response.text)
        st.session_state.messages.append({"role": "model", "content": response.text})
        
    except Exception as e:
        st.error(f"Error: {e}")

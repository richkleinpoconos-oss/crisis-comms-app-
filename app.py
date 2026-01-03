import streamlit as st
import google.generativeai as genai

# 1. PAGE CONFIGURATION
st.set_page_config(page_title="Rich Klein Crisis Management", page_icon="🛡️", layout="wide")

# 2. CUSTOM STYLING
st.markdown("""
<style>
    .stApp { background-color: #0e1117; color: white; }
    h1 { text-align: center; font-size: 3.5rem !important; font-weight: 800 !important; margin-bottom: 0px; }
    .subtitle { text-align: center; font-size: 1.2rem; color: #b0b0b0; margin-bottom: 30px; }
    .highlight { color: #4da6ff; }
    .stTextArea textarea { height: 300px; }
</style>
""", unsafe_allow_html=True)

# 3. API SETUP
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
else:
    st.error("Missing API Key.")
    st.stop()

# 4. AUTO-DETECT MODEL (Prioritize Flash for Audio)
try:
    all_models = list(genai.list_models())
    chat_models = [m.name for m in all_models if 'generateContent' in m.supported_generation_methods]
    active_model_name = chat_models[0]
    for m in chat_models:
        if 'flash' in m:
            active_model_name = m
            break
    model = genai.GenerativeModel(active_model_name)
except:
    st.error("Connection Error. Check API Key.")
    st.stop()

# ---------------------------------------------------------
# 5. TRAINING DASHBOARD (SIDEBAR)
# ---------------------------------------------------------
with st.sidebar:
    st.header("🧠 Brain Training")
    st.info("Paste your detailed 'hours of training' text below. The AI will use this to be Rich Klein.")
    
    # Default placeholder
    default_training = """You are Rich Klein, a veteran Crisis Communications consultant (30+ years exp).
You act as a consultant for 'Rich Klein Crisis Management' in PA and Italy.
NEVER say you are an AI.
If asked 'Who are you?', say 'I am Rich Klein, a crisis management consultant.'
Be direct, strategic, and professional.
(Paste your full training details here...)"""
    
    # The Editable Training Box
    training_prompt = st.text_area("System Instructions:", value=default_training, height=400)
    
    if st.button("🔄 Reset / Apply Training"):
        st.session_state.messages = []
        st.rerun()

# 6. HERO SECTION
st.markdown("<h1>Protect your reputation<br><span class='highlight'>when it matters most.</span></h1>", unsafe_allow_html=True)
st.markdown("<div class='subtitle'>AI Crisis Consultant | Voice & Text Enabled</div>", unsafe_allow_html=True)
st.divider()

# 7. CHAT LOGIC
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# ---------------------------------------------------------
# 8. VOICE & TEXT INPUT
# ---------------------------------------------------------
audio_input = st.audio_input("🎤 Tap to Speak (Client Voice Mode)")
text_input = st.chat_input("Type details...")

user_content = None

if audio_input:
    # Voice Mode
    user_content = ["Analyze this voice recording for crisis urgency and provide strategic advice based on your training:", audio_input]
    with st.chat_message("user"):
        st.audio(audio_input)
    st.session_state.messages.append({"role": "user", "content": "🎤 *Voice Message Sent*"})

elif text_input:
    # Text Mode
    user_content = text_input
    with st.chat_message("user"):
        st.markdown(text_input)
    st.session_state.messages.append({"role": "user", "content": text_input})

# ---------------------------------------------------------
# 9. PROCESSING (Applying Your Training)
# ---------------------------------------------------------
if user_content:
    try:
        # Build History
        history_for_ai = []
        
        # We attach your TRAINING TEXT (from the sidebar) to the first message silently.
        # This restores your "hours of training" instantly.
        for i, m in enumerate(st.session_state.messages[:-1]):
            role = m["role"]
            content = m["content"]
            if i == 0 and role == "user":
                content = f"SYSTEM TRAINING:\n{training_prompt}\n\nUSER MESSAGE:\n{content}"
            history_for_ai.append({"role": role, "parts": [content]})
            
        # Handle the new message
        if len(history_for_ai) == 0:
            # First turn logic
            if isinstance(user_content, list): # Audio
                user_content[0] = f"SYSTEM TRAINING:\n{training_prompt}\n\n{user_content[0]}"
                parts = user_content
            else: # Text
                parts = [f"SYSTEM TRAINING:\n{training_prompt}\n\n{user_content}"]
        else:
            parts = user_content if isinstance(user_content, list) else [user_content]

        # Generate
        if audio_input:
            response = model.generate_content(parts)
        else:
            chat = model.start_chat(history=history_for_ai)
            response = chat.send_message(parts[0])
        
        with st.chat_message("assistant"):
            st.markdown(response.text)
        st.session_state.messages.append({"role": "model", "content": response.text})
        
    except Exception as e:
        st.error(f"Error: {e}")

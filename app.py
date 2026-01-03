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
    /* Make the training box tall so you can paste long text */
    .stTextArea textarea { height: 400px; }
</style>
""", unsafe_allow_html=True)

# 3. API SETUP
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
else:
    st.error("Missing API Key.")
    st.stop()

# 4. AUTO-DETECT MODEL
# We need 'flash' for the best speed and compliance with instructions.
try:
    all_models = list(genai.list_models())
    chat_models = [m.name for m in all_models if 'generateContent' in m.supported_generation_methods]
    
    # Prioritize Flash
    active_model_name = chat_models[0]
    for m in chat_models:
        if 'flash' in m:
            active_model_name = m
            break
            
    model = genai.GenerativeModel(active_model_name)
except:
    # Backup if detection fails
    model = genai.GenerativeModel("gemini-1.5-flash")

# ---------------------------------------------------------
# 5. THE TRAINING SIDEBAR (THIS IS NEW)
# ---------------------------------------------------------
with st.sidebar:
    st.header("🧠 Brain Training")
    st.info("Paste your Google AI Studio instructions below to restore your training.")
    
    # This is the box where you paste your "hours of training"
    default_training = """You are Rich Klein, a veteran Crisis Communications consultant (30+ years exp).
You act as a consultant for 'Rich Klein Crisis Management' in PA and Italy.
NEVER say you are an AI.
If asked 'Who are you?', say 'I am Rich Klein, a crisis management consultant.'
Be direct, strategic, and professional.
(PASTE YOUR FULL RULES HERE)"""
    
    # The Input Box
    training_prompt = st.text_area("System Instructions:", value=default_training)
    
    if st.button("💾 Apply Training"):
        st.session_state.messages = []
        st.success("Training Updated!")
        st.rerun()

# 6. HERO SECTION
st.markdown("<h1>Protect your reputation<br><span class='highlight'>when it matters most.</span></h1>", unsafe_allow_html=True)
st.markdown("<div class='subtitle'>AI Crisis Consultant | Voice & Text Enabled</div>", unsafe_allow_html=True)

st.divider()

# 7. CHAT LOGIC
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display History
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 8. INPUTS (Voice + Text)
audio_input = st.audio_input("🎤 Client Voice Mode (Tap to Record)")
text_input = st.chat_input("Type crisis details...")

user_content = None

if audio_input:
    user_content = ["Analyze this voice recording for crisis urgency and provide strategic advice based on your training:", audio_input]
    with st.chat_message("user"):
        st.audio(audio_input)
    st.session_state.messages.append({"role": "user", "content": "🎤 *Voice Message Sent*"})

elif text_input:
    user_content = text_input
    with st.chat_message("user"):
        st.markdown(text_input)
    st.session_state.messages.append({"role": "user", "content": text_input})

# 9. GENERATE RESPONSE (Using the Sidebar Training)
if user_content:
    try:
        # We attach the text from the Sidebar to the conversation
        # This is how the AI "remembers" your training.
        
        # Build History
        history_for_ai = []
        for i, m in enumerate(st.session_state.messages[:-1]):
            role = m["role"]
            content = m["content"]
            # Inject training into the first message
            if i == 0 and role == "user":
                content = f"SYSTEM INSTRUCTIONS:\n{training_prompt}\n\nUSER MESSAGE:\n{content}"
            history_for_ai.append({"role": role, "parts": [content]})
            
        # Handle current message
        current_prompt = user_content
        if len(history_for_ai) == 0:
            # If this is the very first message, attach instructions now
            if isinstance(current_prompt, list):
                current_prompt[0] = f"SYSTEM INSTRUCTIONS:\n{training_prompt}\n\n{current_prompt[0]}"
            else:
                current_prompt = f"SYSTEM INSTRUCTIONS:\n{training_prompt}\n\n{current_prompt}"

        # Send
        if audio_input:
             # For audio, we use a simple generate call with the instructions attached
            response = model.generate_content(current_prompt if isinstance(current_prompt, list) else [current_prompt])
        else:
            # For text, we use chat
            chat = model.start_chat(history=history_for_ai)
            response = chat.send_message(current_prompt if isinstance(current_prompt, list) else [current_prompt][0])
        
        with st.chat_message("assistant"):
            st.markdown(response.text)
        st.session_state.messages.append({"role": "model", "content": response.text})
        
    except Exception as e:
        st.error(f"Error: {e}")

import streamlit as st
import google.generativeai as genai

# 1. PAGE CONFIGURATION
st.set_page_config(page_title="Rich Klein Crisis Management", page_icon="🛡️", layout="wide")

# 2. CUSTOM STYLING
st.markdown("""
<style>
    .stApp { background-color: #0e1117; color: white; }
    h1 { text-align: center; font-size: 3.5rem !important; font-weight: 800 !important; margin-bottom: 0px; }
    .subtitle { text-align: center; font-size: 1.2rem; color: #b0b0b0; margin-bottom: 40px; }
    .highlight { color: #4da6ff; }
</style>
""", unsafe_allow_html=True)

# 3. API SETUP
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
else:
    st.error("Missing API Key.")
    st.stop()

# 4. INTELLIGENT MODEL SELECTOR (Prioritize Flash)
try:
    all_models = list(genai.list_models())
    # Get all models that can chat
    chat_models = [m.name for m in all_models if 'generateContent' in m.supported_generation_methods]
    
    # LOGIC: Look for 'flash' first because 'pro' is crashing your account
    active_model_name = None
    for name in chat_models:
        if 'flash' in name:
            active_model_name = name
            break
    
    # If no flash, just take the first available one
    if not active_model_name and chat_models:
        active_model_name = chat_models[0]
        
    if active_model_name:
        model = genai.GenerativeModel(active_model_name)
    else:
        st.error("Critical: No AI models found on this account.")
        st.stop()

except Exception as e:
    st.error(f"Connection Error: {e}")
    st.stop()

# 5. SIDEBAR
with st.sidebar:
    st.header("Controls")
    if st.button("🔄 Reset Conversation"):
        st.session_state.messages = []
        st.rerun()
    # This will print exactly which brain we are using so we know for sure
    st.success(f"Connected to: `{active_model_name}`")

# 6. HERO SECTION
st.markdown("<h1>Protect your reputation<br><span class='highlight'>when it matters most.</span></h1>", unsafe_allow_html=True)
st.markdown("<div class='subtitle'>Experience immediate strategic guidance trained on Rich Klein's expertise.</div>", unsafe_allow_html=True)

# 7. INFO CARDS
st.divider()
col1, col2, col3 = st.columns(3)
with col1: st.info("**Global Support**\n\nU.S. and Italy based insights")
with col2: st.info("**Instant Strategy**\n\nImmediate crisis response steps")
with col3: st.success("**Proven Results**\n\n30+ years of agency experience")
st.divider()

# 8. CHAT INTERFACE
st.markdown("### 🛡️ Start Consultation")

if "messages" not in st.session_state:
    st.session_state.messages = []

# Display History
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 9. THE SECRET WHISPER (Persona Injection)
# We add this to the FIRST message to force the Rich Klein persona without crashing the model settings.
PERSONA_INSTRUCTION = """
SYSTEM INSTRUCTIONS:
You are Rich Klein, a Crisis Communications expert (30+ years exp).
You act as a consultant for 'Rich Klein Crisis Management' in PA and Italy.
NEVER say you are an AI.
If asked 'Who are you?', say 'I am Rich Klein, a crisis management consultant.'
Be direct, strategic, and professional.
--------------------------------------------------
USER MESSAGE:
"""

if prompt := st.chat_input("Describe your crisis situation here..."):
    # Show User Message
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    try:
        # Build History for AI
        history_for_ai = []
        
        for i, m in enumerate(st.session_state.messages):
            role = m["role"]
            content = m["content"]
            
            # If it's the very first user message, glue the instruction to it
            if i == 0 and role == "user":
                content = PERSONA_INSTRUCTION + content
            
            history_for_ai.append({"role": role, "parts": [content]})

        # Send to the Auto-Detected Model
        chat = model.start_chat(history=history_for_ai[:-1])
        response = chat.send_message(history_for_ai[-1]["parts"][0])
        
        # Show AI Response
        with st.chat_message("assistant"):
            st.markdown(response.text)
        st.session_state.messages.append({"role": "model", "content": response.text})
        
    except Exception as e:
        st.error(f"Error: {e}")

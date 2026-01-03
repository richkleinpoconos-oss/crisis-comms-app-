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

# 4. AUTO-DETECT WORKING MODEL (The "Crash Preventer")
# We ask Google: "What models do I have?" and use the first one that works.
try:
    all_models = list(genai.list_models())
    # Filter for models that can chat
    valid_models = [m.name for m in all_models if 'generateContent' in m.supported_generation_methods]
    
    if valid_models:
        # Pick the first available model (e.g., gemini-1.5-flash-001 or gemini-pro)
        active_model_name = valid_models[0]
        model = genai.GenerativeModel(active_model_name)
    else:
        st.error("Critical: Your API Key works, but you have no AI models enabled.")
        st.stop()
except Exception as e:
    st.error(f"Connection Error: {e}")
    st.stop()

# 5. SIDEBAR CONTROLS
with st.sidebar:
    st.header("Controls")
    if st.button("🔄 Reset Conversation"):
        st.session_state.messages = []
        st.rerun()
    st.write(f"**Connected Brain:** `{active_model_name}`")

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

# 9. THE SECRET "RICH KLEIN" INSTRUCTION
# We attach this to the first message silently.
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
    # Show User Message
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    try:
        # Build History for AI
        history_for_ai = []
        
        for i, m in enumerate(st.session_state.messages):
            role = m["role"]
            content = m["content"]
            
            # If it's the very first user message, add the Secret Instruction
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

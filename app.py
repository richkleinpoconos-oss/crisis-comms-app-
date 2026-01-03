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
    .stSelectbox { max-width: 300px; margin: 0 auto; } 
</style>
""", unsafe_allow_html=True)

# 3. API SETUP
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
else:
    st.error("Missing API Key.")
    st.stop()

# 4. HERO SECTION
st.markdown("<h1>Protect your reputation<br><span class='highlight'>when it matters most.</span></h1>", unsafe_allow_html=True)
st.markdown("<div class='subtitle'>Experience immediate strategic guidance trained on Rich Klein's expertise.</div>", unsafe_allow_html=True)

# 5. BRAIN SELECTOR (VISIBLE ON MAIN SCREEN)
# We put this right here so you can fix "404 Errors" instantly.
try:
    all_models = list(genai.list_models())
    chat_models = [m.name for m in all_models if 'generateContent' in m.supported_generation_methods]
    
    # Try to find 'flash' or 'pro' to be the default
    default_index = 0
    for i, m in enumerate(chat_models):
        if 'flash' in m:
            default_index = i
            break
            
    # The Dropdown Menu
    selected_model_name = st.selectbox("🔌 Select AI Connection:", chat_models, index=default_index)
    model = genai.GenerativeModel(selected_model_name)

except Exception as e:
    st.error(f"Connection Error: {e}")
    st.stop()

# 6. INFO CARDS
st.divider()
col1, col2, col3 = st.columns(3)
with col1: st.info("**Global Support**\n\nU.S. and Italy based insights")
with col2: st.info("**Instant Strategy**\n\nImmediate crisis response steps")
with col3: st.success("**Proven Results**\n\n30+ years of agency experience")
st.divider()

# 7. CHAT INTERFACE
st.markdown("### 🛡️ Start Consultation")

# Reset Button in Sidebar (Just in case you need it)
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

# 8. THE RICH KLEIN PERSONA (Hidden Injection)
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
            
            # If it's the very first user message, glue the instruction to it
            if i == 0 and role == "user":
                content = PERSONA_INSTRUCTION + content
            
            history_for_ai.append({"role": role, "parts": [content]})

        # Send to the Selected Model
        chat = model.start_chat(history=history_for_ai[:-1])
        response = chat.send_message(history_for_ai[-1]["parts"][0])
        
        # Show AI Response
        with st.chat_message("assistant"):
            st.markdown(response.text)
        st.session_state.messages.append({"role": "model", "content": response.text})
        
    except Exception as e:
        st.error(f"Error: {e}")

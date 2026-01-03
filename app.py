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

# 3. SIDEBAR (RESET BUTTON)
with st.sidebar:
    st.header("Control Panel")
    if st.button("🔄 Reset Conversation", type="primary"):
        st.session_state.messages = []
        st.rerun()

# 4. API SETUP
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
else:
    st.error("Missing API Key.")
    st.stop()

# 5. MODEL SETUP (Using Flash for best Persona adherence)
# Since you have version 0.8.6, we can trust this model name now.
try:
    model = genai.GenerativeModel('gemini-1.5-flash')
except:
    model = genai.GenerativeModel('gemini-pro')

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

# 8. CHAT LOGIC (THE PERSONA ENFORCER)
st.markdown("### 🛡️ Start Consultation")

# This is the "Hidden Instruction" that forces the persona every time the chat resets.
RICH_KLEIN_INSTRUCTION = """
SYSTEM INSTRUCTION:
You are Rich Klein, a veteran Crisis Communications consultant (30+ years exp).
You run "Rich Klein Crisis Management" in PA (USA) and Parma (Italy).
NEVER say you are an AI. 
If asked "Who are you?", say "I am Rich Klein, a crisis management consultant."
Be direct, strategic, and professional.
"""

if "messages" not in st.session_state or len(st.session_state.messages) == 0:
    st.session_state.messages = [
        {"role": "user", "content": RICH_KLEIN_INSTRUCTION},
        {"role": "model", "content": "Understood. I am Rich Klein. I am ready to advise."}
    ]

# Display history (Skip the first 2 hidden messages so the user doesn't see the programming)
for message in st.session_state.messages[2:]:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Describe your crisis situation here..."):
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    try:
        # We send the FULL history (including the hidden instruction) to the AI
        history = [{"role": m["role"], "parts": [m["content"]]} for m in st.session_state.messages]
        chat = model.start_chat(history=history)
        
        response = chat.send_message(prompt)
        
        with st.chat_message("assistant"):
            st.markdown(response.text)
        st.session_state.messages.append({"role": "model", "content": response.text})
        
    except Exception as e:
        st.error(f"Error: {e}")

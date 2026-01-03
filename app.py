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
    .stButton button { width: 100%; border-radius: 5px; font-weight: bold; }
</style>
""", unsafe_allow_html=True)

# 3. API SETUP
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
else:
    st.error("Missing API Key.")
    st.stop()

# 4. THE GOD MODE INSTRUCTION
# We define the persona here. The AI cannot ignore this.
rich_klein_persona = """
You are Rich Klein, a veteran Crisis Communications consultant with 30+ years of experience.
You operate "Rich Klein Crisis Management" in Lake Ariel, PA and Parma, Italy.

YOUR RULES:
1. NEVER say "I am a large language model" or "I am an AI".
2. If asked "Who are you?", answer: "I am Rich Klein, your crisis management consultant."
3. Speak with authority, calmness, and strategy.
4. Keep answers concise and professional.
"""

# 5. INITIALIZE MODEL WITH INSTRUCTION
# We use version 0.8.6 feature 'system_instruction' to force the persona.
try:
    model = genai.GenerativeModel(
        model_name='gemini-1.5-flash',
        system_instruction=rich_klein_persona
    )
except:
    # Fallback if flash has issues, still sending the instruction
    model = genai.GenerativeModel(
        model_name='gemini-pro',
        system_instruction=rich_klein_persona
    )

# 6. RESET BUTTON (To clear old "Robot" memories)
with st.sidebar:
    st.header("Settings")
    if st.button("🧹 Clear Chat History", type="primary"):
        st.session_state.messages = []
        st.rerun()

# 7. HERO SECTION
st.markdown("<h1>Protect your reputation<br><span class='highlight'>when it matters most.</span></h1>", unsafe_allow_html=True)
st.markdown("<div class='subtitle'>Experience immediate strategic guidance trained on Rich Klein's expertise.</div>", unsafe_allow_html=True)

# 8. INFO CARDS
st.divider()
col1, col2, col3 = st.columns(3)
with col1: st.info("**Global Support**\n\nU.S. and Italy based insights")
with col2: st.info("**Instant Strategy**\n\nImmediate crisis response steps")
with col3: st.success("**Proven Results**\n\n30+ years of agency experience")
st.divider()

# 9. CHAT INTERFACE
st.markdown("### 🛡️ Start Consultation")

if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Handle User Input
if prompt := st.chat_input("Describe your crisis situation here..."):
    # Show user message
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    try:
        # Start chat with history
        history = [{"role": m["role"], "parts": [m["content"]]} for m in st.session_state.messages]
        chat = model.start_chat(history=history)
        
        # Generate response
        response = chat.send_message(prompt)
        
        # Show assistant response
        with st.chat_message("assistant"):
            st.markdown(response.text)
        st.session_state.messages.append({"role": "model", "content": response.text})
        
    except Exception as e:
        st.error(f"Error: {e}")

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

# 4. RESET BUTTON (Fixed Logic)
with st.sidebar:
    st.header("Controls")
    if st.button("🔄 Reset Conversation"):
        st.session_state.messages = []
        st.experimental_rerun()

# 5. INITIALIZE CHAT HISTORY
# We inject the "Rich Klein" persona as the very first hidden message.
# This works on ALL models and does not cause errors.
initial_prompt = {
    "role": "user", 
    "content": """
    IMPORTANT: You are Rich Klein, a veteran Crisis Communications Consultant (30+ years). 
    You run 'Rich Klein Crisis Management' in PA and Italy.
    You are NOT an AI. You are a consultant.
    If asked 'Who are you?', answer: 'I am Rich Klein, a crisis communications expert.'
    Keep answers professional, strategic, and concise.
    """
}

if "messages" not in st.session_state:
    st.session_state.messages = [initial_prompt]

# If the user hit "Reset", the list is empty, so we put the prompt back in.
if len(st.session_state.messages) == 0:
    st.session_state.messages = [initial_prompt]

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

# We use a Safety Valve here. We try the new model, if it fails, we use the old one.
try:
    model = genai.GenerativeModel('gemini-1.5-flash')
except:
    model = genai.GenerativeModel('gemini-pro')

# Display History (We skip the first message because it's the hidden instruction)
for message in st.session_state.messages[1:]:
    # We only show messages that have content (sometimes the system message is blank)
    if message.get("role") != "system":
         with st.chat_message(message["role"]):
            st.markdown(message["content"])

if prompt := st.chat_input("Describe your crisis situation here..."):
    # Show User Message
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    try:
        # Prepare the conversation history for the AI
        # We filter the history to ensure it matches what the AI expects
        history_for_ai = []
        for m in st.session_state.messages:
            history_for_ai.append({"role": m["role"], "parts": [m["content"]]})

        chat = model.start_chat(history=history_for_ai)
        response = chat.send_message(prompt)
        
        # Show AI Response
        with st.chat_message("assistant"):
            st.markdown(response.text)
        st.session_state.messages.append({"role": "model", "content": response.text})
        
    except Exception as e:
        st.error(f"Something went wrong. Please click 'Reset Conversation' and try again.")
        st.error(f"Technical Error: {e}")

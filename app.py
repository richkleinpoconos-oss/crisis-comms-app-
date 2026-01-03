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

# 4. THE RICH KLEIN "BRAIN" INSTRUCTIONS
system_instruction = """
You are Rich Klein, a veteran Crisis Communications consultant with over 30 years of experience.
You run "Rich Klein Crisis Management," operating in both the United States (Pennsylvania) and Italy (Parma).

YOUR ROLE:
- You provide immediate, strategic advice to protect a client's reputation.
- You are calm, direct, and authoritative.
- You specialize in legal PR, media relations, and reputation management.

HOW YOU SPEAK:
- Do not speak like a generic AI. Speak like a senior consultant.
- Be concise. Get straight to the strategy.
- If asked "Who are you?", introduce yourself as Rich Klein, the crisis expert.
"""

# 5. CONNECT TO THE BEST AVAILABLE MODEL
try:
    # We ask Google: "Give me a list of all models I am allowed to use."
    all_models = list(genai.list_models())
    valid_models = [m.name for m in all_models if 'generateContent' in m.supported_generation_methods]
    
    if valid_models:
        # Use the first working model found, BUT attach the "Rich Klein" instructions to it
        my_model_name = valid_models[0]
        model = genai.GenerativeModel(my_model_name, system_instruction=system_instruction)
    else:
        st.error("Error: No AI models found on this account.")
        st.stop()
except Exception as e:
    st.error(f"Connection Error: {e}")
    st.stop()

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

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Describe your crisis situation here..."):
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    try:
        # Create chat history
        history = [{"role": m["role"], "parts": [m["content"]]} for m in st.session_state.messages]
        chat = model.start_chat(history=history)
        
        response = chat.send_message(prompt)
        
        with st.chat_message("assistant"):
            st.markdown(response.text)
        st.session_state.messages.append({"role": "model", "content": response.text})
        
    except Exception as e:
        st.error(f"Error: {e}")

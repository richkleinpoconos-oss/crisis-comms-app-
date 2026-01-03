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

# 4. AUTO-DETECT WORKING MODEL (The "Universal Key")
try:
    # We ask Google: "Give me a list of all models I am allowed to use."
    all_models = list(genai.list_models())
    
    # We filter for models that can chat (generateContent)
    valid_models = [m.name for m in all_models if 'generateContent' in m.supported_generation_methods]
    
    if valid_models:
        # We pick the first valid one found (e.g., 'models/gemini-pro' or 'models/gemini-1.5-flash')
        my_model_name = valid_models[0]
        model = genai.GenerativeModel(my_model_name)
    else:
        st.error("CRITICAL ERROR: Your API Key connects, but no AI models are enabled on your Google account.")
        st.stop()
        
except Exception as e:
    st.error(f"Connection Error: {e}")
    st.stop()

# 5. HERO SECTION
st.markdown("<h1>Protect your reputation<br><span class='highlight'>when it matters most.</span></h1>", unsafe_allow_html=True)
st.markdown("<div class='subtitle'>Experience immediate strategic guidance trained on Rich Klein's expertise.</div>", unsafe_allow_html=True)

# 6. INFO CARDS
st.divider()
col1, col2, col3 = st.columns(3)
with col1: st.info("**Global Support**\n\nU.S. and Italy based insights")
with col2: st.info("**Instant Strategy**\n\nImmediate crisis response steps")
with col3: st.success("**Proven Results**\n\n30+ years of agency experience")
st.divider()

# 7. CHAT INTERFACE
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
        st.error(f"Error details: {e}")

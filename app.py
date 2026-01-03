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

# 3. API SETUP & MODEL SCANNING
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
else:
    st.error("Missing API Key.")
    st.stop()

# Function to get available models
def get_working_models():
    try:
        all_models = list(genai.list_models())
        # We only want models that support 'generateContent'
        chat_models = [m.name for m in all_models if 'generateContent' in m.supported_generation_methods]
        return chat_models
    except Exception as e:
        return []

# 4. SIDEBAR CONTROL PANEL
with st.sidebar:
    st.header("🔧 Engineer Panel")
    
    # A. Model Selector (The fix for 404 errors)
    available_models = get_working_models()
    if available_models:
        # distinct "flash" preference if available
        default_index = 0
        for i, m in enumerate(available_models):
            if "flash" in m:
                default_index = i
                break
        
        selected_model = st.selectbox("Select AI Brain:", available_models, index=default_index)
    else:
        st.error("No models found. Check API Key.")
        st.stop()

    # B. Persona Editor (The fix for 'Robot' answers)
    st.subheader("Persona Instructions")
    default_persona = """You are Rich Klein, a veteran Crisis Communications consultant (30+ years).
You run 'Rich Klein Crisis Management' in PA and Italy.
NEVER say you are an AI. 
If asked 'Who are you?', say 'I am Rich Klein, a crisis management consultant.'
Be direct, strategic, and professional."""
    
    persona_instruction = st.text_area("Edit Brain Instructions:", value=default_persona, height=200)

    # C. Reset
    if st.button("🔄 Reset Conversation", type="primary"):
        st.session_state.messages = []
        st.rerun()

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

# 7. CHAT LOGIC
st.markdown("### 🛡️ Start Consultation")

# Initialize Model based on Sidebar Selection
model = genai.GenerativeModel(selected_model)

if "messages" not in st.session_state:
    st.session_state.messages = []

# Display History
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Handle User Input
if prompt := st.chat_input("Describe your crisis situation here..."):
    # Show user message
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    try:
        # Build History with "Secret Whisper" Persona
        history_for_ai = []
        
        for i, m in enumerate(st.session_state.messages):
            role = m["role"]
            content = m["content"]
            
            # Glue the instructions from the Sidebar to the FIRST message
            if i == 0 and role == "user":
                content = f"SYSTEM INSTRUCTION: {persona_instruction}\n\nUSER MESSAGE: {content}"
            
            history_for_ai.append({"role": role, "parts": [content]})

        # Send to the Selected Model
        chat = model.start_chat(history=history_for_ai[:-1])
        response = chat.send_message(history_for_ai[-1]["parts"][0])
        
        # Show AI response
        with st.chat_message("assistant"):
            st.markdown(response.text)
        st.session_state.messages.append({"role": "model", "content": response.text})
        
    except Exception as e:
        st.error(f"Error with model {selected_model}: {e}")
        st.info("💡 Tip: Try selecting a different model in the Sidebar!")

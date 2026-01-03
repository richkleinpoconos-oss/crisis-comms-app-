import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="Engineer Mode", layout="wide")

# ---------------------------------------------------------
# THE "BIG TEXT" TEST
# If you don't see this huge header, you are looking at the wrong tab.
# ---------------------------------------------------------
st.title("🚧 I AM THE NEW CODE 🚧")
st.header("If you see this, the update worked.")
st.write("Now let's find your AI Brain.")

# 1. API SETUP
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
    st.success("✅ API Key Found")
else:
    st.error("❌ Missing API Key in Secrets")
    st.stop()

# 2. MODEL SCANNER (On the main screen, not sidebar)
try:
    all_models = list(genai.list_models())
    chat_models = [m.name for m in all_models if 'generateContent' in m.supported_generation_methods]
    
    if chat_models:
        st.write("### 🧠 Available Brains:")
        selected_model = st.selectbox("Pick one from this list:", chat_models)
        st.success(f"You selected: **{selected_model}**")
        
        # 3. TEST CHAT
        model = genai.GenerativeModel(selected_model)
        if st.button("Test Connection"):
            try:
                response = model.generate_content("Say 'System Operational'")
                st.info(f"Response: {response.text}")
            except Exception as e:
                st.error(f"Test Failed: {e}")
    else:
        st.error("❌ No chat models found on this account.")

except Exception as e:
    st.error(f"❌ Critical Error: {e}")

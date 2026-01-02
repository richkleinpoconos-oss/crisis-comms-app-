import streamlit as st
import google.generativeai as genai
import sys

st.set_page_config(page_title="System Diagnosis", page_icon="🔧")

st.title("🔧 System Diagnosis")

# 1. Check Tool Version
st.write("### 1. Tool Version")
st.write(f"**Installed Library Version:** `{genai.__version__}`")
# If this number is NOT 0.8.3 or higher, the update failed.

# 2. Check API Key & Models
st.write("### 2. Checking Connection")
if "GOOGLE_API_KEY" in st.secrets:
    try:
        genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
        models = list(genai.list_models())
        
        found_models = []
        for m in models:
            if 'generateContent' in m.supported_generation_methods:
                found_models.append(m.name)
        
        if found_models:
            st.success(f"✅ Connection Success! Found {len(found_models)} models.")
            st.write("**Available Models:**")
            st.code(found_models)
        else:
            st.error("❌ Connection established, but NO models found.")
            st.info("This usually means the API Key is from a Google Cloud project that hasn't enabled the 'Generative AI' service.")
            
    except Exception as e:
        st.error(f"❌ Connection Failed: {e}")
else:
    st.error("❌ No API Key found in secrets.")

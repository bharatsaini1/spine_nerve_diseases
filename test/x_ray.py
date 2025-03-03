import os
import streamlit as st
from PIL import Image
import google.generativeai as genai
from configs import SYSTEM_PROMPT, SAFETY_SETTINGS, GENERATION_CONFIG, MODEL_NAME

# Load API Key Securely
genai.configure(api_key=["AIzaSyDvi36_drsfozMYLeL5RsGcA6ILybMY6vs"])  # Store API key in Streamlit secrets

# Load Model
model = genai.GenerativeModel(
    model_name=MODEL_NAME,
    safety_settings=SAFETY_SETTINGS,
    generation_config=GENERATION_CONFIG,
    system_instruction=SYSTEM_PROMPT
)

# Streamlit UI
st.set_page_config(page_title='Axe Analytics')
st.title('Axe Analytics')
st.subheader('Analyzing medical images using AI (Gemini).')

# File Upload Section
st.markdown("### Upload Medical Images (X-Ray or MRI)")
col1, col2 = st.columns([1, 5])
xray_file = col2.file_uploader('Upload X-Ray Image:', type=['png', 'jpg', 'jpeg'])
mri_file = col2.file_uploader('Upload MRI Scan:', type=['png', 'jpg', 'jpeg'])

# Display Uploaded Images
if xray_file:
    st.image(Image.open(xray_file), caption="X-Ray Image", use_column_width=True)
if mri_file:
    st.image(Image.open(mri_file), caption="MRI Scan", use_column_width=True)

# Additional Health Info
st.markdown("### (Optional) Provide Additional Health Information")
user_health_info = st.text_area("Describe any symptoms or concerns related to the images:", "")

# Initialize chat history
if "history" not in st.session_state:
    st.session_state.history = []

# Analyze Button
if (xray_file or mri_file) and col1.button('ANALYZE', use_container_width=True):
    with st.spinner("Analyzing..."):
        chat_session = model.start_chat(history=st.session_state.history)

        # Prepare AI Prompt
        content = ["Analyze the uploaded medical images."]
        if xray_file:
            content.append("This is an X-ray image.")
            content.append(Image.open(xray_file))
        if mri_file:
            content.append("This is an MRI scan.")
            content.append(Image.open(mri_file))
        if user_health_info:
            content.append(f"Additional health information provided by the user: {user_health_info}")

        # AI Analysis
        response = chat_session.send_message(content)

        # Display response
        st.chat_message("Model:").write(response.text)

        # Update chat history
        st.session_state.history = chat_session.history

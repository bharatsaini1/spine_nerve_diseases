import streamlit as st
from PIL import Image
import google.generativeai as genai
from configs import SYSTEM_PROMPT, SAFETY_SETTINGS, GENERATION_CONFIG, MODEL_NAME

# Load API Key Securely
genai.configure(api_key="AIzaSyDvi36_drsfozMYLeL5RsGcA6ILybMY6vs")  # Store key in .streamlit/secrets.toml

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
xray_file = st.file_uploader('Upload X-Ray Image:', type=['png', 'jpg', 'jpeg'])
mri_file = st.file_uploader('Upload MRI Scan:', type=['png', 'jpg', 'jpeg'])

# Display Uploaded Images
if xray_file:
    xray_image = Image.open(xray_file)
    st.image(xray_image, caption="X-Ray Image", use_column_width=True)
if mri_file:
    mri_image = Image.open(mri_file)
    st.image(mri_image, caption="MRI Scan", use_column_width=True)

# Additional Health Info
st.markdown("### (Optional) Provide Additional Health Information")
user_health_info = st.text_area("Describe any symptoms or concerns related to the images:", "")

# Initialize chat history
if "history" not in st.session_state:
    st.session_state.history = []

# Analyze Button
if st.button('ANALYZE', use_container_width=True):
    if not xray_file and not mri_file:
        st.error("Please upload at least one medical image for analysis.")
    else:
        with st.spinner("Analyzing..."):
            chat_session = model.start_chat(history=st.session_state.history)

            # Prepare AI Prompt
            content = ["Analyze the uploaded medical images."]
            if xray_file:
                content.append("This is an X-ray image.")
                content.append(xray_image)
            if mri_file:
                content.append("This is an MRI scan.")
                content.append(mri_image)
            if user_health_info:
                content.append(f"Additional health information provided by the user: {user_health_info}")

            # AI Analysis
            response = chat_session.send_message(content)

            # Display response
            st.write("### AI Analysis Result:")
            st.write(response.text)

            # Update chat history
            st.session_state.history = chat_session.history

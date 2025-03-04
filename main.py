#Import All the Required Libraries
import streamlit as st
import google.generativeai as genai
from PIL import Image
import os
from dotenv import load_dotenv
load_dotenv()

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

#Load the Gemini Pro Vision Model
model = genai.GenerativeModel('gemini-2.0-flash-exp')

def get_gemini_respone(input_prompt, image, user_input_prompt):
    response = model.generate_content([input_prompt, image[0], user_input_prompt])
    return response.text

def input_image_bytes(uploaded_file):
    if uploaded_file is not None:
        #Convert the Uploaded File into bytes
        bytes_data = uploaded_file.getvalue()
        image_parts = [
            {
                "mime_type": uploaded_file.type,
                "data": bytes_data
            }
        ]
        return  image_parts
    else:
        raise FileNotFoundError("No File Uploaded")

# Initialize the Streamlit App
st.set_page_config(layout="wide", page_title="ALGOSTATS CV", page_icon="./logo.png")
st.header('ALGOSTATS VISION - MULTILANGUAGE INVOICE EXTRACTOR')
st.write(
    """
    Welcome to ALGOSTATS! ✨ This app serves as a Multilanguage Invoice Content Extractor, designed to facilitate the Indexing Process within the context of P2P (Procure-to-Pay) Invoice Processing Task Automation. ✨
    """
)
with st.sidebar:
    st.image("./logo.png",  use_column_width=True)
    input_prompt = """
    You are an expert in understanding invoices. Please try to answer the question using the information from the uploaded
    invoice.
    """
user_input_prompt = st.text_input("USER INPUT PROMPT", key="input")
upload_image_file = st.file_uploader("Upload the Image of the Invoice", type=["jpg", "jpeg", "png"])
if upload_image_file is not None:
    image = Image.open(upload_image_file)
    st.image(image, caption = "Uploaded Image", use_column_width=True)

submit = st.button("ALGOSTATS CV RESPONSE")
if submit:
    input_image_data = input_image_bytes(upload_image_file)
    response = get_gemini_respone(input_prompt, input_image_data, user_input_prompt)
    st.subheader("Response")
    st.write(response)
    
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)

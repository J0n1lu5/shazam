
import streamlit as st
from duckduckgo_search import DDGS
import io
import requests
from PIL import Image
from Store_Data import Data
from Fingerprint import AudioFingerprinter
import os
import tempfile
import numpy as np
import settings


# Eine Überschrift der ersten Ebene
st.write("Musikerkennung")

# tabs
tab1, tab2 = st.tabs(["Hochladen", "Erkennen"])


with tab1:
    st.write("Hochladen")
    
      
    
    with st.form ("upload"):

        uploaded_song = st.file_uploader("Choose a file", type=['mp3', 'wav'])
        
        if uploaded_song is not None:
            file_path = os.path.join(os.getcwd(), uploaded_song.name)
            
            with open(uploaded_song.name, 'wb') as f:
                f.write(uploaded_song.getvalue())
            
            st.write("file ausgewählt")
            
        
        title = st.text_input("# Title") 
        
        interpret = st.text_input("# Interpret")   
   
        submitted = st.form_submit_button("Submit")
        
        if submitted:
                
                song_info= ",".join([title,interpret])
                print (uploaded_song)                     
                fingerprinter_instance = AudioFingerprinter()
                fingerprint = fingerprinter_instance.fingerprint_file(file_path)
                print (fingerprint)
                new_song= Data(title,interpret,fingerprint)
                new_song.store_data()         
                st.write("upload complete")    
                os.remove(file_path)
                st.rerun()


    #Brauch noch exeption handling
"""      
    if title and interpret is not None:
            with DDGS() as ddgs:
                keywords = f"{title} {interpret} album cover"
                ddgs_images_gen = ddgs.images(
                    keywords,
                    region="wt-wt",
                    safesearch="off",
                    size=None,
                    color="",
                    type_image=None,
                    layout=None,
                    license_image=None,
                    max_results=1,
                )
                images = list(ddgs_images_gen)
                if images:
                    image_url = images[0].get('image')
                    if image_url:
                        # Fetch the image data
                        response = requests.get(image_url)
                        image_bytes_io = io.BytesIO(response.content)
                        
                        # Open the image using PIL
                        pil_image = Image.open(image_bytes_io)
                        
                        # Display the image in Streamlit
                        st.image(pil_image, caption='Album Cover', use_column_width=True)
                    else:
                        st.write("Album Cover URL nicht gefunden.")
                else:
                    st.write("Album Cover nicht gefunden.")
"""

 

    

with tab2:
    st.write("Erkennen")

    with st.form ("erkennen"):
        uploaded_song = st.file_uploader("Choose a file")
        if uploaded_song is not None:
            #fingerprint erstellen und ablegen in der datenbank
            st.write("file ausgewählt")

        submitted = st.form_submit_button("Submit")
        if submitted:
            AudioFingerprinter.fingerprint_file(uploaded_song)

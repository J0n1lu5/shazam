
import streamlit as st
from duckduckgo_search import DDGS
import io
import requests
from recognise import SongRecognizer
from PIL import Image
from Store_Data import Data
from Fingerprint import AudioFingerprinter
from audio_player import AudioPlayer
import os
import tempfile
import numpy as np
import settings
from database_storage import AudioDatabase
import matplotlib.pyplot as plt
from scipy.io import wavfile


# Eine Überschrift der ersten Ebene
st.write("Musikerkennung")


# tabs
tab1, tab2 = st.tabs(["Hochladen", "Erkennen"])

with tab1:
    st.write("Hochladen")

    with st.form("upload"):
        uploaded_song = st.file_uploader("Choose a file", type=['wav'])

        if uploaded_song is not None:
            

            st.write("file ausgewählt")
            AudioPlayer.play_audio(uploaded_song)

        title = st.text_input("Title")
        interpret = st.text_input("Interpret")

        submitted = st.form_submit_button("Submit")

        if submitted:
            
            file_path = os.path.join(os.getcwd(), uploaded_song.name)

            with open(file_path, 'wb') as f:
                f.write(uploaded_song.getvalue())
            

            song_info = title,interpret
            fingerprinter_instance = AudioFingerprinter()
            fingerprint = fingerprinter_instance.fingerprint_file(file_path)
            new_song = AudioDatabase("database.json")
            new_song.store_song(fingerprint, song_info)
            st.write("upload complete")
            os.remove(file_path)
            st.rerun()

    

with tab2:
    st.write("Erkennen")

    with st.form("recognize_song"):
        uploaded_song = st.file_uploader("Wählen Sie eine Datei aus")

        if uploaded_song is not None:            

            st.write("Datei ausgewählt:", uploaded_song.name)

        submitted = st.form_submit_button("Song erkennen")

        show_cover = st.checkbox("Cover anzeigen")

        if show_cover :
                st.write("Cover wird mit gesucht")
        
        if submitted and uploaded_song:
            file_path = os.path.join(os.getcwd(), uploaded_song.name)

            with open(file_path, 'wb') as f:
                
                    f.write(uploaded_song.getvalue())

            recognizer = SongRecognizer("database.json")
            recognition_result = recognizer.recognise_song(file_path)
            #print(recognition_result)
            os.remove(file_path)

            if recognition_result is not None:
                st.audio(uploaded_song)
                st.write("Der hochgeladene Song wurde erkannt!")
                st.write("Künstler:", recognition_result[1][1])
                st.write("Titel:", recognition_result[1][0])
                # Spotify-Link generieren
                spotify_link = f"https://open.spotify.com/search/{recognition_result[1][0].replace(' ', '_')}+{recognition_result[1][1].replace(' ', '_')}"
                st.write("Spotify Link:", spotify_link)
                youtube_link = f"https://www.youtube.com/results?search_query={recognition_result[1][0].replace(' ', '_')}+{recognition_result[1][1].replace(' ', '_')}"
                st.write("YouTube Link:", youtube_link)

                

                if show_cover:
                    
                    if title and interpret is not None:
                        with DDGS() as ddgs:
                            keywords = f"{recognition_result[1][0]} {recognition_result[1][1]} album cover"
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

            else:
                st.write("Der hochgeladene Song wurde nicht in der Datenbank gefunden.")

with st.sidebar:
    st.write("Wellenfunktion Parameter")
    uploaded_song = st.file_uploader("WAV-Datei hochladen", type=['wav'])

if uploaded_song:
    # Audiodatei einlesen
    fs, data = wavfile.read(uploaded_song)
    
    # Zeitvektor erstellen
    time = np.arange(0, len(data)) / fs
    
    # Plot erstellen
    plt.plot(time, data)
    plt.xlabel('Zeit (s)')
    plt.ylabel('Amplitude')
    plt.title('Waveform des Songs')
    st.pyplot(plt)


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


 

    

with tab2:
    st.write("Erkennen")

    with st.form("recognize_song"):
        uploaded_song = st.file_uploader("Wählen Sie eine Datei aus")
        if uploaded_song is not None:
            st.write("Datei ausgewählt:", uploaded_song.name)

        submitted = st.form_submit_button("Song erkennen")
        if submitted and uploaded_song:
            # Überprüfen, ob der hochgeladene Song in der Datenbank ist
            recognizer = SongRecognizer("shazam/database.json")
            # Speichern der hochgeladenen Datei temporär, um sie an den SongRecognizer zu übergeben
            temp_file_path = "temp_file." + uploaded_song.name.split(".")[-1]
            with open(temp_file_path, "wb") as f:
                f.write(uploaded_song.getvalue())
            # Erkennen des Songs
            recognition_result = recognizer.recognise_song(temp_file_path)
            # Löschen der temporären Datei
            os.remove(temp_file_path)
            # Überprüfen, ob ein Ergebnis vorliegt
            if recognition_result is not None:
                st.write("Der hochgeladene Song wurde erkannt!")
                st.write("Künstler:", recognition_result[0])
                st.write("Album:", recognition_result[1])
                st.write("Titel:", recognition_result[2])
            else:
                st.write("Der hochgeladene Song wurde nicht in der Datenbank gefunden.")
                """
import streamlit as st
from duckduckgo_search import DDGS
import io
import requests
from recognise import SongRecognizer
from PIL import Image
from Fingerprint import AudioFingerprinter
from audio_player import AudioPlayer
import os
import numpy as np
from database_storage import AudioDatabase
import matplotlib.pyplot as plt
from scipy.io import wavfile

def plot_waveform(file_path):
    sample_rate, audio_data = wavfile.read(file_path)

    # Bestimme die Zeitachse
    duration = len(audio_data) / sample_rate
    time_axis = np.linspace(0, duration, len(audio_data))

    # Plotte die Wellenform
    plt.figure(figsize=(10, 4))
    plt.plot(time_axis, audio_data, color='blue')
    plt.title('Wellenform des Songs')
    plt.xlabel('Zeit (s)')
    plt.ylabel('Amplitude')
    plt.grid(True)
    st.pyplot(plt)


# Eine Überschrift der ersten Ebene
st.write("Musikerkennung")


# tabs
tab1, tab2 = st.tabs(["Hochladen", "Erkennen"])

search_history = []

with tab1:
    st.write("Hochladen")

    with st.form("upload"):
        uploaded_song = st.file_uploader("Choose a file", type=['wav'])

        if uploaded_song is not None:

            st.write("file ausgewählt")
            AudioPlayer.play_audio(uploaded_song)

        title = st.text_input("Title")
        interpret = st.text_input("Interpret")
        show_waveform = st.checkbox("Waveform anzeigen")

        submitted = st.form_submit_button("Submit")

        if submitted:
            
            file_path = os.path.join(os.getcwd(), uploaded_song.name)

            with open(file_path, 'wb') as f:
                f.write(uploaded_song.getvalue())
            

            fingerprinter_instance = AudioFingerprinter()
            fingerprint = fingerprinter_instance.fingerprint_file(file_path)
            
            song_info = title,interpret
            new_song = AudioDatabase("database.json")
            new_song.store_song(fingerprint, song_info)
            st.write("upload complete")

            if show_waveform:
                plot_waveform(file_path)

            os.remove(file_path)
            
            

            
                   

            
        

    

with tab2:
    st.write("Erkennen")

    with st.form("recognize_song"):
        uploaded_song = st.file_uploader("Wählen Sie eine Datei aus")

        if uploaded_song is not None:            

            st.write("Datei ausgewählt:", uploaded_song.name)

        submitted = st.form_submit_button("Song erkennen")

        show_cover = st.checkbox("Cover anzeigen")
        show_search_history = st.checkbox("Verlauf anzeigen")
        

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
                
                song_data = {"artist": recognition_result[1][1], "title": recognition_result[1][0]} 
                history = AudioDatabase("database.json")
                history.store_history(song_data)

                # Spotify-Link generieren
                spotify_link = f"https://open.spotify.com/search/{recognition_result[1][0].replace(' ', '_')}+{recognition_result[1][1].replace(' ', '_')}"
                st.write("Spotify Link:", spotify_link)
                youtube_link = f"https://www.youtube.com/results?search_query={recognition_result[1][0].replace(' ', '_')}+{recognition_result[1][1].replace(' ', '_')}"
                st.write("YouTube Link:", youtube_link)

                
                #Albumcover
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
                                    
                                    if response.status_code == 200:
                                        try:
                                            # Open the image using PIL
                                            pil_image = Image.open(io.BytesIO(response.content))
                                            
                                            # Display the image in Streamlit
                                            st.image(pil_image, caption='Album Cover', use_column_width=True)
                                        except Exception as e:
                                            st.write("Error:", e)
                                            st.write("Album Cover kann nicht geöffnet werden.")
                                    else:
                                        st.write("Album Cover kann nicht abgerufen werden:", image_url)
                                else:
                                    st.write("Album Cover URL nicht gefunden.")
                            else:
                                st.write("Album Cover nicht  gefunden.")

            else:
                st.write("Der hochgeladene Song wurde nicht in der Datenbank gefunden.")

        if show_search_history:
            limit = 5
            database = AudioDatabase("database.json")
            recent_songs = database.get_history(limit)
            st.write("Die letzten gesuchten Songs sind")
            st.write (recent_songs)

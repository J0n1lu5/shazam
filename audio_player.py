# audio_player.py

import streamlit as st

class AudioPlayer:
    @staticmethod
    def play_audio(audio_file):
        audio_bytes = audio_file.read()
        st.audio(audio_bytes, format='audio/wav')

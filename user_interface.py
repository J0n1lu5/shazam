### Erste Streamlit App

import streamlit as st
import pandas as pd
from io import StringIO


# Eine Überschrift der ersten Ebene
st.write("# Gerätemanagement")

# tabs
tab1, tab2 = st.tabs(["hochladen", "erkennen"])


with tab1:
     st.write("hochladen")

uploaded_file = st.file_uploader("Choose a file")
if uploaded_file is not None:
    # To read file as bytes:
    bytes_data = uploaded_file.getvalue()
    st.write(bytes_data)

   

 

    


with tab2:
    st.write("erkennen")
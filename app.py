import streamlit as st
from pytube import YouTube

def download_audio(url, bitrate):
    yt = YouTube(url)
    audio_stream = yt.streams.filter(only_audio=True, abr=bitrate).first()
    if audio_stream:
        return audio_stream.download()
    else:
        st.error("Audio stream with the specified bitrate not found.")
        return None

st.title("YouTube MP3 Downloader")

# User input for YouTube URL
url = st.text_input("Enter YouTube Video URL:")

# User input for bitrate selection
bitrate_options = ['128kbps', '192kbps', '256kbps']
bitrate = st.selectbox("Select Bitrate:", bitrate_options)

if st.button("Download MP3"):
    if url:
        st.write("Downloading audio...")
        file_path = download_audio(url, bitrate)
        if file_path:
            with open(file_path, "rb") as f:
                st.download_button(label="Download MP3", data=f, file_name=f"{YouTube(url).title}.mp3", mime="audio/mp3")
    else:
        st.error("Please enter a valid YouTube URL.")

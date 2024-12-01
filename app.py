import streamlit as st
from pytube import YouTube
from pydub import AudioSegment
import os

# Fungsi untuk mengunduh dan mengonversi audio
def download_youtube_audio(url, output_folder="downloads"):
    try:
        # Membuat folder output jika belum ada
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)

        # Mengunduh video YouTube
        yt = YouTube(url)
        video_stream = yt.streams.filter(only_audio=True).first()
        downloaded_file = video_stream.download(output_path=output_folder)

        # Mengonversi file audio ke MP3
        base, ext = os.path.splitext(downloaded_file)
        mp3_file = base + ".mp3"
        AudioSegment.from_file(downloaded_file).export(mp3_file, format="mp3")

        # Menghapus file asli (format non-MP3)
        os.remove(downloaded_file)
        return mp3_file

    except Exception as e:
        st.error(f"Terjadi kesalahan: {e}")
        return None

# Streamlit UI
st.title("YouTube to MP3 Downloader")
st.write("Masukkan URL video YouTube untuk mengunduh audio dalam format MP3.")

# Input URL
url = st.text_input("Masukkan URL YouTube:", "")

if st.button("Unduh MP3"):
    if url:
        with st.spinner("Mengunduh dan mengonversi..."):
            mp3_file = download_youtube_audio(url)
            if mp3_file:
                with open(mp3_file, "rb") as file:
                    st.success("Berhasil! Klik tombol di bawah untuk mengunduh file MP3.")
                    st.download_button(
                        label="Unduh MP3",
                        data=file,
                        file_name=os.path.basename(mp3_file),
                        mime="audio/mp3",
                    )
                os.remove(mp3_file)
    else:
        st.error("Harap masukkan URL YouTube.")

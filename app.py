import os
import streamlit as st
import yt_dlp
import shutil
import requests
import zipfile

# Fungsi untuk memastikan FFmpeg tersedia
def setup_ffmpeg():
    ffmpeg_path = shutil.which("ffmpeg")
    if ffmpeg_path:
        st.write("FFmpeg sudah tersedia.")
        return ffmpeg_path

    # Unduh FFmpeg jika tidak tersedia
    st.write("Mengunduh FFmpeg...")
    url = "https://github.com/yt-dlp/FFmpeg-Builds/releases/download/latest/ffmpeg-master-latest-linux64-gpl.zip"
    ffmpeg_zip = "ffmpeg.zip"
    ffmpeg_folder = "ffmpeg"

    # Unduh file zip
    response = requests.get(url, stream=True)
    with open(ffmpeg_zip, "wb") as f:
        for chunk in response.iter_content(chunk_size=1024):
            if chunk:
                f.write(chunk)

    # Ekstrak FFmpeg
    with zipfile.ZipFile(ffmpeg_zip, "r") as zip_ref:
        zip_ref.extractall(ffmpeg_folder)

    # Tambahkan lokasi FFmpeg ke PATH
    ffmpeg_exe = os.path.join(ffmpeg_folder, "ffmpeg-master-latest-linux64-gpl", "bin", "ffmpeg")
    os.environ["PATH"] += os.pathsep + os.path.dirname(ffmpeg_exe)
    return ffmpeg_exe

# Unduh FFmpeg saat runtime
setup_ffmpeg()

# Fungsi untuk mengunduh audio dari YouTube
def download_youtube_audio(url, output_folder="downloads"):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Konfigurasi yt-dlp untuk mengunduh audio dalam format terbaik
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': f'{output_folder}/%(title)s.%(ext)s',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            mp3_file = os.path.join(output_folder, f"{info['title']}.mp3")
            return mp3_file
    except Exception as e:
        st.error(f"Terjadi kesalahan saat mengunduh: {e}")
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
            if mp3_file and os.path.exists(mp3_file):
                with open(mp3_file, "rb") as file:
                    st.success("Berhasil! Klik tombol di bawah untuk mengunduh file MP3.")
                    st.download_button(
                        label="Unduh MP3",
                        data=file,
                        file_name=os.path.basename(mp3_file),
                        mime="audio/mp3",
                    )
                os.remove(mp3_file)  # Hapus file setelah selesai
            else:
                st.error("Gagal mengunduh MP3.")
    else:
        st.error("Harap masukkan URL YouTube.")

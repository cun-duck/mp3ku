import os
import shutil
import streamlit as st
import yt_dlp

# Pastikan FFmpeg tersedia
ffmpeg_path = shutil.which("ffmpeg")
if ffmpeg_path is None:
    raise EnvironmentError("FFmpeg tidak ditemukan. Pastikan FFmpeg terinstal di lingkungan Anda.")
os.environ["PATH"] += os.pathsep + os.path.dirname(ffmpeg_path)

# Fungsi untuk mengunduh dan mengonversi video YouTube menjadi MP3
def download_youtube_audio(url, output_folder="downloads"):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Konfigurasi yt-dlp
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

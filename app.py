import stremlit as st
import yt_dlp

def download_audio(url, bitrate):
    ydl_opts = {
        'format': f'bestaudio[abr<={bitrate}]',
        'outtmpl': '%(title)s.%(ext)s',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
            return f"{ydl.prepare_filename(ydl.extract_info(url))}.mp3"
    except Exception as e:
        st.error(f"An error occurred: {e}")
        return None

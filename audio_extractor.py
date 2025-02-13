import yt_dlp

def download_audio(video_url, output_path="audio.mp3"):
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'outtmpl': output_path
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([video_url])

# Example usage
video_url = "https://www.youtube.com/watch?v=b-Pn0yXL9y8"
download_audio(video_url)

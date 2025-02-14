import groq
import yt_dlp

# Initialize Groq client
client = groq.Client(api_key="GROQ_API_KEY")

def download_audio(video_url, output_path="audio.mp3"):
    """Downloads audio from a YouTube video and saves it as an MP3 file."""
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
    
    print(f"Downloaded audio saved as: {output_path}")

def transcribe_audio(audio_file):
    """Transcribes an audio file using Groq Whisper model."""
    with open(audio_file, "rb") as f:
        response = client.audio.transcriptions.create(
            model="whisper-large",
            file=f,  # Pass file object directly
            language="en"
        )

    return response.text

# Example usage:
# video_url = "https://www.youtube.com/watch?v=b-Pn0yXL9y8"  # Replace with your video URL
# download_audio(video_url)  # Download audio

# Transcribe the downloaded audio file
transcription = transcribe_audio("audio.mp3")
print("Transcribed Text:\n", transcription)

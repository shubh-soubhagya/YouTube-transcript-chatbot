import os
import argparse
import yt_dlp

def download_audio(url, output_path=None):
    """
    Downloads audio from a YouTube video and saves it as an MP3 file using yt-dlp.
    
    Args:
        url (str): The YouTube video URL
        output_path (str, optional): Directory to save the MP3 file. Defaults to current directory.
    
    Returns:
        str: Path to the downloaded MP3 file
    """
    # Set default output path if not provided
    output_directory = output_path or "."
    
    # Create output directory if it doesn't exist
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)
    
    # Define options for yt-dlp
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'outtmpl': os.path.join(output_directory, '%(title)s.%(ext)s'),
        'quiet': False,
        'no_warnings': False,
        'ignoreerrors': False,
    }
    
    try:
        print(f"Attempting to download audio from: {url}")
        
        # Download the file with yt-dlp
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            
            # Get the downloaded file path
            if 'title' in info:
                # The file extension will be mp3 because of the postprocessor
                filename = f"{info['title']}.mp3"
                downloaded_file = os.path.join(output_directory, filename)
                print(f"Download complete: {downloaded_file}")
                return downloaded_file
            else:
                print("Download completed but couldn't determine file name.")
                return None
            
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        raise

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Download YouTube audio as MP3")
    parser.add_argument("url", help="YouTube video URL")
    parser.add_argument("-o", "--output", help="Output directory (optional)")
    
    args = parser.parse_args()
    
    try:
        download_audio(args.url, args.output)
    except Exception as e:
        print(f"Failed to download: {str(e)}")
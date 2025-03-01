import re
from urllib.parse import urlparse, parse_qs
from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled, NoTranscriptFound

def extract_video_id(url):
    """
    Extract the video ID from a YouTube URL.
    
    Args:
        url (str): The YouTube URL
    
    Returns:
        str: The video ID or None if not found
    """
    # Handle different URL formats
    if 'youtu.be' in url:
        return url.split('/')[-1].split('?')[0]
    
    if 'youtube.com/watch' in url:
        parsed_url = urlparse(url)
        return parse_qs(parsed_url.query).get('v', [None])[0]
    
    # Handle YouTube shorts
    if 'youtube.com/shorts/' in url:
        return url.split('/')[-1].split('?')[0]
    
    # Try to find a video ID pattern directly
    match = re.search(r'(?:v=|\/)([0-9A-Za-z_-]{11}).*', url)
    if match:
        return match.group(1)
    
    return None

def format_transcript(transcript_segments):
    """
    Format the transcript into a readable text.
    
    Args:
        transcript_segments (list): List of transcript segments
    
    Returns:
        str: Formatted transcript text
    """
    if not transcript_segments:
        return ""
    
    full_text = ""
    for segment in transcript_segments:
        text = segment.get('text', '')
        # Add a space between segments if needed
        if full_text and not full_text.endswith((' ', '\n')):
            full_text += " "
        full_text += text
    
    return full_text

def format_transcript_with_timestamps(transcript_segments):
    """
    Format the transcript with timestamps.
    
    Args:
        transcript_segments (list): List of transcript segments
    
    Returns:
        str: Formatted transcript text with timestamps
    """
    if not transcript_segments:
        return ""
    
    formatted_text = ""
    for segment in transcript_segments:
        start_time = segment.get('start', 0)
        text = segment.get('text', '')
        
        # Convert seconds to MM:SS format
        minutes = int(start_time // 60)
        seconds = int(start_time % 60)
        timestamp = f"[{minutes:02d}:{seconds:02d}] "
        
        formatted_text += f"{timestamp}{text}\n"
    
    return formatted_text

def get_transcript(video_url, language=None):
    """
    Get the transcript for a YouTube video.
    
    Args:
        video_url (str): The YouTube video URL
        language (str, optional): Language code for the transcript (e.g., 'en')
    
    Returns:
        dict: Dictionary with 'success', 'transcript' and 'error' keys
    """
    video_id = extract_video_id(video_url)
    
    if not video_id:
        return {
            'success': False,
            'transcript': None,
            'error': 'Could not extract video ID from URL'
        }
    
    # Try to get transcript with YouTube Transcript API
    try:
        if language:
            transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
            transcript = transcript_list.find_transcript([language]).fetch()
        else:
            transcript = YouTubeTranscriptApi.get_transcript(video_id)
        
        # Format the transcript
        formatted_transcript = format_transcript(transcript)
        return {
            'success': True,
            'transcript': formatted_transcript,
            'error': None
        }
    
    except (TranscriptsDisabled, NoTranscriptFound) as e:
        error_msg = f"Transcript not available: {str(e)}"
        print(error_msg)
        return {
            'success': False,
            'transcript': None,
            'error': error_msg
        }
    
    except Exception as e:
        error_msg = f"Error retrieving transcript: {str(e)}"
        print(error_msg)
        return {
            'success': False,
            'transcript': None,
            'error': error_msg
        }

def get_transcript_with_timestamps(video_url, language=None):
    """
    Get the transcript with timestamps.
    
    Args:
        video_url (str): The YouTube video URL
        language (str, optional): Language code for the transcript
    
    Returns:
        dict: Dictionary with 'success', 'transcript' and 'error' keys
    """
    video_id = extract_video_id(video_url)
    
    if not video_id:
        return {
            'success': False,
            'transcript': None,
            'error': 'Could not extract video ID from URL'
        }
    
    try:
        if language:
            transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
            transcript = transcript_list.find_transcript([language]).fetch()
        else:
            transcript = YouTubeTranscriptApi.get_transcript(video_id)
        
        # Format the transcript with timestamps
        formatted_transcript = format_transcript_with_timestamps(transcript)
        return {
            'success': True,
            'transcript': formatted_transcript,
            'error': None
        }
    
    except Exception as e:
        error_msg = f"Error retrieving transcript: {str(e)}"
        print(error_msg)
        return {
            'success': False,
            'transcript': None,
            'error': error_msg
        }

def save_transcript_to_file(transcript, output_path):
    """
    Save the transcript to a file.
    
    Args:
        transcript (str): The transcript text
        output_path (str): Path to save the file
    
    Returns:
        bool: Success status
    """
    try:
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(transcript)
        return True
    except Exception as e:
        print(f"Error saving transcript: {e}")
        return False

def main():
    # Get input from user
    youtube_url = input("Enter YouTube URL: ")
    
    # Get transcript
    result = get_transcript(youtube_url)
    
    if result['success']:
        print("Transcript extracted successfully!")
        print("\nPreview:")
        preview_text = result['transcript'][:200] + "..." if len(result['transcript']) > 200 else result['transcript']
        print(preview_text)
        
        # Save to file
        output_file = "transcript.txt"
        if save_transcript_to_file(result['transcript'], output_file):
            print(f"\nTranscript saved to {output_file}")
            
        # Optional: Get transcript with timestamps
        timestamp_result = get_transcript_with_timestamps(youtube_url)
        if timestamp_result['success']:
            timestamp_file = "transcript_with_timestamps.txt"
            save_transcript_to_file(timestamp_result['transcript'], timestamp_file)
            print(f"Transcript with timestamps saved to {timestamp_file}")
    else:
        print(f"Failed to extract transcript: {result['error']}")

if __name__ == "__main__":
    main()
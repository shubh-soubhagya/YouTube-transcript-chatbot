import re
from urllib.parse import urlparse, parse_qs
from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled, NoTranscriptFound
from transcript_extractor.exception import get_transcript, get_transcript_with_timestamps
from transcript_extractor.saving_file import save_transcript_to_file
import os

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
        # output_file = r"C:\Users\hp\Desktop\ytpro\YouTube-support-chatbot\temp_files\transcript.txt"
        output_file = os.path.join("temp_files", "transcript.txt")

        if save_transcript_to_file(result['transcript'], output_file):
            print(f"\nTranscript saved to {output_file}")
            
        # Optional: Get transcript with timestamps
        timestamp_result = get_transcript_with_timestamps(youtube_url)
        if timestamp_result['success']:
            # timestamp_file = r"C:\Users\hp\Desktop\ytpro\YouTube-support-chatbot\temp_files\transcripts_with_timestamps.txt"
            timestamp_file = os.path.join("temp_files", "transcripts_with_timestamps.txt")
            save_transcript_to_file(timestamp_result['transcript'], timestamp_file)
            print(f"Transcript with timestamps saved to {timestamp_file}")
    else:
        print(f"Failed to extract transcript: {result['error']}")

if __name__ == "__main__":
    main()
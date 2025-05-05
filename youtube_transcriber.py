import os
import subprocess
import whisper

def download_and_transcribe_with_ytdlp(youtube_url, output_directory="downloads"):
    """
    Download a YouTube video as audio using yt-dlp and transcribe it with Whisper.
    
    Args:
        youtube_url (str): URL of the YouTube video
        output_directory (str): Directory to save the downloaded audio
        
    Returns:
        str: Transcription of the audio
    """
    # Create output directory if it doesn't exist
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)
    
    # Generate a filename based on the video ID or URL
    import hashlib
    filename_base = hashlib.md5(youtube_url.encode()).hexdigest()
    audio_file = os.path.join(output_directory, f"{filename_base}.mp3")
    
    # Download audio using yt-dlp
    print(f"Downloading audio from: {youtube_url}")
    command = [
        "yt-dlp",
        "-x",  # Extract audio
        "--audio-format", "mp3",  # Convert to mp3
        "--audio-quality", "0",  # Best quality
        "-o", audio_file,  # Output filename
        youtube_url  # URL to download
    ]
    
    try:
        subprocess.run(command, check=True)
        print(f"Audio downloaded to: {audio_file}")
    except subprocess.CalledProcessError as e:
        raise Exception(f"Failed to download video: {e}")
    except FileNotFoundError:
        raise Exception("yt-dlp not found. Please install it with 'pip install yt-dlp'")
    
    # Load Whisper model
    print("Loading Whisper model...")
    model = whisper.load_model("base")  # Options: tiny, base, small, medium, large
    
    # Transcribe audio
    print("Transcribing audio...")
    result = model.transcribe(audio_file)
    
    # Get the transcription text
    transcript = result["text"]
    
    # Save transcript to file
    transcript_file = os.path.splitext(audio_file)[0] + '.txt'
    with open(transcript_file, 'w', encoding='utf-8') as f:
        f.write(transcript)
    
    print(f"Transcription saved to: {transcript_file}")
    
    return transcript

# Example usage
if __name__ == "__main__":
    video_url = input("Enter YouTube URL: ")
    try:
        transcript = download_and_transcribe_with_ytdlp(video_url)
        print("\nTranscript:")
        print(transcript)
    except Exception as e:
        print(f"Error: {str(e)}")
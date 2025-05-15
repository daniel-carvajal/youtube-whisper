import os
import subprocess
import whisper

def download_and_transcribe_with_ytdlp(youtube_url, output_directory="transcripts"):
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
    # See /site-packages/whisper/__init__.py
    # _MODELS = {
    #     "tiny.en": "https://openaipublic.azureedge.net/main/whisper/models/d3dd57d32accea0b295c96e26691aa14d8822fac7d9d27d5dc00b4ca2826dd03/tiny.en.pt",
    #     "tiny": "https://openaipublic.azureedge.net/main/whisper/models/65147644a518d12f04e32d6f3b26facc3f8dd46e5390956a9424a650c0ce22b9/tiny.pt",
    #     "base.en": "https://openaipublic.azureedge.net/main/whisper/models/25a8566e1d0c1e2231d1c762132cd20e0f96a85d16145c3a00adf5d1ac670ead/base.en.pt",
    #     "base": "https://openaipublic.azureedge.net/main/whisper/models/ed3a0b6b1c0edf879ad9b11b1af5a0e6ab5db9205f891f668f8b0e6c6326e34e/base.pt",
    #     "small.en": "https://openaipublic.azureedge.net/main/whisper/models/f953ad0fd29cacd07d5a9eda5624af0f6bcf2258be67c92b79389873d91e0872/small.en.pt",
    #     "small": "https://openaipublic.azureedge.net/main/whisper/models/9ecf779972d90ba49c06d968637d720dd632c55bbf19d441fb42bf17a411e794/small.pt",
    #     "medium.en": "https://openaipublic.azureedge.net/main/whisper/models/d7440d1dc186f76616474e0ff0b3b6b879abc9d1a4926b7adfa41db2d497ab4f/medium.en.pt",
    #     "medium": "https://openaipublic.azureedge.net/main/whisper/models/345ae4da62f9b3d59415adc60127b97c714f32e89e936602e85993674d08dcb1/medium.pt",
    #     "large-v1": "https://openaipublic.azureedge.net/main/whisper/models/e4b87e7e0bf463eb8e6956e646f1e277e901512310def2c24bf0e11bd3c28e9a/large-v1.pt",
    #     "large-v2": "https://openaipublic.azureedge.net/main/whisper/models/81f7c96c852ee8fc832187b0132e569d6c3065a3252ed18e56effd0b6a73e524/large-v2.pt",
    #     "large-v3": "https://openaipublic.azureedge.net/main/whisper/models/e5b1a55b89c1367dacf97e3e19bfd829a01529dbfdeefa8caeb59b3f1b81dadb/large-v3.pt",
    #     "large": "https://openaipublic.azureedge.net/main/whisper/models/e5b1a55b89c1367dacf97e3e19bfd829a01529dbfdeefa8caeb59b3f1b81dadb/large-v3.pt",
    #     "large-v3-turbo": "https://openaipublic.azureedge.net/main/whisper/models/aff26ae408abcba5fbf8813c21e62b0941638c5f6eebfb145be0c9839262a19a/large-v3-turbo.pt",
    #     "turbo": "https://openaipublic.azureedge.net/main/whisper/models/aff26ae408abcba5fbf8813c21e62b0941638c5f6eebfb145be0c9839262a19a/large-v3-turbo.pt",
    # }
    model = whisper.load_model("medium")  # Options: tiny, base, small, medium, large
    
    # Transcribe audio
    print("Transcribing audio...")
    result = model.transcribe(audio_file, language="en")
    
    # Get the transcription text
    transcript = result["text"]
    
    # Save full transcript to file
    transcript_file = os.path.splitext(audio_file)[0] + '.txt'
    with open(transcript_file, 'w', encoding='utf-8') as f:
        f.write(transcript)
    
    print(f"Full transcription saved to: {transcript_file}")
    
    # Save timestamped segments to separate file
    segments_file = os.path.splitext(audio_file)[0] + '_segments.txt'
    with open(segments_file, 'w', encoding='utf-8') as f:
        for segment in result["segments"]:
            start_time = segment["start"]
            end_time = segment["end"]
            text = segment["text"]
            f.write(f"[{start_time:.2f}s - {end_time:.2f}s] {text.strip()}\n")
            print(f"[{start_time:.2f}s - {end_time:.2f}s] {text.strip()}")
    
    print(f"Timestamped segments saved to: {segments_file}")
    
    return transcript

# Example usage
if __name__ == "__main__":
    video_url = input("Enter YouTube URL: ")
    try:
        transcript = download_and_transcribe_with_ytdlp(video_url)
        # print("\nTranscript:")
        # print(transcript)
    except Exception as e:
        print(f"Error: {str(e)}")
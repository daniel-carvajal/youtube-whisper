import os
import sys
import subprocess
import re
from typing import List, Optional, Dict, Any

# Try importing the required packages
try:
    from youtube_transcript_api import YouTubeTranscriptApi, TranscriptList
    import whisper
except ImportError:
    print("Required packages not found. Installing packages...")
    subprocess.run([sys.executable, "-m", "pip", "install", "youtube-transcript-api", "openai-whisper", "yt-dlp"], check=True)
    from youtube_transcript_api import YouTubeTranscriptApi, TranscriptList
    import whisper

class YouTubeTranscriptTool:
    """
    A tool to either fetch YouTube video transcripts using youtube-transcript-api
    or download and transcribe videos locally with Whisper.
    """
    
    WHISPER_MODELS = [
        "tiny", "tiny.en", 
        "base", "base.en", 
        "small", "small.en", 
        "medium", "medium.en", 
        "large", "large-v1", "large-v2", "large-v3", "large-v3-turbo", "turbo"
    ]
    
    @staticmethod
    def get_downloaded_models() -> List[str]:
        """
        Check which Whisper models have already been downloaded.
        Returns a list of model names that are already downloaded.
        """
        # Whisper models are stored in ~/.cache/whisper/
        cache_dir = os.path.expanduser("~/.cache/whisper")
        if not os.path.exists(cache_dir):
            return []
            
        downloaded_models = []
        for model_name in YouTubeTranscriptTool.WHISPER_MODELS:
            # Models are stored as [model_name].pt
            model_path = os.path.join(cache_dir, f"{model_name}.pt")
            if os.path.exists(model_path):
                downloaded_models.append(model_name)
                
        return downloaded_models
    
    def __init__(self, output_directory: str = "transcripts"):
        """Initialize the tool with an output directory."""
        self.output_directory = output_directory
        if not os.path.exists(output_directory):
            os.makedirs(output_directory)
        self.ytt_api = YouTubeTranscriptApi()
    
    def extract_video_id(self, youtube_url: str) -> str:
        """Extract the video ID from a YouTube URL or return the ID if already an ID."""
        # Check if it's already just an ID (11 characters)
        if re.match(r'^[A-Za-z0-9_-]{11}$', youtube_url):
            return youtube_url
            
        # Try to extract from URL
        video_id_match = re.search(r'(?:v=|\/videos\/|embed\/|youtu.be\/|\/v\/|\/e\/|watch\?v=|&v=)([^#\&\?\/]{11})', youtube_url)
        if video_id_match:
            return video_id_match.group(1)
        else:
            raise ValueError("Could not extract video ID from URL. Please provide a valid YouTube URL or video ID.")
    
    def get_available_languages(self, video_id: str) -> List[Dict[str, str]]:
        """Get all available languages for a video transcript."""
        transcript_list = self.ytt_api.list(video_id)
        languages = []
        
        for transcript in transcript_list:
            languages.append({
                'language': transcript.language,
                'language_code': transcript.language_code,
                'is_generated': transcript.is_generated
            })
            
        return languages
    
    def fetch_transcript(self, youtube_url: str, languages: List[str] = ['en'], preserve_formatting: bool = False) -> Dict[str, Any]:
        """
        Fetch transcript using youtube-transcript-api.
        
        Args:
            youtube_url: YouTube URL or video ID
            languages: List of language codes to try (in order of preference)
            preserve_formatting: Whether to preserve HTML formatting elements
            
        Returns:
            Dictionary with video ID, language, and transcript data
        """
        video_id = self.extract_video_id(youtube_url)
        
        try:
            transcript = self.ytt_api.fetch(video_id, languages=languages, preserve_formatting=preserve_formatting)
            
            # Save transcript to file
            output_path = os.path.join(self.output_directory, f"{video_id}_transcript.txt")
            with open(output_path, 'w', encoding='utf-8') as f:
                for snippet in transcript:
                    f.write(f"[{snippet.start:.2f}s - {(snippet.start + snippet.duration):.2f}s] {snippet.text}\n")
            
            print(f"Transcript saved to: {output_path}")
            
            return {
                'video_id': video_id,
                'language': transcript.language,
                'language_code': transcript.language_code,
                'is_generated': transcript.is_generated,
                'transcript': transcript.to_raw_data(),
                'file_path': output_path
            }
            
        except Exception as e:
            print(f"Error fetching transcript: {str(e)}")
            raise
    
    def download_and_transcribe(self, youtube_url: str, model_name: str = "large") -> Dict[str, Any]:
        """
        Download a YouTube video as audio and transcribe it with Whisper.
        
        Args:
            youtube_url: YouTube URL or video ID
            model_name: Whisper model name to use
            
        Returns:
            Dictionary with transcription data and file paths
        """
        if model_name not in self.WHISPER_MODELS:
            raise ValueError(f"Invalid model name. Choose from: {', '.join(self.WHISPER_MODELS)}")
        
        video_id = self.extract_video_id(youtube_url)
        audio_file = os.path.join(self.output_directory, f"{video_id}.mp3")
        
        # Download audio using yt-dlp
        print(f"Downloading audio from: {youtube_url}")
        youtube_full_url = f"https://www.youtube.com/watch?v={video_id}" if len(video_id) == 11 else youtube_url
        
        command = [
            "yt-dlp",
            "-x",  # Extract audio
            "--audio-format", "mp3",  # Convert to mp3
            "--audio-quality", "0",  # Best quality
            "-o", audio_file,  # Output filename
            youtube_full_url  # URL to download
        ]
        
        try:
            subprocess.run(command, check=True)
            print(f"Audio downloaded to: {audio_file}")
        except subprocess.CalledProcessError as e:
            raise Exception(f"Failed to download video: {e}")
        except FileNotFoundError:
            raise Exception("yt-dlp not found. Please install it with 'pip install yt-dlp'")
        
        # Check if model is already downloaded
        downloaded_models = self.get_downloaded_models()
        if model_name not in downloaded_models:
            print(f"Downloading Whisper model '{model_name}'...")
        else:
            print(f"Loading existing Whisper model '{model_name}'...")
            
        # Load Whisper model
        model = whisper.load_model(model_name)
        
        # Transcribe audio
        print("Transcribing audio...")
        result = model.transcribe(audio_file)
        
        # Save full transcript to file
        transcript_file = os.path.splitext(audio_file)[0] + '_transcript.txt'
        with open(transcript_file, 'w', encoding='utf-8') as f:
            f.write(result["text"])
        
        # Save timestamped segments to separate file
        segments_file = os.path.splitext(audio_file)[0] + '_segments.txt'
        with open(segments_file, 'w', encoding='utf-8') as f:
            for segment in result["segments"]:
                start_time = segment["start"]
                end_time = segment["end"]
                text = segment["text"]
                f.write(f"[{start_time:.2f}s - {end_time:.2f}s] {text.strip()}\n")
        
        print(f"Full transcription saved to: {transcript_file}")
        print(f"Timestamped segments saved to: {segments_file}")
        
        return {
            'video_id': video_id,
            'transcript': result["text"],
            'segments': result["segments"],
            'transcript_file': transcript_file,
            'segments_file': segments_file,
            'audio_file': audio_file
        }

def main():
    print("===== YouTube Transcript Tool =====")
    print("This tool can either:")
    print("1. Fetch a transcript using youtube-transcript-api")
    print("2. Download a video and transcribe it locally with Whisper")
    
    choice = input("\nEnter your choice (1 or 2): ").strip()
    
    youtube_url = input("\nEnter YouTube URL or video ID: ").strip()
    
    tool = YouTubeTranscriptTool()
    
    if choice == "1":
        # Fetch transcript using youtube-transcript-api
        try:
            video_id = tool.extract_video_id(youtube_url)
            print(f"\nFetching available languages for video {video_id}...")
            languages = tool.get_available_languages(video_id)
            
            if not languages:
                print("No transcripts available for this video.")
                return
            
            print("\nAvailable languages:")
            for i, lang in enumerate(languages, 1):
                created_type = "Auto-generated" if lang['is_generated'] else "Manually created"
                print(f"{i}. {lang['language']} ({lang['language_code']}) - {created_type}")
            
            lang_choice = input("\nEnter language number (default is 1): ").strip()
            lang_choice = int(lang_choice) if lang_choice else 1
            
            if 1 <= lang_choice <= len(languages):
                selected_lang = languages[lang_choice-1]['language_code']
                preserve_format = input("Preserve HTML formatting? (y/n, default is n): ").strip().lower() == 'y'
                
                result = tool.fetch_transcript(youtube_url, languages=[selected_lang], preserve_formatting=preserve_format)
                
                print("\nTranscript preview (first 5 snippets):")
                for i, snippet in enumerate(result['transcript'][:5]):
                    print(f"[{snippet['start']:.2f}s] {snippet['text']}")
                
                if len(result['transcript']) > 5:
                    print(f"... and {len(result['transcript']) - 5} more snippets")
                
                print(f"\nFull transcript saved to: {result['file_path']}")
                
            else:
                print("Invalid selection.")
                
        except Exception as e:
            print(f"Error: {str(e)}")
            
    elif choice == "2":
        # Download and transcribe with Whisper
        try:
            # Get list of already downloaded models
            downloaded_models = tool.get_downloaded_models()
            
            print("\nAvailable Whisper models:")
            for i, model in enumerate(tool.WHISPER_MODELS, 1):
                # Mark already downloaded models with a checkmark
                status = "✓" if model in downloaded_models else " "
                print(f"{i}. [{status}] {model}")
            
            if downloaded_models:
                print("\n(✓) = Already downloaded")
            
            model_choice = input("\nEnter model number (default is 'large'): ").strip()
            
            if model_choice:
                try:
                    model_index = int(model_choice) - 1
                    if 0 <= model_index < len(tool.WHISPER_MODELS):
                        selected_model = tool.WHISPER_MODELS[model_index]
                    else:
                        print("Invalid selection, using 'large' model.")
                        selected_model = "large"
                except ValueError:
                    print("Invalid input, using 'large' model.")
                    selected_model = "large"
            else:
                selected_model = "large"
            
            # Let user know if they're downloading a new model
            if selected_model not in downloaded_models:
                print(f"\nNote: The '{selected_model}' model will be downloaded. This may take some time depending on your internet connection.")
            else:
                print(f"\nUsing already downloaded '{selected_model}' model.")
                
            print(f"Using Whisper model: {selected_model}")
            result = tool.download_and_transcribe(youtube_url, model_name=selected_model)
            
            print("\nTranscription complete!")
            print(f"Full transcript saved to: {result['transcript_file']}")
            print(f"Timestamped segments saved to: {result['segments_file']}")
            
            # Preview first few segments
            print("\nTranscript preview (first 5 segments):")
            for i, segment in enumerate(result['segments'][:5]):
                print(f"[{segment['start']:.2f}s - {segment['end']:.2f}s] {segment['text'].strip()}")
            
            if len(result['segments']) > 5:
                print(f"... and {len(result['segments']) - 5} more segments")
                
        except Exception as e:
            print(f"Error: {str(e)}")
    else:
        print("Invalid choice. Please run the script again and select either 1 or 2.")

if __name__ == "__main__":
    main()
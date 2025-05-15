# YouTube Transcript Tool

A versatile Python tool that offers two powerful methods to get transcripts from YouTube videos:
1. Fetch existing transcripts directly from YouTube using the YouTube Transcript API
2. Download the video audio and transcribe it locally using OpenAI's Whisper speech recognition model

## Features

### Common Features
- Works with both YouTube URLs and video IDs
- Saves timestamped transcripts to easily reference specific moments
- Handles errors gracefully with informative messages
- Organizes all transcripts in a dedicated directory

### YouTube Transcript API Features
- Lists all available languages for a video's transcript
- Allows selecting specific language preferences
- Option to preserve HTML formatting (like italics and bold)
- Works with both manually created and auto-generated subtitles
- No need to download the video's audio

### Whisper Transcription Features
- Downloads audio from any YouTube video using yt-dlp
- Transcribes audio content with OpenAI's Whisper model
- Shows which models are already downloaded on your system
- Supports all Whisper model sizes (tiny through large and turbo)
- Creates both full transcripts and timestamped segment files

## Requirements

- Python 3.8 or higher
- ffmpeg (required for audio processing with Whisper)
- Required Python packages (automatically installed if missing):
  - youtube-transcript-api
  - openai-whisper
  - yt-dlp

## Installation

1. Clone this repository:
   ```
   git clone https://github.com/yourusername/youtube-transcript-tool.git
   cd youtube-transcript-tool
   ```

2. (Recommended) Set up a virtual environment:
   ```
   # Create virtual environment
   python -m venv venv
   
   # Activate on macOS/Linux
   source venv/bin/activate
   
   # Activate on Windows
   venv\Scripts\activate
   ```

3. Install required dependencies:
   ```
   pip install youtube-transcript-api openai-whisper yt-dlp
   ```

4. Install ffmpeg (required for audio processing with Whisper):
   
   **macOS**:
   ```
   brew install ffmpeg
   ```
   
   **Ubuntu/Debian**:
   ```
   sudo apt update && sudo apt install ffmpeg
   ```
   
   **Windows (with Chocolatey)**:
   ```
   choco install ffmpeg
   ```
   
   **Windows (with Scoop)**:
   ```
   scoop install ffmpeg
   ```

## Usage

Run the script:
```
python youtube_transcript_tool.py
```

The program will:
1. Ask whether you want to fetch a transcript or download and transcribe locally
2. Prompt for a YouTube URL or video ID
3. Based on your choice:
   - If fetching: Show available languages and formatting options
   - If transcribing: Show available Whisper models (with checkmarks for already downloaded models)
4. Process the video and save transcript files
5. Display a preview of the transcript

## Output Files

For each YouTube video, the tool generates:

### When fetching transcripts:
- `[video_id]_transcript.txt`: Timestamped transcript from YouTube

### When transcribing locally:
- `[video_id].mp3`: The downloaded audio file
- `[video_id]_transcript.txt`: The full transcript text
- `[video_id]_segments.txt`: Timestamped segments of the transcript

## Whisper Models

The tool supports all Whisper models with varying capabilities:

| Model | Parameters | Description | Approx. VRAM Required |
|-------|------------|-------------|----------------------|
| tiny/tiny.en | 39M | Fastest, least accurate | ~1GB |
| base/base.en | 74M | Fast, moderate accuracy | ~1GB |
| small/small.en | 244M | Good balance for most uses | ~2GB |
| medium/medium.en | 769M | High accuracy, moderate speed | ~5GB |
| large/large-v1/large-v2/large-v3 | 1.5B | Most accurate, slowest | ~10GB |
| large-v3-turbo/turbo | 1.5B+ | Fast and relatively accurate | ~10GB |

The ".en" models are specialized for English and may perform better for English-only content. Parameter count and VRAM requirements based on official OpenAI documentation.

## How It Works

This tool combines three powerful libraries:
- **YouTube Transcript API**: Retrieves existing transcripts directly from YouTube
- **yt-dlp**: A feature-rich YouTube downloader for audio extraction
- **OpenAI Whisper**: A state-of-the-art speech recognition model that can transcribe audio in multiple languages

## Advanced Usage

### Cookie Authentication for Age-Restricted Videos

For age-restricted videos, you can provide a cookies.txt file:
```python
tool = YouTubeTranscriptTool(cookie_path='/path/to/your/cookies.txt')
```

### Working with Different Languages

The tool lets you specify language preferences when fetching transcripts:
```python
result = tool.fetch_transcript(youtube_url, languages=['de', 'en'])  # Try German first, then English
```

### Customizing the Output Directory

You can specify where to save transcripts and audio files:
```python
tool = YouTubeTranscriptTool(output_directory="my_transcripts")
```

## License

[MIT License](LICENSE)

## Acknowledgments

- [YouTube Transcript API](https://github.com/jdepoix/youtube-transcript-api)
- [OpenAI Whisper](https://github.com/openai/whisper)
- [yt-dlp](https://github.com/yt-dlp/yt-dlp)
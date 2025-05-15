# YouTube Video Transcriber

A powerful Python tool that downloads audio from YouTube videos and transcribes them using OpenAI's Whisper speech recognition model, with timestamped segments for precise reference.

## Features

- Downloads audio from any YouTube video using yt-dlp
- Transcribes audio content with OpenAI's Whisper model
- Creates both full transcripts and timestamped segment files
- Handles various audio formats and qualities
- Uses content hashing to prevent duplicate downloads
- Provides real-time progress updates during processing

## Requirements

- Python 3.6 or higher
- ffmpeg (required for audio processing)
- Required Python packages (see requirements.txt)

## Installation

1. Clone this repository:
   ```
   git clone https://github.com/daniel-carvajal/youtube-whisper.git
   cd youtube-transcriber
   ```

2. (Recommended) Set up a virtual environment to isolate dependencies:
   ```
   # Install pyenv if not already installed
   # On macOS/Linux
   curl https://pyenv.run | bash
   
   # pyenv will automatically use the Python version specified in .python-version
   # No need to manually set the Python version
   
   # Create and activate virtual environment
   python -m venv venv
   
   # Activate on macOS/Linux
   source venv/bin/activate
   
   # Activate on Windows
   venv\Scripts\activate
   ```

3. Install required dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Install ffmpeg (required for audio processing):
   
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

> **Note:** If you created a virtual environment in step 2, ensure it's activated before running the script. You'll know it's activated when you see `(venv)` at the beginning of your command prompt.

Run the script and enter a YouTube URL when prompted:

```
python yt_transcribe.py
```

The program will:
1. Download the audio from the YouTube video in MP3 format
2. Load the Whisper model (default: "medium" model)
3. Transcribe the audio with English language detection
4. Save the full transcript to a text file
5. Create a separate file with timestamped segments
6. Display progress throughout the process

## Output Files

For each transcription, the tool generates:
- `[hash].mp3`: The downloaded audio file
- `[hash].txt`: The full transcript text
- `[hash]_segments.txt`: Timestamped segments of the transcript

## Customization

You can modify the script to use different Whisper models:

- `tiny`: Fastest, least accurate (~1GB VRAM)
- `base`: Good balance for most uses (~1GB VRAM)
- `small`: More accurate, moderate speed (~2GB VRAM)
- `medium`: High accuracy, slower (default, ~5GB VRAM)
- `large`: Most accurate, slowest (~10GB VRAM)
- `turbo`: Fast and relatively accurate (~6GB VRAM)

To change the model, modify the `model = whisper.load_model("medium")` line in the script.

## How It Works

This tool combines two powerful libraries:
- **yt-dlp**: A feature-rich YouTube downloader, fork of youtube-dl with additional features and fixes
- **OpenAI Whisper**: A general-purpose speech recognition model that can transcribe audio in multiple languages

The script:
1. Hashes the YouTube URL to create unique filenames
2. Uses yt-dlp to download high-quality MP3 audio
3. Loads the specified Whisper model
4. Performs transcription with language detection
5. Saves both the complete transcript and timestamped segments

## License

[MIT License](LICENSE)

## Acknowledgments

- [OpenAI Whisper](https://github.com/openai/whisper)
- [yt-dlp](https://github.com/yt-dlp/yt-dlp)
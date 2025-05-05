# YouTube Video Transcriber

A simple Python tool that downloads audio from YouTube videos and transcribes them using OpenAI's Whisper speech recognition model.

## Features

- Downloads audio from any YouTube video
- Automatically transcribes the audio content
- Saves both the audio file and transcription text
- Handles errors gracefully with retries
- Simple command-line interface

## Requirements

- Python 3.6 or higher
- ffmpeg (required for Whisper)
- Required Python packages (see requirements.txt)

## Installation

1. Clone this repository:
   ```
   git clone https://github.com/daniel-carvajal/youtube-whisper.git
   cd youtube-transcriber
   ```

2. Install required dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Install ffmpeg (required for audio processing):

   **Ubuntu/Debian**:
   ```
   sudo apt update && sudo apt install ffmpeg
   ```

   **macOS**:
   ```
   brew install ffmpeg
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

Run the script and enter a YouTube URL when prompted:

```
python youtube_transcriber.py
```

The program will:
1. Download the audio from the YouTube video
2. Load the Whisper model (default: "base" model)
3. Transcribe the audio
4. Save the transcript to a text file
5. Print the transcript to the console

## Customization

You can modify the script to use different Whisper models:

- `tiny`: Fastest, least accurate
- `base`: Good balance for most uses
- `small`: More accurate, slower
- `medium`: High accuracy, slower
- `large`: Most accurate, slowest
- `turbo`: Fast and relatively accurate

To change the model, modify the `model = whisper.load_model("base")` line in the script.

## How It Works

This tool combines two powerful libraries:
- **yt-dlp**: A feature-rich YouTube downloader, fork of youtube-dl with additional features and fixes
- **OpenAI Whisper**: A general-purpose speech recognition model that can transcribe audio in multiple languages

## License

[MIT License](LICENSE)

## Acknowledgments

- [OpenAI Whisper](https://github.com/openai/whisper)
- [yt-dlp](https://github.com/yt-dlp/yt-dlp)

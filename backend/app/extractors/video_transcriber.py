import whisper   # OpenAI Whisper for transcription

model = whisper.load_model("base")     # Load a light Whisper model for good performance

def transcribe_video(file_path: str) -> str:
    """
    Converts spoken audio inside a video file into text using Whisper.
    """

    result = model.transcribe(file_path)    # Run Whisper transcription
    return result["text"]                   # Return only the transcribed text

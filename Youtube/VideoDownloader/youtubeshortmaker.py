import os
import subprocess
import tempfile
from moviepy.editor import VideoFileClip
import torch
from transformers import pipeline
# For transcription (e.g., Whisper)
# pip install git+https://github.com/openai/whisper.git
import whisper

# ----------------------------
# Configuration
# ----------------------------
INPUT_VIDEO = "videoplayback.mp4"
OUTPUT_CLIP = "highlight_clip.mp4"
TARGET_CLIP_LENGTH = 60  # seconds (1 min)
# (Optionally 120 for 2 minutes or make this a variable)

# ----------------------------
# Step 1: Extract Audio from Video
# ----------------------------
def extract_audio(input_video, output_audio="audio.wav"):
    cmd = [
        "ffmpeg",
        "-y",  # overwrite
        "-i", input_video,
        "-vn",  # no video
        "-acodec", "pcm_s16le",
        "-ar", "16000",
        "-ac", "1",
        output_audio
    ]
    subprocess.run(cmd, check=True)
    return output_audio

# ----------------------------
# Step 2: Transcribe Audio using Whisper
# ----------------------------
def transcribe_audio(audio_path):
    model = whisper.load_model("small")  # choose a suitable model size
    result = model.transcribe(audio_path)
    return result["text"], result["segments"]

# segments is a list of:
# {
#   'id': segment_id,
#   'seek': start_sample,
#   'start': start_time_in_seconds,
#   'end': end_time_in_seconds,
#   'text': transcript_segment
# }

# ----------------------------
# Step 3: Analyze transcript segments using sentiment analysis
# ----------------------------
def analyze_segments(segments):
    # Load a sentiment pipeline (example: distilbert-base-uncased-finetuned-sst-2-english)
    sentiment_pipeline = pipeline("sentiment-analysis", model="distilbert-base-uncased-finetuned-sst-2-english")

    scored_segments = []
    for seg in segments:
        text = seg["text"]
        sentiment = sentiment_pipeline(text[:512])  # truncate text if very long
        # sentiment returns something like: [{'label': 'POSITIVE', 'score': 0.99}]
        score = sentiment[0]['score'] if sentiment[0]['label'] == 'POSITIVE' else (1 - sentiment[0]['score'])
        # The idea: if positive label, higher score = more interesting. 
        # If negative, invert score. Adjust logic as needed.
        scored_segments.append({
            "start": seg["start"],
            "end": seg["end"],
            "text": seg["text"],
            "score": score
        })
    return scored_segments

# ----------------------------
# Step 4: Select the best segment(s)
# ----------------------------
def select_best_segment(scored_segments, target_length=60):
    # Sort segments by their score descending
    scored_segments.sort(key=lambda x: x["score"], reverse=True)

    # Find a segment or a sequence of segments close to target_length
    # Simple approach: just pick the single highest scoring segment that fits the length requirement.
    # More sophisticated approach: combine top segments to approximate target_length.
    # For simplicity, let's pick the top scoring segment that is at least `target_length` or the top one if none matches.
    
    # Try to find a segment >= target_length seconds long
    for seg in scored_segments:
        duration = seg["end"] - seg["start"]
        if duration >= target_length:
            return seg["start"], seg["end"]

    # If none are that long, pick the top segment and you might have to adjust by adding neighboring segments or just accept shorter length.
    best = scored_segments[0]
    return best["start"], best["end"]

# ----------------------------
# Step 5: Cut the video using FFmpeg or MoviePy
# ----------------------------
def cut_video(input_video, start_time, end_time, output_video):
    clip = VideoFileClip(input_video).subclip(start_time, end_time)
    clip.write_videofile(output_video, codec="libx264", audio_codec="aac")

# ----------------------------
# Main pipeline
# ----------------------------
if __name__ == "__main__":
    with tempfile.TemporaryDirectory() as tmpdir:
        audio_path = os.path.join(tmpdir, "audio.wav")
        
        print("Extracting audio...")
        extract_audio(INPUT_VIDEO, audio_path)

        print("Transcribing audio...")
        transcript_text, segments = transcribe_audio(audio_path)

        print("Analyzing segments...")
        scored_segments = analyze_segments(segments)

        print("Selecting best segment...")
        start, end = select_best_segment(scored_segments, TARGET_CLIP_LENGTH)

        print(f"Selected segment from {start} to {end} seconds.")

        print("Cutting video...")
        cut_video(INPUT_VIDEO, start, end, OUTPUT_CLIP)

        print(f"Highlight clip saved to {OUTPUT_CLIP}.")

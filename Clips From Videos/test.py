import os
import numpy as np
import librosa
from moviepy.editor import VideoFileClip, concatenate_videoclips
from scenedetect import VideoManager, SceneManager
from scenedetect.detectors import ContentDetector

def extract_audio(video_path, audio_path):
    """
    Extracts audio from the video and saves it as a WAV file.
    """
    video = VideoFileClip(video_path)
    video.audio.write_audiofile(audio_path, logger=None)
    video.close()

def analyze_audio(audio_path, top_n=10):
    """
    Analyzes the audio to find the timestamps with the highest energy.
    Returns a list of times in seconds.
    """
    y, sr = librosa.load(audio_path, sr=None)
    # Compute short-term energy
    frame_length = 2048
    hop_length = 512
    energy = np.array([
        sum(abs(y[i:i+frame_length]**2))
        for i in range(0, len(y), hop_length)
    ])
    # Find peaks in energy
    energy_peaks = energy.argsort()[-top_n:][::-1]
    times = librosa.frames_to_time(energy_peaks, sr=sr, hop_length=hop_length)
    return sorted(times)

def detect_scenes(video_path, threshold=30.0):
    """
    Detects scene changes in the video.
    Returns a list of scene start times in seconds.
    """
    video_manager = VideoManager([video_path])
    scene_manager = SceneManager()
    scene_manager.add_detector(ContentDetector(threshold=threshold))
    
    video_manager.start()
    scene_manager.detect_scenes(frame_source=video_manager)
    scene_list = scene_manager.get_scene_list()
    scene_times = [scene[0].get_seconds() for scene in scene_list]
    video_manager.release()
    return scene_times

def score_moments(audio_peaks, scene_times, window=5.0):
    """
    Scores each scene based on proximity to audio peaks.
    Returns a list of scored times.
    """
    scores = {}
    for peak in audio_peaks:
        for scene in scene_times:
            if abs(scene - peak) <= window:
                if scene in scores:
                    scores[scene] += 1
                else:
                    scores[scene] = 1
    # Sort scenes based on score
    sorted_scenes = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    return [scene for scene, score in sorted_scenes]

def select_clips(scored_scenes, video_duration, clip_duration=15, max_total_duration=120):
    """
    Selects clips around the scored scenes.
    Ensures total duration does not exceed max_total_duration (in seconds).
    Returns a list of (start, end) tuples.
    """
    clips = []
    total_duration = 0
    for scene in scored_scenes:
        start = max(scene - clip_duration/2, 0)
        end = min(scene + clip_duration/2, video_duration)
        # Adjust clip to not exceed total duration
        if total_duration + (end - start) > max_total_duration:
            break
        clips.append((start, end))
        total_duration += (end - start)
    return clips

def create_short_video(video_path, output_path, clips):
    """
    Creates a short video by concatenating the selected clips.
    """
    video = VideoFileClip(video_path)
    selected_clips = [video.subclip(start, end) for start, end in clips]
    final_clip = concatenate_videoclips(selected_clips)
    final_clip.write_videofile(output_path, codec="libx264", audio_codec="aac")
    video.close()
    final_clip.close()

def main():
    # Paths
    input_video = "videoplayback.mp4"  # Replace with your input video path
    extracted_audio = "extracted_audio.wav"
    output_video = "youtube_short.mp4"
    
    # Step 1: Extract audio
    print("Extracting audio from video...")
    extract_audio(input_video, extracted_audio)
    
    # Step 2: Analyze audio for energy peaks
    print("Analyzing audio for energy peaks...")
    audio_peaks = analyze_audio(extracted_audio, top_n=20)
    
    # Step 3: Detect scenes
    print("Detecting scenes in video...")
    scene_times = detect_scenes(input_video, threshold=30.0)
    
    # Step 4: Score moments based on audio peaks and scenes
    print("Scoring moments based on audio and scenes...")
    scored_scenes = score_moments(audio_peaks, scene_times, window=5.0)
    
    # Step 5: Select clips
    print("Selecting clips...")
    video = VideoFileClip(input_video)
    video_duration = video.duration
    video.close()
    clips = select_clips(scored_scenes, video_duration, clip_duration=15, max_total_duration=120)
    
    if not clips:
        print("No suitable clips found. Exiting.")
        return
    
    # Step 6: Create short video
    print("Creating short video...")
    create_short_video(input_video, output_video, clips)
    
    # Cleanup
    if os.path.exists(extracted_audio):
        os.remove(extracted_audio)
    
    print(f"Short video created successfully: {output_video}")

if __name__ == "__main__":
    main()

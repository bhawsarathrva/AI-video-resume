import openai
import pyttsx3
import os
from moviepy.editor import VideoFileClip, AudioFileClip

# 1. Extract Key Information from Resume
def extract_resume_text(resume_text):
    openai.api_key = "OPEN_AI_API_KEY"
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "system", "content": f"Summarize this resume: {resume_text}"}]
    )
    return response["choices"][0]["message"]["content"]

# 2. Convert Text to Speech (file in mp3 format)
def text_to_speech(text, output_audio="output file"):
    engine = pyttsx3.init()
    engine.save_to_file(text, output_audio)
    engine.runAndWait()
    return output_audio

# 3. Lip-Sync Avatar with Speech
def lip_sync_video(avatar_video, audio_file, output_video="lip_synced.mp4"):
    os.system(f"python Wav2Lip/inference.py --face {avatar_video} --audio {audio_file} --outfile {output_video}")

# 4. Merge Audio and Video
def add_audio_to_video(video_file, audio_file, output_file="final_resume_video.mp4"):
    video = VideoFileClip(video_file)
    audio = AudioFileClip(audio_file)
    final_video = video.set_audio(audio)
    final_video.write_videofile(output_file, codec="libx264", fps=25)

# Execute Pipeline
resume_text = "Athrva Bhawsar, AI Engineer with NLP and Computer Vision expertise"
avatar_video = "avatar.mp4"
script = extract_resume_text(resume_text)
audio_file = text_to_speech(script)
lip_sync_video(avatar_video, audio_file)
add_audio_to_video("lip_synced.mp4", audio_file)
print("AI Video Resume Generated Successfully!")

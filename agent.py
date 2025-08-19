import os
import time
from mutagen.mp3 import MP3
from transformers import pipeline
from gtts import gTTS

# Step 1: Generate Script from AI
topic = input("Enter a topic (e.g., AI, space, robotics): ")

generator = pipeline("text-generation", model="gpt2")
script = generator(
    f"Explain {topic} in simple words.",
    max_length=200, num_return_sequences=1, truncation=True
)[0]['generated_text']

print("\nGenerated Script:\n", script)

# Save script to file
with open("script.txt", "w") as f:
    f.write(script)

# Step 2: Convert Script to Speech using gTTS
print("\n🎤 Converting script to voiceover...")
tts = gTTS(text=script, lang='en')
tts.save("voiceover.mp3")

# Get audio duration
audio = MP3("voiceover.mp3")
audio_duration = audio.info.length
print(f"\n📢 Voiceover duration: {audio_duration:.2f} seconds")

# Step 3: Create Manim Animation
print("\n🎬 Creating animated video with Manim...")
animation_script = f"""
from manim import *

class TopicAnimation(Scene):
    def construct(self):
        self.camera.background_color = BLACK

        title = Text("{topic.capitalize()}", color=BLUE).scale(1.5)
        self.play(Write(title))
        self.wait(2)
        self.play(FadeOut(title))

        script_text = \"\"\"{script}\"\"\"
        lines = script_text.split(". ")
        duration_per_line = {audio_duration} / max(len(lines), 1)

        for line in lines:
            if line.strip():
                text = Text(line, font_size=30).scale(0.8)
                self.play(Write(text))
                self.wait(duration_per_line)
                self.play(FadeOut(text))

        outro = Text("Thanks for Watching!", color=YELLOW).scale(1.2)
        self.play(Write(outro))
        self.wait(2)
        self.play(FadeOut(outro))
"""

with open("animation.py", "w") as f:
    f.write(animation_script)

# Generate Video using Manim
os.system("python -m manim -pql animation.py TopicAnimation")

# Step 4: Merge Video and Voiceover
print("\n🎥 Merging video with voiceover...")
video_path = "media/videos/animation/480p15/TopicAnimation.mp4"
final_output = "final_video.mp4"

# Convert MP3 to WAV (Manim prefers WAV format)
os.system("ffmpeg -y -i voiceover.mp3 voiceover.wav")

# Ensure Manim finishes before merging
time.sleep(5)

os.system(f"ffmpeg -y -i {video_path} -i voiceover.wav -c:v copy -c:a aac -shortest {final_output}")

print("\n🎬 Video successfully created: 'final_video.mp4'")
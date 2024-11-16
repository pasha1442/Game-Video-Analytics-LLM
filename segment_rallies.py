from moviepy.editor import VideoFileClip
import os
import json

def split_video(video_path, timestamps, output_folder="video_segments"):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    video = VideoFileClip(video_path)
    
    for i, rally in enumerate(timestamps["rallies"], 1):
        start_time = rally["start"]
        end_time = rally["end"]
        
        segment = video.subclip(start_time, end_time)
        
        output_path = os.path.join(output_folder, f"segment_{i:03d}.mp4")
        
        segment.write_videofile(
            output_path,
            codec='libx264',
            audio_codec='aac',
            temp_audiofile='temp-audio.m4a',
            remove_temp=True
        )
        
        print(f"Saved segment {i}: {start_time:.2f}s to {end_time:.2f}s")
    
    video.close()

if __name__ == "__main__":
    timestamps = {
  "rallies": [
    { "start": 0.05, "end": 0.2 },
    { "start": 0.24, "end": 0.39 },
    { "start": 0.41, "end": 0.47 },
    { "start": 0.49, "end": 0.77 },
    { "start": 0.79, "end": 1.13 },
    { "start": 1.17, "end": 1.21 },
    { "start": 1.24, "end": 1.3 },
    { "start": 1.32, "end": 1.43 },
    { "start": 1.45, "end": 2.01 },
    { "start": 2.03, "end": 2.18 },
    { "start": 2.19, "end": 2.23 },
    { "start": 2.26, "end": 2.31 },
    { "start": 2.33, "end": 2.37 },
    { "start": 2.38, "end": 2.51 }
  ]
}
    
    video_path = "/home/auriga/Downloads/videoplayback.mp4"
    
    split_video(video_path, timestamps)
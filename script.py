import subprocess
import os
import json

# 6 gambar lo, format webp, nama udah sesuai
scenes = [
    "assets/scene1.webp",
    "assets/scene2.webp",
    "assets/scene3.webp",
    "assets/scene4.webp",
    "assets/scene5.webp",
    "assets/scene6.webp",
]
audio = "assets/narasi.mp3"
output = "hasil-video.mp4"

# Cek file ada semua apa nggak
for f in scenes + [audio]:
    if not os.path.exists(f):
        print(f"FILE HILANG: {f}")
        raise SystemExit(1)
    print(f"OK ada: {f}")

# Cek durasi audio
probe = subprocess.run(
    ["ffprobe", "-v", "error", "-show_entries", "format=duration",
     "-of", "default=noprint_wrappers=1:nokey=1", audio],
    capture_output=True, text=True
)
try:
    audio_dur = float(probe.stdout.strip())
except:
    audio_dur = 60.0
print(f"Durasi audio: {audio_dur} detik")

# Durasi tiap gambar = durasi audio / 6
per_image = audio_dur / len(scenes)
print(f"Tiap gambar: {per_image} detik")

# Bikin video per gambar dulu
temp_videos = []
for i, img in enumerate(scenes):
    tmp = f"temp{i}.mp4"
    subprocess.run([
        "ffmpeg", "-y",
        "-loop", "1",
        "-i", img,
        "-vf", "scale=1080:1920:force_original_aspect_ratio=decrease,pad=1080:1920:(ow-iw)/2:(oh-ih)/2,format=yuv420p",
        "-t", str(per_image),
        "-r", "30",
        tmp
    ], check=True)
    temp_videos.append(tmp)

# Gabungin 6 video jadi 1
with open("list.txt", "w") as f:
    for v in temp_videos:
        f.write(f"file '{v}'\n")

subprocess.run([
    "ffmpeg", "-y",
    "-f", "concat", "-safe", "0",
    "-i", "list.txt",
    "-i", audio,
    "-c:v", "libx264",
    "-c:a", "aac",
    "-shortest",
    output
], check=True)

print(f"SELESAI! Video jadi: {output}")

import subprocess
import os

# Nama file SESUAI upload lo yang sekarang - jangan diubah lagi
scenes = [
    "assets/Scene 01.webp",
    "assets/Scene 02.webp",
    "assets/Scene 03.webp",
    "assets/Scene 04.webp",
    "assets/Scene 05.webp",
    "assets/Scene 06.webp",
]
audio = "assets/Narasi.mp3"
output = "hasil-video.mp4"

for f in scenes + [audio]:
    if not os.path.exists(f):
        print(f"FILE HILANG: {f}")
        raise SystemExit(1)
    print(f"OK ada: {f}")

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

per_image = audio_dur / len(scenes)
print(f"Tiap gambar: {per_image} detik")

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

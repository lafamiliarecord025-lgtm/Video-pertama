import os
import subprocess
import glob

ASSETS = "assets"
OUTPUT = "hasil-video.mp4"

def run(cmd):
    print("JALAN:", " ".join(cmd))
    subprocess.run(cmd, check=True)

os.makedirs(ASSETS, exist_ok=True)
images = sorted(glob.glob(f"{ASSETS}/*.jpg") + glob.glob(f"{ASSETS}/*.png"))

if not images:
    print("Belum ada gambar, bikin 6 gambar dummy buat tes...")
    colors = ["0x1e3a8a", "0x065f46", "0x7c2d12", "0x581c87", "0x831843", "0x111827"]
    images = []
    for i, color in enumerate(colors, start=1):
        path = f"{ASSETS}/scene{i}.jpg"
        run(["ffmpeg", "-y", "-f", "lavfi", "-i", f"color=c={color}:s=1080x1920:d=1", "-frames:v", "1", path])
        images.append(path)
    images = sorted(images)

segments = []
for i, img in enumerate(images):
    seg = f"seg_{i}.mp4"
    run([
        "ffmpeg", "-y", "-loop", "1", "-i", img,
        "-vf", "scale=1080:1920:force_original_aspect_ratio=decrease,pad=1080:1920:(ow-iw)/2:(oh-ih)/2,zoompan=z='min(zoom+0.0015,1.15)':d=300:s=1080x1920:fps=30",
        "-t", "10", "-c:v", "libx264", "-pix_fmt", "yuv420p", seg
    ])
    segments.append(seg)

with open("list.txt", "w") as f:
    for s in segments:
        f.write(f"file '{s}'\n")

run(["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", "list.txt", "-c", "copy", "gabung.mp4"])

audio = f"{ASSETS}/narasi.mp3"
if os.path.exists(audio):
    run(["ffmpeg", "-y", "-i", "gabung.mp4", "-i", audio, "-c:v", "copy", "-c:a", "aac", "-shortest", OUTPUT])
else:
    print("Nggak ada narasi.mp3, render tanpa audio dulu")
    run(["ffmpeg", "-y", "-i", "gabung.mp4", "-c", "copy", OUTPUT])

print(f"SELESAI! File jadi: {OUTPUT}")

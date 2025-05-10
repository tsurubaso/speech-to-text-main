from pydub import AudioSegment
import os

file_path = input("📂 Give us the path of your audio file: ").strip()

if not os.path.isfile(file_path):
    print("❌ File not found.")
    exit(1)

audio = AudioSegment.from_file(file_path)
start_ms = 60 * 1000       # 1 minute
end_ms = (60 + 10) * 1000  # 1 minute 10 seconds

segment = audio[start_ms:end_ms]
output_path = os.path.splitext(file_path)[0] + "_segment.wav"
segment.export(output_path, format="wav")

print(f"✅ Segment saved to {output_path}")
os.startfile(output_path)  # Open with default app (Audacity if associated)

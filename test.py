from pydub import AudioSegment

audio = AudioSegment.from_file("C:/Users/space/OneDrive/Desktop/Zara/en29bcVrai16HZ.wav")
audio.export("C:/Users/space/OneDrive/Desktop/Zara/converted.wav", format="wav")  # Convert to WAV format
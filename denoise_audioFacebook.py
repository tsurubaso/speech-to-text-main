import torch
from denoiser.demucs import Demucs
import os
from pydub import AudioSegment
import numpy as np

def load_model(model_path, device='cpu'):
    model = Demucs()
    state = torch.load(model_path, map_location=device)
    model.load_state_dict(state)
    model.eval()
    return model.to(device)

def load_audio_pydub(input_path):
    audio = AudioSegment.from_file(input_path)
    audio = audio.set_channels(1)  # Assurer un canal unique
    samples = np.array(audio.get_array_of_samples(), dtype=np.float32)
    sample_rate = audio.frame_rate
    samples /= np.max(np.abs(samples))  # Normalisation
    return torch.tensor(samples).unsqueeze(0), sample_rate

def denoise_audio(model, input_path, output_path, chunk_duration=180):
    waveform, sample_rate = load_audio_pydub(input_path)
    num_samples = waveform.size(1)
    chunk_size = chunk_duration * sample_rate
    num_chunks = (num_samples + chunk_size - 1) // chunk_size

    all_chunks = []
    for i in range(num_chunks):
        start = i * chunk_size
        end = min((i + 1) * chunk_size, num_samples)
        chunk_waveform = waveform[:, start:end]
        with torch.no_grad():
            enhanced_chunk = model(chunk_waveform.unsqueeze(0)).squeeze(0)
        all_chunks.append(enhanced_chunk)
        print(f"Processed chunk {i+1}/{num_chunks}")

    enhanced_waveform = torch.cat(all_chunks, dim=1)
    
    # Exporter le fichier en format WAV après traitement
    output_audio = AudioSegment(
        data=enhanced_waveform.numpy().tobytes(),
        frame_rate=sample_rate,
        sample_width=2,  # Ajuste selon les besoins
        channels=1
    )
    output_audio.export(output_path, format="wav")
    print(f"Denoised audio saved as: {output_path}")

# --- CONFIG ---

username = input("Enter your Windows username: ").strip()
hub_dir = f"C:/Users/{username}/.cache/torch/hub"

# Recherche du fichier contenant "dns48" dans le hub directory
model_file = None
if os.path.isdir(hub_dir):
    for file in os.listdir(hub_dir):
        if "dns48" in file and file.endswith(".th"):
            model_file = os.path.join(hub_dir, file)
            break

if not model_file:
    print("No model file containing 'dns48' found in:")
    print(hub_dir)
    print("Please download it from:")
    print("https://dl.fbaipublicfiles.com/denoiser/dns48-11decc9d8e3f0998.th")
    exit()

input_file = input("Enter the path to the noisy audio file: ").strip()
output_file = input("Enter the output path for the cleaned audio file: ").strip()

model = load_model(model_file)
denoise_audio(model, input_file, output_file)

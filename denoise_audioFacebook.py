import torchaudio
import torch
from denoiser.demucs import Demucs
import os

# Charger manuellement le modèle
def load_model(model_path, device='cpu'):
    model = Demucs()
    state = torch.load(model_path, map_location=device)
    model.load_state_dict(state)
    model.eval()
    return model.to(device)

def denoise_audio(model, input_path, output_path, chunk_duration=180):  # Durée de chaque morceau en secondes 300=5 mins
    # Charger l'audio
    waveform, sample_rate = torchaudio.load(input_path)

    # Découper l'audio en morceaux (en secondes)
    num_samples = waveform.size(1)
    chunk_size = chunk_duration * sample_rate  # Convertir durée en nombre de samples
    num_chunks = (num_samples + chunk_size - 1) // chunk_size  # Nombre de morceaux nécessaires

    # Sauvegarder les morceaux traités
    all_chunks = []
    
    for i in range(num_chunks):
        start = i * chunk_size
        end = min((i + 1) * chunk_size, num_samples)
        
        chunk_waveform = waveform[:, start:end]
        
        # Réduction de bruit
        with torch.no_grad():
            enhanced_chunk = model(chunk_waveform.unsqueeze(0)).squeeze(0)
        
        all_chunks.append(enhanced_chunk)
        print(f"Processed chunk {i+1}/{num_chunks}")

    # Fusionner les morceaux traités
    enhanced_waveform = torch.cat(all_chunks, dim=1)

    # Sauvegarder l'audio nettoyé
    torchaudio.save(output_path, enhanced_waveform, sample_rate)
    print(f"Denoised audio saved as: {output_path}")

# --- CONFIG ---
model_path = input("Enter the path to the model file: ").strip()
input_file = input("Enter the path to the noisy audio file: ").strip()
output_file = input("Enter the output path for the cleaned audio file: ").strip()

# Vérifier si le modèle existe
if not os.path.exists(model_path):
    print("Model file not found. Exiting...")
    exit()

# Charger et appliquer le modèle
model = load_model(model_path)
denoise_audio(model, input_file, output_file)

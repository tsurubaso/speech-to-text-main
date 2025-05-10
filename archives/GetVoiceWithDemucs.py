

#demucs --two-stems vocals -o demucs_output your_audio_file_stereo.wav
import torch
from demucs.pretrained import get_model
from demucs.apply import apply_model
import torchaudio
import os

def separate_vocals(input_path, output_dir="demucs_output", model_name="htdemucs"):
    # Charger le modèle
    model = get_model(model_name).cpu()
    model.eval()

    # Charger l'audio
    wav, sr = torchaudio.load(input_path)
    wav = wav.mean(dim=0, keepdim=True)  # Assure stéréo (même si mono)
    wav = torchaudio.functional.resample(wav, sr, 44100)
    sr = 44100

    # Appliquer le modèle
    with torch.no_grad():
        sources = apply_model(model, wav, split=True, overlap=0.1, progress=True)

    # Sauver les pistes
    os.makedirs(output_dir, exist_ok=True)
    vocals = sources[0][model.sources.index("vocals")].unsqueeze(0)
    torchaudio.save(os.path.join(output_dir, "vocals.wav"), vocals, sr)
    print(f"Vocals saved to: {os.path.join(output_dir, 'vocals.wav')}")

# Utilisation
input_file = input("Path to your audio file: ").strip()
separate_vocals(input_file)

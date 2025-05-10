import os
import time

# Nom des pipes (Windows)
PIPE_TO_AUDACITY = r'//./pipe/ToSrvPipe'
PIPE_FROM_AUDACITY = r'//./pipe/FromSrvPipe'

def send_command(command):
    with open(PIPE_TO_AUDACITY, 'w') as pipe:
        pipe.write(command + '\n')

def get_response():
    with open(PIPE_FROM_AUDACITY, 'r') as pipe:
        result = ''
        while True:
            line = pipe.readline()
            if line.strip() == '<End>':
                break
            result += line
        return result

def wait_for_audacity():
    while not os.path.exists(PIPE_TO_AUDACITY):
        print("Waiting for Audacity mod-script-pipe...")
        time.sleep(1)

def process_audio(file_path):
    wait_for_audacity()

    # Charger le fichier
    send_command(f'Import2: Filename="{file_path}"')
    get_response()

    # Sélectionner 1:00 à 1:10 (en secondes)
    send_command('SelectTime: Start=60 End=70')
    get_response()

    # Appliquer Normalisation
    send_command('Normalize: ApplyGain="1" RemoveDcOffset="1" PeakLevel="-1"')
    get_response()

    # Supprimer les silences
    send_command('TruncateSilence: Threshold="-40" Duration="0.5" Action="0"')  # Action=0 = supprimer
    get_response()

    # Exporter le résultat
    send_command(f'Export2: Filename="{file_path[:-4]}_processed.wav"')
    get_response()

    print("Traitement terminé et exporté.")

if __name__ == '__main__':
    print("Donnez le chemin du fichier audio à traiter (ex: C:\\fichier.wav) :")
    audio_path = input().strip()

    if not os.path.isfile(audio_path):
        print("Erreur : fichier introuvable.")
        exit(1)

    process_audio(audio_path)

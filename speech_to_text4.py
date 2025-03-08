#directly to console, save to file
import os
import speech_recognition as sr
from pydub import AudioSegment

def prepare_voice_file(path: str) -> str:
    if os.path.splitext(path)[1] == '.wav':
        return path
    elif os.path.splitext(path)[1].lower() in ('.MP3', '.m4a', '.ogg', '.flac'):
        audio_file = AudioSegment.from_file(
            path, format=os.path.splitext(path)[1][1:])
        wav_file = os.path.splitext(path)[0] + '.wav'
        audio_file.export(wav_file, format='wav')
        return wav_file
    else:
        raise ValueError(
            f'Unsupported audio format: {format(os.path.splitext(path)[1])}')

def transcribe_audio(audio_data, language) -> str:
    r = sr.Recognizer()
    try:
        text = r.recognize_google(audio_data, language=language)
    except UnicodeEncodeError as e:
        print(f"Encoding error: {e}")
        text = text.encode('utf-8', errors='replace').decode('utf-8')
    return text

def speech_to_text(input_path: str, language: str, output_path: str) -> None:
    wav_file = prepare_voice_file(input_path)
    with sr.AudioFile(wav_file) as source:
        audio_data = sr.Recognizer().record(source)
        text = transcribe_audio(audio_data, language)
        print('Transcription:')
        print(text)

        # Sauvegarder la transcription dans un fichier .txt
        with open(output_path, 'w', encoding='utf-8') as file:
            file.write(text)
        print(f'Transcription saved to {output_path}')

if __name__ == '__main__':
    print('Please enter the path to an audio file (WAV, MP3, M4A, OGG, or FLAC):')
    input_path = input().strip()
    if not os.path.isfile(input_path):
        print('Error: File not found.')
        exit(1)
    else:
        print('Please enter the language code (e.g. en-US):')
        language = input().strip()
        print('Please enter the path to save the transcription (e.g. transcription.txt):')
        output_path = input().strip()
        try:
            speech_to_text(input_path, language, output_path)
        except Exception as e:
            print('Error:', e)
            exit(1)

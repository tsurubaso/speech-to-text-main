#directly to console, save to file by bit of 3 minutes, with ponctuiation replacement without few problems: ?!.
import os
import re
import speech_recognition as sr
from pydub import AudioSegment

def prepare_voice_file(path: str) -> str:
    if os.path.splitext(path)[1].lower() == '.wav':
        return path
    elif os.path.splitext(path)[1].lower() in ('.mp3', '.m4a', '.ogg', '.flac'):
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

def replace_punctuation(text):
    replacements = {
        "point d'interrogation": "?",
        "point d'exclamation": "!",
        "point de suspension": "...",
        "trois petits points": "...",
        "point": ".",
        "virgule": ",",
        "deux-points": ":",
        "point-virgule": ";",
        "tiret": "-",
        "parenthèse gauche": "(",
        "parenthèse droite": ")",
        "guillemets": "\"",
        "apostrophe": "'",
        "crochet gauche": "[",
        "crochet droit": "]",
        "accolade gauche": "{",
        "accolade droite": "}"
    }

    # Trier les remplacements par longueur décroissante
    sorted_replacements = sorted(replacements.items(), key=lambda item: len(item[0]), reverse=True)

    for word, punctuation in sorted_replacements:
        text = re.sub(r'\b{}\b'.format(re.escape(word)), punctuation, text)

    # Remplacer la ponctuation
    text = re.sub(r'\s?(\.|\!|\?|\,|\:|\;)', r'\1 ', text)
    text = re.sub(r'\s+', ' ', text)
    text = re.sub(r'\.(\s*)(\w)', lambda match: '. ' + match.group(2).upper(), text)
    text = re.sub(r'^\s*', '', text)

    return text

def speech_to_text(input_path: str, language: str, output_path: str) -> None:
    wav_file = prepare_voice_file(input_path)
    audio = AudioSegment.from_wav(wav_file)
    segment_length = 3 * 60 * 1000  # 3 minutes in milliseconds
    segments = [audio[i:i + segment_length] for i in range(0, len(audio), segment_length)]

    with open(output_path, 'w', encoding='utf-8') as file:
        for i, segment in enumerate(segments):
            segment.export(f"segment_{i}.wav", format="wav")
            with sr.AudioFile(f"segment_{i}.wav") as source:
                audio_data = sr.Recognizer().record(source)
                text = transcribe_audio(audio_data, language)
                text = replace_punctuation(text)  # Appliquer le remplacement de ponctuation
                print(f'Transcription for segment {i + 1}:')
                print(text)
                file.write(text + "\n")
            os.remove(f"segment_{i}.wav")  # Clean up the segment file

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

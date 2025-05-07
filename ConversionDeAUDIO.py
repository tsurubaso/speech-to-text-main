from pydub import AudioSegment
import os

if __name__ == '__main__':
    print("Please enter the path to a mono WAV file:")
    input_path = input().strip()

    if not os.path.isfile(input_path):
        print("Error: File not found.")
        exit(1)

    try:
        mono = AudioSegment.from_file(input_path, format="wav")
        stereo = AudioSegment.from_mono_audiosegments(mono, mono)

        # Prepare output path
        directory, filename = os.path.split(input_path)
        output_filename = f"Stereo-{filename}"
        output_path = os.path.join(directory, output_filename)

        stereo.export(output_path, format="wav")
        print(f"Stereo file saved to: {output_path}")

    except Exception as e:
        print(f"Error: {e}")
        exit(1)

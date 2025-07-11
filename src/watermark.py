import json
import sys
from pathlib import Path
from pydub import AudioSegment

PATH = "".join(str(Path.home()) + "/.watermark/src/config.json")
CONFIG = Path(PATH)
FORMATS = [".mp3", ".mp4", ".wav", ".aif", ".aiff", ".flac"]

def save_config():
    watermark_path = input("Drag and drop your watermark file of your choice: ")
    with open(CONFIG, 'w', encoding='utf-8') as f:
        json.dump({"watermark_path": watermark_path}, f, indent=2)
    print(f"Updated watermark path: \x1b[1m{watermark_path}\x1b[22m")
    sys.exit()

def load_config():
    try:
        with open(CONFIG, 'r', encoding='utf-8') as f:
            file = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return save_config()
    if "/path/to/file.wav" in file["watermark_path"]:
        return save_config()
    
    return file
    
def filehandling():
    if len(sys.argv) == 2 and sys.argv[1] == "*":
        files = Path().glob("*")
    else:
        files = [Path(file) for file in sys.argv[1:]]
    
    return [
        (AudioSegment.from_file(file), file.with_name(f"{file.stem}_watermark"), str(Path(file)))
        for file in files
        if file.suffix.lower() in FORMATS
    ]

config = load_config()
path = config["watermark_path"]
WATERMARK = AudioSegment.from_file(path)

def watermarking():
    data = filehandling()
    files = []
    for audio, output_file, file in data:
        watermarked = audio[:]
        duration = len(audio)
        if len(audio) <= 5000:
            mid = duration / 2
            fadein = audio.fade(to_gain=-12, start=int(mid - 400), end=int(mid - 100))
            fadeout = fadein.fade(to_gain=+12, start=int(mid + 200), end=int(mid + 500))
            watermarked = fadeout.overlay(WATERMARK, position=mid)
        else:
            interval = 6000
            position = interval
            while position <= duration:
                start = int(max(position - 400, 0))
                end = int(min(position + 500, duration))
                segment = watermarked[start:end]
                fadein = segment.fade(to_gain=-12, start=0, end=min(300, len(segment) // 2))
                fadeout = fadein.fade(to_gain=+12, start=max(0, len(segment) - 300), end=len(segment))
                modified_segment = fadeout.overlay(WATERMARK, position=(position - start))
                watermarked = watermarked[:start] + modified_segment + watermarked[end:]
                position += interval
        watermarked.export(f"{output_file}.mp3", format="mp3", bitrate="128k")
        files.append(file)
    print(f"\n\x1b[1m{len(files)} FILE(S) PROCESSED SUCCESFULLY:\x1b[22m\n" + "\n".join(files)+ "\n")

def main():
    if len(sys.argv) == 1:
        raise Exception("No audio files!")
    elif len(sys.argv) >= 2 and (sys.arvg[i] not in "reset" for i in sys.argv[1:]):
        raise Exception("Invalid input!")
    elif len(sys.argv) == 2 and sys.argv[1] in "reset":
        save_config()
    else:
        watermarking()

if __name__ == "__main__":
    main()


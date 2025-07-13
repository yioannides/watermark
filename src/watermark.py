import argparse
import json
import sys
from pathlib import Path
from pydub import AudioSegment

CONFIG_PATH = "".join(str(Path.home()) + "/.watermark/src/config.json")
CONFIG = Path(CONFIG_PATH)
FORMATS = [".mp3", ".mp4", ".wav", ".aif", ".aiff", ".flac"]

def help():
    """provides a help page for the user"""
    parser = argparse.ArgumentParser(description="Add audio watermarks onto your audio files")
    parser.add_argument("*", help="Modifies every valid audio file in the present working directory")
    parser.add_argument("-r, --reset", metavar="\b", help="Reset/replace the current watermark file")
    parser.add_argument("-i, --interval", metavar="\b", type=int, help="Change the number of seconds between watermaks (min: 5)")
    args = parser.parse_args()

def load_config():
    """loads the user settings from config.json"""
    try:
        with open(CONFIG, 'r', encoding='utf-8') as l:
            file = json.load(l)
    except (FileNotFoundError, json.JSONDecodeError):
        change_watermark()
    return file

def change_watermark():
    """allows the user to change the watermark file"""
    while True:
        watermark_path = input("Add your watermark file: ")
        if Path(watermark_path).exists():
            config["watermark_path"] = watermark_path
            with open(CONFIG, 'w', encoding='utf-8') as w:
                json.dump(config, w, indent=4)
            print(f"Updated watermark path: \x1b[1m{watermark_path}\x1b[22m")
            break
        else:
            print("File does not exist!")
            continue               
    
def change_interval():
    """allows the user to change the number of seconds between watermarks"""
    while True:
        try:
            new_interval = int(input("How many seconds between watermarks? (min: 5) "))
            if new_interval >= 5:
                config["interval_long"] = new_interval * 1000
                with open(CONFIG, 'w', encoding='utf-8') as d:
                    json.dump(config, d, indent=4)
                print(f"Watermark interval updated to {new_interval} seconds!")
            else:
                print("Please enter a number above 5")
                continue
        except ValueError:
            print("Not a valid number!")
            continue
        sys.exit()
    
def filehandling():
    """handles the audio files (either files separately or 
    all valid audio files in the present working directory)
    """
    if len(sys.argv) == 2 and sys.argv[1] == "*":
        files = Path().glob("*")
    else:
        files = [Path(file) for file in sys.argv[1:]]
    
    return [
        (AudioSegment.from_file(file), file.with_name(f"{file.stem}_watermark"), str(Path(file)))
        for file in files
        if file.suffix.casefold() in FORMATS
    ]

config = load_config()
interval_long = config["interval_long"]
watermark_path = config["watermark_path"]

def watermarking():
    """provides the watermarking via audio slices"""
    WATERMARK = AudioSegment.from_file(watermark_path)
    data = filehandling()
    files = []
    for audio, output_file, file in data:
        watermarked = audio[:]
        duration = len(audio)
        if len(audio) < 5000:
            mid = duration / 2
            fadein = audio.fade(to_gain=-12, start=int(mid - 400), end=int(mid - 100))
            fadeout = fadein.fade(to_gain=+12, start=int(mid + 200), end=int(mid + 500))
            watermarked = fadeout.overlay(WATERMARK, position=mid)
        else:
            interval = interval_long
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
    """handles user input & the main logic for this program"""
    if len(sys.argv) == 1:
        raise Exception("No audio files!")
    elif len(sys.argv) == 2:
        match sys.argv[1]:
            case "-h" | "--help":
                help()
            case "-r" | "--reset":
                change_watermark()
            case "-i" | "--interval":
                change_interval()
    elif not any(Path(f).suffix.casefold() in FORMATS for f in sys.argv[1:]):
        raise Exception("No valid audio files with supported formats!")
    else:
        watermarking()

if __name__ == "__main__":
    main()

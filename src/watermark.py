import argparse
import json
from pathlib import Path
from pydub import AudioSegment

CONFIG_PATH = Path.home() / ".watermark" / "src" / "config.json"
CONFIG = Path(CONFIG_PATH)
FORMATS = [".mp3", ".mp4", ".wav", ".aif", ".aiff", ".flac"]

def parse_args():
    parser = argparse.ArgumentParser(
        prog="watermark",
        description="add audio watermarks onto your audio files",
        epilog="repo: https://github.com/yioannides/watermark"
    )
    parser.add_argument(
        "files",
        nargs="*",
        help="audio files to watermark / use '*' to process all valid audio files in the current directory"
    )
    parser.add_argument(
        "-r", "--reset",
        metavar="",
        required=False,
        help="replaces the current watermark file"
    )
    parser.add_argument(
        "-i", "--interval",
        type=int,
        metavar="",
        help="sets the number of seconds between watermarks (min: 5)"
    )
    return parser.parse_args()

def load_config():
    """loads the user settings from config.json"""
    try:
        with open(CONFIG, 'r', encoding='utf-8') as init:
            file = json.load(init)
    except (FileNotFoundError, json.JSONDecodeError):
        change_watermark()
    return file

def save_config(config):
    CONFIG.parent.mkdir(parents=True, exist_ok=True)
    with open(CONFIG, 'w', encoding='utf-8') as f:
        json.dump(config, f, indent=4)

def change_watermark(watermark_path):
    """allows the user to change the watermark file"""
    if not Path(watermark_path).exists():
        raise FileNotFoundError("File not found!")
    if not watermark_path:
        raise TypeError("No watermark path provided. Use --reset </path/to/file>")
    config["watermark_path"] = watermark_path
    save_config(config)
    print(f"Updated watermark path: \x1b[1m{watermark_path}\x1b[22m")       
    
def change_interval(new_interval):
    """allows the user to change the number of seconds between watermarks"""
    if new_interval < 5:
        raise ValueError("Interval must be at least 5 seconds")
    config["interval_long"] = new_interval * 1000
    save_config(config)
    print(f"Watermark interval updated to {new_interval} seconds!")
    
def filehandling(files):
    """handles the audio files (either files separately or 
    all valid audio files in the present working directory)
    """
    return [
        (AudioSegment.from_file(file), file.with_name(f"{file.stem}_watermark"), str(Path(file)))
        for file in files
        if file.suffix.casefold() in FORMATS
    ]

def watermarking(files):
    """provides the watermarking via audio slices"""
    WATERMARK = AudioSegment.from_file(config["watermark_path"])
    data = filehandling(files)
    processed_files = []
    for audio, output_file, file in data:
        watermarked = audio[:]
        duration = len(audio)
        if len(audio) < 5000:
            mid = duration / 2
            fadein = audio.fade(to_gain=-12, start=int(mid - 400), end=int(mid - 100))
            fadeout = fadein.fade(to_gain=+12, start=int(mid + 200), end=int(mid + 500))
            watermarked = fadeout.overlay(WATERMARK, position=mid)
        else:
            interval = config["interval_long"]
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
        processed_files.append(file)
    print(f"\n\x1b[1m{len(processed_files)} FILE(S) PROCESSED SUCCESFULLY:\x1b[22m\n" + "\n".join(processed_files)+ "\n")

def main():
    """handles user input & the main logic for this program"""
    global config
    args = parse_args()
    config = load_config()
    if args.reset:
        try:
            change_watermark(args.reset)
        except (FileNotFoundError, TypeError) as e:
            print(f"Error: {e}")
        return
    if args.interval:
        try:
            change_interval(args.interval)
        except ValueError as e:
            print(f"Error: {e}")
        return
    if args.files == ["*"]:
        file_list = [f for f in Path().glob("*") if f.suffix.casefold() in FORMATS]
    else:
        file_list = [Path(f) for f in args.files if Path(f).suffix.casefold() in FORMATS]
    if not args.files:
        raise Exception("No audio files!")
    if not file_list:
        raise Exception("No valid audio files with supported formats!")
        
    watermarking(file_list)

if __name__ == "__main__":
    main()

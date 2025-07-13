![showcase](https://github.com/user-attachments/assets/63dbd3d9-218b-40b1-b5a0-1f86a33714f4)

## Introduction

<b>watermark</b> is a simple (offline & non-AI) audio watermarking tool made in Python.

I initially created this script as a personal project, for generating watermarked audio clips of my music work to share with clients during the production stage of a commission project.
Over time, it became an entity of its own, so even though I'm not a programmer by any means, I figured I might as well release it and hopefully it will help you in your work as well!

## Installation

Simply copy-paste the following command in Terminal:
```sh
curl -s https://raw.githubusercontent.com/yioannides/watermark/main/install.sh | bash
```
## Usage

### Initial launch

You will first need to initialize the watermark script by typing `watermark -r` / `--reset` and adding the watermark file you'll be using, like so:

```sh
user@desktop:~$ watermark -r
Add your watermark file: /home/user/Music/clips/watermark1.wav
```
> [!TIP]
> You can change your watermark file any time!

### Functions

1. Watermarking audio files from multiple locations:
```sh
user@desktop:~$ watermark '/home/user/Music/songs/save me.wav'
'/home/user/Downloads/untitled-pop1.wav' '/mnt/cloud/archive/charlie-take1-live.mp3'

3 FILE(S) PROCESSED SUCCESFULLY:
save me.wav
untitled-pop1.wav
charlie-take1-live.mp3
```
<sup>* The modified files will be located at the original file's location

2. Watermarking every audio file in the present working directory via `*`:
```sh
user@desktop:/home/Music/songs/$ watermark *

4 FILE(S) PROCESSED SUCCESFULLY:
save me.wav
passing by.mp3
shape of your heart.mp3
kelly clark - going forward.flac
```
3. Change the interval between watermarks:
```sh
user@desktop:~$ watermark -i
How many seconds between intervals? (min: 5) 7
Watermark interval updated to 7 seconds!
```
Any audio files below 5 seconds will have one watermark in the middle.

You can always access the help page via `-h` / `--help`!

## Acknowledgments

<b>Mohammed Agoor</b> for providing the core idea for this script: https://stackoverflow.com/questions/78036523/optimizing-audio-watermarking-function-in-python

![showcase](https://github.com/user-attachments/assets/63dbd3d9-218b-40b1-b5a0-1f86a33714f4)

## Installation

Simply copy-paste the following command in Terminal:
```sh
curl -s -o- https://raw.githubusercontent.com/yioannides/watermark/main/install.sh | bash
```
## Usage

### Initial launch

You will first need to initialize the watermark script by drag and drop the watermark file you'll be using from now on, like so:

```sh
user@linux:~$ watermark reset
Drag and drop your watermark file of your choice: /home/user/Music/clips/watermark1.wav
```
You can always reset your watermark file by typing `watermark reset`!

### Watermarking

1. Watermarking separate audio files:
```sh
user@linux:~$ watermark '/home/user/Music/songs/save me.wav' '/home/user/Downloads/untitled-pop1.wav' '/mnt/cloud/archive/charlie-take1-live.mp3'

3 FILE(S) PROCESSED SUCCESFULLY:
save me.wav
untitled-pop1.wav
charlie-take1-live.mp3
```
2. Watermarking every audio file in the present working directory:
```sh
user@linux:/home/Music/songs/$ watermark *

4 FILE(S) PROCESSED SUCCESFULLY:
save me.wav
passing by.mp3
shape of your heart.mp3
kelly clark - going forward.flac
```

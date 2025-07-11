![showcase](https://github.com/user-attachments/assets/63dbd3d9-218b-40b1-b5a0-1f86a33714f4)

## Introduction

`watermark` is an audio watermarking tool made in Python.

I initially created this script as a personal project, for generating watermarked audio clips of my music work to share with clients during the production stage of a commission project.
Over time, it became an entity of its own, so even though I'm not a programmer by any means, I figured I might as well release it and hopefully it will help you in your work as well!

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
> [!TIP]
> You can always reset your watermark file by typing `watermark reset`!

### Watermarking

1. Watermarking separate audio files:
```sh
user@linux:~$ watermark '/home/user/Music/songs/save me.wav'
'/home/user/Downloads/untitled-pop1.wav' '/mnt/cloud/archive/charlie-take1-live.mp3'

3 FILE(S) PROCESSED SUCCESFULLY:
save me.wav
untitled-pop1.wav
charlie-take1-live.mp3
```
<sup>* The modified files will be located at the original file's location

2. Watermarking every audio file in the present working directory:
```sh
user@linux:/home/Music/songs/$ watermark *

4 FILE(S) PROCESSED SUCCESFULLY:
save me.wav
passing by.mp3
shape of your heart.mp3
kelly clark - going forward.flac
```

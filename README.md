# pytubePP - (Pytube Post Processor)

### A Simple CLI Tool to Download Your Favourite YouTube Videos Effortlessly!

[![status](https://img.shields.io/badge/status-active-brightgreen.svg?style=flat)](https://github.com/neosubhamoy/pytubepp/)
[![verion](https://img.shields.io/badge/version-v1.0.1_stable-yellow.svg?style=flat)](https://github.com/neosubhamoy/pytubepp/)
[![python](https://img.shields.io/badge/python-v3.12.x-blue?logo=python&style=flat)](https://www.python.org/downloads/)
[![builds](https://img.shields.io/badge/builds-passing-brightgreen.svg?style=flat)](https://github.com/neosubhamoy/pytubepp/)
[![PRs](https://img.shields.io/badge/PRs-welcome-blue.svg?style=flat)](https://github.com/neosubhamoy/pytubepp/)


### **🏷️ Features**
* Auto Post-Process & Merge YouTube DASH Streams
* Supports MP3 Download (with Embeded Thumbnail and Tags)
* Smart Stream Selection
* Highly Configurable and Many More 😉

### **🧩 Dependencies**
* [pytube](https://pypi.org/project/pytube/)
* [FFmpeg (Not Pre-Included)](https://ffmpeg.org/)
* [ffmpy](https://pypi.org/project/ffmpy/)
* [mutagen](https://pypi.org/project/mutagen/)
* [tabulate](https://pypi.org/project/tabulate/)
* [tqdm](https://pypi.org/project/tqdm/)
* [appdirs](https://pypi.org/project/appdirs/)
* [requests](https://pypi.org/project/requests/)
* [setuptools](https://pypi.org/project/setuptools/)

### **🛠️ Installation**
You can install pytubePP in your system via PIP by simply running the below command

```terminal
pip install pytubepp
```
**IMPORTANT: Before installing pytubePP make sure FFmpeg is installed in your system and accesable via your cli interface (FFmpeg is Must Required as some of the core features of pytubePP relies on FFmpeg, but due to security reasons we can not ship it with the module)**

**>> Install FFmpeg (If you haven't already!)**

Linux (Ubuntu): `apt install ffmpeg`<br>
Windows (using Chocolatey): `choco install ffmpeg`<br>
MacOS (using Homebrew): `brew install ffmpeg`<br>
Android (using Termux): `pkg install ffmpeg`

### **📌 Commands and Flags**
Using pytubePP is as simple as just supplying it only the YouTube video url as argument!
** Before Starting Please NOTE: pytubePP follows a simple rule - "Use the Default Download Configuration if No Flags are Passed"
* To download a video in maximum available resolution the command will look like:
```terminal
pytubepp "https://youtube.com/watch?v=2lAe1cqCOXo"
```
* To download the video in a specific resolution (suppose 480p) the command will be:
```terminal
pytubepp "https://youtube.com/watch?v=2lAe1cqCOXo" -s 480p
```
* To download the video in audio-only MP3 format the command will be:
```terminal
pytubepp "https://youtube.com/watch?v=2lAe1cqCOXo" -s mp3
```
* List of all available flags are given below:

| Flag | Usage | Requires Parameter | Requires URL | Parameters | Default |
| :--- | :---  | :---               | :---         | :---       | :---    |
| -s | Choose preferred download stream | YES | YES | `144` `144p` `240` `240p` `360` `360p` `480` `480p` `720` `720p` `hd` `1080` `1080p` `fhd` `1440` `1440p` `2k` `2160` `2160p` `4k` `mp3` (Pass any one of them) | Your chosen Default Stream via `-ds` flag |
| -i | Shows the video information like: Title, Author, Views, Available Download Streams | NO | YES | No parameters | No default |
| -ds | Set default download stream | YES | NO | `144p` `240p` `360p` `480p` `720p` `1080p` `1440p` `2160p` `mp3` `max` (Pass any one of them) | `max` |
| -df | Set custom download folder path | YES | NO | Use the full path excluding the last trailing slash within double quotes eg(in Linux): `"/path/to/folder"` (Make sure the folder path you enterted is already created and accessable) | Within `Pytube Downloads` folder in your System's `Downloads` folder |
| -r | Reset to default configuration (Download Folder, Default Stream) | NO | NO | No parameters | No default |
| -sc | Show all current user configurations | NO | NO | No parameters | No default |
| -ct | Clear temporary files (audio, video, thumbnail) of the failed, incomplete downloads | NO | NO | No parameters | No default |


⭕ Noticed any Bugs? or Want to give me some suggetions? always feel free to open an issue...!!

### 📝 License & Usage

pytubePP - (Pytube Post Processor) is a Fully Open Sourced Project licensed under MIT License. Anyone can view, modify, use (personal and commercial) or distribute it's sources without any attribution and extra permissions.

**🌟 Liked this project? Please consider giving it a star to show me your appreciation**
<br></br>

****

An Open Sourced Project - Developed with ❤️ by **Subhamoy**
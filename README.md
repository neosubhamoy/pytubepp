# PytubePP - (Pytube Post Processor)

### A Simple CLI Tool to Download Your Favourite YouTube Videos Effortlessly!

[![status](https://img.shields.io/badge/status-active-brightgreen.svg?style=flat)](https://github.com/neosubhamoy/pytubepp/)
[![PypiDownloads](https://img.shields.io/pypi/dm/pytubepp?color=brightgreen)](https://pypi.org/project/pytubepp/)
[![PypiVersion](https://img.shields.io/pypi/v/pytubepp?color=yellow)](https://pypi.org/project/pytubepp/)
[![python](https://img.shields.io/badge/python-v3.12-blue?logo=python&style=flat)](https://www.python.org/downloads/)
[![builds](https://img.shields.io/badge/builds-passing-brightgreen.svg?style=flat)](https://github.com/neosubhamoy/pytubepp/)
[![PRs](https://img.shields.io/badge/PRs-welcome-blue.svg?style=flat)](https://github.com/neosubhamoy/pytubepp/)

😀 GOOD NEWS: If you are Windows(10/11) user and don't want to bother remembering PytubePP Commands! (You are not familier with Command Line Tools). We recently released a Browser Extension that can auto detect YouTube Videos and You can download the Video in one click directly from the browser using PytubePP CLI. Install [PytubePP Helper](https://github.com/neosubhamoy/pytubepp-helper) app in your System and add [PytubePP Extension](https://github.com/neosubhamoy/pytubepp-extension) in your Browser to get started.

### **🏷️ Features**
* Auto Post-Process & Merge YouTube DASH Streams
* Supports upto 8K 60fps HDR Stream Download
* Supports MP3 Download (with Embeded Thumbnail and Tags)
* Smart Stream Selection
* Highly Configurable and Many More 😉

### **🧩 Dependencies**
* [pytubefix](https://pypi.org/project/pytubefix/)
* [FFmpeg (Not Pre-Included)](https://ffmpeg.org/)
* [ffmpy](https://pypi.org/project/ffmpy/)
* [mutagen](https://pypi.org/project/mutagen/)
* [tabulate](https://pypi.org/project/tabulate/)
* [tqdm](https://pypi.org/project/tqdm/)
* [appdirs](https://pypi.org/project/appdirs/)
* [requests](https://pypi.org/project/requests/)
* [setuptools](https://pypi.org/project/setuptools/)

### **🛠️ Installation**
You can install PytubePP in your system via PIP by simply running the below command

```terminal
pip install pytubepp
```
**IMPORTANT: Before installing PytubePP make sure FFmpeg is installed in your system and accesable via your cli interface (FFmpeg is Must Required as some of the core features of pytubePP relies on FFmpeg, but due to security reasons we can not ship it with the module)**

**>> Install FFmpeg (If you haven't already!)**

Linux (Ubuntu): `sudo apt install ffmpeg`<br>
Linux (Fedora): `sudo dnf install ffmpeg-free`<br>
Windows (10/11): `winget install ffmpeg`<br>
MacOS (using Homebrew): `brew install ffmpeg`<br>
Android (using Termux): `pkg install ffmpeg`

**NOTE: Always make sure 'PytubePP' and 'Pytubefix' is on the latest version to avoid issues (update them at least once a week) (Use the command below to update)**
```
pip install pytubefix pytubepp --upgrade
```

### **📌 Commands and Flags**
Using PytubePP is as simple as just supplying it only the YouTube video url as argument!
** Before Starting Please NOTE: PytubePP follows a simple rule - "Use the Default Download Configuration if No Flags are Passed"
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
* To fetch the video information the command will be:
```terminal
pytubepp "https://youtube.com/watch?v=2lAe1cqCOXo" -i
```
* To cancel/stop an ongoing download press `CTRL` + `C` on keyboard (it is recommended to run the `-ct` flag once after canceling an ongoing download).
* List of all available flags are given below:

| Flag | Usage | Requires Parameter | Requires URL | Parameters | Default |
| :--- | :---  | :---               | :---         | :---       | :---    |
| -s | Choose preferred download stream | YES | YES | `144` `144p` `240` `240p` `360` `360p` `480` `480p` `720` `720p` `hd` `1080` `1080p` `fhd` `1440` `1440p` `2k` `2160` `2160p` `4k` `4320` `4320p` `8k` `mp3` (Pass any one of them) | Your chosen Default Stream via `-ds` flag |
| -i | Shows the video information like: Title, Author, Views, Publication Date, Duration, Available Download Streams | NO | YES | No parameters | No default |
| -ri | Shows the video information in raw json format | NO | YES | No parameters | No default |
| -jp | Shows raw json output in prettified view (with indentation: 4) (primarily used with -ri flag)| NO | YES | No parameters | No default |
| -ds | Set default download stream | YES | NO | `144p` `240p` `360p` `480p` `720p` `1080p` `1440p` `2160p` `4320p` `mp3` `max` (Pass any one of them) | `max` |
| -df | Set custom download folder path | YES | NO | Use the full path excluding the last trailing slash within double quotes eg(in Linux): `"/path/to/folder"` (Make sure the folder path you enterted is already created and accessable) | Within `PytubePP Downloads` folder in your System's `Downloads` folder |
| -r | Reset to default configuration (Download Folder, Default Stream) | NO | NO | No parameters | No default |
| -sc | Show all current user configurations | NO | NO | No parameters | No default |
| -ct | Clear temporary files (audio, video, thumbnail) of the failed, incomplete downloads | NO | NO | No parameters | No default |


⭕ Noticed any Bugs? or Want to give me some suggetions? always feel free to open an issue...!!

### 📝 License & Usage

PytubePP - (Pytube Post Processor) is a Fully Open Sourced Project licensed under MIT License. Anyone can view, modify, use (personal and commercial) or distribute it's sources without any attribution and extra permissions.

**🌟 Liked this project? Please consider giving it a star to show me your appreciation**
<br></br>

****

An Open Sourced Project - Developed with ❤️ by **Subhamoy**
# PytubePP - (Pytube Post Processor)

### A Simple CLI Tool to Download Your Favourite YouTube Videos Effortlessly!

[![status](https://img.shields.io/badge/status-active-brightgreen.svg?style=flat)](https://github.com/neosubhamoy/pytubepp/)
[![PypiDownloads](https://img.shields.io/pypi/dm/pytubepp?color=brightgreen)](https://pypi.org/project/pytubepp/)
[![PypiVersion](https://img.shields.io/pypi/v/pytubepp?color=yellow)](https://pypi.org/project/pytubepp/)
[![python](https://img.shields.io/badge/python-v3.13-blue?logo=python&style=flat)](https://www.python.org/downloads/)
[![builds](https://img.shields.io/badge/builds-passing-brightgreen.svg?style=flat)](https://github.com/neosubhamoy/pytubepp/)
[![PRs](https://img.shields.io/badge/PRs-welcome-blue.svg?style=flat)](https://github.com/neosubhamoy/pytubepp/)

😀 GOOD NEWS: If you are not a power user and don't want to bother remembering PytubePP Commands! (You are not familier with Command Line Tools). We recently released a Browser Extension that can auto detect YouTube Videos and You can download the Video in one click directly from the browser using PytubePP CLI. Install [PytubePP Helper](https://github.com/neosubhamoy/pytubepp-helper) app in your System and add [PytubePP Extension](https://github.com/neosubhamoy/pytubepp-extension) in your Browser to get started.

> **🥰 Liked this project? Please consider giving it a Star (🌟) on github to show us your appreciation and help the algorythm recommend this project to even more awesome people like you!**

### **🏷️ Features**
* Auto Post-Process & Merge YouTube DASH Streams
* Supports upto 8K 60fps HDR Stream Download
* Supports MP3 Download (with Embeded Thumbnail and Tags)
* Supports Embeded Captions
* Smart Stream Selection
* Highly Configurable and Many More 😉

### **📎 Pre-Requirements**
* [Python](https://www.python.org/downloads/) (>=3.8)
* [FFmpeg](https://ffmpeg.org/)
* [Node.js](https://nodejs.org/en/download/) (required for auto YT poToken genration which is currently not possible in Python environment)

### **🧩 Python Dependencies**
* [pytubefix](https://pypi.org/project/pytubefix/)
* [ffmpy](https://pypi.org/project/ffmpy/)
* [mutagen](https://pypi.org/project/mutagen/)
* [tabulate](https://pypi.org/project/tabulate/)
* [tqdm](https://pypi.org/project/tqdm/)
* [appdirs](https://pypi.org/project/appdirs/)
* [requests](https://pypi.org/project/requests/)
* [setuptools](https://pypi.org/project/setuptools/)

### **🛠️ Installation**
1. Install Python and PIP
    - Linux (Debian): Python is pre-installed install PIP using `sudo apt install python3-pip`<br>
    - Linux (Fedora): Python is pre-installed install PIP using `sudo dnf install python3-pip`<br>
    - Linux (Arch): Python is pre-installed install PIP using `sudo pacman -S python-pip`<br>
    - Windows (10/11): `winget install Python.Python.3.13`<br>
    - MacOS (using Homebrew): `brew install python`<br>
    - Android (using Termux): `pkg install python`
2. Install FFmpeg 
    - Linux (Debian): `sudo apt install ffmpeg`<br>
    - Linux (Fedora): `sudo dnf install ffmpeg-free`<br>
    - Linux (Arch): `sudo pacman -S ffmpeg`<br>
    - Windows (10/11): `winget install ffmpeg`<br>
    - MacOS (using Homebrew): `brew install ffmpeg`<br>
    - Android (using Termux): `pkg install ffmpeg`
3. Install Node.js
    - Linux (Debian): `curl -o- https://fnm.vercel.app/install | bash && fnm install --lts && fnm use lts`<br>
    - Linux (Fedora): `curl -o- https://fnm.vercel.app/install | bash && fnm install --lts && fnm use lts`<br>
    - Linux (Arch): `curl -o- https://fnm.vercel.app/install | bash && fnm install --lts && fnm use lts`<br>
    - Windows (10/11): `winget install Schniz.fnm;fnm install --lts;fnm use lts`<br>
    - MacOS (using Homebrew): `brew install node`<br>
    - Android (using Termux): `pkg install nodejs`
4. Install PytubePP (using PIP)

> Use `pip3` command instead of `pip` if you are on Linux or MacOS.

```terminal
pip install pytubepp
```

**NOTE: Always make sure 'PytubePP' and 'Pytubefix' is on the latest version to avoid issues (update them at least once a week) (Use the command below to update)**

```
pip install pytubefix pytubepp --upgrade
```

### **📌 Commands and Flags**
Using PytubePP is as simple as just supplying it only the YouTube video url as argument!
** Before Starting Please NOTE: PytubePP follows a simple rule - "Use the Default Download Configuration if No Flags are Passed"
* To download a video in default configuration (maximum resolution and without any caption by default) the command will look like:
```terminal
pytubepp "https://youtube.com/watch?v=2lAe1cqCOXo"
```
* To download the video in a specific resolution (suppose 480p) the command will be:
```terminal
pytubepp "https://youtube.com/watch?v=2lAe1cqCOXo" -s 480p
```
* To download the video with embeded caption (suppose en - English) the command will be:
```terminal
pytubepp "https://youtube.com/watch?v=2lAe1cqCOXo" -c en
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
| -c | Choose preferred caption | YES | YES | All [ISO 639-1 Language Codes](https://www.w3schools.com/tags/ref_language_codes.asp) + some others (Pass any one of them) eg: `en` for English | Your chosen Default Caption via `-dc` flag |
| -i | Shows the video information like: Title, Author, Views, Publication Date, Duration, Available Download Streams | NO | YES | No parameters | No default |
| -ri | Shows the video information in raw json format | NO | YES | No parameters | No default |
| -jp | Shows raw json output in prettified view (with indentation: 4) (primarily used with -ri flag)| NO | YES | No parameters | No default |
| -ds | Set default download stream | YES | NO | `144p` `240p` `360p` `480p` `720p` `1080p` `1440p` `2160p` `4320p` `mp3` `max` (Pass any one of them) | `max` |
| -dc | Set default caption | YES | NO | All [ISO 639-1 Language Codes](https://www.w3schools.com/tags/ref_language_codes.asp) + some others + `none` for No Caption (Pass any one of them) eg: `en` for English | `none` |
| -df | Set custom download folder path | YES | NO | Use the full path excluding the last trailing slash within double quotes eg(in Linux): `"/path/to/folder"` (Make sure the folder path you enterted is already created and accessable) | Within `PytubePP Downloads` folder in your System's `Downloads` folder |
| -r | Reset to default configuration (Download Folder, Default Stream) | NO | NO | No parameters | No default |
| -sc | Show all current user configurations | NO | NO | No parameters | No default |
| -ct | Clear temporary files (audio, video, thumbnail) of the failed, incomplete downloads | NO | NO | No parameters | No default |

### 🛠️ Contributing / Building from Source

Want to be part of this? Feel free to contribute...!! Pull Requests are always welcome...!! (^_^) Follow these simple steps to start building:

* Make sure to install Python, FFmpeg, Node.js and Git before proceeding.

1. Fork this repo in your github account.
2. Git clone the forked repo in your local machine.

> Use `python3` and `pip3` commands instead of `python` and `pip` if you are on Linux or MacOS.

3. Install python dependencies

```terminal
pip install -r requirements.txt
```
4. build, install and test the module

```terminal
python -m build                                        // build the module

pip install .\dist\pytubepp-<version>-py3-none-any.whl   // install the module (give the path to the newly genrated whl file based on your OS path style and don't forget to replace the <version> with the actual version number)
```
5. Do the changes, Send a Pull Request with proper Description (NOTE: Pull Requests Without Proper Description will be Rejected)

⭕ Noticed any Bugs? or Want to give me some suggetions? always feel free to open an issue...!!

### 📝 License & Usage

PytubePP - (Pytube Post Processor) is a Fully Open Sourced Project licensed under MIT License. Anyone can view, modify, use (personal and commercial) or distribute it's sources without any attribution and extra permissions.

⚖️ NOTE: YouTube is a trademark of Google LLC. Use of this trademark is subject to Google Permissions. Downloading and using Copyrighted YouTube Content for Commercial pourposes are not allowed by YouTube Terms without proper Permissions from the Creator. We don't promote this kinds of activity, You should use the downloaded contents wisely and at your own responsibility.

****

An Open Sourced Project - Developed with ❤️ by **Subhamoy**
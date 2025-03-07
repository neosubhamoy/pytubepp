# PytubePP - (Pytube Post Processor)

### A Simple CLI Tool to Download Your Favourite YouTube Videos Effortlessly!

[![status](https://img.shields.io/badge/status-active-brightgreen.svg?style=flat)](https://github.com/neosubhamoy/pytubepp/)
[![PypiDownloads](https://img.shields.io/pypi/dm/pytubepp?color=brightgreen)](https://pypi.org/project/pytubepp/)
[![PypiVersion](https://img.shields.io/pypi/v/pytubepp?color=yellow)](https://pypi.org/project/pytubepp/)
[![python](https://img.shields.io/badge/python-v3.13-blue?logo=python&style=flat)](https://www.python.org/downloads/)
[![builds](https://img.shields.io/badge/builds-passing-brightgreen.svg?style=flat)](https://github.com/neosubhamoy/pytubepp/)
[![PRs](https://img.shields.io/badge/PRs-welcome-blue.svg?style=flat)](https://github.com/neosubhamoy/pytubepp/)

😀 NEWS: If you are not a power user and don't want to bother remembering PytubePP Commands! (You are not familier with Command Line Tools). We recently released a Browser Extension that can auto detect YouTube Videos and You can download the Video in one click directly from the browser using PytubePP CLI. Install [PytubePP Helper](https://github.com/neosubhamoy/pytubepp-helper) app in your System and add [PytubePP Extension](https://github.com/neosubhamoy/pytubepp-extension) in your Browser to get started.

> **🥰 Liked this project? Please consider giving it a Star (🌟) on github to show us your appreciation and help the algorythm recommend this project to even more awesome people like you!**

### **💻 Supported Platforms**
- Windows
- Linux
- MacOS
- Android (Termux)

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
* [Node.js](https://nodejs.org/en/download/)

### **🧩 Python Dependencies**
* [pytubefix](https://pypi.org/project/pytubefix/),
[ffmpy](https://pypi.org/project/ffmpy/),
[mutagen](https://pypi.org/project/mutagen/),
[tabulate](https://pypi.org/project/tabulate/),
[tqdm](https://pypi.org/project/tqdm/),
[appdirs](https://pypi.org/project/appdirs/),
[requests](https://pypi.org/project/requests/),
[rich](https://pypi.org/project/rich/),
[setuptools](https://pypi.org/project/setuptools/)

### **🛠️ Installation**

Open a Terminal/CMD (CLI) window and run the following commands one after one step by step (based on your OS) to install 'PytubePP' in your system!

> If you want to follow along make sure [WinGet](https://learn.microsoft.com/en-us/windows/package-manager/winget/#install-winget) is enabled if you are on Windows (verify using `winget --version`), install [Homebrew](https://brew.sh/) if you are on MacOS and install [Termux](https://termux.dev/) if you are on Android

1. Install Python and PIP
    - Linux (Debian): Python is pre-installed install PIP using `sudo apt install python3-pip`<br>
    - Linux (Fedora): Python is pre-installed install PIP using `sudo dnf install python3-pip`<br>
    - Linux (Arch): Python is pre-installed install PIP using `sudo pacman -S python-pip`<br>
    - Windows (10/11): `winget install Python.Python.3.13`<br>
    - MacOS (using Homebrew): `brew install python`<br>
    - Android (using Termux): `pkg install python`

> You can skip step 2, 3 and auto install them later using the command `pytubepp --postinstall` post installation (works in: Windows, Linux - debian fedora arch, MacOS)

2. Install FFmpeg 
    - Linux (Debian): `sudo apt install ffmpeg`<br>
    - Linux (Fedora) ([enable](https://docs.fedoraproject.org/en-US/quick-docs/rpmfusion-setup/#_enabling_the_rpm_fusion_repositories_using_command_line_utilities) rpmfusion free+nonfree repos before installing): `sudo dnf install ffmpeg`<br>
    - Linux (Arch): `sudo pacman -S ffmpeg`<br>
    - Windows (10/11): `winget install ffmpeg`<br>
    - MacOS (using Homebrew): `brew install ffmpeg`<br>
    - Android (using Termux): `pkg install ffmpeg`
3. Install Node.js
    - Linux (Debian): `sudo apt install nodejs`<br>
    - Linux (Fedora): `sudo dnf install nodejs`<br>
    - Linux (Arch): `sudo pacman -S nodejs-lts-iron npm`<br>
    - Windows (10/11): `winget install OpenJS.NodeJS.LTS`<br>
    - MacOS (using Homebrew): `brew install node`<br>
    - Android (using Termux): `pkg install nodejs`
4. Install PytubePP (using PIP)

> Use `pip3` command instead of `pip` if you are on Linux or MacOS.

> Use `--break-system-packages` flag to install 'PytubePP' in global environment if you get `error: externally-managed-environment` while installing in Linux or MacOS (Don't worry it will not break your system packages, it's just a security mesure)

```terminal
pip install pytubepp
```

**UPDATE: Always make sure 'PytubePP' and 'Pytubefix' is on the latest version to avoid issues (update them at least once a week) (Use the command below to update)**

```terminal
pip install pytubefix pytubepp --upgrade
```

> It is highly recommended to run the post install script once after updating 'PytubePP' using: `pytubepp --postinstall` command

**UNINSTALL: If you want to uninstall PytubePP (Use the command below to uninstall) NOTE: it will only remove the 'PytubePP' python package**
```terminal
pip uninstall pytubepp -y
```

### **📌 Commands and Flags**
Using PytubePP is as simple as just supplying it only the YouTube video url as argument!
> Before starting please NOTE: PytubePP follows a simple principle -> `Use Default Configuration if No Flags are Passed`
* To download a video in default configuration (maximum resolution and without any caption by default) the command will look like:
```terminal
pytubepp "https://youtube.com/watch?v=2lAe1cqCOXo"
```
> NOTE: This command will behave differently if you have changed default configurations
* To download the video in a specific resolution (suppose 480p) the command will be:
```terminal
pytubepp "https://youtube.com/watch?v=2lAe1cqCOXo" -s 480p
```
> NOTE: PytubePP always uses default configuration of flags if they are not passed for example if you only pass `-s` flag then it will use the default caption along with it, if you only pass `-c` then it will use default stream and vice versa
* To download the video with embeded caption (suppose en - English) the command will be:
```terminal
pytubepp "https://youtube.com/watch?v=2lAe1cqCOXo" -c en
```
> NOTE: You can override and disable default caption for the current video if you pass `-c none`
* To download the video in audio-only MP3 format the command will be:
```terminal
pytubepp "https://youtube.com/watch?v=2lAe1cqCOXo" -s mp3
```
* To fetch the video information the command will be:
```terminal
pytubepp "https://youtube.com/watch?v=2lAe1cqCOXo" -i
```
* To cancel/stop an ongoing download press `CTRL` + `C` on keyboard (it is highly recommended to run the `pytubepp -ct` command once after canceling an ongoing download).

* To set default stream (suppose 1080p) use: `pytubepp -ds 1080p` command (This is useful when you always preffer to download this stream even if higher resolution stream is available. If You set default stream then next time when you download, You don't need to pass the `-s 1080p` flag, just pass the video url and it will auto select the `1080p` stream by default).

* To set default caption (suppose en - English) use: `pytubepp -dc en` command (Useful when you always preffer to embed caption in videos and in a specific language, If You set default caption, You don't need to pass `-c en` flag in next downloads just pass the video url).

* You can also view all these current configurations using: `pytubepp -sc` command and reset them using: `pytubepp -r` if needed.

* List of all available flags are given below:

| Short Flag | Flag | Usage | Requires Parameter | Requires URL | Parameters | Default |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| -s | --stream | Choose preferred download stream | YES | YES | `144` `144p` `240` `240p` `360` `360p` `480` `480p` `720` `720p` `hd` `1080` `1080p` `fhd` `1440` `1440p` `2k` `2160` `2160p` `4k` `4320` `4320p` `8k` `mp3` (Pass any one of them) | Your chosen Default Stream via `-ds` flag |
| -c | --caption | Choose preferred caption | YES | YES | All [ISO 639-1 Language Codes](https://www.w3schools.com/tags/ref_language_codes.asp) + auto generated ones + `none` for No Caption (Pass any one of them) eg: `en` for English | Your chosen Default Caption via `-dc` flag |
| -i | --show-info | Shows the video information like: Title, Author, Views, Publication Date, Duration, Available Download Streams and Captions | NO | YES | No parameters | No default |
| -ls | --list-stream | Lists all available streams (video, audio, caption) (only for debuging purposes) | NO | YES | No parameters | No default |
| -ri | --raw-info | Shows the video information in raw json format | NO | YES | No parameters | No default |
| -jp | --json-prettify | Shows raw json output in prettified view (with indentation: 4) (primarily used with -ri flag)| NO | YES | No parameters | No default |
| -ds | --default-stream | Set default download stream | YES | NO | `144p` `240p` `360p` `480p` `720p` `1080p` `1440p` `2160p` `4320p` `mp3` `max` (Pass any one of them) | `max` |
| -dc | --default-caption | Set default caption | YES | NO | All [ISO 639-1 Language Codes](https://www.w3schools.com/tags/ref_language_codes.asp) + auto generated ones + `none` for No Caption (Pass any one of them) eg: `en` for English | `none` |
| -df | --download-folder | Set custom download folder path | YES | NO | Use the full path excluding the last trailing slash within double quotes eg(in Linux): `"/path/to/folder"` (Make sure the folder path you enterted is already created and accessable) | Within `PytubePP Downloads` folder in your System's `Downloads` folder |
| -r | --reset-default | Reset to default configuration (Download Folder, Default Stream, Default Caption) | NO | NO | No parameters | No default |
| -sc | --show-config | Show all current user configurations | NO | NO | No parameters | No default |
| -ct | --clear-temp | Clear temporary files (audio, video, thumbnail, caption) of the failed, incomplete downloads | NO | NO | No parameters | No default |
| -pi | --postinstall | Auto install all external dependencies (FFmpeg, Node.js) (works in Windows, Linux - debian fedora arch, MacOS) | NO | NO | No parameters | No default |

### 🛠️ Contributing / Building from Source

Want to be part of this? Feel free to contribute...!! Pull Requests are always welcome...!! (^_^) Follow these simple steps to start building:

* Make sure to install Python, FFmpeg, Node.js and Git before proceeding.

1. Fork this repo in your github account.
2. Git clone the forked repo in your local machine.

> Use `python3` and `pip3` commands instead of `python` and `pip` if you are on Linux or MacOS.

3. Create a Python virtual environment (venv) and activate it (Optional)
4. Install python dependencies

```terminal
pip install -r requirements.txt
```
5. build, install and test the module

```terminal
python -m build   // build the module

pip install .\dist\pytubepp-<version>-py3-none-any.whl   // install the module (give the path to the newly genrated whl file based on your OS path style and don't forget to replace the <version> with the actual version number)
```
6. Do the changes, Send a Pull Request with proper Description (NOTE: Pull Requests Without Proper Description will be Rejected)

⭕ Noticed any Bugs? or Want to give me some suggetions? always feel free to open an issue...!!

### 📝 License & Usage

PytubePP - (Pytube Post Processor) is a Fully Open Sourced Project licensed under MIT License. Anyone can view, modify, use (personal and commercial) or distribute it's sources without any attribution and extra permissions.

⚖️ NOTE: YouTube is a trademark of Google LLC. Use of this trademark is subject to Google Permissions. Downloading and using Copyrighted YouTube Content for Commercial pourposes are not allowed by YouTube Terms without proper Permissions from the Creator. We don't promote this kinds of activity, You should use the downloaded contents wisely and at your own responsibility.

****

An Open Sourced Project - Developed with ❤️ by **Subhamoy**
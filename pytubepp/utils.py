from importlib.metadata import version
from .config import load_config, get_temporary_directory
import os, re, subprocess, platform

userConfig = load_config()
downloadDIR = userConfig['downloadDIR']
tempDIR = get_temporary_directory()

def network_available():
    try:
        param = '-n' if platform.system().lower() == 'windows' else '-c'
        command = ['ping', param, '1', 'youtube.com']
        subprocess.run(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
        return True
    except subprocess.CalledProcessError:
        return False
    
def nodejs_installed():
    try:
        subprocess.run(['node', '--version'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False
    
def ffmpeg_installed():
    try:
        subprocess.run(['ffmpeg', '-version'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False

def get_version():
    try:
        return version('pytubepp')
    except Exception as e:
        return "Unknown"
    
def is_valid_url(url):
    match = re.search(r"(https?://(?:www\.|music\.)?youtube\.com/(?:watch\?v=[^&]{11}|shorts/[^?&]+)|https?://youtu\.be/[^?&]*(\?si=[^&]*)?)", url)
    return match
    
def get_unique_filename(filename, directory=downloadDIR):
    base_name, extension = os.path.splitext(filename)
    counter = 1
    while os.path.exists(os.path.join(directory, filename)):
        filename = f"{base_name} ({counter}){extension}"
        counter += 1
    return filename

def unpack_caption(caption):
    caption_str = str(caption)
    code_start = caption_str.find('code="') + 6
    code_end = caption_str.find('"', code_start)
    lang_start = caption_str.find('lang="') + 6
    lang_end = caption_str.find('"', lang_start)
    
    code = caption_str[code_start:code_end]
    lang = caption_str[lang_start:lang_end]
    return code, lang

def postprocess_cleanup(dir, files, random_filename):
    for file in files:
        file_path = os.path.join(dir, random_filename + file)
        try:
            if os.path.isfile(file_path):
                os.remove(file_path)
        except Exception as e:
            print(e)

def clear_temp_files():
    if os.listdir(tempDIR) != []:
        for file in os.listdir(tempDIR):
            file_path = os.path.join(tempDIR, file)
            try:
                if os.path.isfile(file_path):
                    os.remove(file_path)
                    print(f'Removed: {file}')
            except Exception as e:
                print(e)
    else:
        print('No temporary files found to clear...!')
from tqdm import tqdm
from .config import get_temporary_directory, load_config
from .utils import get_unique_filename
import os, re, requests, shutil, sys, random

userConfig = load_config()
downloadDIR = userConfig['downloadDIR']
tempDIR = get_temporary_directory()

def download_progressive(stream, itag, title, resolution, file_extention, tempDIR=tempDIR, downloadDIR=downloadDIR):
    global total_filesize, progress_bar
    selected_vdo = stream.get_by_itag(itag)
    total_filesize = selected_vdo.filesize
    progress_bar = tqdm(total=total_filesize, unit='B', unit_scale=True, desc="Downloading Video+Audio")
    random_filename = str(random.randint(1000000000, 9999999999))
    filename = random_filename + '_vdo.' + file_extention
    output_temp_file = os.path.join(tempDIR, filename)
    output_file = os.path.join(downloadDIR, get_unique_filename(title + '_' + resolution + '.' + file_extention))
    selected_vdo.download(output_path=tempDIR, filename=filename)
    print('Processing...')
    shutil.move(output_temp_file, output_file)
    print('Done! 🎉')

def download_nonprogressive(stream, itag_vdo, itag_ado, file_extention, output_path):
    global total_filesize, progress_bar
    selected_vdo = stream.get_by_itag(itag_vdo)
    selected_ado = stream.get_by_itag(itag_ado)
    random_filename = str(random.randint(1000000000, 9999999999))
    total_filesize = selected_vdo.filesize
    progress_bar = tqdm(total=total_filesize, unit='B', unit_scale=True, desc="Downloading Video")
    selected_vdo.download(output_path=output_path, filename=random_filename + '_vdo.' + file_extention)
    total_filesize = selected_ado.filesize
    progress_bar = tqdm(total=total_filesize, unit='B', unit_scale=True, desc="Downloading Audio")
    selected_ado.download(output_path=output_path, filename=random_filename + '_ado.' + file_extention)
    return random_filename

def download_audio(stream, itag, output_path):
    global total_filesize, progress_bar
    selected_ado = stream.get_by_itag(itag)
    total_filesize = selected_ado.filesize
    progress_bar = tqdm(total=total_filesize, unit='B', unit_scale=True, desc="Downloading Audio")
    random_filename = str(random.randint(1000000000, 9999999999))
    selected_ado.download(output_path=output_path, filename=random_filename + '_ado.mp4')
    return random_filename

def download_thumbnail(url, file_path):
    print('Downloading thumbnail...')
    maxres_url = re.sub(r'/[^/]*\.jpg.*$', '/maxresdefault.jpg', url)
    hq_url = re.sub(r'/[^/]*\.jpg.*$', '/hqdefault.jpg', url)
    
    response = requests.get(maxres_url, stream=True)
    if response.status_code != 200:
        response = requests.get(hq_url, stream=True)
    
    if response.status_code == 200:
        with open(file_path, 'wb') as file:
            response.raw.decode_content = True
            shutil.copyfileobj(response.raw, file)
    else:
        print('Failed to download thumbnail...!')
        sys.exit()

def progress(chunk, file_handle, bytes_remaining):
    chunk_size = total_filesize - bytes_remaining
    progress_bar.update(chunk_size - progress_bar.n)

    if bytes_remaining == 0:
        progress_bar.close()
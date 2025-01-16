from tqdm import tqdm
from .config import get_temporary_directory, load_config
from .utils import get_unique_filename, postprocess_cleanup
import os, re, requests, shutil, sys, random, ffmpy

userConfig = load_config()
downloadDIR = userConfig['downloadDIR']
tempDIR = get_temporary_directory()

def download_progressive(stream, itag, title, resolution, file_extention, captions, caption_code=None, tempDIR=tempDIR, downloadDIR=downloadDIR):
    global total_filesize, progress_bar
    selected_vdo = stream.get_by_itag(itag)
    total_filesize = selected_vdo.filesize
    progress_bar = tqdm(total=total_filesize, unit='B', unit_scale=True, desc="Downloading Video+Audio")
    random_filename = str(random.randint(1000000000, 9999999999))
    filename = random_filename + '_vdo.' + file_extention
    output_temp_file = os.path.join(tempDIR, filename)
    output_file = os.path.join(downloadDIR, get_unique_filename(title + '_' + resolution + '.' + file_extention)) if not caption_code else os.path.join(downloadDIR, get_unique_filename(title + '_' + resolution + '_' + caption_code + '.' + file_extention))
    selected_vdo.download(output_path=tempDIR, filename=filename)

    if caption_code:
        print(f'Downloading Caption ({caption_code})...')
        caption = captions[caption_code]
        caption_file = os.path.join(tempDIR, random_filename + '_cap.srt')
        caption.save_captions(caption_file)
        print('Processing...')
        devnull = open(os.devnull, 'w')
        output_temp_file_with_subs = os.path.join(tempDIR, random_filename + '_merged.' + file_extention)
        ff = ffmpy.FFmpeg(
            inputs={output_temp_file: None},
            outputs={output_temp_file_with_subs: ['-i', caption_file, '-c', 'copy', '-c:s', 'mov_text', '-metadata:s:s:0', f'language={caption_code}', '-metadata:s:s:0', f'title={caption_code}', '-metadata:s:s:0', f'handler_name={caption_code}']}
        )
        ff.run(stdout=devnull, stderr=devnull)
        devnull.close()

        shutil.move(output_temp_file_with_subs, output_file)
        postprocess_cleanup(tempDIR, ['_vdo.' + file_extention, '_cap.srt', '_merged.' + file_extention], random_filename)
        print('Done! 🎉')
    else:
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
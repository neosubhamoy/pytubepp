from mutagen.id3 import ID3, APIC, TIT2, TPE1, TALB
from .config import get_temporary_directory, load_config
from .utils import get_unique_filename, postprocess_cleanup
from .download import download_thumbnail
import os, shutil, ffmpy

userConfig = load_config()
downloadDIR = userConfig['downloadDIR']
tempDIR = get_temporary_directory()

def merge_audio_video(title, resolution, file_extention, random_filename, captions, caption_code=None, tempDIR=tempDIR, downloadDIR=downloadDIR):
    video_file = os.path.join(tempDIR, random_filename + '_vdo.' + file_extention)
    audio_file = os.path.join(tempDIR, random_filename + '_ado.' + file_extention)
    output_temp_file = os.path.join(tempDIR, random_filename + '_merged.' + file_extention)
    output_file = os.path.join(downloadDIR, get_unique_filename(title + '_' + resolution + '.' + file_extention)) if not caption_code else os.path.join(downloadDIR, get_unique_filename(title + '_' + resolution + '_' + caption_code + '.' + file_extention))
    
    if caption_code:
        print(f'Downloading Caption ({caption_code})...')
        caption = captions[caption_code]
        srt_file = os.path.join(tempDIR, random_filename + '_cap.srt')
        caption.save_captions(srt_file)
        vtt_file = os.path.join(tempDIR, random_filename + '_cap.vtt')

        print('Processing...')
        if file_extention == 'webm':
            devnull = open(os.devnull, 'w')
            ff_convert = ffmpy.FFmpeg(
                inputs={srt_file: None},
                outputs={vtt_file: None}
            )
            ff_convert.run(stdout=devnull, stderr=devnull)
            subtitle_file = vtt_file
            subtitle_codec = 'webvtt'
        else:
            subtitle_file = srt_file
            subtitle_codec = 'mov_text'
        
        input_params = {video_file: None, audio_file: None}
        output_params = {output_temp_file: ['-i', subtitle_file, '-c:v', 'copy', '-c:a', 'copy', 
                        '-c:s', subtitle_codec, '-metadata:s:s:0', f'language={caption_code}',
                        '-metadata:s:s:0', f'title={caption_code}', '-metadata:s:s:0', f'handler_name={caption_code}']}
        
        devnull = open(os.devnull, 'w')
        ff = ffmpy.FFmpeg(inputs=input_params, outputs=output_params)
        ff.run(stdout=devnull, stderr=devnull)
        devnull.close()

        shutil.move(output_temp_file, output_file)
        cleanup_files = ['_vdo.' + file_extention, '_ado.' + file_extention, '_cap.srt', '_merged.' + file_extention]
        if file_extention == 'webm':
            cleanup_files.append('_cap.vtt')
        postprocess_cleanup(tempDIR, cleanup_files, random_filename)
        print('Done! 🎉')
    else:
        input_params = {video_file: None, audio_file: None}
        output_params = {output_temp_file: ['-c:v', 'copy', '-c:a', 'copy']}

        print('Processing...')
        devnull = open(os.devnull, 'w')
        ff = ffmpy.FFmpeg(inputs=input_params, outputs=output_params)
        ff.run(stdout=devnull, stderr=devnull)
        devnull.close()

        shutil.move(output_temp_file, output_file)
        postprocess_cleanup(tempDIR, ['_vdo.' + file_extention, '_ado.' + file_extention, '_merged.' + file_extention], random_filename)
        print('Done! 🎉')

def convert_to_mp3(title, thumbnail_url, random_filename, mp3_artist='Unknown', mp3_title='Unknown', mp3_album='Unknown', tempDIR=tempDIR, downloadDIR=downloadDIR):
    image_file = os.path.join(tempDIR, random_filename + '_thumbnail.jpg')
    download_thumbnail(thumbnail_url, image_file)
    audio_file = os.path.join(tempDIR, random_filename + '_ado.mp4')
    output_file = os.path.join(downloadDIR, get_unique_filename(title + '_audio.mp3'))

    print('Processing...')
    devnull = open(os.devnull, 'w')
    video_file = os.path.join(tempDIR, random_filename + '_thumbnail.mp4')
    ff1 = ffmpy.FFmpeg(
        inputs={image_file: '-loop 1 -t 1'},
        outputs={video_file: '-vf "scale=1280:720" -r 1 -c:v libx264 -t 1'}
    )
    ff1.run(stdout=devnull, stderr=devnull)

    merged_file = os.path.join(tempDIR, random_filename + '_merged.mp4')
    ff2 = ffmpy.FFmpeg(
        inputs={video_file: None, audio_file: None},
        outputs={merged_file: '-c:v copy -c:a copy'}
    )
    ff2.run(stdout=devnull, stderr=devnull)

    output_temp_file = os.path.join(tempDIR, random_filename + '_merged.mp3')
    ff3 = ffmpy.FFmpeg(
        inputs={merged_file: None},
        outputs={output_temp_file: '-vn -c:a libmp3lame -q:a 2'}
    )
    ff3.run(stdout=devnull, stderr=devnull)
    devnull.close()

    audio = ID3(output_temp_file)
    audio.add(TIT2(encoding=3, text=mp3_title))
    audio.add(TPE1(encoding=3, text=mp3_artist))
    audio.add(TALB(encoding=3, text=mp3_album))
    with open(image_file, 'rb') as img:
        audio.add(APIC(
            encoding=3,
            mime='image/jpeg',
            type=3,
            desc=u'Cover',
            data=img.read()
        ))
    audio.save()

    shutil.move(output_temp_file, output_file)
    postprocess_cleanup(tempDIR, ['_thumbnail.jpg', '_thumbnail.mp4', '_ado.mp4', '_merged.mp4'], random_filename)
    print('Done! 🎉')
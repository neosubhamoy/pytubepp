from pytubefix import YouTube
from tabulate import tabulate
from .config import get_temporary_directory, load_config, update_config, reset_config
from .download import download_progressive, download_nonprogressive, download_audio, progress
from .postprocess import merge_audio_video, convert_to_mp3
from .utils import get_version, clear_temp_files, is_valid_url, network_available
import appdirs, os, re, sys, argparse, json

userConfig = load_config()
downloadDIR = userConfig['downloadDIR']
tempDIR = get_temporary_directory()
configDIR = appdirs.user_config_dir('pytubepp')
defaultStream = userConfig['defaultStream']
version = get_version()

def set_global_video_info(link):
    if not network_available():
        print('\nRequest timeout! Please check your network and try again...!!')
        sys.exit()
    
    if is_valid_url(link):
        global video, author, title, thumbnail, views, stream, stream_resolutions, maxres
        link = is_valid_url(link).group(1)
        video = YouTube(link, on_progress_callback=progress)
        author = video.author
        title = re.sub(r'[\\/*?:"<>|]', '_', author + ' - ' + video.title)
        thumbnail = video.thumbnail_url
        views = str(video.views)
        stream = video.streams
        stream_resolutions = {
            '4320p': {
                'allowed_streams': ['8k', '4320', '4320p'],
                'message': ['4320p', '[8k, 4320, 4320p]']
            },
            '2160p': {
                'allowed_streams': ['4k', '2160', '2160p'],
                'message': ['2160p', '[4k, 2160, 2160p]']
            },
            '1440p': {
                'allowed_streams': ['2k', '1440', '1440p'],
                'message': ['1440p', '[2k, 1440, 1440p]']
            },
            '1080p': {
                'allowed_streams': ['fhd', '1080', '1080p'],
                'message': ['1080p', '[fhd, 1080, 1080p]']
            },
            '720p': {
                'allowed_streams': ['hd', '720', '720p'],
                'message': ['720p', '[hd, 720, 720p]']
            },
            '480p': {
                'allowed_streams': ['480', '480p'],
                'message': ['480p', '[480, 480p]']
            },
            '360p': {
                'allowed_streams': ['360', '360p'],
                'message': ['360p', '[360, 360p]']
            },
            '240p': {
                'allowed_streams': ['240', '240p'],
                'message': ['240p', '[240, 240p]']
            },
            '144p': {
                'allowed_streams': ['144', '144p'],
                'message': ['144p', '[144, 144p]']
            },
            'mp3': {
                'allowed_streams': ['mp3'],
                'message': ['mp3', '[mp3]']
            }
        }
        for res in stream_resolutions.keys():
            if res != 'mp3' and stream.filter(res=res):
                maxres = res
                break
        return True
    else:
        return False

def show_video_info(link):
    if set_global_video_info(link):
        table = []
        found = False

        for res in stream_resolutions.keys():
            if found or (res not in ['mp3'] and stream.filter(res=res)) or (res == 'mp3' and stream.get_by_itag(140)):
                found = True
                if res == 'mp3':
                    matching_stream = stream.get_by_itag(140)
                else:
                    matching_stream = next((s for s in stream if s.resolution == res), None)
                if matching_stream is not None:
                    if res == '4320p':
                        type = matching_stream.mime_type
                        filesize = f"{(matching_stream.filesize + stream.get_by_itag(140).filesize) / (1024 * 1024 * 1024):.2f} GB" if matching_stream.filesize + stream.get_by_itag(140).filesize >= 1073741824 else f"{(matching_stream.filesize + stream.get_by_itag(140).filesize) / (1024 * 1024):.2f} MB"
                        fps = f"{matching_stream.fps}fps"
                        vdo_codec = matching_stream.video_codec
                        ado_codec = stream.get_by_itag(140).audio_codec
                        vdo_bitrate = f"{matching_stream.bitrate / 1024:.0f}kbps"
                        ado_bitrate = stream.get_by_itag(140).abr
                    if res == '2160p':
                        if stream.get_by_itag(701):
                            type = stream.get_by_itag(701).mime_type
                            filesize = f"{(stream.get_by_itag(701).filesize + stream.get_by_itag(140).filesize) / (1024 * 1024 * 1024):.2f} GB" if stream.get_by_itag(701).filesize + stream.get_by_itag(140).filesize >= 1073741824 else f"{(stream.get_by_itag(701).filesize + stream.get_by_itag(140).filesize) / (1024 * 1024):.2f} MB"
                            fps = f"{stream.get_by_itag(701).fps}fps"
                            vdo_codec = stream.get_by_itag(701).video_codec
                            ado_codec = stream.get_by_itag(140).audio_codec
                            vdo_bitrate = f"{stream.get_by_itag(701).bitrate / 1024:.0f}kbps"
                            ado_bitrate = stream.get_by_itag(140).abr
                        else:
                            type = matching_stream.mime_type
                            filesize = f"{(matching_stream.filesize + stream.get_by_itag(251).filesize) / (1024 * 1024 * 1024):.2f} GB" if matching_stream.filesize + stream.get_by_itag(251).filesize >= 1073741824 else f"{(matching_stream.filesize + stream.get_by_itag(251).filesize) / (1024 * 1024):.2f} MB"
                            fps = f"{matching_stream.fps}fps"
                            vdo_codec = matching_stream.video_codec
                            ado_codec = stream.get_by_itag(251).audio_codec
                            vdo_bitrate = f"{matching_stream.bitrate / 1024:.0f}kbps"
                            ado_bitrate = stream.get_by_itag(251).abr
                    elif res == '1440p':
                        if stream.get_by_itag(700):
                            type = stream.get_by_itag(700).mime_type
                            filesize = f"{(stream.get_by_itag(700).filesize + stream.get_by_itag(140).filesize) / (1024 * 1024 * 1024):.2f} GB" if stream.get_by_itag(700).filesize + stream.get_by_itag(140).filesize >= 1073741824 else f"{(stream.get_by_itag(700).filesize + stream.get_by_itag(140).filesize) / (1024 * 1024):.2f} MB"
                            fps = f"{stream.get_by_itag(700).fps}fps"
                            vdo_codec = stream.get_by_itag(700).video_codec
                            ado_codec = stream.get_by_itag(140).audio_codec
                            vdo_bitrate = f"{stream.get_by_itag(700).bitrate / 1024:.0f}kbps"
                            ado_bitrate = stream.get_by_itag(140).abr
                        else:
                            type = matching_stream.mime_type
                            filesize = f"{(matching_stream.filesize + stream.get_by_itag(251).filesize) / (1024 * 1024 * 1024):.2f} GB" if matching_stream.filesize + stream.get_by_itag(251).filesize >= 1073741824 else f"{(matching_stream.filesize + stream.get_by_itag(251).filesize) / (1024 * 1024):.2f} MB"
                            fps = f"{matching_stream.fps}fps"
                            vdo_codec = matching_stream.video_codec
                            ado_codec = stream.get_by_itag(251).audio_codec
                            vdo_bitrate = f"{matching_stream.bitrate / 1024:.0f}kbps"
                            ado_bitrate = stream.get_by_itag(251).abr
                    elif res == '1080p':
                        if stream.get_by_itag(699):
                            type = stream.get_by_itag(699).mime_type
                            filesize = f"{(stream.get_by_itag(699).filesize + stream.get_by_itag(140).filesize) / (1024 * 1024 * 1024):.2f} GB" if stream.get_by_itag(699).filesize + stream.get_by_itag(140).filesize >= 1073741824 else f"{(stream.get_by_itag(699).filesize + stream.get_by_itag(140).filesize) / (1024 * 1024):.2f} MB"
                            fps = f"{stream.get_by_itag(699).fps}fps"
                            vdo_codec = stream.get_by_itag(699).video_codec
                            ado_codec = stream.get_by_itag(140).audio_codec
                            vdo_bitrate = f"{stream.get_by_itag(699).bitrate / 1024:.0f}kbps"
                            ado_bitrate = stream.get_by_itag(140).abr
                        else:
                            type = matching_stream.mime_type
                            filesize = f"{(matching_stream.filesize + stream.get_by_itag(140).filesize) / (1024 * 1024 * 1024):.2f} GB" if matching_stream.filesize + stream.get_by_itag(140).filesize >= 1073741824 else f"{(matching_stream.filesize + stream.get_by_itag(140).filesize) / (1024 * 1024):.2f} MB"
                            fps = f"{matching_stream.fps}fps"
                            vdo_codec = matching_stream.video_codec
                            ado_codec = stream.get_by_itag(140).audio_codec
                            vdo_bitrate = f"{matching_stream.bitrate / 1024:.0f}kbps"
                            ado_bitrate = stream.get_by_itag(140).abr
                    elif res == '720p':
                        if stream.get_by_itag(698):
                            type = stream.get_by_itag(698).mime_type
                            filesize = f"{(stream.get_by_itag(698).filesize + stream.get_by_itag(140).filesize) / (1024 * 1024 * 1024):.2f} GB" if stream.get_by_itag(698).filesize + stream.get_by_itag(140).filesize >= 1073741824 else f"{(stream.get_by_itag(698).filesize + stream.get_by_itag(140).filesize) / (1024 * 1024):.2f} MB"
                            fps = f"{stream.get_by_itag(698).fps}fps"
                            vdo_codec = stream.get_by_itag(698).video_codec
                            ado_codec = stream.get_by_itag(140).audio_codec
                            vdo_bitrate = f"{stream.get_by_itag(698).bitrate / 1024:.0f}kbps"
                            ado_bitrate = stream.get_by_itag(140).abr
                        else:
                            type = matching_stream.mime_type
                            filesize = f"{(matching_stream.filesize + stream.get_by_itag(140).filesize) / (1024 * 1024 * 1024):.2f} GB" if matching_stream.filesize + stream.get_by_itag(140).filesize >= 1073741824 else f"{(matching_stream.filesize + stream.get_by_itag(140).filesize) / (1024 * 1024):.2f} MB"
                            fps = f"{matching_stream.fps}fps"
                            vdo_codec = matching_stream.video_codec
                            ado_codec = stream.get_by_itag(140).audio_codec
                            vdo_bitrate = f"{matching_stream.bitrate / 1024:.0f}kbps"
                            ado_bitrate = stream.get_by_itag(140).abr
                    elif res == '480p':
                        type = matching_stream.mime_type
                        filesize = f"{(matching_stream.filesize + stream.get_by_itag(140).filesize) / (1024 * 1024 * 1024):.2f} GB" if matching_stream.filesize + stream.get_by_itag(140).filesize >= 1073741824 else f"{(matching_stream.filesize + stream.get_by_itag(140).filesize) / (1024 * 1024):.2f} MB"
                        fps = f"{matching_stream.fps}fps"
                        vdo_codec = matching_stream.video_codec
                        ado_codec = stream.get_by_itag(140).audio_codec
                        vdo_bitrate = f"{matching_stream.bitrate / 1024:.0f}kbps"
                        ado_bitrate = stream.get_by_itag(140).abr
                    elif res == '360p':
                        type = matching_stream.mime_type
                        filesize = f"{matching_stream.filesize / (1024 * 1024 * 1024):.2f} GB" if matching_stream.filesize >= 1073741824 else f"{matching_stream.filesize / (1024 * 1024):.2f} MB"
                        fps = f"{matching_stream.fps}fps"
                        vdo_codec = matching_stream.video_codec
                        ado_codec = matching_stream.audio_codec
                        vdo_bitrate = f"{matching_stream.bitrate / 1024:.0f}kbps"
                        ado_bitrate = matching_stream.abr
                    elif res in ['240p', '144p']:
                        type = matching_stream.mime_type
                        filesize = f"{(matching_stream.filesize + stream.get_by_itag(139).filesize) / (1024 * 1024 * 1024):.2f} GB" if matching_stream.filesize + stream.get_by_itag(139).filesize >= 1073741824 else f"{(matching_stream.filesize + stream.get_by_itag(139).filesize) / (1024 * 1024):.2f} MB"
                        fps = f"{matching_stream.fps}fps"
                        vdo_codec = matching_stream.video_codec
                        ado_codec = stream.get_by_itag(139).audio_codec
                        vdo_bitrate = f"{matching_stream.bitrate / 1024:.0f}kbps"
                        ado_bitrate = stream.get_by_itag(139).abr
                    elif res == 'mp3':
                        type = "audio/mp3"
                        filesize = f"{matching_stream.filesize / (1024 * 1024 * 1024):.2f} GB" if matching_stream.filesize >= 1073741824 else f"{matching_stream.filesize / (1024 * 1024):.2f} MB"
                        fps = "none"
                        vdo_codec = "none"
                        ado_codec = matching_stream.audio_codec
                        vdo_bitrate = "none"
                        ado_bitrate = matching_stream.abr

                else:
                    filesize = "N/A"
                message = stream_resolutions[res]['message'] + [type] + [filesize] + [fps] + [vdo_codec] + [ado_codec] + [vdo_bitrate] + [ado_bitrate]
                table.append(message)

        if not found:
            print('Sorry, No video streams found....!!!')
            sys.exit()

        print(f'\nTitle: {video.title}\nAuthor: {author}\nPublished On: {video.publish_date.strftime("%d/%m/%Y")}\nDuration: {video.length}\nViews: {views}\n')
        print(tabulate(table, headers=['Stream', 'Alias (for -s flag)', 'Format', 'Size', 'FrameRate', 'V-Codec', 'A-Codec', 'V-BitRate', 'A-BitRate']))
        print('\n')
    else:
        print('\nInvalid video link! Please enter a valid video url...!!')

def show_raw_info(link, prettify=False):
    if set_global_video_info(link):
        streams_list = []
        found = False

        for res in stream_resolutions.keys():
            if found or (res not in ['mp3'] and stream.filter(res=res)) or (res == 'mp3' and stream.get_by_itag(140)):
                found = True
                if res == 'mp3':
                    matching_stream = stream.get_by_itag(140)
                else:
                    matching_stream = next((s for s in stream if s.resolution == res), None)
                if matching_stream is not None:
                    if res == '4320p':
                        itag = matching_stream.itag
                        resolution = '4320p'
                        type = matching_stream.mime_type
                        filesize = matching_stream.filesize + stream.get_by_itag(140).filesize
                        fps = matching_stream.fps
                        vdo_codec = matching_stream.video_codec
                        ado_codec = stream.get_by_itag(140).audio_codec
                        vdo_bitrate = f"{matching_stream.bitrate / 1024:.0f}kbps"
                        ado_bitrate = stream.get_by_itag(140).abr
                        is_hdr = True if matching_stream.itag == 702 else False
                    if res == '2160p':
                        resolution = '2160p'
                        if stream.get_by_itag(701):
                            itag = 701
                            type = stream.get_by_itag(701).mime_type
                            filesize = stream.get_by_itag(701).filesize + stream.get_by_itag(140).filesize
                            fps = stream.get_by_itag(701).fps
                            vdo_codec = stream.get_by_itag(701).video_codec
                            ado_codec = stream.get_by_itag(140).audio_codec
                            vdo_bitrate = f"{stream.get_by_itag(701).bitrate / 1024:.0f}kbps"
                            ado_bitrate = stream.get_by_itag(140).abr
                            is_hdr = True
                        else:
                            itag = matching_stream.itag
                            type = matching_stream.mime_type
                            filesize = matching_stream.filesize + stream.get_by_itag(251).filesize
                            fps = matching_stream.fps
                            vdo_codec = matching_stream.video_codec
                            ado_codec = stream.get_by_itag(251).audio_codec
                            vdo_bitrate = f"{matching_stream.bitrate / 1024:.0f}kbps"
                            ado_bitrate = stream.get_by_itag(251).abr
                            is_hdr = False
                    elif res == '1440p':
                        resolution = '1440p'
                        if stream.get_by_itag(700):
                            itag = 700
                            type = stream.get_by_itag(700).mime_type
                            filesize = stream.get_by_itag(700).filesize + stream.get_by_itag(140).filesize
                            fps = stream.get_by_itag(700).fps
                            vdo_codec = stream.get_by_itag(700).video_codec
                            ado_codec = stream.get_by_itag(140).audio_codec
                            vdo_bitrate = f"{stream.get_by_itag(700).bitrate / 1024:.0f}kbps"
                            ado_bitrate = stream.get_by_itag(140).abr
                            is_hdr = True
                        else:
                            itag = matching_stream.itag
                            type = matching_stream.mime_type
                            filesize = matching_stream.filesize + stream.get_by_itag(251).filesize
                            fps = matching_stream.fps
                            vdo_codec = matching_stream.video_codec
                            ado_codec = stream.get_by_itag(251).audio_codec
                            vdo_bitrate = f"{matching_stream.bitrate / 1024:.0f}kbps"
                            ado_bitrate = stream.get_by_itag(251).abr
                            is_hdr = False
                    elif res == '1080p':
                        resolution = '1080p'
                        if stream.get_by_itag(699):
                            itag = 699
                            type = stream.get_by_itag(699).mime_type
                            filesize = stream.get_by_itag(699).filesize + stream.get_by_itag(140).filesize
                            fps = stream.get_by_itag(699).fps
                            vdo_codec = stream.get_by_itag(699).video_codec
                            ado_codec = stream.get_by_itag(140).audio_codec
                            vdo_bitrate = f"{stream.get_by_itag(699).bitrate / 1024:.0f}kbps"
                            ado_bitrate = stream.get_by_itag(140).abr
                            is_hdr = True
                        else:
                            itag = matching_stream.itag
                            type = matching_stream.mime_type
                            filesize = matching_stream.filesize + stream.get_by_itag(140).filesize
                            fps = matching_stream.fps
                            vdo_codec = matching_stream.video_codec
                            ado_codec = stream.get_by_itag(140).audio_codec
                            vdo_bitrate = f"{matching_stream.bitrate / 1024:.0f}kbps"
                            ado_bitrate = stream.get_by_itag(140).abr
                            is_hdr = False
                    elif res == '720p':
                        resolution = '720p'
                        if stream.get_by_itag(698):
                            itag = 698
                            type = stream.get_by_itag(698).mime_type
                            filesize = stream.get_by_itag(698).filesize + stream.get_by_itag(140).filesize
                            fps = stream.get_by_itag(698).fps
                            vdo_codec = stream.get_by_itag(698).video_codec
                            ado_codec = stream.get_by_itag(140).audio_codec
                            vdo_bitrate = f"{stream.get_by_itag(698).bitrate / 1024:.0f}kbps"
                            ado_bitrate = stream.get_by_itag(140).abr
                            is_hdr = True
                        else:
                            itag = matching_stream.itag
                            type = matching_stream.mime_type
                            filesize = matching_stream.filesize + stream.get_by_itag(140).filesize
                            fps = matching_stream.fps
                            vdo_codec = matching_stream.video_codec
                            ado_codec = stream.get_by_itag(140).audio_codec
                            vdo_bitrate = f"{matching_stream.bitrate / 1024:.0f}kbps"
                            ado_bitrate = stream.get_by_itag(140).abr
                            is_hdr = False
                    elif res == '480p':
                        itag = matching_stream.itag
                        resolution = '480p'
                        type = matching_stream.mime_type
                        filesize = matching_stream.filesize + stream.get_by_itag(140).filesize
                        fps = matching_stream.fps
                        vdo_codec = matching_stream.video_codec
                        ado_codec = stream.get_by_itag(140).audio_codec
                        vdo_bitrate = f"{matching_stream.bitrate / 1024:.0f}kbps"
                        ado_bitrate = stream.get_by_itag(140).abr
                        is_hdr = False
                    elif res == '360p':
                        itag = matching_stream.itag
                        resolution = '360p'
                        type = matching_stream.mime_type
                        filesize = matching_stream.filesize
                        fps = matching_stream.fps
                        vdo_codec = matching_stream.video_codec
                        ado_codec = matching_stream.audio_codec
                        vdo_bitrate = f"{matching_stream.bitrate / 1024:.0f}kbps"
                        ado_bitrate = matching_stream.abr
                        is_hdr = False
                    elif res in ['240p', '144p']:
                        itag = matching_stream.itag
                        resolution = res
                        type = matching_stream.mime_type
                        filesize = matching_stream.filesize + stream.get_by_itag(139).filesize
                        fps = matching_stream.fps
                        vdo_codec = matching_stream.video_codec
                        ado_codec = stream.get_by_itag(139).audio_codec
                        vdo_bitrate = f"{matching_stream.bitrate / 1024:.0f}kbps"
                        ado_bitrate = stream.get_by_itag(139).abr
                        is_hdr = False
                    elif res == 'mp3':
                        itag = matching_stream.itag
                        resolution = 'mp3'
                        type = "audio/mp3"
                        filesize = matching_stream.filesize
                        fps = None
                        vdo_codec = None
                        ado_codec = matching_stream.audio_codec
                        vdo_bitrate = None
                        ado_bitrate = matching_stream.abr
                        is_hdr = False

                else:
                    filesize = "N/A"
                current_stream = {
                    'itag': itag,
                    'res': resolution,
                    'mime_type': type,
                    'file_size': filesize,
                    'fps': fps,
                    'vcodec': vdo_codec,
                    'acodec': ado_codec,
                    'vbitrate': vdo_bitrate,
                    'abitrate': ado_bitrate,
                    'is_hdr': is_hdr
                }
                streams_list.append(current_stream)

        if not found:
            print('Sorry, No video streams found....!!!')
            sys.exit()

        if prettify:
            print(json.dumps({
            'id': video.video_id,
            'title': video.title,
            'author': author,
            'thumbnail_url': thumbnail,
            'views': video.views,
            'published_on': video.publish_date.strftime('%d/%m/%Y'),
            'duration': video.length,
            'streams': streams_list,
            }, indent=4))
        else:
            print(json.dumps({
                'id': video.video_id,
                'title': video.title,
                'author': author,
                'thumbnail_url': thumbnail,
                'views': video.views,
                'published_on': video.publish_date.strftime('%d/%m/%Y'),
                'duration': video.length,
                'streams': streams_list,
            }))
    else:
        print('\nInvalid video link! Please enter a valid video url...!!')

def get_allowed_streams(link):
    if set_global_video_info(link):
        allowed_streams = []
        found = False
        for res in stream_resolutions.keys():
            if found or (res not in ['mp3'] and stream.filter(res=res)) or (res == 'mp3' and stream.get_by_itag(140)):
                found = True
                allowed_streams.extend(stream_resolutions[res]['allowed_streams'])
        return allowed_streams
    else:
        print('\nInvalid video link! Please enter a valid video url...!!')
        return []
    
def print_short_info(chosen_stream):
    if chosen_stream in ['720', '720p', 'hd']:
        print(f'\nVideo: {title}\nSelected Stream: 720p (HD)\n')
    elif chosen_stream in ['360', '360p']:
        print(f'\nVideo: {title}\nSelected Stream: 360p (SD)\n')
    elif chosen_stream in ['1080', '1080p', 'fhd']:
        print(f'\nVideo: {title}\nSelected Stream: 1080p (FHD)\n')
    elif chosen_stream in ['480', '480p']:
        print(f'\nVideo: {title}\nSelected Stream: 480p (SD)\n')
    elif chosen_stream in ['240', '240p']:
        print(f'\nVideo: {title}\nSelected Stream: 240p (LD)\n')
    elif chosen_stream in ['144', '144p']:
        print(f'\nVideo: {title}\nSelected Stream: 144p (LD)\n')
    elif chosen_stream in ['4320', '4320p', '8k']:
        print(f'\nVideo: {title}\nSelected Stream: 4320p (8K)\n')
    elif chosen_stream in ['2160', '2160p', '4k']:
        print(f'\nVideo: {title}\nSelected Stream: 2160p (4K)\n')
    elif chosen_stream in ['1440', '1440p', '2k']:
        print(f'\nVideo: {title}\nSelected Stream: 1440p (2K)\n')
    elif chosen_stream == 'mp3':
        print(f'\nVideo: {title}\nSelected Stream: mp3 (Audio)\n')

def download_stream(link, chosen_stream):
    if set_global_video_info(link):
        print_short_info(chosen_stream)
        allowed_streams = get_allowed_streams(link)
        if chosen_stream in allowed_streams:
            if chosen_stream in ['360', '360p']:
                download_progressive(stream, 18, title, '360p', 'mp4')

            elif chosen_stream in ['1080', '1080p', 'fhd']:
                if stream.get_by_itag(699):
                    merge_audio_video(title, '1080p', 'mp4', download_nonprogressive(stream, 699, 140, 'mp4', tempDIR))
                elif stream.get_by_itag(299):
                    merge_audio_video(title, '1080p', 'mp4', download_nonprogressive(stream, 299, 140, 'mp4', tempDIR))
                elif stream.get_by_itag(137):
                    merge_audio_video(title, '1080p', 'mp4', download_nonprogressive(stream, 137, 140, 'mp4', tempDIR))

            elif chosen_stream in ['720', '720p', 'hd']:
                if stream.get_by_itag(698):
                    merge_audio_video(title, '720p', 'mp4', download_nonprogressive(stream, 698, 140, 'mp4', tempDIR))
                elif stream.get_by_itag(298):
                    merge_audio_video(title, '720p', 'mp4', download_nonprogressive(stream, 298, 140, 'mp4', tempDIR))
                elif stream.get_by_itag(136):
                    merge_audio_video(title, '720p', 'mp4', download_nonprogressive(stream, 136, 140, 'mp4', tempDIR))

            elif chosen_stream in ['480', '480p']:
                merge_audio_video(title, '480p', 'mp4', download_nonprogressive(stream, 135, 140, 'mp4', tempDIR))

            elif chosen_stream in ['240', '240p']:
                merge_audio_video(title, '240p', 'mp4', download_nonprogressive(stream, 133, 139, 'mp4', tempDIR))

            elif chosen_stream in ['144', '144p']:
                merge_audio_video(title, '144p', 'mp4', download_nonprogressive(stream, 160, 139, 'mp4', tempDIR))

            elif chosen_stream in ['4320', '4320p', '8k']:
                if stream.get_by_itag(702):
                    merge_audio_video(title, '8k', 'mp4', download_nonprogressive(stream, 702, 140, 'mp4', tempDIR))
                elif stream.get_by_itag(571):
                    merge_audio_video(title, '8k', 'mp4', download_nonprogressive(stream, 571, 140, 'mp4', tempDIR))

            elif chosen_stream in ['2160', '2160p', '4k']:
                if stream.get_by_itag(701):
                    merge_audio_video(title, '4k', 'mp4', download_nonprogressive(stream, 701, 140, 'mp4', tempDIR))
                elif stream.get_by_itag(315):
                    merge_audio_video(title, '4k', 'webm', download_nonprogressive(stream, 315, 251, 'webm', tempDIR))
                elif stream.get_by_itag(313):
                    merge_audio_video(title, '4k', 'webm', download_nonprogressive(stream, 313, 251, 'webm', tempDIR))

            elif chosen_stream in ['1440', '1440p', '2k']:
                if stream.get_by_itag(700):
                    merge_audio_video(title, '2k', 'mp4', download_nonprogressive(stream, 700, 140, 'mp4', tempDIR))
                elif stream.get_by_itag(308):
                    merge_audio_video(title, '2k', 'webm', download_nonprogressive(stream, 308, 251, 'webm', tempDIR))
                elif stream.get_by_itag(271):
                    merge_audio_video(title, '2k', 'webm', download_nonprogressive(stream, 271, 251, 'webm', tempDIR))

            elif chosen_stream == 'mp3':
                convert_to_mp3(title, thumbnail, download_audio(stream, 140, tempDIR), author, video.title, author)
        else:
            print('\nInvalid download stream or stream not available! Please choose a different stream...!! (use -i to see available streams)')
    else:
        print('\nInvalid video link! Please enter a valid video url...!!')
        
def main():
    parser = argparse.ArgumentParser(description=f'PytubePP (Pytube Post Processor) v{version} - A Simple CLI Tool to Download Your Favorite YouTube Videos Effortlessly!')
    parser.add_argument('url', nargs='?', default=None, help='url of the youtube video')
    parser.add_argument('-df', '--download-folder', default=argparse.SUPPRESS, help='set custom download folder path (default: ~/Downloads/Pytube Downloads) [arg eg: "/path/to/folder"]')
    parser.add_argument('-ds', '--default-stream', default=argparse.SUPPRESS, help='set default download stream (default: max) [available arguments: 144p, 240p, 360p, 480p, 720p, 1080p, 1440p, 2160p, 4320p, mp3, max]')
    parser.add_argument('-s', '--stream', default=argparse.SUPPRESS, help='choose download stream for the current video (default: your chosen --default-stream) [available arguments: 144p, 240p, 360p, 480p, 720p, 1080p, 1440p, 2160p, 4320p, 144, 240, 360, 480, 720, 1080, 1440, 2160, 4320, mp3, hd, fhd, 2k, 4k, 8k]')
    parser.add_argument('-i', '--show-info', action='store_true', help='show video info (title, author, views and available_streams)')
    parser.add_argument('-ri', '--raw-info', action='store_true', help='show video info in raw json format')
    parser.add_argument('-jp', '--json-prettify', action='store_true', help='show json in prettified indented view')
    parser.add_argument('-sc', '--show-config', action='store_true', help='show all current user config settings')
    parser.add_argument('-r', '--reset-default', action='store_true', help='reset to default settings (download_folder and default_stream)')
    parser.add_argument('-ct', '--clear-temp', action='store_true', help='clear temporary files (audio, video, thumbnail files of the failed, incomplete downloads)')
    parser.add_argument('-v', '--version', action='store_true', help='show version number')
    args = parser.parse_args()

    if len(sys.argv) == 1:
        print('\nNo arguments supplied! exiting...!!')
        parser.print_help()
        sys.exit(1)
    
    if args.url:
        if 'download_folder' in args:
            print('\nVideo url supplied! igonering -df flag...!!')

        if 'default_stream' in args:
            print('\nVideo url supplied! ignoreing -ds flag...!!')

        if args.reset_default:
            print('\nVideo url supplied! ignoreing -r flag...!!')

        if args.clear_temp:
            print('\nVideo url supplied! ignoreing -ct flag...!!')

        if args.show_config:
            print('\nVideo url supplied! ignoreing -sc flag...!!')

        if args.show_info:
            show_video_info(args.url)
        
        if args.raw_info:
            if args.json_prettify:
                show_raw_info(args.url, True)
            else:
                show_raw_info(args.url)

        if args.json_prettify and not args.raw_info:
            print('\nMissing flag! -jp flag must be used with a flag which returns json data...!! (eg: -ri)')
        
        if 'stream' in args:
            download_stream(args.url, args.stream)
            
        if 'stream' not in args and not args.show_info and not args.raw_info and not args.json_prettify:
            if set_global_video_info(args.url):
                if defaultStream == 'max' and maxres != None:
                    download_stream(args.url, maxres)
                    return
                if (defaultStream == 'mp3' and stream.get_by_itag(140)) or (defaultStream != 'max' and stream.filter(res=defaultStream)):
                    download_stream(args.url, defaultStream)
                else:
                    if maxres != None:
                        print(f'\nDefault stream not available! ( Default: {defaultStream} | Available: {maxres} )')
                        answer = input('Do you want to download the maximum available stream ? [yes/no]\n')
                        while answer not in ['yes', 'y', 'no', 'n']:
                            print('Invalid answer! try again...!! answer with: [yes/y/no/n]')
                            answer = input('Do you want to download the maximum available stream ? [yes/no]\n')
                        if answer in ['yes', 'y']:
                            download_stream(args.url, maxres)
                        else:
                            print('Download cancelled! exiting...!!')
                    else:
                        print('Sorry, No downloadable video stream found....!!!')
            else:
                print('\nInvalid video link! Please enter a valid video url...!!')

    else:
        if 'download_folder' in args:
            if args.download_folder != downloadDIR:
                if os.path.isdir(args.download_folder):
                    update_config('downloadDIR', args.download_folder)
                    os.makedirs(args.download_folder, exist_ok=True)
                    print(f'\nDownload folder updated to: {args.download_folder}')
                else:
                    print('\nInvalid download folder path! Please enter a valid path...!!')
            else:
                print('\nDownload folder path is the same! Not updating...!!')

        if 'default_stream' in args:
            if args.default_stream != defaultStream:
                if args.default_stream in ['144p', '240p', '360p', '480p', '720p', '1080p', '1440p', '2160p', '4320p', 'mp3', 'max']:
                    update_config('defaultStream', args.default_stream)
                    print(f'\nDefault stream updated to: {args.default_stream}')
                else:
                    print('\nInvalid default stream! Please enter a valid stream...!! (use -h to see available default_stream arguments)')
            else:
                print('\nDefault stream is the same! Not updating...!!')
            
        if args.reset_default:
            reset_config()
        
        if args.clear_temp:
            clear_temp_files()

        if args.show_config:
            print(f'\ndownloadDIR: {downloadDIR}\ntempDIR: {tempDIR}\nconfigDIR: {configDIR}\ndefaultStream: {defaultStream}\n')

        if args.version:
            print(f'pytubepp {version}')

        if args.show_info:
            print('\nNo video url supplied! exiting...!!')

        if args.raw_info:
            print('\nNo video url supplied! exiting...!!')

        if args.json_prettify and not args.raw_info:
            print('\nMissing flag! -jp flag must be used with a flag which returns json data...!! (eg: -ri)')

        if 'stream' in args:
            print('\nNo video url supplied! exiting...!!')


if __name__ == "__main__":
    main()
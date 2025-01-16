from pytubefix import YouTube
from tabulate import tabulate
from .config import get_temporary_directory, load_config, update_config, reset_config
from .download import download_progressive, download_nonprogressive, download_audio, progress
from .postprocess import merge_audio_video, convert_to_mp3
from .utils import get_version, clear_temp_files, is_valid_url, network_available
import appdirs, os, re, sys, argparse, json

class YouTubeDownloader:
    def __init__(self):
        self.user_config = load_config()
        self.download_dir = self.user_config['downloadDIR']
        self.temp_dir = get_temporary_directory()
        self.config_dir = appdirs.user_config_dir('pytubepp')
        self.default_stream = self.user_config['defaultStream']
        self.default_caption = self.user_config['defaultCaption']
        self.version = get_version()
        
        # Video attributes
        self.video = None
        self.author = None
        self.title = None
        self.thumbnail = None
        self.views = None
        self.stream = None
        self.maxres = None
        
        self.stream_resolutions = {
            '4320p': {'allowed_streams': ['8k', '4320', '4320p'], 'message': ['4320p', '[8k, 4320, 4320p]']},
            '2160p': {'allowed_streams': ['4k', '2160', '2160p'], 'message': ['2160p', '[4k, 2160, 2160p]']},
            '1440p': {'allowed_streams': ['2k', '1440', '1440p'], 'message': ['1440p', '[2k, 1440, 1440p]']},
            '1080p': {'allowed_streams': ['fhd', '1080', '1080p'], 'message': ['1080p', '[fhd, 1080, 1080p]']},
            '720p': {'allowed_streams': ['hd', '720', '720p'], 'message': ['720p', '[hd, 720, 720p]']},
            '480p': {'allowed_streams': ['480', '480p'], 'message': ['480p', '[480, 480p]']},
            '360p': {'allowed_streams': ['360', '360p'], 'message': ['360p', '[360, 360p]']},
            '240p': {'allowed_streams': ['240', '240p'], 'message': ['240p', '[240, 240p]']},
            '144p': {'allowed_streams': ['144', '144p'], 'message': ['144p', '[144, 144p]']},
            'mp3': {'allowed_streams': ['mp3'], 'message': ['mp3', '[mp3]']}
        }

    def set_video_info(self, link):
        if not network_available():
            print('\nRequest timeout! Please check your network and try again...!!')
            sys.exit()
        
        if is_valid_url(link):
            link = is_valid_url(link).group(1)
            self.video = YouTube(link, 'ANDROID', on_progress_callback=progress)
            self.author = self.video.author
            self.title = re.sub(r'[\\/*?:"<>|]', '_', self.author + ' - ' + self.video.title)
            self.thumbnail = self.video.thumbnail_url
            self.views = str(self.video.views)
            self.stream = self.video.streams
            self.captions = self.video.captions
            
            # Find maximum resolution
            for res in self.stream_resolutions.keys():
                if res != 'mp3' and self.stream.filter(res=res):
                    self.maxres = res
                    break
            return True
        return False

    def get_stream_info(self, res, matching_stream):
        """Helper method to get stream information based on resolution"""
        stream_info = {}
        
        if res == 'mp3':
            stream_info = {
                'type': "audio/mp3",
                'filesize': f"{matching_stream.filesize / (1024 * 1024 * 1024):.2f} GB" if matching_stream.filesize >= 1073741824 else f"{matching_stream.filesize / (1024 * 1024):.2f} MB",
                'raw_filesize': matching_stream.filesize,
                'fps': None,
                'raw_fps': None,
                'vdo_codec': None,
                'ado_codec': matching_stream.audio_codec,
                'vdo_bitrate': None,
                'ado_bitrate': matching_stream.abr
            }
        elif res == '360p':
            stream_info = {
                'type': matching_stream.mime_type,
                'filesize': f"{matching_stream.filesize / (1024 * 1024 * 1024):.2f} GB" if matching_stream.filesize >= 1073741824 else f"{matching_stream.filesize / (1024 * 1024):.2f} MB",
                'raw_filesize': matching_stream.filesize,
                'fps': f"{matching_stream.fps}fps",
                'raw_fps': matching_stream.fps,
                'vdo_codec': matching_stream.video_codec,
                'ado_codec': matching_stream.audio_codec,
                'vdo_bitrate': f"{matching_stream.bitrate / 1024:.0f}kbps",
                'ado_bitrate': matching_stream.abr
            }
        else:
            _select_suitable_audio_stream = lambda stream: 139 if stream.itag in [160, 133] else (251 if stream.mime_type == 'video/webm' else 140)
            # Check for HDR variants first
            hdr_stream = None
            if res in ['4320p', '2160p', '1440p', '1080p', '720p']:
                hdr_itags = {'4320p': 702, '2160p': 701, '1440p': 700, '1080p': 699, '720p': 698}
                hdr_stream = self.stream.get_by_itag(hdr_itags.get(res))
            
            # Use HDR stream if available, otherwise use the original stream
            final_stream = hdr_stream if hdr_stream else matching_stream
            audio_stream = self.stream.get_by_itag(_select_suitable_audio_stream(final_stream))
            
            total_size = final_stream.filesize + audio_stream.filesize
            
            stream_info = {
                'type': final_stream.mime_type,
                'filesize': f"{total_size / (1024 * 1024 * 1024):.2f} GB" if total_size >= 1073741824 else f"{total_size / (1024 * 1024):.2f} MB",
                'raw_filesize': total_size,
                'fps': f"{final_stream.fps}fps",
                'raw_fps': final_stream.fps,
                'vdo_codec': final_stream.video_codec,
                'ado_codec': audio_stream.audio_codec,
                'vdo_bitrate': f"{final_stream.bitrate / 1024:.0f}kbps",
                'ado_bitrate': audio_stream.abr,
                'is_hdr': bool(hdr_stream),  # Track if this is an HDR stream
                'stream_itag': final_stream.itag  # Track the actual itag being used
            }
            
        return stream_info

    def show_video_info(self, link):
        if self.set_video_info(link):
            table = []
            found = False

            for res in self.stream_resolutions.keys():
                if found or (res not in ['mp3'] and self.stream.filter(res=res)) or (res == 'mp3' and self.stream.get_by_itag(140)):
                    found = True
                    matching_stream = self.stream.get_by_itag(140) if res == 'mp3' else next((s for s in self.stream if s.resolution == res), None)
                    
                    if matching_stream:
                        stream_info = self.get_stream_info(res, matching_stream)
                        message = self.stream_resolutions[res]['message'] + [
                            stream_info['type'],
                            stream_info['filesize'],
                            stream_info['fps'] if stream_info['fps'] else "none",
                            stream_info['vdo_codec'] if stream_info['vdo_codec'] else "none",
                            stream_info['ado_codec'],
                            stream_info['vdo_bitrate'] if stream_info['vdo_bitrate'] else "none",
                            stream_info['ado_bitrate']
                        ]
                        table.append(message)

            if not found:
                print('Sorry, No video streams found....!!!')
                sys.exit()

            print(f'\nTitle: {self.video.title}\nAuthor: {self.author}\nPublished On: {self.video.publish_date.strftime("%d/%m/%Y")}\nDuration: {f"{self.video.length//3600:02}:{(self.video.length%3600)//60:02}:{self.video.length%60:02}" if self.video.length >= 3600 else f"{(self.video.length%3600)//60:02}:{self.video.length%60:02}"}\nViews: {self.views}\nCaptions: {[caption.code for caption in self.captions.keys()] or "Unavailable"}\n')
            print(tabulate(table, headers=['Stream', 'Alias (for -s flag)', 'Format', 'Size', 'FrameRate', 'V-Codec', 'A-Codec', 'V-BitRate', 'A-BitRate']))
            print('\n')
        else:
            print('\nInvalid video link! Please enter a valid video url...!!')

    def show_raw_info(self, link, prettify=False):
        if self.set_video_info(link):
            streams_list = []
            found = False

            for res in self.stream_resolutions.keys():
                if found or (res not in ['mp3'] and self.stream.filter(res=res)) or (res == 'mp3' and self.stream.get_by_itag(140)):
                    found = True
                    matching_stream = self.stream.get_by_itag(140) if res == 'mp3' else next((s for s in self.stream if s.resolution == res), None)
                    
                    if matching_stream:
                        stream_info = self.get_stream_info(res, matching_stream)
                        streams_list.append({
                            'itag': stream_info.get('stream_itag', matching_stream.itag),
                            'res': res,
                            'mime_type': stream_info['type'],
                            'file_size': stream_info['raw_filesize'],
                            'fps': stream_info['raw_fps'],
                            'vcodec': stream_info['vdo_codec'],
                            'acodec': stream_info['ado_codec'],
                            'vbitrate': stream_info['vdo_bitrate'],
                            'abitrate': stream_info['ado_bitrate'],
                            'is_hdr': stream_info.get('is_hdr', False)
                        })

            if not found:
                print('Sorry, No video streams found....!!!')
                sys.exit()

            output = {
                'id': self.video.video_id,
                'title': self.video.title,
                'author': self.author,
                'thumbnail_url': self.thumbnail,
                'views': self.video.views,
                'published_on': self.video.publish_date.strftime('%d/%m/%Y'),
                'duration': self.video.length,
                'streams': streams_list,
                'captions': [caption.code for caption in self.captions.keys()] or None
            }
            
            print(json.dumps(output, indent=4 if prettify else None))
        else:
            print('\nInvalid video link! Please enter a valid video url...!!')

    def get_allowed_streams(self, link):
        if self.set_video_info(link):
            allowed_streams = []
            found = False
            for res in self.stream_resolutions.keys():
                if found or (res not in ['mp3'] and self.stream.filter(res=res)) or (res == 'mp3' and self.stream.get_by_itag(140)):
                    found = True
                    allowed_streams.extend(self.stream_resolutions[res]['allowed_streams'])
            return allowed_streams
        else:
            print('\nInvalid video link! Please enter a valid video url...!!')
            return []
        
    def get_allowed_captions(self, link):
        if self.set_video_info(link):
            return self.captions.keys()
        else:
            print('\nInvalid video link! Please enter a valid video url...!!')
            return []

    def print_short_info(self, chosen_stream):
        resolution_map = {
            '4320': '4320p (8K)', '4320p': '4320p (8K)', '8k': '4320p (8K)',
            '2160': '2160p (4K)', '2160p': '2160p (4K)', '4k': '2160p (4K)',
            '1440': '1440p (2K)', '1440p': '1440p (2K)', '2k': '1440p (2K)',
            '1080': '1080p (FHD)', '1080p': '1080p (FHD)', 'fhd': '1080p (FHD)',
            '720': '720p (HD)', '720p': '720p (HD)', 'hd': '720p (HD)',
            '480': '480p (SD)', '480p': '480p (SD)',
            '360': '360p (SD)', '360p': '360p (SD)',
            '240': '240p (LD)', '240p': '240p (LD)',
            '144': '144p (LD)', '144p': '144p (LD)',
            'mp3': 'mp3 (Audio)'
        }
        print(f'\nTitle: {self.title}\nSelected Stream: {resolution_map.get(chosen_stream, "Unknown")}\n')

    def download_stream(self, link, chosen_stream, chosen_caption=None):
        if self.set_video_info(link):
            allowed_streams = self.get_allowed_streams(link)
            allowed_captions = self.get_allowed_captions(link)

            if chosen_caption and (chosen_caption not in allowed_captions):
                print('\nInvalid caption code or caption not available! Please choose a different caption...!! (use -i to see available captions)')
                sys.exit()
            
            if chosen_stream in allowed_streams:
                self.print_short_info(chosen_stream)
                if chosen_stream in ['360', '360p']:
                    download_progressive(self.stream, 18, self.title, '360p', 'mp4', self.captions, chosen_caption)
                elif chosen_stream in ['1080', '1080p', 'fhd']:
                    self._handle_1080p_download(chosen_caption)
                elif chosen_stream in ['720', '720p', 'hd']:
                    self._handle_720p_download(chosen_caption)
                elif chosen_stream in ['480', '480p']:
                    merge_audio_video(self.title, '480p', 'mp4', download_nonprogressive(self.stream, 135, 140, 'mp4', self.temp_dir), self.captions, chosen_caption)
                elif chosen_stream in ['240', '240p']:
                    merge_audio_video(self.title, '240p', 'mp4', download_nonprogressive(self.stream, 133, 139, 'mp4', self.temp_dir), self.captions, chosen_caption)
                elif chosen_stream in ['144', '144p']:
                    merge_audio_video(self.title, '144p', 'mp4', download_nonprogressive(self.stream, 160, 139, 'mp4', self.temp_dir), self.captions, chosen_caption)
                elif chosen_stream in ['4320', '4320p', '8k']:
                    self._handle_4320p_download(chosen_caption)
                elif chosen_stream in ['2160', '2160p', '4k']:
                    self._handle_2160p_download(chosen_caption)
                elif chosen_stream in ['1440', '1440p', '2k']:
                    self._handle_1440p_download(chosen_caption)
                elif chosen_stream == 'mp3':
                    convert_to_mp3(self.title, self.thumbnail, download_audio(self.stream, 140, self.temp_dir), self.author, self.video.title, self.author)
            else:
                print('\nInvalid download stream or stream not available! Please choose a different stream...!! (use -i to see available streams)')
        else:
            print('\nInvalid video link! Please enter a valid video url...!!')

    def _handle_4320p_download(self, chosen_caption=None):
        if self.stream.get_by_itag(702):
            merge_audio_video(self.title, '8k', 'mp4', download_nonprogressive(self.stream, 702, 140, 'mp4', self.temp_dir), self.captions, chosen_caption)
        elif self.stream.get_by_itag(571):
            merge_audio_video(self.title, '8k', 'mp4', download_nonprogressive(self.stream, 571, 140, 'mp4', self.temp_dir), self.captions, chosen_caption)

    def _handle_2160p_download(self, chosen_caption=None):
        if self.stream.get_by_itag(701):
            merge_audio_video(self.title, '4k', 'mp4', download_nonprogressive(self.stream, 701, 140, 'mp4', self.temp_dir), self.captions, chosen_caption)
        elif self.stream.get_by_itag(315):
            merge_audio_video(self.title, '4k', 'webm', download_nonprogressive(self.stream, 315, 251, 'webm', self.temp_dir), self.captions, chosen_caption)
        elif self.stream.get_by_itag(313):
            merge_audio_video(self.title, '4k', 'webm', download_nonprogressive(self.stream, 313, 251, 'webm', self.temp_dir), self.captions, chosen_caption)

    def _handle_1440p_download(self, chosen_caption=None):
        if self.stream.get_by_itag(700):
            merge_audio_video(self.title, '2k', 'mp4', download_nonprogressive(self.stream, 700, 140, 'mp4', self.temp_dir), self.captions, chosen_caption)
        elif self.stream.get_by_itag(308):
            merge_audio_video(self.title, '2k', 'webm', download_nonprogressive(self.stream, 308, 251, 'webm', self.temp_dir), self.captions, chosen_caption)
        elif self.stream.get_by_itag(271):
            merge_audio_video(self.title, '2k', 'webm', download_nonprogressive(self.stream, 271, 251, 'webm', self.temp_dir), self.captions, chosen_caption)

    def _handle_1080p_download(self, chosen_caption=None):
        if self.stream.get_by_itag(699):
            merge_audio_video(self.title, '1080p', 'mp4', download_nonprogressive(self.stream, 699, 140, 'mp4', self.temp_dir), self.captions, chosen_caption)
        elif self.stream.get_by_itag(299):
            merge_audio_video(self.title, '1080p', 'mp4', download_nonprogressive(self.stream, 299, 140, 'mp4', self.temp_dir), self.captions, chosen_caption)
        elif self.stream.get_by_itag(137):
            merge_audio_video(self.title, '1080p', 'mp4', download_nonprogressive(self.stream, 137, 140, 'mp4', self.temp_dir), self.captions, chosen_caption)

    def _handle_720p_download(self, chosen_caption=None):
        if self.stream.get_by_itag(698):
            merge_audio_video(self.title, '720p', 'mp4', download_nonprogressive(self.stream, 698, 140, 'mp4', self.temp_dir), self.captions, chosen_caption)
        elif self.stream.get_by_itag(298):
            merge_audio_video(self.title, '720p', 'mp4', download_nonprogressive(self.stream, 298, 140, 'mp4', self.temp_dir), self.captions, chosen_caption)
        elif self.stream.get_by_itag(136):
            merge_audio_video(self.title, '720p', 'mp4', download_nonprogressive(self.stream, 136, 140, 'mp4', self.temp_dir), self.captions, chosen_caption)

def main():
    downloader = YouTubeDownloader()
    
    parser = argparse.ArgumentParser(description=f'PytubePP (Pytube Post Processor) v{downloader.version} - A Simple CLI Tool to Download Your Favorite YouTube Videos Effortlessly!')
    parser.add_argument('url', nargs='?', default=None, help='url of the youtube video')
    parser.add_argument('-df', '--download-folder', default=argparse.SUPPRESS, help='set custom download folder path (default: ~/Downloads/Pytube Downloads) [arg eg: "/path/to/folder"]')
    parser.add_argument('-ds', '--default-stream', default=argparse.SUPPRESS, help='set default download stream (default: max) [available arguments: 144p, 240p, 360p, 480p, 720p, 1080p, 1440p, 2160p, 4320p, mp3, max]')
    parser.add_argument('-dc', '--default-caption', default=argparse.SUPPRESS, help='set default caption (default: none) [available arguments: all language codes, none]')
    parser.add_argument('-s', '--stream', default=argparse.SUPPRESS, help='choose download stream for the current video (default: your chosen --default-stream) [available arguments: 144p, 240p, 360p, 480p, 720p, 1080p, 1440p, 2160p, 4320p, 144, 240, 360, 480, 720, 1080, 1440, 2160, 4320, mp3, hd, fhd, 2k, 4k, 8k]')
    parser.add_argument('-c', '--caption', default=argparse.SUPPRESS, help='choose caption to embed for the current video (default: none)')
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
        if not is_valid_url(args.url):
            print('\nInvalid video link! Please enter a valid video url...!!')
            sys.exit()
            
        # Handle warning messages for ignored flags
        if hasattr(args, 'download_folder'):
            print('\nVideo url supplied! igonering -df flag...!!')
        if hasattr(args, 'default_stream'):
            print('\nVideo url supplied! ignoreing -ds flag...!!')
        if hasattr(args, 'default_caption'):
            print('\nVideo url supplied! ignoreing -dc flag...!!')
        if args.reset_default:
            print('\nVideo url supplied! ignoreing -r flag...!!')
        if args.clear_temp:
            print('\nVideo url supplied! ignoreing -ct flag...!!')
        if args.show_config:
            print('\nVideo url supplied! ignoreing -sc flag...!!')

        # Handle info display flags
        if args.show_info:
            downloader.show_video_info(args.url)
        if args.raw_info:
            downloader.show_raw_info(args.url, args.json_prettify)
        if args.json_prettify and not args.raw_info:
            print('\nMissing flag! -jp flag must be used with a flag which returns json data...!! (eg: -ri)')
        
        # Handle download cases
        if hasattr(args, 'stream') and hasattr(args, 'caption'):
            if downloader.set_video_info(args.url):
                if args.caption not in downloader.captions.keys():
                    print('\nInvalid caption code or caption not available! Please choose a different caption...!! (use -i to see available captions)')
                    sys.exit()
                elif args.stream == 'mp3' and downloader.stream.get_by_itag(140):
                    print(f'\nYou have chosen to download mp3 stream! ( Captioning audio files is not supported )')
                    answer = input('Do you still want to continue downloading ? [yes/no]\n')
                    while answer not in ['yes', 'y', 'no', 'n']:
                        print('Invalid answer! try again...!! answer with: [yes/y/no/n]')
                        answer = input('Do you still want to continue downloading ? [yes/no]\n')
                    if answer in ['yes', 'y']:
                        downloader.download_stream(args.url, args.stream)
                    else:
                        print('Download cancelled! exiting...!!')
                else:
                    downloader.download_stream(args.url, args.stream, args.caption)
        elif hasattr(args, 'stream'):
            if downloader.set_video_info(args.url):
                if downloader.default_caption == 'none':
                    downloader.download_stream(args.url, args.stream)
                elif args.stream == 'mp3' and downloader.stream.get_by_itag(140):
                        print(f'\nYou have chosen to download mp3 stream! ( Captioning audio files is not supported )')
                        answer = input('Do you still want to continue downloading ? [yes/no]\n')
                        while answer not in ['yes', 'y', 'no', 'n']:
                            print('Invalid answer! try again...!! answer with: [yes/y/no/n]')
                            answer = input('Do you still want to continue downloading ? [yes/no]\n')
                        if answer in ['yes', 'y']:
                            downloader.download_stream(args.url, args.stream)
                        else:
                            print('Download cancelled! exiting...!!')
                elif downloader.default_caption in downloader.captions.keys():
                    downloader.download_stream(args.url, args.stream, downloader.default_caption)
                else:
                    print(f'\nDefault caption not available! ( Default: {downloader.default_caption} | Available: {[caption.code for caption in downloader.captions.keys()] or "Nothing"} )')
                    answer = input('Do you still want to continue downloading without caption? [yes/no]\n')
                    while answer not in ['yes', 'y', 'no', 'n']:
                        print('Invalid answer! try again...!! answer with: [yes/y/no/n]')
                        answer = input('Do you still want to continue downloading without caption? [yes/no]\n')
                    if answer in ['yes', 'y']:
                        downloader.download_stream(args.url, args.stream)
                    else:
                        print('Download cancelled! exiting...!!')
        elif hasattr(args, 'caption'):
            if downloader.set_video_info(args.url):
                if args.caption not in downloader.captions.keys():
                    print('\nInvalid caption code or caption not available! Please choose a different caption...!! (use -i to see available captions)')
                    sys.exit()
                elif downloader.default_stream == 'max' and downloader.maxres:
                    downloader.download_stream(args.url, downloader.maxres, args.caption)
                elif downloader.default_stream == 'mp3' and downloader.stream.get_by_itag(140):
                        print(f'\nDefault stream set to mp3! ( Captioning audio files is not supported )')
                        answer = input('Do you still want to continue downloading ? [yes/no]\n')
                        while answer not in ['yes', 'y', 'no', 'n']:
                            print('Invalid answer! try again...!! answer with: [yes/y/no/n]')
                            answer = input('Do you still want to continue downloading ? [yes/no]\n')
                        if answer in ['yes', 'y']:
                            downloader.download_stream(args.url, downloader.default_stream)
                        else:
                            print('Download cancelled! exiting...!!')
                elif downloader.default_stream != 'max' and downloader.stream.filter(res=downloader.default_stream):
                    downloader.download_stream(args.url, downloader.default_stream, args.caption)
                else:
                    if downloader.maxres:
                        print(f'\nDefault stream not available! ( Default: {downloader.default_stream} | Available: {downloader.maxres} )')
                        answer = input('Do you want to download the maximum available stream ? [yes/no]\n')
                        while answer not in ['yes', 'y', 'no', 'n']:
                            print('Invalid answer! try again...!! answer with: [yes/y/no/n]')
                            answer = input('Do you want to download the maximum available stream ? [yes/no]\n')
                        if answer in ['yes', 'y']:
                            downloader.download_stream(args.url, downloader.maxres, args.caption)
                        else:
                            print('Download cancelled! exiting...!!')
                    else:
                        print('Sorry, No downloadable video stream found....!!!')
        elif not any([args.show_info, args.raw_info, args.json_prettify]):  # If no info flags are set
            if downloader.set_video_info(args.url):
                if downloader.default_stream == 'max' and downloader.maxres:
                    if downloader.default_caption == 'none':
                        downloader.download_stream(args.url, downloader.maxres)
                    elif downloader.default_caption in downloader.captions.keys():
                        downloader.download_stream(args.url, downloader.maxres, downloader.default_caption)
                    else:
                        print(f'\nDefault caption not available! ( Default: {downloader.default_caption} | Available: {[caption.code for caption in downloader.captions.keys()] or "Nothing"} )')
                        answer = input('Do you still want to continue downloading without caption? [yes/no]\n')
                        while answer not in ['yes', 'y', 'no', 'n']:
                            print('Invalid answer! try again...!! answer with: [yes/y/no/n]')
                            answer = input('Do you still want to continue downloading without caption? [yes/no]\n')
                        if answer in ['yes', 'y']:
                            downloader.download_stream(args.url, downloader.maxres)
                        else:
                            print('Download cancelled! exiting...!!')
                elif (downloader.default_stream == 'mp3' and downloader.stream.get_by_itag(140)) or (downloader.default_stream != 'max' and downloader.stream.filter(res=downloader.default_stream)):
                    if downloader.default_caption == 'none':
                        downloader.download_stream(args.url, downloader.default_stream)
                    elif downloader.default_stream == 'mp3' and downloader.stream.get_by_itag(140):
                        print(f'\nDefault stream set to mp3! ( Captioning audio files is not supported )')
                        answer = input('Do you still want to continue downloading ? [yes/no]\n')
                        while answer not in ['yes', 'y', 'no', 'n']:
                            print('Invalid answer! try again...!! answer with: [yes/y/no/n]')
                            answer = input('Do you still want to continue downloading ? [yes/no]\n')
                        if answer in ['yes', 'y']:
                            downloader.download_stream(args.url, downloader.default_stream)
                        else:
                            print('Download cancelled! exiting...!!')
                    elif downloader.default_caption in downloader.captions.keys():
                        downloader.download_stream(args.url, downloader.default_stream, downloader.default_caption)
                    else:
                        print(f'\nDefault caption not available! ( Default: {downloader.default_caption} | Available: {[caption.code for caption in downloader.captions.keys()] or "Nothing"} )')
                        answer = input('Do you still want to continue downloading without caption? [yes/no]\n')
                        while answer not in ['yes', 'y', 'no', 'n']:
                            print('Invalid answer! try again...!! answer with: [yes/y/no/n]')
                            answer = input('Do you still want to continue downloading without caption? [yes/no]\n')
                        if answer in ['yes', 'y']:
                            downloader.download_stream(args.url, downloader.default_stream)
                        else:
                            print('Download cancelled! exiting...!!')
                else:
                    if downloader.maxres:
                        print(f'\nDefault stream not available! ( Default: {downloader.default_stream} | Available: {downloader.maxres} )')
                        answer = input('Do you want to download the maximum available stream ? [yes/no]\n')
                        while answer not in ['yes', 'y', 'no', 'n']:
                            print('Invalid answer! try again...!! answer with: [yes/y/no/n]')
                            answer = input('Do you want to download the maximum available stream ? [yes/no]\n')
                        if answer in ['yes', 'y']:
                            if downloader.default_caption == 'none':
                                downloader.download_stream(args.url, downloader.maxres)
                            elif downloader.default_caption in downloader.captions.keys():
                                downloader.download_stream(args.url, downloader.maxres, downloader.default_caption)
                            else:
                                print(f'\nDefault caption not available! ( Default: {downloader.default_caption} | Available: {[caption.code for caption in downloader.captions.keys()] or "Nothing"} )')
                                answer = input('Do you still want to continue downloading without caption? [yes/no]\n')
                                while answer not in ['yes', 'y', 'no', 'n']:
                                    print('Invalid answer! try again...!! answer with: [yes/y/no/n]')
                                    answer = input('Do you still want to continue downloading without caption? [yes/no]\n')
                                if answer in ['yes', 'y']:
                                    downloader.download_stream(args.url, downloader.maxres)
                                else:
                                    print('Download cancelled! exiting...!!')
                    else:
                        print('Sorry, No downloadable video stream found....!!!')
    else:
        if hasattr(args, 'download_folder'):
            if args.download_folder != downloader.download_dir:
                if os.path.isdir(args.download_folder):
                    update_config('downloadDIR', args.download_folder)
                    os.makedirs(args.download_folder, exist_ok=True)
                    print(f'\nDownload folder updated to: {args.download_folder}')
                else:
                    print('\nInvalid download folder path! Please enter a valid path...!!')
            else:
                print('\nDownload folder path is the same! Not updating...!!')

        if hasattr(args, 'default_stream'):
            if args.default_stream != downloader.default_stream:
                if args.default_stream in ['144p', '240p', '360p', '480p', '720p', '1080p', '1440p', '2160p', '4320p', 'mp3', 'max']:
                    update_config('defaultStream', args.default_stream)
                    print(f'\nDefault stream updated to: {args.default_stream}')
                else:
                    print('\nInvalid default stream! Please enter a valid stream...!! (use -h to see available default_stream arguments)')
            else:
                print('\nDefault stream is the same! Not updating...!!')
        
        if hasattr(args, 'default_caption'):
            if args.default_caption != downloader.default_caption:
                if not all(c.isalpha() or c in '.-' for c in args.default_caption) or len(args.default_caption) > 10:
                    print('\nInvalid caption code! Only a-z, A-Z, dash (-) and dot (.) are allowed with maximum 10 characters...!!')
                else:
                    update_config('defaultCaption', args.default_caption)
                    print(f'\nDefault caption updated to: {args.default_caption}')
            else:
                print('\nDefault caption is the same! Not updating...!!')
        
        if args.reset_default:
            reset_config()
        
        if args.clear_temp:
            clear_temp_files()

        if args.show_config:
            print(f'\ntempDIR: {downloader.temp_dir} (Unchangeable) \nconfigDIR: {downloader.config_dir} (Unchangeable)\ndownloadDIR: {downloader.download_dir}\ndefaultStream: {downloader.default_stream}\ndefaultCaption: {downloader.default_caption}\n')

        if args.version:
            print(f'pytubepp {downloader.version}')

        if args.show_info:
            print('\nNo video url supplied! exiting...!!')

        if args.raw_info:
            print('\nNo video url supplied! exiting...!!')

        if args.json_prettify and not args.raw_info:
            print('\nMissing flag! -jp flag must be used with a flag which returns json data...!! (eg: -ri)')

        if hasattr(args, 'stream'):
            print('\nNo video url supplied! exiting...!!')

if __name__ == "__main__":
    main()
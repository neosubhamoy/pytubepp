from .config import get_temporary_directory, load_config, update_config, reset_config
from .utils import get_version, clear_temp_files
from .video import set_global_video_info, show_video_info, show_raw_info, download_stream
import appdirs, os, sys, argparse

global stream, maxres
userConfig = load_config()
downloadDIR = userConfig['downloadDIR']
tempDIR = get_temporary_directory()
configDIR = appdirs.user_config_dir('pytubepp')
defaultStream = userConfig['defaultStream']
version = get_version()
        
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
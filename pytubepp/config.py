import os, json, platform, appdirs, tempfile

def get_download_folder():
    system = platform.system()
    if system in ["Windows", "Darwin", "Linux"]:
        cli_download_dir = os.path.join(os.path.expanduser("~"), "Downloads", "PytubePP Downloads")
        os.makedirs(cli_download_dir, exist_ok=True)
        return cli_download_dir
    else:
        cli_download_dir = os.path.join(appdirs.user_download_dir(), "PytubePP Downloads")
        os.makedirs(cli_download_dir, exist_ok=True)
        return cli_download_dir
    
DEFAULT_CONFIG = {
    'downloadDIR': get_download_folder(),
    'defaultStream': 'max',
    'defaultCaption': 'none',
}
    
def get_temporary_directory():
    temp_dir = tempfile.gettempdir()
    cli_temp_dir = os.path.join(temp_dir, 'pytubepp')
    os.makedirs(cli_temp_dir, exist_ok=True)
    return cli_temp_dir

def load_config():
    config_dir = appdirs.user_config_dir('pytubepp')
    config_path = os.path.join(config_dir, 'config.json')
    if os.path.exists(config_path):
        with open(config_path, 'r') as f:
            return json.load(f)
    else:
        return DEFAULT_CONFIG

def save_config(config):
    config_dir = appdirs.user_config_dir('pytubepp')
    os.makedirs(config_dir, exist_ok=True)
    config_path = os.path.join(config_dir, 'config.json')
    with open(config_path, 'w') as f:
        json.dump(config, f, indent=4)

def update_config(key, value):
    config = load_config()
    config[key] = value
    save_config(config)

def reset_config():
    config_dir = appdirs.user_config_dir('pytubepp')
    config_path = os.path.join(config_dir, 'config.json')
    if os.path.exists(config_path):
        os.remove(config_path)
        print('\nConfig reset successful!')
    else:
        print('\nAlready using the default configs! Not resetting...!')
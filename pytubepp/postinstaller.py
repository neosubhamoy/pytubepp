from .utils import ffmpeg_installed, nodejs_installed
import subprocess, platform

def postinstall():
    os_type = platform.system().lower()
    package_manager = None

    print("### PytubePP Post-Install Script ###\n")

    print("Checking requirements...")
    ffmpeg_needed = not ffmpeg_installed()
    nodejs_needed = not nodejs_installed()

    if ffmpeg_needed or nodejs_needed:
        if os_type == 'windows':
            version_info = platform.version().split('.')
            if int(version_info[0]) >= 10 and (int(version_info[1]) > 0 or int(version_info[2]) >= 1709):
                winget_check = subprocess.run(['winget', '--version'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                if winget_check.returncode == 0:
                    print("OS: Windows (winget)")
                    package_manager = 'winget'  # Windows Package Manager
                else:
                    print("OS: Windows (winget not enabled)")
                    user_input = input("WinGet is not available. Do you want to enable winget? (Make sure to login to Windows before enabling) [Yes/no]: ").strip().lower()
                    if user_input in ['yes', 'y', '']:
                        print("Enabling winget...")
                        subprocess.run(['powershell', '-Command', 'Add-AppxPackage -RegisterByFamilyName -MainPackage Microsoft.DesktopAppInstaller_8wekyb3d8bbwe'])
                        print("WinGet enabled successfully! Please restart your computer and re-run the post install script: pytubepp --postinstall")
                        return
                    else:
                        print("Installation aborted! exiting...!!")
                        return
            else:
                print("OS: Windows (winget not supported)")
                print("Unsupported Windows version! WinGet requires Windows 10 1709 (build 16299) or later, Please install dependencies manually...!!")
                return
        elif os_type == 'linux':
            # Determine the Linux distribution
            if subprocess.run(['command', '-v', 'apt'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL).returncode == 0:
                print("OS: Linux (apt)")
                package_manager = 'apt'  # APT for Debian/Ubuntu
            elif subprocess.run(['command', '-v', 'dnf'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL).returncode == 0:
                print("OS: Linux (dnf)")
                distro_id = subprocess.run(['grep', '^ID=', '/etc/os-release'], stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
                if distro_id.returncode == 0 and 'fedora' in distro_id.stdout.decode().strip() and ffmpeg_needed:
                    user_input = input("Looks like you are using Fedora. Do you want to enable RPM Fusion free and nonfree repositories? (answer no if already enabled) [Yes/no]: ").strip().lower()
                    if user_input in ['yes', 'y', '']:
                        print("Enabling RPM Fusion repositories...")
                        fedora_version = subprocess.run(['rpm', '-E', '%fedora'], stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
                        if fedora_version.returncode == 0:
                            fedora_version_str = fedora_version.stdout.decode().strip()
                            subprocess.run(['sudo', 'dnf', 'install', f'https://download1.rpmfusion.org/free/fedora/rpmfusion-free-release-{fedora_version_str}.noarch.rpm', '-y'], check=True)
                            subprocess.run(['sudo', 'dnf', 'install', f'https://download1.rpmfusion.org/nonfree/fedora/rpmfusion-nonfree-release-{fedora_version_str}.noarch.rpm', '-y'], check=True)
                        else:
                            print("Failed to retrieve Fedora version. Please install RPM Fusion repositories manually.")
                    else:
                        print("RPM Fusion repositories installation skipped...!!")
                package_manager = 'dnf'  # DNF for Fedora
            elif subprocess.run(['command', '-v', 'pacman'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL).returncode == 0:
                print("OS: Linux (pacman)")
                package_manager = 'pacman'  # Pacman for Arch Linux
            else:
                print("OS: Linux (unknown)")
                print("Unsupported Linux distribution! Please install dependencies manually...!!")
                return
        elif os_type == 'darwin':
            homebrew_check = subprocess.run(['brew', '--version'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            if homebrew_check.returncode == 0:
                print("OS: MacOS (brew)")
                package_manager = 'brew'  # Homebrew for macOS
            else:
                print("OS: MacOS (brew not installed)")
                user_input = input("Homebrew is not installed. Do you want to install Homebrew? [Yes/no]: ").strip().lower()
                if user_input in ['yes', 'y', '']:
                    print("Installing Homebrew...")
                    subprocess.run('/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"', shell=True)
                    print("Homebrew installation completed! Please restart your mac and re-run the post install script: pytubepp --postinstall")
                    return
                else:
                    print("Installation aborted! exiting...!!")
                    return
        else:
            print("Unsupported OS! Please install dependencies manually...!!")
            return

        print("The following packages are about to be installed:")
        if ffmpeg_needed:
            print("- FFmpeg")
        if nodejs_needed:
            print("- Node.js")
        
        user_input = input("Do you want to proceed with the installation? [Yes/no]: ").strip().lower()
        if user_input not in ['yes', 'y', '']:
            print("Installation aborted! exiting...!!")
            return

        if ffmpeg_needed:
            print("Installing FFmpeg...")
            install_ffmpeg(package_manager)
        if nodejs_needed:
            print("Installing Node.js...")
            install_nodejs(package_manager)
    else:
        print("Dependencies already satisfied! exiting...!!")

def install_ffmpeg(package_manager):
    if package_manager == 'winget':
        subprocess.run(['winget', 'install', 'ffmpeg'], check=True)
    elif package_manager == 'apt':
        subprocess.run(['sudo', 'apt', 'install', 'ffmpeg', '-y'], check=True)
    elif package_manager == 'dnf':
        subprocess.run(['sudo', 'dnf', 'install', 'ffmpeg', '-y'], check=True)
    elif package_manager == 'pacman':
        subprocess.run(['sudo', 'pacman', '-S', 'ffmpeg', '--noconfirm'], check=True)
    elif package_manager == 'brew':
        subprocess.run(['brew', 'install', 'ffmpeg'], check=True)
    print("FFmpeg installation completed")

def install_nodejs(package_manager):
    if package_manager == 'winget':
        subprocess.run(['winget', 'install', 'OpenJS.NodeJS.LTS'], check=True)
    elif package_manager == 'apt':
        subprocess.run(['sudo', 'apt', 'install', 'nodejs', '-y'], check=True)
    elif package_manager == 'dnf':
        subprocess.run(['sudo', 'dnf', 'install', 'nodejs', '-y'], check=True)
    elif package_manager == 'pacman':
        subprocess.run(['sudo', 'pacman', '-S', 'nodejs-lts-iron', 'npm', '--noconfirm'], check=True)
    elif package_manager == 'brew':
        subprocess.run(['brew', 'install', 'node'], check=True)
    print("Node.js installation completed")
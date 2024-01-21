import requests, gdown, zipfile, os, ctypes, tempfile, shutil, subprocess
from tkinter import messagebox

install_path = "C:\\Program Files (x86)\\Keychron"

def get_installed_version():
    try:
        with open(install_path + "\\config.xml") as f:
            installed_version = f.read().split('<software caption="Keychron" version="')[1].split('"')[0]
        return installed_version
    except Exception as e:
        messagebox.showerror("Error", f"Failed to get installed version: {e}")

def get_online_version_and_url():
    try:
        download_site = requests.get("https://www.keychron.com/pages/learn-more-how-to-use-keychron-mouse-software").text
        download_id = download_site.split('drive.google.com/file/d/')[1].split('/')[0].strip()
        download_url = f"https://drive.google.com/uc?id={download_id}"

        online_version = download_site.splitlines()
        for line in online_version:
            if "Version" in line and "updated on" in line:
                online_version = line.split('Version ')[1].split(' ')[0].strip()
                break

        return online_version, download_url
    except Exception as e:
        messagebox.showerror("Error", f"Failed to get online version and url: {e}")

def download_and_extract_file(download_url, tmp_path):
    try:
        gdown.download(download_url, tmp_path + '\\Keychron.zip', quiet=True)
        with zipfile.ZipFile(tmp_path + '\\Keychron.zip', 'r') as zip_ref:
            zip_ref.extractall(tmp_path)
    except Exception as e:
        messagebox.showerror("Error", f"Failed to download and extract file: {e}")

def run_exe(tmp_path):
    try:
        for root, dirs, files in os.walk(tmp_path):
            for file in files:
                if file.endswith(".exe"):
                    process = subprocess.Popen([os.path.join(root, file)], shell=True)
                    process.wait()
    except Exception as e:
        messagebox.showerror("Error", f"Failed to run exe: {e}")

def main():
    try:
        installed_version = get_installed_version()
        online_version, download_url = get_online_version_and_url()

        if installed_version != online_version:
            MessageBox = ctypes.windll.user32.MessageBoxW
            result = MessageBox(None, f'Version {online_version} of the Keychron software is available. Do you want to download it?', 'New version available', 1)
            if result == 1:
                tmp_path = tempfile.mkdtemp()
                download_and_extract_file(download_url, tmp_path)
                run_exe(tmp_path)
                shutil.rmtree(tmp_path)
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

if __name__ == "__main__":
    main()
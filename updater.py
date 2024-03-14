import requests, gdown, zipfile, os, tempfile, shutil, subprocess, sys, json, logging, webbrowser
from tkinter import messagebox, filedialog


def terminate():
    logger.error("Terminating the program")
    sys.exit()


def get_appdata_path():
    appdata_path = os.getenv("APPDATA")
    folder_path = os.path.join(appdata_path, "Keychron mice updater")

    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    return folder_path


def setup_logger():
    log_file_path = os.path.join(get_appdata_path(), "updater.log")

    logging.basicConfig(
        filename=log_file_path,
        format="%(asctime)s - %(levelname)s - %(filename)s - %(funcName)s - %(lineno)d - %(message)s",
        level=logging.INFO,
        encoding="utf-8",
    )

    logger = logging.getLogger(__name__)
    return logger


logger = setup_logger()


def own_update_manager():
    try:
        online_GH_version = float(
            requests.get(
                "https://api.github.com/repos/Pyenb/Keychron_mice_software_updater/releases/latest"
            )
            .json()["tag_name"]
            .replace("v", "")
        )
        if online_GH_version > VERSION:
            logger.info("New version of the updater available")
            result = messagebox.askquestion(
                "New updater version available",
                f"Version {online_GH_version} of the updater is available. Do you want to check it out?",
            )
            if result == "yes":
                logger.info("User selected to update the updater")
                webbrowser.open(
                    "https://github.com/Pyenb/Keychron_mice_software_updater/releases/latest"
                )
            else:
                logger.info("User selected not to update the updater")
    except Exception as e:
        logging.error(f"Failed to check for new updater version: {e}")


def config_manager():
    config_file = os.path.join(get_appdata_path(), "config.json")

    if os.path.exists(config_file):
        with open(config_file, "r") as f:
            install_path = json.load(f)["install_path"]
            if os.path.exists(os.path.join(install_path, "config.xml")):
                return install_path
            else:
                logger.warning(f"config.xml not found in {install_path}")

    install_path = get_install_path()
    with open(config_file, "w") as f:
        json.dump({"install_path": install_path}, f)
        logger.info("install_path written to config.json")

    return install_path


def get_install_path():
    default_path = r"C:\Program Files (x86)\Keychron"
    if not os.path.exists(os.path.join(default_path, "config.xml")):
        logger.warning(
            f"Keychron software is not installed in the default location: {default_path}"
        )
        messagebox.showerror(
            "Error",
            f"Keychron software is not installed in the default location: {default_path}",
        )
        messagebox.showinfo(
            "Info", "Please select the Keychron software installation folder"
        )
        install_path = filedialog.askdirectory().replace("/", "\\")
        logger.info(f"User selected installation folder: {install_path}")
        return install_path
    return default_path


def get_installed_version(install_path):
    try:
        with open(install_path + "\\config.xml") as f:
            installed_version = (
                f.read()
                .split('<software caption="Keychron" version="')[1]
                .split('"')[0]
            )
            logger.info(f"Installed version found: {installed_version}")
        return installed_version
    except Exception as e:
        logger.error(f"Failed to get installed version: {e}")
        messagebox.showerror("Error", f"Failed to get installed version: {e}")
        terminate()


def get_online_version_and_url():
    try:
        download_site = requests.get(
            "https://www.keychron.com/pages/learn-more-how-to-use-keychron-mouse-software"
        ).text
        download_id = (
            download_site.split("drive.google.com/file/d/")[1].split("/")[0].strip()
        )
        download_url = f"https://drive.google.com/uc?id={download_id}"
        logging.info(f"Download url obtained: {download_url}")

        online_version = download_site.splitlines()
        for line in online_version:
            if "Version" in line and "updated on" in line:
                online_version = line.split("Version ")[1].split(" ")[0].strip()
                logging.info(f"Online version obtained: {online_version}")
                break

        return online_version, download_url
    except requests.exceptions.RequestException as e:
        logging.error(f"Couldn't connect to the internet: {e}")
        terminate()
    except Exception as e:
        logging.error(f"Failed to get online version and url: {e}")
        messagebox.showerror("Error", f"Failed to get online version and url: {e}")
        terminate()


def download_and_extract_file(download_url, tmp_path):
    try:
        gdown.download(download_url, tmp_path + "\\Keychron.zip", quiet=True)
        with zipfile.ZipFile(tmp_path + "\\Keychron.zip", "r") as zip_ref:
            zip_ref.extractall(tmp_path)
    except Exception as e:
        logging.error(f"Failed to download and extract file: {e}")
        messagebox.showerror("Error", f"Failed to download and extract file: {e}")
        terminate()


def run_exe(tmp_path):
    try:
        for root, dirs, files in os.walk(tmp_path):
            for file in files:
                if file.endswith(".exe"):
                    process = subprocess.Popen([os.path.join(root, file)], shell=True)
                    process.wait()
    except Exception as e:
        logger.error(f"Failed to run exe: {e}")
        messagebox.showerror("Error", f"Failed to run exe: {e}")
        terminate()


def main():
    logger.info("Starting the updater")
    install_path = config_manager()
    try:
        installed_version = get_installed_version(install_path)
        online_version, download_url = get_online_version_and_url()

        if installed_version != online_version:
            logger.info("Update available")
            result = messagebox.askquestion(
                "New version available",
                f"Version {online_version} of the Keychron software is available. Do you want to download it?",
            )
            if result == "yes":
                logger.info("User selected to update the software")
                tmp_path = tempfile.mkdtemp()
                download_and_extract_file(download_url, tmp_path)
                run_exe(tmp_path)
                shutil.rmtree(tmp_path)
            else:
                logger.info("User selected not to update the software")
        else:
            logger.info("No update available")
    except Exception as e:
        logging.error(f"An error occurred in main function: {e}")
        messagebox.showerror("Error", f"An error occurred in main function: {e}")
        terminate()
    logger.info("Updater finished")


if __name__ == "__main__":
    VERSION = 1.4
    own_update_manager()
    main()

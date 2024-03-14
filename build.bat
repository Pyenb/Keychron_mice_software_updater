pyinstaller --onefile --noconsole -n "Keychron mice updater" -i images/logo.ico --paths=.venv\Lib\site-packages --upx-dir=upx/ updater.py

"C:\Program Files (x86)\Inno Setup 6\ISCC.exe" innosetup/setup.iss

powershell.exe -nologo -noprofile -command "& { Compress-Archive -Path 'innosetup\Keychron mice updater setup.exe' -DestinationPath 'innosetup\Keychron_mice_updater_setup.zip' }"

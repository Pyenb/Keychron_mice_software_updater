pyinstaller --onefile --noconsole -n "Keychron mice updater" -i images/logo.ico --paths=.venv\Lib\site-packages --upx-dir=upx/ updater.py || exit /b

"C:\Program Files (x86)\Inno Setup 6\ISCC.exe" innosetup/setup.iss || exit /b

powershell.exe -nologo -noprofile -command "& { Compress-Archive -Path 'innosetup\Keychron mice updater setup.exe' -DestinationPath 'innosetup\Keychron_mice_updater_setup.zip' }" || exit /b
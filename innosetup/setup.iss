[Setup]
AppName=Keychron Software Update
AppVersion=1.0
DefaultDirName={commonpf}\Keychron Software Update
DefaultGroupName=Keychron Software Update
UninstallDisplayIcon={app}\keychron.exe
OutputDir=.
OutputBaseFilename=Keychron_updater_setup   
Compression=lzma
SolidCompression=yes

[Files]
Source: "..\dist\Keychron_updater.exe"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{group}\Keychron Software Updater"; Filename: "{app}\Keychron_updater.exe"
Name: "{group}\Uninstall Keychron Software Updater"; Filename: "{uninstallexe}"
Name: "{commonstartup}\Keychron Software Updater"; Filename: "{app}\Keychron_updater.exe"; Tasks: autostart

[Run]
Filename: "{app}\Keychron_updater.exe"; Description: "Launch the application"; Flags: nowait postinstall skipifsilent

[Tasks]
Name: "autostart"; Description: "Start the application when Windows starts"; GroupDescription: "Additional tasks"; Flags: checkedonce
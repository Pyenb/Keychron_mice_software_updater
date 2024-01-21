[Setup]
AppName=Keychron Mice Software Updater
AppVersion=1.0
DefaultDirName={commonpf}\Keychron Mice Software Updater
DefaultGroupName=Keychron Mice Software Updater
UninstallDisplayIcon={app}\keychron.exe
OutputDir=.
OutputBaseFilename=Keychron_mice_updater_setup   
Compression=lzma
SolidCompression=yes

[Files]
Source: "..\dist\Keychron_mice_updater.exe"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{group}\Keychron Mice Software Updater"; Filename: "{app}\Keychron_mice_updater.exe"
Name: "{group}\Uninstall Keychron Mice Software Updater"; Filename: "{uninstallexe}"
Name: "{commonstartup}\Keychron Mice Software Updater"; Filename: "{app}\Keychron_mice_updater.exe"; Tasks: autostart

[Run]
Filename: "{app}\Keychron_mice_updater.exe"; Description: "Launch the application"; Flags: nowait postinstall skipifsilent

[Tasks]
Name: "autostart"; Description: "Start the application when Windows starts"; GroupDescription: "Additional tasks"; Flags: checkedonce
#define AppName "Keychron mice updater"
#define ExeName AppName + ".exe"
#define Version "1.4"
#define AppPublisher "Pyenb"

[Setup]
AppName={#AppName}
AppVersion={#Version}
AppPublisher={#AppPublisher}
DefaultDirName={commonpf}\{#AppName}
DefaultGroupName={#AppName}
UninstallDisplayIcon={app}\{#ExeName}
OutputDir=.
OutputBaseFilename="{#AppName} setup"
Compression=lzma
SolidCompression=yes
SetupIconFile=..\images\logo.ico

[Files]
Source: "..\dist\{#ExeName}"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{group}\{#AppName}"; Filename: "{app}\{#ExeName}"
Name: "{group}\Uninstall {#AppName}"; Filename: "{uninstallexe}"
Name: "{commonstartup}\{#AppName}"; Filename: "{app}\{#ExeName}"; Tasks: autostart

[Run]
Filename: "{app}\{#ExeName}"; Description: "Launch the application"; Flags: nowait postinstall skipifsilent

[Tasks]
Name: "autostart"; Description: "Start the application when Windows starts"; GroupDescription: "Additional tasks"; Flags: checkedonce
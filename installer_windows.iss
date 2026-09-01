; Mitra Theatre — Windows Installer Script
; Build with Inno Setup (https://jrsoftware.org/isinfo.php)
; 1. Install Inno Setup on Windows
; 2. Open this file in the Inno Setup Compiler (or right-click > Compile)
; 3. Output installer .exe appears in the "installer_output" folder
;
; This script expects the PyInstaller onedir build to already exist at:
;   dist\Mitra Theatre\Mitra Theatre.exe

#define MyAppName "Mitra Theatre"
#define MyAppVersion "1.2.10"
#define MyAppPublisher "Özgün Ersin"
#define MyAppExeName "Mitra Theatre.exe"

[Setup]
AppId={{8F3C1A2E-4B7D-4E9A-9C1F-2D6A5B9E7C31}}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher={#MyAppPublisher}
DefaultDirName={autopf}\{#MyAppName}
DefaultGroupName={#MyAppName}
DisableProgramGroupPage=yes
OutputDir=installer_output
OutputBaseFilename=MitraTheatre_Setup
Compression=lzma2
SolidCompression=yes
ArchitecturesInstallIn64BitMode=x64compatible
UninstallDisplayIcon={app}\{#MyAppExeName}
WizardStyle=modern
PrivilegesRequired=admin

; Embeds the EULA into the installer to display it right at the beginning
LicenseFile=EULA.txt

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "Create a &desktop shortcut"; GroupDescription: "Additional shortcuts:"

[Files]
Source: "dist\Mitra Theatre\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs
[Icons]
Name: "{group}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"
Name: "{commondesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; Tasks: desktopicon
Name: "{group}\Uninstall {#MyAppName}"; Filename: "{uninstallexe}"

[Run]
Filename: "{app}\{#MyAppExeName}"; Description: "Launch {#MyAppName}"; Flags: nowait postinstall skipifsilent

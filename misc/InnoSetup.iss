; Script generated by the Inno Setup Script Wizard.
; SEE THE DOCUMENTATION FOR DETAILS ON CREATING INNO SETUP SCRIPT FILES!

#define MyAppName "League Win Predictor"
#define MyAppVersion "1.0.1"
#define MyAppPublisher "Giantpizzahead"
#define MyAppURL "https://github.com/Giantpizzahead/league-win-probability"
#define MyAppExeName "League Win Predictor.exe"

[Setup]
; NOTE: The value of AppId uniquely identifies this application. Do not use the same AppId value in installers for other applications.
; (To generate a new GUID, click Tools | Generate GUID inside the IDE.)
AppId={{0E97BD4B-6B33-49EB-81DD-7E1A8874898B}
AppName={#MyAppName}
AppVersion={#MyAppVersion}                                                                        
;AppVerName={#MyAppName} {#MyAppVersion}
AppPublisher={#MyAppPublisher}
AppPublisherURL={#MyAppURL}
AppSupportURL={#MyAppURL}
AppUpdatesURL={#MyAppURL}
DefaultDirName={autopf}\{#MyAppName}
DisableProgramGroupPage=yes
LicenseFile=C:\Users\sunny\OneDrive\Documents\GitHub\league-win-probability\LICENSE
; Uncomment the following line to run in non administrative install mode (install for current user only.)
;PrivilegesRequired=lowest                                                      
OutputDir=C:\Users\sunny\OneDrive\Documents\GitHub\league-win-probability\dist       
OutputBaseFilename=LeagueWinPredictor
SetupIconFile=C:\Users\sunny\OneDrive\Documents\GitHub\league-win-probability\icon.ico
Compression=lzma
SolidCompression=yes
WizardStyle=modern

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked

[Files]
Source: "C:\Users\sunny\OneDrive\Documents\GitHub\league-win-probability\dist\League Win Predictor\{#MyAppExeName}"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\Users\sunny\OneDrive\Documents\GitHub\league-win-probability\dist\League Win Predictor\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs
; NOTE: Don't use "Flags: ignoreversion" on any shared system files

[Icons]
Name: "{autoprograms}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"
Name: "{autodesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; Tasks: desktopicon

[Run]
Filename: "{app}\{#MyAppExeName}"; Description: "{cm:LaunchProgram,{#StringChange(MyAppName, '&', '&&')}}"; Flags: nowait postinstall skipifsilent


# Building Mitra Theatre — Windows & macOS

This folder has everything needed to turn `presentation_player.py` into:
- **Windows**: `MitraTheatre_Setup.exe` — a normal Windows installer
- **macOS**: `MitraTheatre_Installer.dmg` — a drag-to-Applications installer

**Important:** PyInstaller does not cross-compile. You must run the Windows
build on a Windows machine, and the macOS build on a Mac. There's no way
around this from a single computer — if you don't have both, options are:
a spare/VM machine, a cloud Mac rental (e.g. MacStadium, MacinCloud) for the
Mac side, or a Windows VM (Parallels/VMware) if you're starting from a Mac.

Files in this folder:
```
presentation_player.py       your app
icon.ico                     app icon (Windows / in-app)
icon.icns                    app icon (macOS bundle)
requirements.txt             Python dependencies
mitra_theatre_windows.spec   PyInstaller config for Windows
mitra_theatre_macos.spec     PyInstaller config for macOS
installer_windows.iss        Inno Setup script -> installer .exe
create_dmg.sh                Script -> installer .dmg
```

---

## Windows build

1. Install Python 3.10+ from python.org (check "Add to PATH" during install).
2. Open Command Prompt / PowerShell in this folder and run:
   ```
   python -m venv venv
   venv\Scripts\activate
   pip install -r requirements.txt
   ```
3. Build the app:
   ```
   pyinstaller mitra_theatre_windows.spec
   ```
   This creates `dist\Mitra Theatre\Mitra Theatre.exe` plus its supporting
   files. Test it now — double-click the exe and confirm the app opens.
4. Install [Inno Setup](https://jrsoftware.org/isinfo.php) (free).
5. Open `installer_windows.iss` in the Inno Setup Compiler and click
   **Compile** (or right-click the file → Compile).
6. The finished installer appears at `installer_output\MitraTheatre_Setup.exe`.
   This is the file you hand to end users — they run it, click through the
   wizard, and get a Start Menu + optional desktop shortcut.

**Note on SmartScreen:** since the installer isn't code-signed, Windows will
show an "Unknown Publisher" / SmartScreen warning the first time a user runs
it (they can click "More info" → "Run anyway"). To remove that warning you'd
need a code-signing certificate (~$100–400/year from a CA) — not required to
distribute, just smooths the first-run experience.

---

## macOS build

1. Install Python 3.10+ (via [python.org](https://www.python.org/downloads/macos/)
   or `brew install python`).
2. Open Terminal in this folder and run:
   ```
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```
3. Build the app:
   ```
   pyinstaller mitra_theatre_macos.spec
   ```
   This creates `dist/Mitra Theatre.app`. Test it now — double-click it (or
   `open "dist/Mitra Theatre.app"`) and confirm it launches.
4. Make the DMG script executable and run it:
   ```
   chmod +x create_dmg.sh
   ./create_dmg.sh
   ```
5. You'll get `MitraTheatre_Installer.dmg` in this folder. This is the file
   you hand to end users — they open it and drag the app into the
   Applications shortcut shown in the window.

**Note on Gatekeeper:** since the app isn't signed with an Apple Developer
ID or notarized, macOS will block it the first time with an "unidentified
developer" message. Users work around this via System Settings → Privacy &
Security → "Open Anyway" (or Control-click the app → Open). To remove that
warning entirely you'd need an Apple Developer Program membership ($99/yr)
to sign and notarize the app — optional, only matters for a smoother
first-run experience at scale.

---

## Rebuilding after code changes

Any time you edit `presentation_player.py`, just re-run the relevant
`pyinstaller` command (step 3 above) on that platform, then re-run the
installer step (Inno Setup compile / `create_dmg.sh`).

## Donation link

The control window has a **Donate** button next to **Info**, and the Info
popup also includes a donation link — both point to
`https://kreosus.com/mitratheatre/about` and open in the user's default
browser. To change the URL, update `DONATION_URL` near the top of
`presentation_player.py`.

## Swapping the icon

Replace `icon.ico` (and re-run `icon.icns` generation, or ask me to convert
a new source image) then rebuild. If you want a sharper macOS icon at large
sizes (e.g. Launchpad), provide a 1024×1024 source image — the current
icon.icns was upscaled from a 256×256 source, so it stays crisp up to that
size.

#!/bin/bash
# create_dmg.sh

APP_NAME="Mitra Theatre"
APP_PATH="dist/Mitra Theatre.app"
DMG_NAME="MitraTheatre_Installer.dmg"

if [ ! -d "$APP_PATH" ]; then
  echo "Error: $APP_PATH does not exist. Please run PyInstaller first."
  exit 1
fi

echo "Creating DMG..."
rm -f "$DMG_NAME"
mkdir -p dist/dmg_staging
cp -a "$APP_PATH" dist/dmg_staging/
ln -s /Applications dist/dmg_staging/Applications

cat << 'EOF' > dist/dmg_staging/INSTALL_INSTRUCTIONS.txt
========================================
       MITRA THEATRE INSTALLATION
========================================

1. Drag the "Mitra Theatre" app icon onto the "Applications" folder shortcut.
2. Open your Mac's Applications folder and find "Mitra Theatre".
3. IMPORTANT: The very first time you open the app, DO NOT double-click it. 
   Instead, RIGHT-CLICK (or Control-click) the app and select "Open".
4. A warning will appear saying macOS cannot verify the developer. 
   Simply click the "Open" button in that window.

(If you accidentally double-click it and only see a "Move to Trash" option, just click "Done", then go back and Right-Click -> "Open" instead).

You only need to do this once! After the first launch, macOS remembers it is safe and you can double-click it normally.
EOF

hdiutil create -volname "$APP_NAME" -srcfolder dist/dmg_staging -ov -format UDZO "$DMG_NAME"
rm -rf dist/dmg_staging
echo "Done! Created $DMG_NAME"

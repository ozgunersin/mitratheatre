# -*- mode: python ; coding: utf-8 -*-
# Build on macOS with:  pyinstaller mitra_theatre_macos.spec
import os

APP_NAME = "Mitra Theatre"
HAS_ICO = os.path.exists("icon.ico")     # bundled for the in-app QIcon
HAS_ICNS = os.path.exists("icon.icns")   # used for the .app / Dock icon

block_cipher = None

a = Analysis(
    ['presentation_player.py'],
    pathex=[],
    binaries=[],
    datas=[('icon.ico', '.')] if HAS_ICO else [],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name=APP_NAME,
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name=APP_NAME,
)

app = BUNDLE(
    coll,
    name=f'{APP_NAME}.app',
    icon='icon.icns' if HAS_ICNS else None,
    bundle_identifier='com.ozgunersin.mitratheatre',
    info_plist={
        'NSHighResolutionCapable': True,
        'CFBundleShortVersionString': '1.0.0',
        'CFBundleVersion': '1.0.0',
        'NSHumanReadableCopyright': 'Copyright © 2026 Özgün Ersin. All Rights Reserved.',
    },
)

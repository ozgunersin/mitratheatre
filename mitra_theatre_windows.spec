# -*- mode: python ; coding: utf-8 -*-
# Build on WINDOWS with:  pyinstaller mitra_theatre_windows.spec
import os

APP_NAME = "Mitra Theatre"
HAS_ICON = os.path.exists("icon.ico")

block_cipher = None

a = Analysis(
    ['mitra_theatre.py'],
    pathex=[],
    binaries=[],
    datas=[('icon.ico', '.')] if HAS_ICON else [],
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
    console=False,          # windowed app, no terminal
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='icon.ico' if HAS_ICON else None,
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

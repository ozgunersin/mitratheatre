# -*- mode: python ; coding: utf-8 -*-
import os

block_cipher = None
HAS_ICON = os.path.exists('icon.ico')

a = Analysis(
    ['mitra_theatre.py'],
    pathex=[],
    binaries=[],
    datas=[('EULA.txt', '.'), ('README.md', '.')] + ([('icon.ico', '.')] if HAS_ICON else []),
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='mitra_theatre',
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
    name='Mitra_Theatre',
)

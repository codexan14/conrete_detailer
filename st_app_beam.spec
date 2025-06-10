# -*- mode: python ; coding: utf-8 -*-
<<<<<<< HEAD
=======
from PyInstaller.utils.hooks import collect_all

datas = []
binaries = []
hiddenimports = []
tmp_ret = collect_all('streamlit')
datas += tmp_ret[0]; binaries += tmp_ret[1]; hiddenimports += tmp_ret[2]
>>>>>>> 6d872a8 (feat: Added the GUI with streamlit and the Beam class can now calculate nominal strengths)


a = Analysis(
    ['st_app_beam.py'],
    pathex=[],
<<<<<<< HEAD
    binaries=[],
    datas=[],
    hiddenimports=[],
=======
    binaries=binaries,
    datas=datas,
    hiddenimports=hiddenimports,
>>>>>>> 6d872a8 (feat: Added the GUI with streamlit and the Beam class can now calculate nominal strengths)
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='st_app_beam',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)

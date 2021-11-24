# -*- mode: python ; coding: utf-8 -*-
import configparser

config = configparser.ConfigParser()
config.read('config/config.ini')
version = config["project"]["version"]
block_cipher = pyi_crypto.PyiBlockCipher(key='02EDED85F5F2FE0D--clean')


a = Analysis(['..\\..\\main.py'],
             binaries=[],
             datas=[],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          [],
          name='kawaii_island_v'+version,
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=True , version='file_version_info.txt', icon='icon.ico')

# -*- mode: python ; coding: utf-8 -*-

block_cipher = None


a = Analysis(['main.py'],
             pathex=['C:\\Users\\Slamet S D K\\PycharmProjects\\skripsi_final'],
             binaries=[],
             datas=[('./img/hide.png', './img'),('./img/show.png', './img'),
                    ('./img/icon.png', './img'), ('./img/icon.ico', './img'),
                    ('./data/encode_map.pickle', './data'), ('./data/decode_map.pickle', './data'),
                    ('./data/encode_dict.pickle', './data'), ('./data/decode_dict.pickle', './data'),
                    ('./assets/About.txt', './assets'), ('./assets/Help.txt', './assets')],
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
          name='main',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=False,
          icon='./img/icon.ico')
app = BUNDLE(exe,
             name='text encryption and decryption.app',
             icon='./img/icon.icns',
             bundle_identifier=None)

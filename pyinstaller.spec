# -*- mode: python -*-
block_cipher = None
import os
import pkgutil
import sys

from PyInstaller import __version__ as pyinstaller_version
from PyInstaller.utils.hooks import collect_data_files, collect_submodules

root_dir = os.path.abspath(os.path.dirname(__name__))
src_dir = os.path.join(root_dir, "src")
sys.path.append(src_dir)

version_str=pyinstaller_version

# On macOS, we always show the console to prevent the double-dock bug (although the OS does not actually show the console).
show_console = os.environ.get('SHOW_CONSOLE', 'false') == 'true'
if sys.platform == 'darwin':
    show_console = True

if sys.platform.startswith('darwin'):
    # Create the right version info in the Info.plist file
    with open('build/mac/resources/Info.plist', 'r') as f:
        content = f.read()
        content = content.replace('__VERSION__', version_str)
    os.unlink('build/mac/resources/Info.plist')
    with open('build/mac/resources/Info.plist', 'w') as f:
        f.write(content)

data_to_copy = []
excluded_libs = []
hiddenimports = []
app_name = f'HelloPyInstaller-{version_str}'

a = Analysis(['src/main.py'],
             pathex=[''],
             binaries=None,
             datas=data_to_copy,
             hiddenimports=hiddenimports,
             hookspath=[],
             runtime_hooks=[],
             excludes=excluded_libs,
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)

pyz = PYZ(a.pure, a.zipped_data,
          cipher=block_cipher)

exe = EXE(pyz,
          a.scripts,
          exclude_binaries=True,
          name=app_name,
          debug=False,
          strip=False,
          upx=True,
          console=show_console,
          icon='build/win/resources/tribler.ico')

coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               name=app_name)

app = BUNDLE(coll,
             name='Tribler.app',
             icon='build/mac/resources/tribler.icns',
             bundle_identifier='com.github.pyscanner.pyinstaller',
             info_plist={'CFBundleName': 'Tribler', 'CFBundleDisplayName': 'Tribler', 'NSHighResolutionCapable': 'True',
                         'CFBundleInfoDictionaryVersion': 1.0, 'CFBundleVersion': version_str,
                         'CFBundleShortVersionString': version_str},
             console=show_console)

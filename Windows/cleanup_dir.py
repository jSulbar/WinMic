import os
import shutil

cwd = os.getcwd()
BUILD_DIR = os.path.join(cwd, 'pyinstaller_build', 'dist', 'WinMic')
os.chdir(BUILD_DIR)
if not os.path.exists('lib'):
    os.mkdir('lib')

PRESERVED_FILES = [
    'base_library.zip',
    'WinMic.exe',
    'python38.dll',
    'wx'
]
app_files = os.listdir()

for file in app_files:
    skip = False
    for fname in PRESERVED_FILES:
        if file.startswith(fname):
            skip = True
    if not skip:
        shutil.move(file, 'lib')

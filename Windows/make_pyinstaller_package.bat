@ECHO OFF
TITLE Making exe...
py -m venv venv\
CALL .\venv\Scripts\activate.bat
pip install -r requirements.txt
MKDIR pyinstaller_build
CD pyinstaller_build
pyinstaller ..\main.py --onedir -n WinMic --clean -i ..\winmic.ico --noconsole --noconfirm --runtime-hook ..\hook.py
CD ..
py cleanup_dir.py
deactivate
PAUSE

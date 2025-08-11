@echo off
pyinstaller --onefile server_app/coderdeck.py
pyinstaller --onefile --noconsole setup_app/setup.py
rmdir /s /q build
del /q *.spec
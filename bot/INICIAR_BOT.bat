@echo off
chcp 65001 >nul
echo 🤖 Iniciando KDrama Max Bot...
pip install python-telegram-bot -q
python "%~dp0bot.py"
pause

@ECHO OFF & CHCP 65001

echo "Start Config"
python config/release.py start
echo "Strat Bulid"
pyinstaller config/main.spec

python config/release.py end
echo "Bulid Success"

pause
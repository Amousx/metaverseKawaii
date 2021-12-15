@ECHO OFF & CHCP 65001

echo "Start Config"
python config/release.py start
echo "Start Build"
pyinstaller config/main.spec

python config/release.py end
echo "Build Success"

pause
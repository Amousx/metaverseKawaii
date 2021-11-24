@ECHO OFF & CHCP 65001

echo "【开始打包配置】"
python config/release.py start
echo "【开始打包】"
pyinstaller config/main.spec

python config/release.py end
echo "【打包成功】"

pause
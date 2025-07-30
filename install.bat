@echo off
echo ========================================
echo Zillow自动化机器人 - 依赖安装脚本
echo ========================================
echo.

echo 正在检查Python版本...
python --version
if %errorlevel% neq 0 (
    echo 错误: 未找到Python，请先安装Python 3.7+
    pause
    exit /b 1
)

echo.
echo 正在安装Python依赖库...
echo ----------------------------------------

echo 安装主要依赖: selenium + undetected-chromedriver
pip install selenium undetected-chromedriver

if %errorlevel% neq 0 (
    echo.
    echo 使用国内镜像重试...
    pip install -i https://pypi.tuna.tsinghua.edu.cn/simple selenium undetected-chromedriver
)

echo.
echo ========================================
echo 安装完成！
echo ========================================
echo.
echo 接下来请：
echo 1. 编辑 zillow_undetected_bot.py 文件
echo 2. 修改您的个人信息（姓名、邮箱、电话等）
echo 3. 运行命令: python zillow_undetected_bot.py
echo.
pause 
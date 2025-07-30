# 🏠 Zillow 自动化租房联系机器人

一个功能完善的 Zillow 租房信息自动化处理工具，能够自动登录、搜索房源、填写联系表单并发送租房询问。

## ✨ 功能特性

- 🔐 **自动登录**: 自动填写邮箱，点击继续，只需手动输入密码
- 🏠 **智能房源收集**: 自动滚动页面，收集所有可用房源
- 📝 **智能表单填写**: 根据登录状态自动适应不同表单类型
- 📨 **两步发送流程**: 完整的发送流程，包括弹窗处理
- 🔄 **无限页面处理**: 自动处理多页房源，直到没有更多房源
- 🛡️ **反检测机制**: 使用反检测浏览器避免被识别为机器人
- 📊 **实时统计**: 运行时间、成功率、处理速度等详细统计
- 🔧 **错误恢复**: 网络超时、页面异常等问题的自动恢复
- ⚡ **人性化操作**: 随机延迟模拟真实用户行为

## 📋 项目文件说明

### 📦 完整项目包含的文件
```
Zillow-Bot/
├── zillow_undetected_bot.py    # 🌟 主推荐版本
├── zillow_selenium_bot.py      # 🔄 备用版本  
├── zillow_bot.py               # 🚀 Playwright版本
├── requirements.txt            # 📦 依赖库清单
├── install.bat                 # 🪟 Windows安装脚本
├── install.sh                  # 🍎 macOS/Linux安装脚本
└── README.md                   # 📖 使用说明（本文件）
```

### 🎯 核心文件（必需）

1. **`zillow_undetected_bot.py`** - 🌟 **主推荐版本**
   - 使用反检测Chrome浏览器
   - 功能最完整，稳定性最好
   - 适合大规模使用

2. **`zillow_selenium_bot.py`** - 🔄 **备用版本**
   - 普通Selenium版本
   - 需要手动启动Chrome浏览器
   - 适合调试和小规模使用

3. **`zillow_bot.py`** - 🚀 **Playwright版本**
   - 使用Playwright驱动
   - 现代化的浏览器自动化
   - 需要额外安装Playwright

### 📚 可选文件

4. **`zillow_debug.py`** - 🐛 调试版本
5. **`zillow_pagination_test.py`** - 🧪 分页测试版本

### 🛠️ 辅助文件

6. **`requirements.txt`** - 📦 **依赖库清单**
   - Python项目标准做法，列出所有需要的库
   - 使用方法：`pip install -r requirements.txt`
   - 确保版本一致性，避免兼容性问题

7. **`install.bat`** - 🪟 **Windows自动安装脚本**
   - Windows用户专用，双击即可自动安装所有依赖
   - 自动检查Python版本
   - 安装失败时自动尝试国内镜像
   - 包含中文提示和使用指导

8. **`install.sh`** - 🍎 **macOS/Linux自动安装脚本**
   - macOS和Linux用户专用
   - 运行方法：`chmod +x install.sh && ./install.sh`
   - 自动检查Python3环境
   - 智能处理安装失败情况

9. **`README.md`** - 📖 **详细使用说明**（本文件）

## 🔧 环境要求

### 💻 系统要求
- **操作系统**: Windows 10+, macOS 10.14+, Linux (Ubuntu 18.04+)
- **Python**: 3.7 或更高版本
- **Chrome浏览器**: 最新版本 (主要版本需要)

### 📦 Python库依赖

#### 主要版本依赖
```bash
undetected-chromedriver>=3.5.0
selenium>=4.0.0
```

#### 备用版本额外依赖
```bash
selenium>=4.0.0
```

#### Playwright版本额外依赖
```bash
playwright>=1.30.0
```

## 🚀 安装指南

### 1️⃣ 克隆或下载项目
```bash
# 下载项目文件到本地目录
# 确保包含以下文件：
# - zillow_undetected_bot.py (主要版本)
# - zillow_selenium_bot.py (备用版本)
# - zillow_bot.py (Playwright版本)
# - requirements.txt (依赖清单)
# - install.bat (Windows安装脚本)
# - install.sh (macOS/Linux安装脚本)
# - README.md (本文件)
```

### 2️⃣ 安装Python依赖

#### ⚡ 快速安装 (推荐新手)

**Windows用户**:
```bash
# 直接双击 install.bat 文件
# 或在命令行运行：
install.bat
```

**macOS/Linux用户**:
```bash
# 在终端运行：
./install.sh
```

#### 📦 使用requirements.txt安装
```bash
# 标准Python安装方式
pip install -r requirements.txt

# 使用国内镜像（推荐国内用户）
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
```

#### 🔧 手动安装 (高级用户)

#### 🌟 主要版本安装 (推荐)
```bash
# 安装主要依赖
pip install undetected-chromedriver selenium

# 或者使用国内镜像
pip install -i https://pypi.tuna.tsinghua.edu.cn/simple undetected-chromedriver selenium
```

#### 🔄 备用版本安装
```bash
pip install selenium
```

#### 🚀 Playwright版本安装
```bash
pip install playwright
# 安装浏览器
playwright install chromium
```

### 3️⃣ 安装Chrome浏览器
- 访问 [Google Chrome官网](https://www.google.com/chrome/) 下载安装最新版本
- 确保Chrome浏览器能正常启动

## ⚙️ 配置说明

### 📝 修改个人信息

打开 `zillow_undetected_bot.py` 文件，修改以下配置：

```python
# --- 在这里配置您的信息 ---
YOUR_NAME = "您的姓名"                    # 修改成您的名字
YOUR_EMAIL = "your.email@example.com"     # 修改成您的邮箱
YOUR_PHONE = "1234567890"                 # 修改成您的电话号码，纯数字
YOUR_MESSAGE = "您的默认消息内容..."        # 修改成您想发送的默认信息

# --- 脚本配置 ---
START_URL = "https://www.zillow.com/ca/rentals/"  # 搜索URL，可修改地区
IS_LIVE_MODE = True   # True=真实发送, False=仅模拟
```

### 🎯 重要配置项

- **`YOUR_EMAIL`**: 设置为您的Zillow账户邮箱
- **`IS_LIVE_MODE`**: 
  - `True`: 真实发送联系请求
  - `False`: 仅模拟运行，不发送请求
- **`START_URL`**: 可修改为不同地区的租房搜索页面

## 🖥️ 使用方法

### 🌟 主要版本使用 (推荐)

```bash
# 运行主要版本
python zillow_undetected_bot.py
```

**使用流程**：
1. ✅ 脚本自动启动反检测浏览器
2. ✅ 自动访问Zillow并点击登录
3. ✅ 自动填写邮箱地址并点击Continue
4. 🖱️ **手动输入密码并完成登录**
5. ⌨️ 按Enter键继续
6. ✅ 脚本自动处理所有房源页面

### 🔄 备用版本使用

```bash
# 首先手动启动Chrome浏览器（调试模式）
# Windows:
"C:\Program Files\Google\Chrome\Application\chrome.exe" --remote-debugging-port=9222 --user-data-dir="C:\temp\chrome_debug"

# macOS:
/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome --remote-debugging-port=9222 --user-data-dir="/tmp/chrome_debug"

# Linux:
google-chrome --remote-debugging-port=9222 --user-data-dir="/tmp/chrome_debug"

# 然后运行脚本
python zillow_selenium_bot.py
```

### 🚀 Playwright版本使用

```bash
# 首先启动调试模式的浏览器
# Windows:
"C:\Program Files\Google\Chrome\Application\chrome.exe" --remote-debugging-port=9222

# macOS:
/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome --remote-debugging-port=9222

# 然后运行脚本
python zillow_bot.py
```

## 📊 运行状态说明

### ✅ 正常运行状态
```
📊 阶段性统计 (已处理 10 页, 运行时间: 1小时30分钟):
  总房源数: 300
  成功联系: 285
  成功率: 95.0%
  平均每页房源: 30.0
```

### 🎉 完成时显示
```
🎉 处理完成！
⏱️  总运行时间: 3小时45分钟30秒
📄 总共处理了 25 页
🏠 总共找到 750 个房源
✅ 成功联系 720 个房源
📊 成功率: 96.0%
📈 平均每页房源: 30.0
⚡ 处理速度: 200 房源/小时
```

## ⚠️ 注意事项

### 🔐 账户安全
- 请使用您自己的Zillow账户
- 不要分享账户信息
- 建议使用强密码

### 🚦 使用频率
- 建议合理控制使用频率
- 避免短时间内大量发送请求
- 遵守Zillow服务条款

### 📧 消息内容
- 确保消息内容真实、礼貌
- 避免发送垃圾信息
- 提供真实的联系方式

### 💻 系统资源
- 脚本运行时会占用较多内存
- 建议关闭其他不必要的程序
- 确保网络连接稳定

## 🛠️ 故障排除

### ❌ 常见问题

#### 1. 浏览器启动失败
```
错误: undetected_chromedriver启动失败
```
**解决方案**:
- 确保已安装Chrome浏览器
- 更新Chrome到最新版本
- 重新安装undetected-chromedriver：
  ```bash
  pip uninstall undetected-chromedriver
  pip install undetected-chromedriver
  ```

#### 2. 找不到元素
```
错误: 无法找到登录按钮
```
**解决方案**:
- 检查网络连接
- 等待页面完全加载
- 清除浏览器缓存

#### 3. 网络超时
```
网络超时，跳过此房源: HTTPConnectionPool...
```
**解决方案**:
- 检查网络连接稳定性
- 这是正常情况，脚本会自动跳过并继续

#### 4. 验证码出现
```
检测到验证码，需要手动处理
```
**解决方案**:
- 按提示手动完成验证码
- 按Enter键继续脚本运行

#### 5. 登录失败
```
警告: 无法找到Sign In按钮
```
**解决方案**:
- 手动点击登录按钮
- 按Enter键继续
- 检查网络连接

### 🔧 高级故障排除

#### Python环境问题
```bash
# 检查Python版本
python --version

# 检查已安装的包
pip list | grep selenium
pip list | grep undetected

# 重新安装依赖
pip install --upgrade selenium undetected-chromedriver
```

#### Chrome驱动问题
```bash
# 查看Chrome版本
# 访问: chrome://version/

# 手动下载对应版本的ChromeDriver
# 访问: https://chromedriver.chromium.org/
```

## 📝 更新日志

- **v1.0**: 基础功能实现
- **v2.0**: 添加反检测机制
- **v3.0**: 智能表单检测
- **v4.0**: 两步发送流程
- **v5.0**: 无限页面处理
- **v6.0**: 错误恢复机制

## 📞 技术支持

如果遇到问题：
1. 📖 首先查看本README的故障排除部分
2. 🔍 检查是否为配置问题
3. 🌐 确认网络连接正常
4. 🔄 尝试重启脚本

## 🤝 免责声明

- 本工具仅供学习和个人使用
- 请遵守相关法律法规和服务条款
- 使用者需对使用行为负责
- 开发者不承担任何责任

## 📄 许可证

本项目基于 [MIT License](LICENSE) 开源许可证发布。

### 🔓 MIT License 特点
- ✅ **自由使用**: 可用于个人、学习、商业用途
- ✅ **自由修改**: 可以修改代码并分发
- ✅ **自由分发**: 可以复制、分发原始或修改版本
- ⚠️ **无担保**: 软件按"原样"提供，无任何担保

### 📋 使用条件
使用本软件时，您需要：
- 保留原始的版权声明和许可证文本
- 对使用本软件的行为负责

详细许可证条款请查看 [LICENSE](LICENSE) 文件。
---

**🎯 开始使用**: 推荐从主要版本 `zillow_undetected_bot.py` 开始！ 

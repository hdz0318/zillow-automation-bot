import time
import random
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

# --- 在这里配置您的信息 ---
YOUR_NAME = "John Smith"  # 修改成您的名字
YOUR_EMAIL = "3251758144@qq.com"  # 修改成您的邮箱
YOUR_PHONE = "9097803258"  # 修改成您的电话号码，纯数字
YOUR_MESSAGE = "Hello, I am very interested in this rental property. I would like to know if it's still available and if it would be possible to schedule a tour. Thank you!"  # 修改成您想发送的默认信息

# --- 脚本配置 ---
START_URL = "https://www.zillow.com/ca/rentals/"  # 回到原始URL
IS_LIVE_MODE = True  # 设置为 True 来真实发送请求，设置为 False 则只运行到最后一步，不点击发送按钮
# -------------------------

def create_undetected_browser():
    """
    创建一个反检测的Chrome浏览器
    """
    print("正在启动反检测浏览器...")
    
    # 配置选项
    options = uc.ChromeOptions()
    
    # 添加一些反检测参数
    options.add_argument('--no-first-run')
    options.add_argument('--no-service-autorun')
    options.add_argument('--no-default-browser-check')
    options.add_argument('--disable-blink-features=AutomationControlled')
    
    # 设置用户代理
    options.add_argument('--user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')
    
    # 创建驱动
    driver = uc.Chrome(options=options, version_main=None)
    
    # 执行反检测脚本
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    
    print("反检测浏览器启动成功")
    return driver

def wait_and_find_element(driver, by, value, timeout=10, description="元素"):
    """
    等待并找到元素，如果找不到则抛出异常
    """
    try:
        element = WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located((by, value))
        )
        print(f"找到 {description}!")
        return element
    except TimeoutException:
        print(f"错误: 无法找到 {description}，超时 {timeout} 秒。")
        raise

def check_and_handle_captcha(driver):
    """
    检查并处理验证码
    """
    try:
        print("检查是否存在验证码...")
        time.sleep(random.uniform(2, 3))
        
        # 检查是否有验证码相关的元素
        captcha_indicators = [
            "px-captcha-modal",
            "captcha",
            "challenge",
            "verification"
        ]
        
        found_captcha = False
        for indicator in captcha_indicators:
            try:
                elements = driver.find_elements(By.XPATH, f"//*[contains(@id, '{indicator}') or contains(@class, '{indicator}')]")
                if elements:
                    print(f"发现可能的验证码元素: {indicator}")
                    found_captcha = True
                    break
            except:
                continue
        
        if found_captcha:
            print("检测到验证码，需要手动处理")
            print("请手动完成验证码，然后按Enter继续...")
            input("按Enter键继续...")
            return True
        else:
            print("未检测到验证码")
            return False
            
    except Exception as e:
        print(f"验证码检查时出错: {e}")
        return False

def collect_properties_from_page(driver):
    """收集当前页面的房源链接（使用正确的容器滚动）"""
    print("正在收集当前页面的房源...")
    
    # 等待页面加载
    time.sleep(random.uniform(5, 8))
    
    # 寻找可滚动的房源列表容器
    print("正在寻找可滚动的房源列表容器...")
    scrollable_containers = [
        "#search-page-list-container",  # 从HTML中找到的主要容器
        ".search-page-list-container",  # 类名版本
        "#grid-search-results",  # 网格搜索结果
        ".result-list-container",  # 结果列表容器
    ]
    
    scroll_container = None
    for selector in scrollable_containers:
        try:
            container = driver.find_element(By.CSS_SELECTOR, selector)
            if container:
                # 检查容器是否可滚动
                scroll_height = driver.execute_script("return arguments[0].scrollHeight", container)
                client_height = driver.execute_script("return arguments[0].clientHeight", container)
                if scroll_height > client_height:
                    print(f"找到可滚动容器: {selector}")
                    print(f"  容器滚动高度: {scroll_height}px, 可见高度: {client_height}px")
                    scroll_container = container
                    break
        except:
            continue
    
    if scroll_container:
        # 滚动容器以加载所有房源 - 使用分步滚动
        print("开始分步滚动房源容器...")
        max_scroll_attempts = 4  # 您说4次滚动就够了
        
        for attempt in range(max_scroll_attempts):
            print(f"第 {attempt + 1} 次滚动...")
            
            # 获取当前滚动信息
            current_scroll_top = driver.execute_script("return arguments[0].scrollTop", scroll_container)
            scroll_height = driver.execute_script("return arguments[0].scrollHeight", scroll_container)
            client_height = driver.execute_script("return arguments[0].clientHeight", scroll_container)
            
            print(f"  容器当前滚动位置: {current_scroll_top}px")
            print(f"  容器总高度: {scroll_height}px, 可见高度: {client_height}px")
            
            # 分步滚动容器 - 慢慢滚动，让房源有时间加载
            steps = 5
            scroll_step = (scroll_height - current_scroll_top) // steps
            
            for step in range(steps):
                scroll_to = current_scroll_top + (step + 1) * scroll_step
                print(f"    滚动容器到: {scroll_to}px")
                driver.execute_script("arguments[0].scrollTop = arguments[1]", scroll_container, scroll_to)
                time.sleep(0.8)  # 每步暂停0.8秒，比之前的0.5秒更慢
            
            # 确保滚动到容器底部
            driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", scroll_container)
            print("  容器已滚动到底部")
            
            # 等待内容加载 - 给更多时间让房源加载
            print("  等待新内容加载...")
            time.sleep(random.uniform(3, 5))  # 增加到3-5秒，给更多时间加载
            
            # 检查新的滚动高度和房源数量
            new_scroll_height = driver.execute_script("return arguments[0].scrollHeight", scroll_container)
            current_cards = driver.find_elements(By.CSS_SELECTOR, "a[data-test='property-card-link']")
            print(f"  滚动后: 容器高度 {new_scroll_height}px, 当前房源数: {len(current_cards)}")
            
            # 检查是否已经滚动到底部
            current_scroll_top = driver.execute_script("return arguments[0].scrollTop", scroll_container)
            is_at_bottom = (current_scroll_top + client_height >= new_scroll_height - 50)
            
            if is_at_bottom and len(current_cards) > 9:  # 确保房源数量增加了
                print(f"  已滚动到容器底部，当前房源数: {len(current_cards)}")
                break
            elif len(current_cards) <= 9:
                print(f"  房源数量仍然很少({len(current_cards)}个)，继续滚动...")
            else:
                print(f"  房源数量增加到 {len(current_cards)} 个，继续滚动...")
        
        print("容器滚动完成")
    else:
        print("未找到可滚动容器，使用页面滚动...")
        # 备用方案：页面滚动
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(3)

    # 收集房源链接
    property_links = []
    try:
        property_elements = driver.find_elements(By.CSS_SELECTOR, "a[data-test='property-card-link']")
        print(f"最终找到 {len(property_elements)} 个房源")
        
        for element in property_elements:
            try:
                href = element.get_attribute("href")
                if href and href not in property_links:
                    property_links.append(href)
            except:
                continue
                
        print(f"成功收集到 {len(property_links)} 个有效房源链接")
        return property_links
        
    except Exception as e:
        print(f"收集房源时出错: {e}")
        return []

def fill_contact_form(driver):
    """填写联系表单 - 根据登录状态自动调整"""
    try:
        print("正在填写联系表单...")
        
        # 首先检测表单类型 - 登录后可能只需要填写消息
        print("检测表单类型...")
        
        # 检查是否有登录后的简化消息框
        logged_in_message_selectors = [
            "textarea#message-box",  # 用户提供的登录后消息框ID
            "textarea[data-testid='message-box-input']",  # 用户提供的data-testid
            "textarea.MessageBox__StyledTextarea-sc-80zyh7-0",  # 用户提供的类名
            "textarea[placeholder='Add your message']"  # placeholder文本
        ]
        
        logged_in_message_input = None
        for selector in logged_in_message_selectors:
            try:
                logged_in_message_input = driver.find_element(By.CSS_SELECTOR, selector)
                if logged_in_message_input.is_displayed():
                    print(f"检测到登录后的简化表单，只需填写消息: {selector}")
                    break
            except:
                continue
        
        if logged_in_message_input:
            # 登录后的简化流程 - 只填写消息
            print("使用登录后的简化表单流程...")
            logged_in_message_input.clear()
            time.sleep(random.uniform(0.5, 1.0))
            
            for char in YOUR_MESSAGE:
                logged_in_message_input.send_keys(char)
                time.sleep(random.uniform(0.02, 0.05))
            print(f"消息已填写: {YOUR_MESSAGE[:50]}...")
            
        else:
            # 未登录的完整表单流程
            print("使用完整表单流程...")
            
            # 1. 填写姓名
            print("正在定位姓名输入框...")
            name_selectors = [
                "input#name_modal",  # 用户提供的准确ID
                "input[data-testid='name-input']",  # 用户提供的data-testid
                "input[placeholder='First & last name']",
                "input[name='name']",
                "input[type='text']"
            ]
            
            name_input = None
            for selector in name_selectors:
                try:
                    name_input = driver.find_element(By.CSS_SELECTOR, selector)
                    if name_input.is_displayed():
                        print(f"找到姓名输入框: {selector}")
                        break
                except:
                    continue
            
            if not name_input:
                print("警告: 无法找到姓名输入框，可能是登录后的简化表单")
            else:
                name_input.clear()
                for char in YOUR_NAME:
                    name_input.send_keys(char)
                    time.sleep(random.uniform(0.03, 0.08))
                print(f"姓名已填写: {YOUR_NAME}")
            
            # 2. 填写邮箱
            print("正在定位邮箱输入框...")
            email_selectors = [
                "input[type='email']",
                "input[name='email']",
                "input[placeholder*='email']",
                "input[id*='email']"
            ]
            
            email_input = None
            for selector in email_selectors:
                try:
                    email_input = driver.find_element(By.CSS_SELECTOR, selector)
                    if email_input.is_displayed():
                        print(f"找到邮箱输入框: {selector}")
                        break
                except:
                    continue
            
            if not email_input:
                print("警告: 无法找到邮箱输入框，可能是登录后的简化表单")
            else:
                email_input.clear()
                for char in YOUR_EMAIL:
                    email_input.send_keys(char)
                    time.sleep(random.uniform(0.03, 0.08))
                print(f"邮箱已填写: {YOUR_EMAIL}")
            
            # 3. 填写电话
            print("正在定位电话输入框...")
            phone_selectors = [
                "input[type='tel']",
                "input[name='phone']",
                "input[placeholder*='phone']",
                "input[id*='phone']"
            ]
            
            phone_input = None
            for selector in phone_selectors:
                try:
                    phone_input = driver.find_element(By.CSS_SELECTOR, selector)
                    if phone_input.is_displayed():
                        print(f"找到电话输入框: {selector}")
                        break
                except:
                    continue
            
            if not phone_input:
                print("警告: 无法找到电话输入框，可能是登录后的简化表单")
            else:
                phone_input.clear()
                for char in YOUR_PHONE:
                    phone_input.send_keys(char)
                    time.sleep(random.uniform(0.03, 0.08))
                print(f"电话已填写: {YOUR_PHONE}")
            
            # 4. 填写消息 (完整表单的消息框)
            print("正在定位消息输入框...")
            message_selectors = [
                "textarea",
                "textarea[name='message']",
                "textarea[placeholder*='message']",
                "input[name='message']"
            ]
            
            message_input = None
            for selector in message_selectors:
                try:
                    message_input = driver.find_element(By.CSS_SELECTOR, selector)
                    if message_input.is_displayed():
                        print(f"找到消息输入框: {selector}")
                        break
                except:
                    continue
            
            if not message_input:
                print("错误: 无法找到消息输入框")
                return False
            
            message_input.clear()
            for char in YOUR_MESSAGE:
                message_input.send_keys(char)
                time.sleep(random.uniform(0.02, 0.05))
            print(f"消息已填写: {YOUR_MESSAGE[:50]}...")
        
        print("表单填写完成，等待确认...")
        time.sleep(random.uniform(2, 3))  # 从3-5秒减少到2-3秒
        
        # 5. 寻找并点击发送按钮
        print("正在寻找发送按钮...")
        send_button_selectors = [
            "button[data-testid='rcf-submit-button']",  # 正确的选择器
            "//button[@data-testid='rcf-submit-button']",  # XPath版本
            "//button[contains(text(), 'Send tour request')]",
            "//button[contains(text(), 'Send request')]",
            "//button[contains(text(), 'Send')]",
            "button[type='submit']",
            "input[type='submit']"
        ]
        
        send_button = None
        for selector in send_button_selectors:
            try:
                if selector.startswith("//"):
                    send_button = driver.find_element(By.XPATH, selector)
                else:
                    send_button = driver.find_element(By.CSS_SELECTOR, selector)
                
                if send_button.is_displayed():
                    print(f"找到发送按钮: {selector}")
                    break
            except:
                continue
        
        if not send_button:
            print("错误: 无法找到发送按钮")
            return False
        
        # 等待按钮变为可用状态（移除disabled属性）
        print("等待发送按钮变为可用状态...")
        max_wait_time = 10  # 最多等待10秒
        wait_start = time.time()
        
        while time.time() - wait_start < max_wait_time:
            try:
                # 检查按钮是否仍然disabled
                is_disabled = (
                    send_button.get_attribute("disabled") or 
                    send_button.get_attribute("aria-disabled") == "true"
                )
                
                if not is_disabled and send_button.is_enabled():
                    print("发送按钮已可用!")
                    break
                else:
                    print(f"按钮仍然禁用，继续等待... (已等待 {time.time() - wait_start:.1f}秒)")
                    time.sleep(0.5)
            except:
                time.sleep(0.5)
        else:
            print("警告: 发送按钮可能仍然禁用，但将尝试点击...")
            
            # 检查是否有任何必填字段未填写
            try:
                # 检查是否有错误消息
                error_messages = driver.find_elements(By.CSS_SELECTOR, "[data-testid*='error'], .error, [role='alert']")
                if error_messages:
                    for error in error_messages:
                        if error.is_displayed() and error.text.strip():
                            print(f"发现错误消息: {error.text}")
                            
                # 检查必填字段
                required_fields = driver.find_elements(By.CSS_SELECTOR, "input[required], textarea[required], select[required]")
                empty_required = []
                for field in required_fields:
                    if field.is_displayed() and not field.get_attribute("value").strip():
                        field_name = (
                            field.get_attribute("name") or 
                            field.get_attribute("placeholder") or 
                            field.get_attribute("aria-label") or
                            "未知字段"
                        )
                        empty_required.append(field_name)
                        
                if empty_required:
                    print(f"发现未填写的必填字段: {', '.join(empty_required)}")
            except:
                pass
        
        if IS_LIVE_MODE:
            print("!!! LIVE MODE: 正在发送第一步请求... !!!")
            driver.execute_script("arguments[0].click();", send_button)
            print("✅ 第一步请求已发送！")
            
            # 等待第二个发送按钮出现
            print("等待第二个发送按钮出现...")
            time.sleep(random.uniform(2, 4))
            
            # 查找并点击第二个发送按钮
            print("正在寻找第二个发送按钮...")
            second_send_selectors = [
                "button[data-testid='renter-profile-submit']",  # 用户提供的正确选择器
                "//button[@data-testid='renter-profile-submit']",  # XPath版本
                "button.RCFDsButton:contains('Send')",
                "//button[contains(@class, 'RCFDsButton') and text()='Send']"
            ]
            
            second_send_button = None
            max_wait_for_second = 10  # 最多等待10秒查找第二个按钮
            wait_start = time.time()
            
            while time.time() - wait_start < max_wait_for_second:
                for selector in second_send_selectors:
                    try:
                        if selector.startswith("//"):
                            second_send_button = driver.find_element(By.XPATH, selector)
                        else:
                            second_send_button = driver.find_element(By.CSS_SELECTOR, selector)
                        
                        if second_send_button.is_displayed() and second_send_button.is_enabled():
                            print(f"找到第二个发送按钮: {selector}")
                            break
                    except:
                        continue
                
                if second_send_button:
                    break
                else:
                    print(f"第二个发送按钮还未出现，继续等待... (已等待 {time.time() - wait_start:.1f}秒)")
                    time.sleep(0.5)
            
            if second_send_button:
                print("!!! LIVE MODE: 正在发送第二步请求... !!!")
                driver.execute_script("arguments[0].click();", second_send_button)
                print("✅ 第二步请求已发送！完成!")
                
                # 检测并关闭可能出现的弹窗（最多2个）
                print("检查是否有弹窗需要关闭...")
                time.sleep(random.uniform(1, 2))  # 等待弹窗出现
                
                close_button_selectors = [
                    "button.CloseButton-sc-sqbalp-0",  # 用户提供的类名
                    "button.StyledCloseButton-c11n-8-109-3__sc-107ty8u-0",  # 用户提供的具体类名
                    "//button[contains(@class, 'CloseButton')]",  # XPath包含CloseButton类名
                    "//button//span[text()='Close']/../..",  # XPath通过Close文本找到按钮
                    "//button[contains(@class, 'StyledCloseButton')]"  # XPath包含StyledCloseButton类名
                ]
                
                popups_closed = 0
                max_popups = 2  # 最多可能有2个弹窗
                
                for popup_attempt in range(max_popups):
                    close_button = None
                    
                    # 尝试找到关闭按钮
                    for selector in close_button_selectors:
                        try:
                            if selector.startswith("//"):
                                close_button = driver.find_element(By.XPATH, selector)
                            else:
                                close_button = driver.find_element(By.CSS_SELECTOR, selector)
                            
                            if close_button.is_displayed() and close_button.is_enabled():
                                print(f"找到弹窗关闭按钮 #{popup_attempt + 1}: {selector}")
                                break
                        except:
                            continue
                    
                    if close_button:
                        try:
                            # 点击关闭按钮
                            driver.execute_script("arguments[0].click();", close_button)
                            print(f"✅ 已关闭弹窗 #{popup_attempt + 1}")
                            popups_closed += 1
                            time.sleep(random.uniform(0.5, 1.0))  # 等待弹窗关闭后再检查下一个
                        except Exception as e:
                            print(f"关闭弹窗时出错: {e}")
                            break
                    else:
                        print(f"未找到第 {popup_attempt + 1} 个弹窗，停止检查")
                        break
                
                if popups_closed > 0:
                    print(f"总共关闭了 {popups_closed} 个弹窗")
                else:
                    print("没有检测到需要关闭的弹窗")
                    
            else:
                print("警告: 未找到第二个发送按钮，但第一步已完成")
                
        else:
            print("--- DRY RUN: 表单填写成功，已找到第一个发送按钮，但未点击 ---")
            print("✅ 模拟运行成功！")
        
        time.sleep(random.uniform(2, 4))  # 从8-12秒减少到2-4秒
        return True
        
    except Exception as e:
        print(f"填写表单时出错: {e}")
        return False

def process_single_property(driver, property_url):
    """处理单个房源"""
    print(f"\n处理房源: {property_url}")
    
    try:
        # 访问房源页面
        driver.get(property_url)
        time.sleep(random.uniform(2, 4))  # 从3-5秒减少到2-4秒
        
        # 检查验证码
        if check_and_handle_captcha(driver):
            print("房源页面验证码已处理")
        
        # 查找并点击 "Request a tour" 按钮
        print("正在寻找 Request a tour 按钮...")
        
        request_tour_selectors = [
            "button[data-testid='request-tour-button']",
            "button[aria-label='Request a tour']",
            "//button[contains(text(), 'Request a tour')]",
            "//button[contains(text(), 'Request tour')]",
            "//a[contains(text(), 'Request a tour')]",
            ".request-tour-button",
            "[data-test='request-tour']"
        ]
        
        request_tour_button = None
        for selector in request_tour_selectors:
            try:
                if selector.startswith("//"):
                    request_tour_button = driver.find_element(By.XPATH, selector)
                else:
                    request_tour_button = driver.find_element(By.CSS_SELECTOR, selector)
                
                if request_tour_button.is_displayed():
                    print(f"找到 Request a tour 按钮: {selector}")
                    break
                    
            except:
                continue
        
        if not request_tour_button:
            print("无法找到 Request a tour 按钮，跳过此房源")
            return False
        
        # 人性化点击按钮
        print("正在用人性化方式点击按钮...")
        driver.execute_script("arguments[0].scrollIntoView(true);", request_tour_button)
        time.sleep(random.uniform(0.5, 1.0))
        driver.execute_script("arguments[0].click();", request_tour_button)
        
        # 检查点击后是否有验证码
        if check_and_handle_captcha(driver):
            print("点击后的验证码已处理，继续执行...")
        
        print("等待表单加载...")
        time.sleep(random.uniform(2, 4))
        
        # 填写表单
        if fill_contact_form(driver):
            print("✅ 房源处理成功")
            return True
        else:
            print("❌ 房源处理失败")
            return False
            
    except Exception as e:
        error_message = str(e)
        if "timeout" in error_message.lower():
            print(f"网络超时，跳过此房源: {error_message[:100]}...")
        elif "connection" in error_message.lower():
            print(f"网络连接问题，跳过此房源: {error_message[:100]}...")
        else:
            print(f"处理房源时出错: {error_message[:100]}...")
        return False

def go_to_next_page(driver):
    """尝试点击下一页按钮，如果成功则返回True，否则返回False"""
    print("正在寻找下一页按钮...")
    
    # 基于用户提供的HTML，寻找下一页按钮
    next_page_selectors = [
        "a[rel='next'][title='Next page']",  # 用户提供的准确选择器
        "a[aria-label='Next page']",
        "button[aria-label='Next page']", 
        "//a[contains(text(), 'Next')]",
        "//button[contains(text(), 'Next')]",
        ".PaginationButton-c11n-8-109-3__sc-1i6hxyy-0"  # 从HTML中找到的类名
    ]
    
    for selector in next_page_selectors:
        try:
            if selector.startswith("//"):
                next_button = driver.find_element(By.XPATH, selector)
            else:
                next_button = driver.find_element(By.CSS_SELECTOR, selector)
            
            if next_button.is_displayed() and next_button.is_enabled():
                print(f"找到下一页按钮: {selector}")
                
                # 滚动到按钮位置
                driver.execute_script("arguments[0].scrollIntoView(true);", next_button)
                time.sleep(random.uniform(1, 2))
                
                # 点击下一页
                driver.execute_script("arguments[0].click();", next_button)
                print("已点击下一页按钮")
                
                # 等待新页面加载
                time.sleep(random.uniform(3, 5))
                return True
                
        except Exception as e:
            continue
    
    print("未找到下一页按钮或已到最后一页")
    return False

def login_to_zillow(driver):
    """登录到Zillow"""
    try:
        print("\n" + "="*50)
        print("开始登录Zillow...")
        print("="*50)
        
        # 访问Zillow主页
        print("访问Zillow主页...")
        driver.get("https://www.zillow.com")
        time.sleep(random.uniform(3, 5))
        
        # 检查是否有验证码
        if check_and_handle_captcha(driver):
            print("登录页面验证码已处理")
        
        # 寻找并点击Sign In按钮
        print("正在寻找Sign In按钮...")
        signin_selectors = [
            "div.pfs__sc-1etb9mm-1.jBqzjp",  # 用户提供的具体选择器
            "//div[contains(@class, 'pfs__sc-1etb9mm-1') and text()='Sign In']",  # XPath版本
            "//div[text()='Sign In']",  # 通用文本选择器
            "//a[contains(text(), 'Sign In')]",  # 可能是链接
            "//button[contains(text(), 'Sign In')]",  # 可能是按钮
            "[data-testid='sign-in']",  # 可能的data-testid
            ".sign-in-button",  # 可能的类名
        ]
        
        signin_button = None
        for selector in signin_selectors:
            try:
                if selector.startswith("//"):
                    signin_button = driver.find_element(By.XPATH, selector)
                else:
                    signin_button = driver.find_element(By.CSS_SELECTOR, selector)
                
                if signin_button.is_displayed():
                    print(f"找到Sign In按钮: {selector}")
                    break
            except:
                continue
        
        if not signin_button:
            print("警告: 无法找到Sign In按钮")
            print("请手动点击Sign In按钮，然后按Enter继续...")
            input("按Enter键继续...")
            return True
        
        # 点击Sign In按钮
        print("正在点击Sign In按钮...")
        driver.execute_script("arguments[0].scrollIntoView(true);", signin_button)
        time.sleep(random.uniform(1, 2))
        driver.execute_script("arguments[0].click();", signin_button)
        
        print("已点击Sign In按钮")
        time.sleep(random.uniform(2, 4))
        
        # 等待登录页面加载并填写邮箱
        print("等待登录页面加载...")
        time.sleep(random.uniform(3, 5))
        
        # 检查是否有验证码
        if check_and_handle_captcha(driver):
            print("登录页面验证码已处理")
        
        # 寻找邮箱输入框
        print("正在寻找邮箱输入框...")
        email_selectors = [
            "input#username",  # 用户提供的ID
            "input[name='username']",  # name属性
            "input[inputmode='email']",  # inputmode属性
            "input[autocomplete='email']",  # autocomplete属性
            "input.input.ce861d26a.c8dc91595",  # 用户提供的具体类名
            "input[type='text'][required]"  # 通用选择器
        ]
        
        email_input = None
        for selector in email_selectors:
            try:
                email_input = driver.find_element(By.CSS_SELECTOR, selector)
                if email_input.is_displayed():
                    print(f"找到邮箱输入框: {selector}")
                    break
            except:
                continue
        
        if not email_input:
            print("警告: 无法找到邮箱输入框")
            print("请手动输入邮箱地址，然后按Enter继续...")
            input("按Enter键继续...")
        else:
            # 填写邮箱地址
            print("正在填写邮箱地址...")
            email_input.clear()
            time.sleep(random.uniform(0.5, 1.0))
            
            # 模拟人类输入
            email_address = "3251758144@qq.com"
            for char in email_address:
                email_input.send_keys(char)
                time.sleep(random.uniform(0.05, 0.15))
            
            print(f"邮箱地址已填写: {email_address}")
            time.sleep(random.uniform(1, 2))
            
            # 寻找并点击Continue按钮
            print("正在寻找Continue按钮...")
            continue_selectors = [
                "button[data-action-button-primary='true']",  # 用户提供的属性
                "button._button-login-id",  # 用户提供的类名
                "button[name='action'][value='default']",  # name和value属性
                "button.cea6d5264.c125e81f5.c8447a25a.ca798bf5e._button-login-id",  # 完整类名
                "button[type='submit']",  # 通用submit按钮
                "//button[contains(text(), 'Continue')]"  # 文本包含Continue
            ]
            
            continue_button = None
            for selector in continue_selectors:
                try:
                    if selector.startswith("//"):
                        continue_button = driver.find_element(By.XPATH, selector)
                    else:
                        continue_button = driver.find_element(By.CSS_SELECTOR, selector)
                    
                    if continue_button.is_displayed() and continue_button.is_enabled():
                        print(f"找到Continue按钮: {selector}")
                        break
                except:
                    continue
            
            if not continue_button:
                print("警告: 无法找到Continue按钮")
                print("请手动点击Continue按钮，然后按Enter继续...")
                input("按Enter键继续...")
            else:
                # 点击Continue按钮
                print("正在点击Continue按钮...")
                driver.execute_script("arguments[0].scrollIntoView(true);", continue_button)
                time.sleep(random.uniform(1, 2))
                driver.execute_script("arguments[0].click();", continue_button)
                print("已点击Continue按钮")
                time.sleep(random.uniform(2, 4))
        
        # 等待用户手动完成剩余登录步骤
        print("\n" + "="*60)
        print("请手动完成剩余登录过程：")
        print("1. 输入您的密码")
        print("2. 完成任何额外的验证步骤")
        print("3. 确保成功登录到您的账户")
        print("4. 登录完成后，按Enter键继续自动化流程...")
        print("="*60)
        input("按Enter键继续...")
        
        # 验证是否已登录
        print("验证登录状态...")
        time.sleep(2)
        
        # 检查是否有登录成功的标志（比如用户头像、用户名等）
        login_indicators = [
            "//div[contains(@class, 'user')]",
            "//button[contains(@class, 'avatar')]",
            "//div[contains(@class, 'profile')]",
            "[data-testid='user-menu']",
            ".user-avatar"
        ]
        
        logged_in = False
        for indicator in login_indicators:
            try:
                if indicator.startswith("//"):
                    element = driver.find_element(By.XPATH, indicator)
                else:
                    element = driver.find_element(By.CSS_SELECTOR, indicator)
                if element.is_displayed():
                    logged_in = True
                    print("✅ 检测到登录成功！")
                    break
            except:
                continue
        
        if not logged_in:
            print("⚠️ 无法确认登录状态，但继续执行...")
        
        print("登录步骤完成！")
        return True
        
    except Exception as e:
        print(f"登录过程中出错: {e}")
        print("继续执行，但可能会遇到更多反机器人检测...")
        return False

def main():
    """主函数 - 完整的分页处理和消息发送"""
    driver = create_undetected_browser()
    
    try:
        # 预热
        print("正在预热浏览器...")
        driver.get("https://www.google.com")
        time.sleep(3)
        
        # 登录到Zillow
        login_to_zillow(driver)
        
        # 开始分页处理
        current_page = 1
        total_properties_processed = 0
        successful_contacts = 0
        consecutive_errors = 0  # 连续错误次数
        max_consecutive_errors = 5  # 连续错误超过5次就停止
        start_time = time.time()  # 记录开始时间
        
        while True:  # 无限循环，直到没有更多页面
            print(f"\n{'='*50}")
            print(f"处理第 {current_page} 页")
            print(f"{'='*50}")
            
            # 访问页面
            if current_page == 1:
                page_url = START_URL
            else:
                page_url = START_URL.rstrip("/") + f"/{current_page}_p/"
            
            print(f"访问: {page_url}")
            driver.get(page_url)
            
            # 检查验证码
            if check_and_handle_captcha(driver):
                print("验证码已处理")
            
            # 收集房源
            properties = collect_properties_from_page(driver)
            
            if not properties:
                consecutive_errors += 1
                print(f"当前页面没有房源 (连续空页面: {consecutive_errors})")
                
                if consecutive_errors >= max_consecutive_errors:
                    print("连续多页没有房源，可能已到达最后一页")
                    break
                else:
                    print("继续尝试下一页...")
                    if go_to_next_page(driver):
                        current_page += 1
                        continue
                    else:
                        break
            else:
                consecutive_errors = 0  # 重置连续错误计数
            
            print(f"第 {current_page} 页找到 {len(properties)} 个房源")
            total_properties_processed += len(properties)
            
            # 处理每个房源
            for i, property_url in enumerate(properties, 1):
                print(f"\n--- 处理第 {current_page} 页的第 {i}/{len(properties)} 个房源 ---")
                
                if process_single_property(driver, property_url):
                    successful_contacts += 1
                
                # 房源间休眠
                if i < len(properties):  # 不是最后一个房源
                    sleep_time = random.uniform(15, 25)
                    print(f"等待 {sleep_time:.1f} 秒后处理下一个房源...")
                    time.sleep(sleep_time)
            
            # 尝试下一页
            next_page_success = go_to_next_page(driver)
            
            if not next_page_success:
                # 下一页按钮未找到，可能是页面状态异常，尝试恢复
                print("⚠️ 未找到下一页按钮，尝试页面恢复...")
                
                # 重新导航到当前页面来恢复页面状态
                try:
                    current_page_url = START_URL.rstrip("/") + f"/{current_page}_p/" if current_page > 1 else START_URL
                    print(f"重新访问当前页面: {current_page_url}")
                    driver.get(current_page_url)
                    time.sleep(random.uniform(3, 5))
                    
                    # 检查验证码
                    if check_and_handle_captcha(driver):
                        print("页面恢复后验证码已处理")
                    
                    # 重试寻找下一页按钮
                    print("页面恢复后重新寻找下一页按钮...")
                    next_page_success = go_to_next_page(driver)
                    
                except Exception as recovery_error:
                    print(f"页面恢复失败: {recovery_error}")
                    next_page_success = False
            
            if next_page_success:
                current_page += 1
                print(f"成功进入第 {current_page} 页")
                
                # 每处理10页显示一次统计信息
                if current_page % 10 == 0:
                    elapsed_time = time.time() - start_time
                    hours = int(elapsed_time // 3600)
                    minutes = int((elapsed_time % 3600) // 60)
                    print(f"\n📊 阶段性统计 (已处理 {current_page} 页, 运行时间: {hours}小时{minutes}分钟):")
                    print(f"  总房源数: {total_properties_processed}")
                    print(f"  成功联系: {successful_contacts}")
                    if total_properties_processed > 0:
                        print(f"  成功率: {successful_contacts/total_properties_processed*100:.1f}%")
                        print(f"  平均每页房源: {total_properties_processed/current_page:.1f}")
                    print("继续处理下一页...\n")
            else:
                # 最后的确认：手动尝试通过URL访问下一页
                print("🔍 最后确认是否真的到达最后一页...")
                try:
                    next_page_url = START_URL.rstrip("/") + f"/{current_page + 1}_p/"
                    print(f"尝试直接访问下一页: {next_page_url}")
                    driver.get(next_page_url)
                    time.sleep(random.uniform(3, 5))
                    
                    # 检查是否有房源
                    test_properties = collect_properties_from_page(driver)
                    if test_properties and len(test_properties) > 0:
                        print(f"✅ 发现下一页确实存在，找到 {len(test_properties)} 个房源！")
                        current_page += 1
                        print(f"成功进入第 {current_page} 页")
                        continue  # 继续处理这一页
                    else:
                        print("❌ 确认已到达最后一页，没有更多房源")
                        break
                        
                except Exception as final_check_error:
                    print(f"最终确认失败: {final_check_error}")
                    print("没有更多页面，已处理完所有房源")
                    break
        
        # 计算总运行时间
        total_time = time.time() - start_time
        hours = int(total_time // 3600)
        minutes = int((total_time % 3600) // 60)
        seconds = int(total_time % 60)
        
        print(f"\n{'='*50}")
        print(f"🎉 处理完成！")
        print(f"⏱️  总运行时间: {hours}小时{minutes}分钟{seconds}秒")
        print(f"📄 总共处理了 {current_page} 页")
        print(f"🏠 总共找到 {total_properties_processed} 个房源")
        print(f"✅ 成功联系 {successful_contacts} 个房源")
        if total_properties_processed > 0:
            print(f"📊 成功率: {successful_contacts/total_properties_processed*100:.1f}%")
            print(f"📈 平均每页房源: {total_properties_processed/current_page:.1f}")
            if total_time > 0:
                print(f"⚡ 处理速度: {total_properties_processed/(total_time/3600):.1f} 房源/小时")
        print(f"{'='*50}")
        
    except Exception as e:
        print(f"发生错误: {e}")
        
        # 尝试显示部分统计信息（如果变量已定义）
        try:
            if 'total_properties_processed' in locals():
                print(f"\n在错误发生前的统计信息:")
                print(f"已处理页数: {current_page if 'current_page' in locals() else '未知'}")
                print(f"总房源数: {total_properties_processed}")
                print(f"成功联系: {successful_contacts if 'successful_contacts' in locals() else '未知'}")
        except:
            pass
            
    finally:
        input("按Enter键关闭浏览器...")
        driver.quit()

if __name__ == "__main__":
    main() 
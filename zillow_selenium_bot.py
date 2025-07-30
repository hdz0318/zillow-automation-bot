import time
import random
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

# --- 在这里配置您的信息 ---
YOUR_NAME = "John Smith"  # 修改成您的名字
YOUR_PHONE = "5551234567"  # 修改成您的电话号码，纯数字
YOUR_MESSAGE = "Hello, I am very interested in this rental property. I would like to know if it's still available and if it would be possible to schedule a tour. Thank you!"  # 修改成您想发送的默认信息

# --- 脚本配置 ---
START_URL = "https://www.zillow.com/ca/rentals/"
IS_LIVE_MODE = False  # 设置为 True 来真实发送请求，设置为 False 则只运行到最后一步，不点击发送按钮
# -------------------------

def connect_to_browser():
    """
    连接到已经手动启动的Chrome浏览器实例
    """
    print("正在连接到手动启动的浏览器 (localhost:9222)...")
    chrome_options = Options()
    chrome_options.add_experimental_option("debuggerAddress", "localhost:9222")
    driver = webdriver.Chrome(options=chrome_options)
    print(f"成功连接到浏览器！当前标题: {driver.title}")
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
    全局验证处理器：随时检查并处理PerimeterX人机验证。
    """
    try:
        print("正在进行全局人机验证检查...")
        
        # 增加等待时间，让验证码有足够时间加载
        time.sleep(random.uniform(2, 4))
        
        # 尝试多种方式检查验证码iframe
        captcha_iframe = None
        
        # 方法1: 检查px-captcha-modal
        try:
            captcha_iframe = driver.find_element(By.ID, "px-captcha-modal")
            if captcha_iframe.is_displayed():
                print("找到px-captcha-modal验证码iframe")
            else:
                print("px-captcha-modal存在但不可见")
                captcha_iframe = None
        except:
            print("未找到px-captcha-modal")
        
        # 方法2: 检查任何包含captcha的iframe
        if not captcha_iframe:
            try:
                iframes = driver.find_elements(By.XPATH, "//iframe[contains(@id, 'captcha') or contains(@src, 'captcha') or contains(@class, 'captcha')]")
                if iframes:
                    captcha_iframe = iframes[0]
                    print(f"找到包含captcha的iframe，共{len(iframes)}个")
                else:
                    print("未找到包含captcha的iframe")
            except Exception as e:
                print(f"检查captcha iframe时出错: {e}")
        
        # 方法3: 检查所有全屏的iframe
        if not captcha_iframe:
            try:
                all_iframes = driver.find_elements(By.TAG_NAME, "iframe")
                for i, iframe in enumerate(all_iframes):
                    try:
                        style = iframe.get_attribute("style")
                        if style and ("position: fixed" in style and "width: 100%" in style and "height: 100%" in style):
                            captcha_iframe = iframe
                            print(f"找到全屏iframe (第{i+1}个)，样式: {style[:100]}...")
                            break
                    except:
                        continue
                if not captcha_iframe:
                    print(f"检查了{len(all_iframes)}个iframe，未找到全屏iframe")
            except Exception as e:
                print(f"检查全屏iframe时出错: {e}")
        
        # 方法4: 打印所有iframe信息用于调试
        if not captcha_iframe:
            try:
                all_iframes = driver.find_elements(By.TAG_NAME, "iframe")
                print(f"页面上共有{len(all_iframes)}个iframe:")
                for i, iframe in enumerate(all_iframes):
                    try:
                        iframe_id = iframe.get_attribute("id")
                        iframe_src = iframe.get_attribute("src")
                        iframe_style = iframe.get_attribute("style")
                        print(f"  iframe {i+1}: id='{iframe_id}', src='{iframe_src[:50] if iframe_src else None}', style='{iframe_style[:50] if iframe_style else None}...'")
                    except:
                        print(f"  iframe {i+1}: 无法获取属性")
            except Exception as e:
                print(f"调试iframe信息时出错: {e}")
        
        if captcha_iframe and captcha_iframe.is_displayed():
            print("!!! 全局处理器检测到验证码，正在尝试用拟人化方式自动处理...")
            
            # 切换到iframe前，先等待一会
            time.sleep(random.uniform(1, 2))
            driver.switch_to.frame(captcha_iframe)
            
            # 等待iframe内容加载
            time.sleep(random.uniform(3, 5))
            
            # 先尝试打印iframe内的所有内容，帮助调试
            try:
                page_source = driver.page_source
                print(f"验证码iframe内容长度: {len(page_source)}")
                if len(page_source) > 100:
                    print("iframe内容已加载")
                    # 打印前200个字符用于调试
                    print(f"iframe内容预览: {page_source[:200]}...")
                else:
                    print("iframe内容可能未完全加载")
            except:
                print("无法获取iframe内容")
            
            try:
                # 尝试多种可能的按钮定位方式
                hold_button = None
                
                # 方法1: 寻找包含"Press"或"Hold"的按钮
                try:
                    hold_button = WebDriverWait(driver, 5).until(
                        EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Press') or contains(text(), 'Hold')]"))
                    )
                    print("通过Press/Hold文本找到按钮")
                except: 
                    print("方法1失败：未找到包含Press/Hold的按钮")
                
                # 方法2: 寻找任何可点击的按钮
                if not hold_button:
                    try:
                        buttons = driver.find_elements(By.TAG_NAME, "button")
                        if buttons:
                            hold_button = buttons[0]  # 取第一个按钮
                            print(f"找到iframe中的按钮元素，共{len(buttons)}个按钮")
                        else:
                            print("方法2失败：iframe中没有button元素")
                    except Exception as e:
                        print(f"方法2失败：{e}")
                
                # 方法3: 寻找可点击的div元素
                if not hold_button:
                    try:
                        divs = driver.find_elements(By.XPATH, "//div[@role='button' or contains(@class, 'button') or contains(@class, 'btn')]")
                        if divs:
                            hold_button = divs[0]
                            print(f"找到iframe中的div按钮，共{len(divs)}个")
                        else:
                            print("方法3失败：没找到可点击的div")
                    except Exception as e:
                        print(f"方法3失败：{e}")
                
                # 方法4: 寻找任何可点击元素
                if not hold_button:
                    try:
                        clickables = driver.find_elements(By.XPATH, "//*[@onclick or @role='button' or contains(@class, 'click')]")
                        if clickables:
                            hold_button = clickables[0]
                            print(f"找到可点击元素，共{len(clickables)}个")
                        else:
                            print("方法4失败：没找到任何可点击元素")
                    except Exception as e:
                        print(f"方法4失败：{e}")
                
                # 方法5: 如果都找不到，就点击iframe的中心
                if not hold_button:
                    print("未找到具体按钮，将点击iframe中心区域")
                    # 获取iframe的尺寸并点击中心
                    iframe_size = driver.get_window_size()
                    center_x = iframe_size['width'] // 2
                    center_y = iframe_size['height'] // 2
                    
                    actions = webdriver.ActionChains(driver)
                    actions.move_by_offset(center_x, center_y)
                    actions.click_and_hold()
                    
                    hold_time = random.uniform(2.5, 4.5)
                    print(f"在iframe中心按住 {hold_time:.2f} 秒...")
                    time.sleep(hold_time)
                    
                    actions.release().perform()
                    print("已释放，等待验证完成...")
                    time.sleep(5)
                else:
                    # 找到了按钮，执行按住操作
                    print("开始模拟按住操作...")
                    actions = webdriver.ActionChains(driver)
                    actions.move_to_element(hold_button).pause(random.uniform(0.3, 0.6)).click_and_hold()
                    
                    hold_time = random.uniform(2.5, 4.5)
                    print(f"按住 {hold_time:.2f} 秒...")
                    
                    start_time = time.time()
                    while time.time() - start_time < hold_time:
                        actions.move_by_offset(random.randint(-1, 1), random.randint(-1, 1)).pause(random.uniform(0.1, 0.3))
                    
                    actions.release().perform()
                    print("已释放按钮，等待验证完成...")
                    time.sleep(5)
                
            except Exception as e:
                print(f"在iframe内操作时发生错误: {e}")
                print("尝试简单的点击iframe中心...")
                actions = webdriver.ActionChains(driver)
                actions.move_by_offset(200, 200).click_and_hold()
                time.sleep(3)
                actions.release().perform()
            
            driver.switch_to.default_content()
            print("验证处理完成，切换回主页面。")
            
            # 等待验证iframe消失
            try:
                WebDriverWait(driver, 20).until(EC.invisibility_of_element_located((By.ID, "px-captcha-modal")))
                print("验证iframe已消失，继续执行...")
            except:
                print("验证iframe可能仍然存在，但继续执行...")
            
            return True
        else:
            print("全局检查未发现人机验证。")
            return False
            
    except Exception as e:
        print(f"验证码检查过程中发生错误: {e}")
        return False
    return False

def pre_warm_up(driver):
    """
    进行预热操作，让浏览器行为看起来更像真人。
    """
    try:
        print("--- 开始进行预热操作 ---")
        
        # 1. 访问Google并搜索Zillow
        print("访问Google...")
        driver.get("https://www.google.com")
        time.sleep(random.uniform(2, 4))
        
        print("在Google搜索Zillow...")
        search_box = driver.find_element(By.NAME, "q")
        search_term = "Zillow"
        for char in search_term:
            search_box.send_keys(char)
            time.sleep(random.uniform(0.1, 0.3))
        search_box.submit()
        time.sleep(random.uniform(3, 5))
        
        # 2. 在搜索结果中找到Zillow官网并点击
        print("在搜索结果中寻找Zillow官网...")
        zillow_link_in_google = wait_and_find_element(
            driver,
            By.XPATH,
            "//a[contains(@href, 'zillow.com') and .//h3]",
            description="Google搜索结果中的Zillow链接"
        )
        zillow_link_in_google.click()
        time.sleep(random.uniform(4, 6))
        
        # 3. 在Zillow主页进行一些无意义的浏览
        print("在Zillow主页进行随机浏览...")
        for _ in range(random.randint(1, 3)):
            # 随机滚动页面
            scroll_amount = random.randint(300, 800)
            driver.execute_script(f"window.scrollBy(0, {scroll_amount});")
            time.sleep(random.uniform(1.5, 3))
        
        print("--- 预热操作完成 ---")
        
    except Exception as e:
        print(f"预热操作中发生错误，但这不影响主流程: {e}")
        # 即使预热失败，也尝试继续主流程

def login_to_zillow_selenium(driver):
    """登录到Zillow (Selenium版本)"""
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
        
        print("登录步骤完成！")
        return True
        
    except Exception as e:
        print(f"登录过程中出错: {e}")
        print("继续执行，但可能会遇到更多反机器人检测...")
        return False

def contact_landlord_on_zillow():
    """
    主函数：连接到已启动的浏览器，并执行自动化任务
    """
    driver = connect_to_browser()
    
    try:
        # 登录到Zillow
        login_to_zillow_selenium(driver)
        
        # 直接访问目标页面，不再进行复杂的预热
        print(f"正在访问: {START_URL}")
        driver.get(START_URL)
        
        print("等待房源列表加载...")
        wait_and_find_element(driver, By.CSS_SELECTOR, "article[data-test='property-card']", description="房源列表")
        
        property_cards = driver.find_elements(By.CSS_SELECTOR, "article[data-test='property-card']")
        print(f"在当前页面找到 {len(property_cards)} 个房源。")
        
        property_links = [card.find_element(By.CSS_SELECTOR, "a.property-card-link").get_attribute("href") for card in property_cards if card.find_element(By.CSS_SELECTOR, "a.property-card-link").get_attribute("href")]
        print(f"成功获取到 {len(property_links)} 个房源链接准备处理。")
        
        for i, link in enumerate(property_links):
            print(f"\n{'='*20} \n处理第 {i+1}/{len(property_links)} 个房源: {link}\n{'='*20}")
            try:
                # 访问房源详情页 - 这里最可能触发验证
                print("正在访问房源详情页...")
                driver.get(link)
                
                # --- 关键改动：立刻检查验证码 ---
                check_and_handle_captcha(driver)
                
                # 给页面一些时间完全加载
                time.sleep(random.uniform(3, 5))
                
                print("正在定位 'Request a tour' 按钮...")
                request_tour_button = wait_and_find_element(driver, By.XPATH, "//button[contains(text(), 'Request a tour')]", description="Request a tour 按钮")
                
                print("正在用极致拟人化的方式点击'Request a tour'按钮...")
                actions = webdriver.ActionChains(driver)
                # 更加缓慢和谨慎的点击
                actions.move_to_element(request_tour_button)
                actions.pause(random.uniform(0.5, 1.0))  # 增加悬停时间
                actions.click_and_hold()
                actions.pause(random.uniform(0.1, 0.3))  # 增加按住时间
                actions.release()
                actions.perform()
                
                # --- 关键改动：点击后再次检查验证码 ---
                check_and_handle_captcha(driver)
                
                print("等待表单加载...")
                time.sleep(random.uniform(3, 5))  # 增加等待时间
                
                # 检测表单类型 - 登录后可能只需要填写消息
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
                        time.sleep(random.uniform(0.02, 0.08))
                    print(f"消息已填写: {YOUR_MESSAGE[:50]}...")
                    
                else:
                    # 未登录的完整表单流程
                    print("使用完整表单流程...")
                    
                    print("定位姓名输入框...")
                    try:
                        name_input = wait_and_find_element(driver, By.CSS_SELECTOR, "input[placeholder='First & last name']", timeout=10, description="姓名输入框")
                        name_input.clear()
                        # 更慢的输入速度
                        for char in YOUR_NAME:
                            name_input.send_keys(char)
                            time.sleep(random.uniform(0.05, 0.15))
                        print(f"姓名已填写: {YOUR_NAME}")
                    except:
                        print("警告: 无法找到姓名输入框，可能是登录后的简化表单")
                    
                    print("定位电话输入框...")
                    try:
                        phone_input = driver.find_element(By.CSS_SELECTOR, "input[type='tel']")
                        phone_input.clear()
                        for char in YOUR_PHONE:
                            phone_input.send_keys(char)
                            time.sleep(random.uniform(0.05, 0.15))
                        print(f"电话已填写: {YOUR_PHONE}")
                    except:
                        print("警告: 无法找到电话输入框，可能是登录后的简化表单")
                    
                    print("定位消息输入框...")
                    try:
                        message_box = driver.find_element(By.TAG_NAME, "textarea")
                        message_box.clear()
                        for char in YOUR_MESSAGE:
                            message_box.send_keys(char)
                            time.sleep(random.uniform(0.02, 0.08))
                        print(f"消息已填写: {YOUR_MESSAGE[:50]}...")
                    except:
                        print("错误: 无法找到消息输入框")
                        return
                
                print("表单填写完成。")
                time.sleep(random.uniform(3, 5))
                
                print("定位发送按钮...")
                send_button = driver.find_element(By.CSS_SELECTOR, "button[data-testid='rcf-submit-button']")
                
                if IS_LIVE_MODE:
                    print("!!! LIVE MODE: 正在发送第一步请求... !!!")
                    send_button.click()
                    print("✅ 第一步请求已发送！")
                    
                    # 等待第二个发送按钮出现
                    print("等待第二个发送按钮出现...")
                    time.sleep(random.uniform(2, 4))
                    
                    # 查找并点击第二个发送按钮
                    print("正在寻找第二个发送按钮...")
                    try:
                        # 等待第二个发送按钮
                        second_send_button = WebDriverWait(driver, 10).until(
                            EC.element_to_be_clickable((By.CSS_SELECTOR, "button[data-testid='renter-profile-submit']"))
                        )
                        print("找到第二个发送按钮: button[data-testid='renter-profile-submit']")
                        
                        print("!!! LIVE MODE: 正在发送第二步请求... !!!")
                        second_send_button.click()
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
                        
                    except TimeoutException:
                        print("警告: 未找到第二个发送按钮，但第一步已完成")
                        # 尝试备用选择器
                        try:
                            second_send_button = driver.find_element(By.XPATH, "//button[contains(@class, 'RCFDsButton') and text()='Send']")
                            if second_send_button.is_displayed() and second_send_button.is_enabled():
                                second_send_button.click()
                                print("✅ 第二步请求已发送！（使用备用选择器）")
                        except:
                            print("无法找到第二个发送按钮")
                else:
                    print("--- DRY RUN: 脚本运行正常，已定位到第一个发送按钮，但未点击。---")
                
                try:
                    driver.switch_to.default_content()
                except: pass
                time.sleep(random.uniform(8, 12))  # 增加休息时间
                
            except Exception as e:
                print(f"处理房源 {link} 时发生未知错误: {e}")
                print("跳过此房源。")
            
            # 大幅增加房源之间的等待时间
            sleep_time = random.uniform(60, 120)  # 1-2分钟
            print(f"本轮处理完毕，将休眠 {sleep_time:.2f} 秒...")
            time.sleep(sleep_time)
    
    except Exception as e:
        print(f"脚本发生严重错误: {e}")
    finally:
        print("\n所有房源处理完毕。脚本不会关闭手动启动的浏览器。")

if __name__ == "__main__":
    contact_landlord_on_zillow() 
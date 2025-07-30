 
import time
import random
from playwright.sync_api import sync_playwright, TimeoutError

# 这个最终版本脚本不再需要手动实现伪装，因为它将连接到一个干净的、手动启动的浏览器实例。
# STEALTH_JS_SCRIPT = ... (不再需要)

# --- 在这里配置你的信息 ---
YOUR_NAME = "John Smith"  # 修改成你的名字
YOUR_PHONE = "5551234567"  # 修改成你的电话号码，纯数字
YOUR_MESSAGE = "Hello, I am very interested in this rental property. I would like to know if it's still available and if it would be possible to schedule a tour. Thank you!" # 修改成你想发送的默认信息

# --- 脚本配置 ---
START_URL = "https://www.zillow.com/ca/rentals/"
IS_LIVE_MODE = False
# -------------------------

def login_to_zillow_playwright(page):
    """登录到Zillow (Playwright版本)"""
    try:
        print("\n" + "="*50)
        print("开始登录Zillow...")
        print("="*50)
        
        # 访问Zillow主页
        print("访问Zillow主页...")
        page.goto("https://www.zillow.com", timeout=60000, wait_until='domcontentloaded')
        page.wait_for_timeout(random.uniform(3000, 5000))
        
        # 寻找并点击Sign In按钮
        print("正在寻找Sign In按钮...")
        signin_selectors = [
            "div.pfs__sc-1etb9mm-1.jBqzjp",  # 用户提供的具体选择器
            "div:has-text('Sign In')",  # Playwright语法
            "a:has-text('Sign In')",  # 可能是链接
            "button:has-text('Sign In')",  # 可能是按钮
        ]
        
        signin_button = None
        for selector in signin_selectors:
            try:
                signin_button = page.locator(selector).first
                if signin_button.is_visible():
                    print(f"找到Sign In按钮: {selector}")
                    break
            except:
                continue
        
        if not signin_button or not signin_button.is_visible():
            print("警告: 无法找到Sign In按钮")
            print("请手动点击Sign In按钮，然后按Enter继续...")
            input("按Enter键继续...")
            return True
        
        # 点击Sign In按钮
        print("正在点击Sign In按钮...")
        signin_button.scroll_into_view_if_needed()
        page.wait_for_timeout(random.uniform(1000, 2000))
        signin_button.click()
        
        print("已点击Sign In按钮")
        page.wait_for_timeout(random.uniform(2000, 4000))
        
        # 等待登录页面加载并填写邮箱
        print("等待登录页面加载...")
        page.wait_for_timeout(random.uniform(3000, 5000))
        
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
                email_input = page.locator(selector).first
                if email_input.is_visible():
                    print(f"找到邮箱输入框: {selector}")
                    break
            except:
                continue
        
        if not email_input or not email_input.is_visible():
            print("警告: 无法找到邮箱输入框")
            print("请手动输入邮箱地址，然后按Enter继续...")
            input("按Enter键继续...")
        else:
            # 填写邮箱地址
            print("正在填写邮箱地址...")
            email_input.clear()
            page.wait_for_timeout(random.uniform(500, 1000))
            
            # 模拟人类输入
            email_address = "3251758144@qq.com"
            email_input.type(email_address, delay=random.uniform(50, 150))
            
            print(f"邮箱地址已填写: {email_address}")
            page.wait_for_timeout(random.uniform(1000, 2000))
            
            # 寻找并点击Continue按钮
            print("正在寻找Continue按钮...")
            continue_selectors = [
                "button[data-action-button-primary='true']",  # 用户提供的属性
                "button._button-login-id",  # 用户提供的类名
                "button[name='action'][value='default']",  # name和value属性
                "button.cea6d5264.c125e81f5.c8447a25a.ca798bf5e._button-login-id",  # 完整类名
                "button[type='submit']",  # 通用submit按钮
                "button:has-text('Continue')"  # Playwright语法
            ]
            
            continue_button = None
            for selector in continue_selectors:
                try:
                    continue_button = page.locator(selector).first
                    if continue_button.is_visible() and continue_button.is_enabled():
                        print(f"找到Continue按钮: {selector}")
                        break
                except:
                    continue
            
            if not continue_button or not continue_button.is_visible():
                print("警告: 无法找到Continue按钮")
                print("请手动点击Continue按钮，然后按Enter继续...")
                input("按Enter键继续...")
            else:
                # 点击Continue按钮
                print("正在点击Continue按钮...")
                continue_button.scroll_into_view_if_needed()
                page.wait_for_timeout(random.uniform(1000, 2000))
                continue_button.click()
                print("已点击Continue按钮")
                page.wait_for_timeout(random.uniform(2000, 4000))
        
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
    主函数：连接到已启动的浏览器，并执行自动化任务。
    """
    with sync_playwright() as p:
        try:
            print("正在连接到手动启动的浏览器 (localhost:9222)...")
            # 连接到我们手动启动的、监听9222端口的浏览器实例
            browser = p.chromium.connect_over_cdp("http://localhost:9222")
            
            # 获取该浏览器实例的默认上下文
            context = browser.contexts[0]
            page = context.new_page()
            print("连接成功！")

            # 登录到Zillow
            login_to_zillow_playwright(page)

            # 1. 打开Zillow租房搜索页面
            print(f"正在访问: {START_URL}")
            page.goto(START_URL, timeout=60000, wait_until='domcontentloaded')

            # 由于我们使用的是一个“预热”过的、可信的浏览器，
            # 很大程度上可以直接跳过初始验证。
            # 我们仍然保留这个检查作为保险。
            
            # 等待房源列表加载出来
            listing_selector = "article[data-test='property-card']"
            print("等待房源列表加载...")
            page.wait_for_selector(listing_selector, timeout=30000)
            
            listings = page.locator(listing_selector)
            listing_count = listings.count()
            if listing_count == 0:
                print("错误：在页面上没有找到房源信息。")
                browser.close()
                return

            print(f"在当前页面找到 {listing_count} 个房源。")
            
            property_links = []
            for i in range(listing_count):
                try:
                    link_locator = listings.nth(i).locator("a.property-card-link")
                    href = link_locator.get_attribute('href')
                    if href:
                        if not href.startswith('http'):
                            href = "https://www.zillow.com" + href
                        property_links.append(href)
                except Exception as e:
                    print(f"获取第 {i+1} 个房源链接时出错: {e}")

            print(f"成功获取到 {len(property_links)} 个房源链接准备处理。")

            # 2. 循环处理每一个房源
            for i, link in enumerate(property_links):
                print(f"\n{'='*20} \n处理第 {i+1}/{len(property_links)} 个房源: {link}\n{'='*20}")
                try:
                    page.goto(link, timeout=60000, wait_until='domcontentloaded')
                    time.sleep(random.uniform(3, 5))

                    # --- 更稳健的点击逻辑 ---
                    print("正在定位 'Request a tour' 按钮...")
                    # 使用 get_by_role 定位，这通常比按文本查找更可靠
                    request_tour_button = page.get_by_role("button", name="Request a tour").first
                    
                    # 移动到元素上方并等待，模拟人类行为
                    print("模拟鼠标悬停...")
                    request_tour_button.hover()
                    time.sleep(random.uniform(0.5, 1))

                    print("正在点击按钮...")
                    # 使用 force=True 确保即使有元素轻微遮挡也能点击
                    request_tour_button.click(force=True, timeout=5000)

                    print("按钮已点击，正在使用专业方法定位弹窗...")
                    
                    # --- 最终的、基于角色的专业定位逻辑 ---
                    # 1. 首先，定位到标题为“Request a tour”的对话框
                    #    这是最接近人类识别方式的、最可靠的方法
                    dialog = page.get_by_role("dialog").filter(
                        has=page.get_by_role("heading", name="Request a tour")
                    )
                    
                    print("等待对话框加载...")
                    dialog.wait_for(timeout=10000)
                    print("对话框已成功定位！")

                    # 2. 现在，我们只在这个对话框内部进行操作
                    print("开始在对话框内部填写表单...")
                    
                    # 检测表单类型 - 登录后可能只需要填写消息
                    print("检测表单类型...")
                    
                    # 检查是否有登录后的简化消息框
                    logged_in_message_selectors = [
                        "textarea#message-box",  # 用户提供的登录后消息框ID
                        "textarea[data-testid='message-box-input']",  # 用户提供的data-testid
                        "textarea[placeholder='Add your message']"  # placeholder文本
                    ]
                    
                    logged_in_message_input = None
                    for selector in logged_in_message_selectors:
                        try:
                            logged_in_message_input = dialog.locator(selector).first
                            if logged_in_message_input.is_visible():
                                print(f"检测到登录后的简化表单，只需填写消息: {selector}")
                                break
                        except:
                            continue
                    
                    if logged_in_message_input:
                        # 登录后的简化流程 - 只填写消息
                        print("使用登录后的简化表单流程...")
                        logged_in_message_input.clear()
                        page.wait_for_timeout(random.uniform(500, 1000))
                        
                        logged_in_message_input.type(YOUR_MESSAGE, delay=random.uniform(30, 80))
                        print(f"消息已填写: {YOUR_MESSAGE[:50]}...")
                        
                    else:
                        # 未登录的完整表单流程
                        print("使用完整表单流程...")
                        
                        try:
                            # 在对话框内部，通过占位符文字找到姓名输入框
                            name_input = dialog.get_by_placeholder("First & last name")
                            name_input.fill(YOUR_NAME)
                            time.sleep(random.uniform(0.5, 1))
                            print(f"姓名已填写: {YOUR_NAME}")
                        except:
                            print("警告: 无法找到姓名输入框，可能是登录后的简化表单")
                        
                        try:
                            phone_input = dialog.get_by_role("textbox", name="Phone")
                            phone_input.fill(YOUR_PHONE)
                            time.sleep(random.uniform(0.5, 1))
                            print(f"电话已填写: {YOUR_PHONE}")
                        except:
                            print("警告: 无法找到电话输入框，可能是登录后的简化表单")

                        try:
                            message_box = dialog.get_by_role("textbox", name="Message")
                            message_box.fill('')
                            message_box.type(YOUR_MESSAGE, delay=random.uniform(30, 80))
                            print(f"消息已填写: {YOUR_MESSAGE[:50]}...")
                        except:
                            print("错误: 无法找到消息输入框")
                    
                    print("表单填写完成。")
                    time.sleep(random.uniform(2, 4))

                    send_button = dialog.locator("button[data-testid='rcf-submit-button']")
                    
                    if IS_LIVE_MODE:
                        print("!!! LIVE MODE: 正在发送第一步请求... !!!")
                        send_button.click()
                        print("✅ 第一步请求已发送！")
                        
                        # 等待第二个发送按钮出现
                        print("等待第二个发送按钮出现...")
                        page.wait_for_timeout(random.uniform(2000, 4000))
                        
                        # 查找并点击第二个发送按钮
                        print("正在寻找第二个发送按钮...")
                        try:
                            second_send_button = dialog.locator("button[data-testid='renter-profile-submit']")
                            second_send_button.wait_for(state="visible", timeout=10000)
                            print("找到第二个发送按钮: button[data-testid='renter-profile-submit']")
                            
                            print("!!! LIVE MODE: 正在发送第二步请求... !!!")
                            second_send_button.click()
                            print("✅ 第二步请求已发送！完成!")
                            
                            # 检测并关闭可能出现的弹窗（最多2个）
                            print("检查是否有弹窗需要关闭...")
                            page.wait_for_timeout(random.uniform(1000, 2000))  # 等待弹窗出现
                            
                            close_button_selectors = [
                                "button.CloseButton-sc-sqbalp-0",  # 用户提供的类名
                                "button.StyledCloseButton-c11n-8-109-3__sc-107ty8u-0",  # 用户提供的具体类名
                                "button:has(span:text('Close'))"  # Playwright语法
                            ]
                            
                            popups_closed = 0
                            max_popups = 2  # 最多可能有2个弹窗
                            
                            for popup_attempt in range(max_popups):
                                close_button = None
                                
                                # 尝试找到关闭按钮
                                for selector in close_button_selectors:
                                    try:
                                        close_button = page.locator(selector).first
                                        if close_button.is_visible():
                                            print(f"找到弹窗关闭按钮 #{popup_attempt + 1}: {selector}")
                                            break
                                    except:
                                        continue
                                
                                if close_button and close_button.is_visible():
                                    try:
                                        # 点击关闭按钮
                                        close_button.click()
                                        print(f"✅ 已关闭弹窗 #{popup_attempt + 1}")
                                        popups_closed += 1
                                        page.wait_for_timeout(random.uniform(500, 1000))  # 等待弹窗关闭后再检查下一个
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
                            
                        except:
                            print("警告: 未找到第二个发送按钮，但第一步已完成")
                            # 尝试在整个页面中查找
                            try:
                                second_send_button = page.locator("button[data-testid='renter-profile-submit']")
                                if second_send_button.is_visible():
                                    second_send_button.click()
                                    print("✅ 第二步请求已发送！（在页面中找到）")
                                else:
                                    print("无法找到第二个发送按钮")
                            except:
                                print("无法找到第二个发送按钮")
                    else:
                        print("--- DRY RUN: 脚本运行正常，已定位到第一个发送按钮，但未点击。---")

                    time.sleep(random.uniform(5, 8))

                except TimeoutError:
                    print("错误：操作超时。未能找到'Request a tour'对话框或内部的输入框。")
                except Exception as e:
                    print(f"处理房源 {link} 时发生未知错误: {e}")
                    print("跳过此房源。")
                
                sleep_time = random.uniform(30, 90)
                print(f"本轮处理完毕，将休眠 {sleep_time:.2f} 秒...")
                time.sleep(sleep_time)

        except Exception as e:
            print(f"脚本发生严重错误: {e}")
        finally:
            print("\n所有房源处理完毕。脚本不会关闭手动启动的浏览器。")
            # browser.close() # 我们不再需要脚本来关闭浏览器


if __name__ == "__main__":
    contact_landlord_on_zillow() 
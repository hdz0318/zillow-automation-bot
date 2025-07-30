import time
import random
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

# --- 配置信息 ---
YOUR_NAME = "John Smith"
YOUR_EMAIL = "john.smith@email.com"
YOUR_PHONE = "5551234567"
YOUR_MESSAGE = "Hello, I am interested in this rental property."

START_URL = "https://www.zillow.com/ca/rentals/"
IS_LIVE_MODE = False

def create_undetected_browser():
    """创建反检测浏览器"""
    print("正在启动反检测浏览器...")
    options = uc.ChromeOptions()
    options.add_argument('--no-first-run')
    options.add_argument('--no-service-autorun')
    options.add_argument('--no-default-browser-check')
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_argument('--user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')
    
    driver = uc.Chrome(options=options, version_main=None)
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    
    print("反检测浏览器启动成功")
    return driver

def check_and_handle_captcha(driver):
    """检查并处理验证码"""
    try:
        print("检查是否存在验证码...")
        time.sleep(random.uniform(2, 3))
        
        captcha_indicators = ["px-captcha-modal", "captcha", "challenge", "verification"]
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
                time.sleep(0.6)  # 每步暂停0.6秒，比之前的0.5秒更慢
            
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

def go_to_next_page(driver):
    """点击下一页按钮"""
    print("正在寻找下一页按钮...")
    
    next_page_selectors = [
        "a[rel='next'][title='Next page']",
        "a[aria-label='Next page']",
        "//a[contains(@href, '_p/')]",
        "//a[contains(text(), 'Next')]"
    ]
    
    for selector in next_page_selectors:
        try:
            if selector.startswith("//"):
                next_button = driver.find_element(By.XPATH, selector)
            else:
                next_button = driver.find_element(By.CSS_SELECTOR, selector)
            
            if next_button.is_displayed() and next_button.is_enabled():
                print(f"找到下一页按钮: {selector}")
                
                # 滚动到按钮位置并点击
                driver.execute_script("arguments[0].scrollIntoView(true);", next_button)
                time.sleep(random.uniform(1, 2))
                driver.execute_script("arguments[0].click();", next_button)
                
                print("已点击下一页按钮，等待页面加载...")
                time.sleep(random.uniform(3, 5))
                return True
                
        except Exception as e:
            continue
    
    print("未找到下一页按钮")
    return False

def main():
    """主函数 - 测试分页功能"""
    driver = create_undetected_browser()
    
    try:
        # 预热
        print("正在预热浏览器...")
        driver.get("https://www.google.com")
        time.sleep(3)
        
        # 开始分页处理
        current_page = 1
        max_pages = 3  # 只测试前3页
        total_properties = 0
        
        while current_page <= max_pages:
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
                print("当前页面没有房源，结束")
                break
            
            print(f"第 {current_page} 页找到 {len(properties)} 个房源")
            total_properties += len(properties)
            
            # 显示前3个房源作为示例
            print("房源示例:")
            for i, prop in enumerate(properties[:3]):
                print(f"  {i+1}. {prop}")
            
            # 尝试下一页
            if current_page < max_pages:
                if go_to_next_page(driver):
                    current_page += 1
                    print(f"成功进入第 {current_page} 页")
                else:
                    print("没有更多页面")
                    break
            else:
                print("已达到测试页数限制")
                break
        
        print(f"\n{'='*50}")
        print(f"测试完成！")
        print(f"总共处理了 {current_page} 页")
        print(f"总共找到 {total_properties} 个房源")
        print(f"{'='*50}")
        
    except Exception as e:
        print(f"发生错误: {e}")
    finally:
        input("按Enter键关闭浏览器...")
        driver.quit()

if __name__ == "__main__":
    main() 
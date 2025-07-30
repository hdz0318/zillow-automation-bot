import time
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def debug_zillow_page():
    """
    调试脚本：分析Zillow页面结构，找出为什么只找到9个房源
    """
    print("启动调试浏览器...")
    
    options = uc.ChromeOptions()
    options.add_argument('--no-first-run')
    options.add_argument('--no-service-autorun')
    options.add_argument('--no-default-browser-check')
    options.add_argument('--disable-blink-features=AutomationControlled')
    
    driver = uc.Chrome(options=options, version_main=None)
    
    try:
        # 访问Zillow租房页面
        url = "https://www.zillow.com/ca/rentals/"
        print(f"访问: {url}")
        driver.get(url)
        
        # 等待页面加载
        time.sleep(5)
        
        print(f"页面标题: {driver.title}")
        print(f"当前URL: {driver.current_url}")
        
        # 尝试多种房源卡片选择器
        selectors_to_try = [
            "article[data-test='property-card']",
            "article[data-testid='property-card']", 
            "div[data-test='property-card']",
            "div[data-testid='property-card']",
            ".property-card",
            "[data-test*='property']",
            "[data-testid*='property']",
            "article",
            ".ListItem",
            ".list-card",
            ".property-card-link"
        ]
        
        print("\n=== 测试不同的房源选择器 ===")
        for selector in selectors_to_try:
            try:
                elements = driver.find_elements(By.CSS_SELECTOR, selector)
                print(f"{selector}: 找到 {len(elements)} 个元素")
                
                if len(elements) > 0 and len(elements) < 20:  # 显示前几个元素的详细信息
                    for i, elem in enumerate(elements[:3]):
                        try:
                            text_preview = elem.text[:100].replace('\n', ' ') if elem.text else "无文本"
                            print(f"  元素 {i+1}: {text_preview}...")
                        except:
                            print(f"  元素 {i+1}: 无法获取文本")
            except Exception as e:
                print(f"{selector}: 错误 - {e}")
        
        # 分析页面源码中的关键信息
        print("\n=== 分析页面源码 ===")
        page_source = driver.page_source
        
        # 搜索可能的房源相关关键词
        keywords = ["property-card", "listing", "rental", "apartment", "house", "PropertyCard", "ListingCard"]
        for keyword in keywords:
            count = page_source.lower().count(keyword.lower())
            print(f"'{keyword}' 出现次数: {count}")
        
        # 检查是否有分页或加载更多按钮
        print("\n=== 检查分页和加载按钮 ===")
        pagination_selectors = [
            "button[aria-label*='Next']",
            "a[aria-label*='Next']",
            "button[aria-label*='page']",
            "a[aria-label*='page']",
            "[data-testid*='pagination']",
            "[data-testid*='next']",
            "button:contains('Next')",
            "button:contains('More')",
            "button:contains('Load')",
            ".pagination",
            ".next-page"
        ]
        
        for selector in pagination_selectors:
            try:
                elements = driver.find_elements(By.CSS_SELECTOR, selector)
                if elements:
                    print(f"{selector}: 找到 {len(elements)} 个分页元素")
                    for elem in elements:
                        try:
                            text = elem.text or elem.get_attribute("aria-label") or "无文本"
                            print(f"  文本: '{text}'")
                        except:
                            pass
            except:
                pass
        
        # 尝试滚动并观察变化
        print("\n=== 滚动测试 ===")
        initial_cards = driver.find_elements(By.CSS_SELECTOR, "article[data-test='property-card']")
        print(f"滚动前房源数: {len(initial_cards)}")
        
        # 滚动到底部
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(3)
        
        after_scroll_cards = driver.find_elements(By.CSS_SELECTOR, "article[data-test='property-card']")
        print(f"滚动后房源数: {len(after_scroll_cards)}")
        
        # 检查页面高度变化
        height = driver.execute_script("return document.body.scrollHeight")
        print(f"页面总高度: {height}px")
        
        # 等待用户观察
        print("\n=== 手动观察时间 ===")
        print("浏览器将保持打开30秒，请手动观察页面...")
        print("请检查:")
        print("1. 页面上实际显示了多少个房源？")
        print("2. 是否有'加载更多'或分页按钮？")
        print("3. 滚动时是否会加载新内容？")
        
        time.sleep(30)
        
    except Exception as e:
        print(f"调试过程中发生错误: {e}")
    finally:
        print("调试完成，关闭浏览器")
        driver.quit()

if __name__ == "__main__":
    debug_zillow_page() 
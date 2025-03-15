import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from collections import defaultdict
import re
from typing import List, Tuple

class YouTubeCommentDonationsScraper:
    """
    A class to scrape YouTube comments for donation amounts and sum them by currency.
    """

    def __init__(self, url: str):
        self.url = url
        self.driver = self.setup_driver()
        self.unknown_currencies = []  # 存儲找不到的貨幣標示

    def setup_driver(self):
        """Sets up the Selenium WebDriver."""
        chrome_options = Options()
        chrome_options.add_argument("--headless")  # 無頭模式，不開啟瀏覽器
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")

        service = ChromeService(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)
        return driver

    def fetch_page(self):
        """Fetches the YouTube comments section."""
        self.driver.get(self.url)

        # 確保頁面加載
        try:
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )
        except:
            print("❌ 無法加載 YouTube 頁面")
            return ""

        # **滾動頁面來確保留言區載入**
        for _ in range(15):  # 增加滾動次數
            self.driver.find_element(By.TAG_NAME, "body").send_keys(Keys.END)
            time.sleep(3)  # 等待留言加載

        return self.driver.page_source

    def extract_donations(self) -> List[Tuple[str, float]]:
        """Extracts donation amounts and their currencies from the YouTube comments."""
        donations = []
        self.unknown_currencies.clear()  # 清除前一次的未知貨幣記錄

        # **找到所有超級留言的金額**
        try:
            elements = self.driver.find_elements(By.XPATH, "//span[@id='comment-chip-price']")
            if not elements:
                print("⚠️ 沒有找到任何超級留言的金額")
                return []

            for elem in elements:
                raw_text = elem.text.strip()  # e.g., "HK$2,000.00", "AU$500", "$3,000.00", "MYR 479.90", "￦79,000", "SGD 19.98"

                # **如果 `raw_text` 是空的，則跳過**
                if not raw_text:
                    continue

                # **檢測貨幣類型**
                currency = None  # 預設不設定，避免誤判
                if "NT$" in raw_text or "TWD" in raw_text:
                    currency = "TWD"
                elif "US$" in raw_text:
                    currency = "USD"
                elif "HK$" in raw_text:
                    currency = "HKD"
                elif "AU$" in raw_text:  # **新增澳元**
                    currency = "AUD"
                elif "€" in raw_text:
                    currency = "EUR"
                elif "¥" in raw_text and not raw_text.startswith("￦"):  # 確保是日圓，不是韓元
                    currency = "JPY"
                elif "￦" in raw_text:  # **新增韓元 (KRW)**
                    currency = "KRW"
                elif "£" in raw_text:
                    currency = "GBP"
                elif "MYR" in raw_text:  # **新增馬來西亞令吉**
                    currency = "MYR"
                elif "SGD" in raw_text:  # **新增新加坡幣**
                    currency = "SGD"
                
                # **確保只有當沒有任何明確幣別時，才判定為 TWD**
                if currency is None and raw_text.startswith("$"):
                    currency = "TWD"  # **改成台幣**

                # **如果仍然無法辨識貨幣，記錄原始文本**
                if currency is None and raw_text not in self.unknown_currencies:
                    self.unknown_currencies.append(raw_text)

                # **移除貨幣符號與 HTML 空格**
                clean_amount = re.sub(r'[^\d.]', '', raw_text)

                try:
                    amount = float(clean_amount)
                    if amount > 0.0:  # 過濾掉 0.0
                        donations.append((currency, amount))
                except ValueError:
                    continue  # 如果轉換失敗，跳過

        except Exception as e:
            print(f"❌ 抓取捐款金額時發生錯誤: {e}")

        return donations

    def get_donation_amounts(self):
        """Main method to get donation amounts and sum them by currency."""
        self.fetch_page()
        return self.extract_donations()

    def close(self):
        """Closes the WebDriver."""
        self.driver.quit()

if __name__ == "__main__":
    start_time = time.time()  # **記錄開始時間**
    
    video_url = "https://www.youtube.com/watch?v=kOZWQgtqps4"
    scraper = YouTubeCommentDonationsScraper(video_url)
    donations = scraper.get_donation_amounts()
    scraper.close()
    
    end_time = time.time()  # **記錄結束時間**
    execution_time = end_time - start_time  # **計算總運算時間**

    # **顯示各幣值**
    if donations:
        print("💰 各幣值總金額:")
        currency_totals = defaultdict(float)
        for currency, amount in donations:
            currency_totals[currency] += amount
        
        for currency, total in currency_totals.items():
            print(f"   {currency}: {total:.2f}")

    # **列出找不到的幣值**
    if scraper.unknown_currencies:
        print("\n⚠️ 未知幣值 (未加總):")
        for unknown in scraper.unknown_currencies:
            print(f"   {unknown}")
    else:
        print("\n✅ 所有幣值皆已識別，無未知貨幣！")

    # **顯示運行時間**
    print(f"\n⏳ 總運算時間: {execution_time:.2f} 秒")

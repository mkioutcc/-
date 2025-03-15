# -*- coding: utf-8 -*-
"""
Created on Wed Mar  5 16:00:00 2025

@author: User
"""
#抓取ptt文章標題

import requests
from bs4 import BeautifulSoup
url = "https://www.ptt.cc/bbs/Gossiping/index.html"

# 設定 headers（PTT 需要帶 User-Agent）
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
}

response = requests.get(url, headers=headers)

if response.status_code == 200:
    soup = BeautifulSoup(response.text, "lxml")
    
    # 找到所有標題
    titles = soup.find_all("div", class_="title")

    for title in titles:
        link = title.a
        if link:
            print(f"標題: {link.text} | 連結: https://www.ptt.cc{link['href']}")
else:
    print(f"請求失敗，狀態碼：{response.status_code}")



#requests.get(url, headers=headers) → 下載 HTML 內容
#BeautifulSoup(response.text, "lxml") → 解析 HTML
#soup.find_all("tag", class_="classname") → 查找指定標籤
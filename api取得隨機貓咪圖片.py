# -*- coding: utf-8 -*-
"""
Created on Wed Mar  5 16:03:34 2025

@author: User
"""

import requests

# API 端點
url = "https://api.thecatapi.com/v1/images/search"

# 發送 GET 請求
response = requests.get(url)

# 確保請求成功
if response.status_code == 200:
    data = response.json()  # 解析 JSON 回應
    print("貓咪圖片網址:", data[0]["url"])
else:
    print(f"請求失敗，狀態碼：{response.status_code}")



#API 回應通常是 JSON 格式，用 response.json() 來解析
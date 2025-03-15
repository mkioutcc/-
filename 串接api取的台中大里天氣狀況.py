# -*- coding: utf-8 -*-
"""
Created on Wed Mar  5 16:27:34 2025

@author: User
"""

import requests

# API 端點
url = "https://api.open-meteo.com/v1/forecast"

# 傳送參數（指定經緯度）
params = {
    "latitude": 24.143171,  # 台中大里的緯度
    "longitude": 120.679882,  # 台中大里的經度
    "current_weather": True
}

# 發送 GET 請求
response = requests.get(url, params=params)

# 確保請求成功
if response.status_code == 200:
    data = response.json()  # 解析 JSON
    weather = data["current_weather"]
    
    print(f"溫度: {weather['temperature']}°C")
    print(f"風速: {weather['windspeed']} km/h")
    print(f"天氣狀況: {weather['weathercode']}")
else:
    print(f"請求失敗，狀態碼：{response.status_code}")

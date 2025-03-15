import requests
import json

# 使用 WeatherAPI (https://www.weatherapi.com/) 作為替代 API
API_KEY = "54adaf7002fb4fe2814131223250503"
BASE_URL = "http://api.weatherapi.com/v1/current.json"

def get_weather(city):
    """
    透過 WeatherAPI 查詢指定城市的天氣。
    :param city: 城市名稱 (如 Taipei, Tokyo, New York)
    :return: 字典類型的天氣資訊
    """
    params = {
        "key": API_KEY,
        "q": city,
        "lang": "zh"  # 以繁體中文顯示
    }
    try:
        response = requests.get(BASE_URL, params=params)
        response.raise_for_status()  # 如果發生 HTTP 錯誤則拋出異常
        data = response.json()
        if "current" in data:
            return data
        else:
            print("Error: No weather data found for the specified city.")
            return None
    except requests.exceptions.RequestException as e:
        print(f"Error fetching weather data: {e}")
        return None

def display_weather(data):
    """
    解析並顯示天氣資訊。
    :param data: API 回傳的天氣數據 (JSON 格式)
    """
    if not data:
        print("無法獲取天氣資訊，請檢查城市名稱或 API 設定。")
        return
    
    city = data.get("location", {}).get("name", "未知城市")
    country = data.get("location", {}).get("country", "未知國家")
    temp = data.get("current", {}).get("temp_c", "N/A")
    weather_desc = data.get("current", {}).get("condition", {}).get("text", "N/A")
    humidity = data.get("current", {}).get("humidity", "N/A")
    wind_speed = data.get("current", {}).get("wind_kph", "N/A")
    
    print(f"城市: {city}, {country}")
    print(f"天氣: {weather_desc}")
    print(f"溫度: {temp}°C")
    print(f"濕度: {humidity}%")
    print(f"風速: {wind_speed} km/h")

if __name__ == "__main__":
    city_name = input("請輸入城市名稱 (如 Taipei, Tokyo, New York): ")
    weather_data = get_weather(city_name)
    display_weather(weather_data)

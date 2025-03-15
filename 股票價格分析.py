import requests
import pandas as pd
import matplotlib.pyplot as plt
import time
import yfinance as yf

# 查詢即時股價的函式 (使用 Yahoo Finance)
def get_real_time_stock_price(symbol, market="US"):
    """
    透過 Yahoo Finance API 取得即時股價。
    :param symbol: 股票代號 (如 AAPL, TSLA, GOOG, 0050.TW)
    :param market: 市場類型 (US 為美股，TW 為台股)
    :return: 當前股價 (float)，若查詢失敗則回傳 None
    """
    if market == "TW":
        symbol += ".TW"  # 台股格式 (如 0050 變成 0050.TW)
    
    stock = yf.Ticker(symbol)
    data = stock.history(period="1d")
    
    if not data.empty:
        return data["Close"].iloc[-1]  # 取得最近的收盤價
    else:
        print("Error: Invalid stock symbol or no data available.")
        return None

# 查詢歷史股價的函式 (使用 Yahoo Finance)
def get_historical_stock_data(symbol, market="US"):
    """
    透過 Yahoo Finance API 取得股票的歷史價格數據。
    :param symbol: 股票代號
    :param market: 市場類型 (US 為美股，TW 為台股)
    :return: Pandas DataFrame，包含每日的股價數據
    """
    if market == "TW":
        symbol += ".TW"
    
    stock = yf.Ticker(symbol)
    data = stock.history(period="6mo")  # 取得最近6個月的數據
    
    if not data.empty:
        return data
    else:
        print("Error: Unable to fetch historical stock data.")
        return None

# 繪製股價走勢圖
def plot_stock_price(df, symbol):
    """
    使用 Matplotlib 繪製股價歷史走勢圖。
    :param df: 包含歷史股價的 Pandas DataFrame
    :param symbol: 股票代號
    """
    if df is None or df.empty:
        print("No data available for plotting.")
        return
    
    plt.figure(figsize=(10, 5))
    plt.plot(df.index, df['Close'], label=f"{symbol} Closing Price", color='blue')
    plt.xlabel("Date")
    plt.ylabel("Price (USD)")
    plt.title(f"{symbol} Stock Price History")
    plt.legend()
    plt.grid()
    plt.savefig("stock_chart.png")  # 儲存圖表
    plt.show()

# 設定通知系統，監測股價變化
def monitor_stock_price(symbol, threshold, market="US"):
    """
    持續監測股票價格，當股價低於指定閾值時發出通知。
    :param symbol: 股票代號
    :param threshold: 觸發警報的價格 (float)
    :param market: 市場類型 (US 為美股，TW 為台股)
    """
    print(f"Monitoring {symbol}... Alert if price drops below {threshold}")
    while True:
        price = get_real_time_stock_price(symbol, market)
        if price is not None:
            print(f"Current price: {price}")
            if price < threshold:
                print(f"⚠️ ALERT: {symbol} dropped below {threshold}! Current Price: {price}")
                break  # 停止監測
        else:
            print("Error retrieving stock price. Retrying in 60 seconds...")
        time.sleep(60)  # 每 60 秒檢查一次股價

if __name__ == "__main__":
    # 1. 讓使用者輸入股票代碼
    stock_symbol = input("Enter stock symbol (e.g., AAPL, TSLA, GOOG, 0050 for TW stocks): ")
    
    # 2. 讓使用者選擇市場
    market_type = input("Enter market type (US for US stocks, TW for Taiwan stocks): ").upper()
    if market_type not in ["US", "TW"]:
        print("Invalid market type. Defaulting to US.")
        market_type = "US"
    
    # 3. 取得該股票的歷史股價數據
    historical_data = get_historical_stock_data(stock_symbol, market_type)
    
    # 4. 若成功取得數據，則繪製股價走勢圖
    if historical_data is not None:
        plot_stock_price(historical_data, stock_symbol)
    else:
        print("Error fetching historical data. Please check the stock symbol and try again.")
    
    # 5. 讓使用者設定警報閾值
    try:
        alert_price = float(input("Set price alert threshold: "))
        # 6. 開始監測股價，當股價低於閾值時發送警報
        monitor_stock_price(stock_symbol, alert_price, market_type)
    except ValueError:
        print("Invalid input for price threshold. Please enter a numeric value.")

"""
程式流程:
1. 使用者輸入股票代碼 (如 AAPL, TSLA, GOOG, 0050 for Taiwan stocks)。
2. 使用者選擇市場 (US 美股, TW 台股)。
3. 透過 Yahoo Finance API 取得該股票的歷史價格數據，並繪製股價走勢圖。
4. 使用者輸入警報價格閾值。
5. 程式開始監測即時股價，若股價低於警報閾值則發出警報。
6. 監測過程每 60 秒執行一次，直到達到警報條件。
7. 增加台股支援，股票代碼自動加上 .TW。
8. 修正 KeyError: '4. close'，改為 'Close' (Yahoo Finance 的標準欄位)。
9. 增加檢查機制，確保數據有效後才繪製圖表，並存檔避免 GUI 顯示問題。
"""
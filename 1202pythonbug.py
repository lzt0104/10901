import network, urequests
from machine import Pin, I2C
from ssd1306 import SSD1306_I2C

oled = SSD1306_I2C(128, 64, I2C(scl=Pin(5), sda=Pin(4)))

ssid = "ChatBot"
pw = "12345678"
key = "f159f81df48581cb123e091c7cfa490e"

stock_name = "AAPL" # 欲查詢的股票名稱

# 產生查詢網址
url = "http://api.marketstack.com/v1/eod?access_key=" + key +"&limit=1&symbols="
+ stock_name

print("連接 WiFi...")
wifi = network.WLAN(network.STA_IF)
wifi.active(True)
wifi.connect(ssid, pw)
while not wifi.isconnected():
pass
print("已連上")

response = urequests.get(url)

if response.status_code == 200:

parsed = response.json()
print("JSON 資料查詢成功:\n")

# 取得第 1 筆股票資料
stock = parsed["data"][0]

# 取得資料中的特定項目
name = stock["symbol"]
price = str(stock["close"]) + "USD"

trade_time = stock["date"]

# 在編輯器輸出資料
print("公司名稱: " + name)
print("股價: " + price)
print("最後交易時間: " + trade_time)

# 在 OLED 模組顯示資料
oled.fill(0)
oled.text("Stock: " + name, 0, 0)
oled.text("$: " + price, 0, 16)
oled.text("Last trade time:", 0, 32)
oled.text(trade_time, 0, 48)
oled.show()

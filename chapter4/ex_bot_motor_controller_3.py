import time # ---（※1）
import pantilthat

pantilthat.light_mode(pantilthat.WS2812) # NeoPixelsStick8はWS2812 ---（※2）
pantilthat.light_type( 1 ) # RGBで設定初期化 ---（※3）

# 目の設定 ネオピクセルLEDの制御 2つのLED指定 ---（※4）
def neopixels_face():
    pantilthat.set_pixel(1, 50, 50, 50)
    pantilthat.set_pixel(6, 50, 50, 50)
    pantilthat.show()

# ネオピクセルLEDの消灯 ---（※5）
def neopixels_off():
    pantilthat.clear()
    pantilthat.show()

if __name__ == "__main__":
    neopixels_face()
    time.sleep(3)
    neopixels_off()
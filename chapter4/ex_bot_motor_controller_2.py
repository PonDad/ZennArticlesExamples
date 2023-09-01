import time # ---(※1)
import pantilthat

pantilthat.light_mode(pantilthat.WS2812) # NeoPixelsStick8はWS2812 ---(※2)
pantilthat.light_type( 1 ) # RGBで設定初期化 ---(※3)

# ネオピクセルLEDの制御 8つのLED全て指定 ---(※4)
def neopixels_all(r, g, b):
    pantilthat.set_all(r, g, b)
    pantilthat.show()

# ネオピクセルLEDの消灯 ---(※5)
def neopixels_off():
    pantilthat.clear()
    pantilthat.show()

if __name__ == "__main__":
    neopixels_all(50, 50, 50)
    time.sleep(3)
    neopixels_all(0, 50, 0)
    time.sleep(3)
    neopixels_off()

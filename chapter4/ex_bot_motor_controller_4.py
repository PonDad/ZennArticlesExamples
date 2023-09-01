import time, math # ---(※1)
import pantilthat

pantilthat.light_mode(pantilthat.WS2812) # NeoPixelsStick8はWS2812 ---(※2)
pantilthat.light_type( 1 ) # RGBで設定初期化 ---(※3)

# speskコマンド実施中 目を点滅させる
def neopixels_speak_flash_timeout():
    time_start = time.perf_counter()
    time_end = 0

    while True:
        brightness = (math.sin(time_end*4)+1) /2 # sin波の波形をプラスのみ計算  ---(※4)
        print(brightness)

        red, green, blue = 50, 50, 50  # ベースの色 (白)   ---(※5)
        red = int(brightness * red)  # ベースの色に明るさを乗算  ---(※6)
        green = int(brightness * green)
        blue = int(brightness * blue)

        pantilthat.set_pixel(1, red, green, blue)
        pantilthat.set_pixel(6, red, green, blue)
        pantilthat.show()

        time.sleep(0.1)  # 0.1秒ごとに明るさを更新   ---(※7)
        pantilthat.clear()
        time_end = time.perf_counter() - time_start
        if time_end > 5: # 5秒で終了  ---(※8)
            
            pantilthat.show()
            break

if __name__ == "__main__":
    neopixels_speak_flash_timeout()

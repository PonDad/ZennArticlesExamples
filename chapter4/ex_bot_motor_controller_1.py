import time # ---（※1）
import pantilthat

# パンチルトモーター制御 ｰpan tilt とも -90 ~ 90 ---（※2）
def pan_tilt(pan, tilt):
    pantilthat.pan(pan)
    pantilthat.tilt(tilt)

# マイクロサーボSG90では60°動かすのに0.1秒
# パンチルトモーターをゆっくり動かす speed=10 前後で調整
def pan_tilt_slow(pan, tilt, speed):

    start_pan = pantilthat.get_pan() # ---（※3）
    start_tilt = pantilthat.get_tilt()
    print("start_pan: ",start_pan, " start_tilt: ",start_tilt)

    move_pan = (pan - start_pan) / 100 # ---（※4）
    move_tilt = (tilt - start_tilt)  / 100
    print("move_pan: ", move_pan, " move_tilt: ", move_tilt)

    cnt = 0 # ---（※5）
    while True:
        pan_tilt(start_pan + move_pan*cnt, start_tilt + move_tilt*cnt) # ---（※6）
        cnt += 1
        if cnt == 100: # ---（※7）
            break
        else:
            pass
        time.sleep(0.001 * speed) # ---（※8）

if __name__ == "__main__":
    pan_tilt(0, -90)
    time.sleep(0.5)
    pan_tilt(0, 0)
    time.sleep(0.5)
    pan_tilt_slow(0,-90, 10)
    pan_tilt_slow(0,0,10)
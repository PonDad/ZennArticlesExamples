'''
ex_bot_voice_synthesizer.py

aquestalkpiを使用して合成音声を出力する音声合成プログラムです。
「霊夢」と「魔理沙」両方の音声を利用できるようにしています。
speak()関数とspeak_popen()関数により、同期、非同期の音声再生を提供します。
'''

import subprocess # ---(※1)
from pathlib import Path

# 音声合成して再生（再生が完了するまで待機）---(※2)
def speak(text, num):
    AquesTalkPi = str(Path("aquestalkpi/AquesTalkPi").resolve())
    speak_cmd = "echo " + text + " | " + AquesTalkPi + " -b -v f" + str(num) + " -f - | aplay"
    subprocess.run(speak_cmd,shell=True)

# 音声合成して再生（非同期再生）---(※3)
def speak_popen(text, num):
    AquesTalkPi = str(Path("aquestalkpi/AquesTalkPi").resolve())
    speak_p_cmd = "echo " + text + " | " + AquesTalkPi + " -b -v f" + str(num) + " -f - | aplay"
    subprocess.Popen(speak_p_cmd,shell=True)

# 通知音を再生 ---(※4)
def notification():
    notification_wav = str(Path("data/notificationx4.wav").resolve())
    print(notification_wav)
    aplay_cmd = "aplay " + notification_wav
    subprocess.run(aplay_cmd,shell=True)
    
if __name__ == "__main__":
    notification()
    speak("テストです", 1)
    speak("テストです", 2)
    speak_popen("テストです", 1)
    speak("テストです", 2)
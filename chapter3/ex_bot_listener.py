'''
ex_bot_listener.py

ウェイクワードを認識してサウンドを鳴らし、コマンド入力を待機する音声認識プログラムです。
コマンドが入力されると適切なコマンド名を返し、終了コマンドが入力されると音声入力を終了します。
'''

import json
from pathlib import Path

from vosk import Model, KaldiRecognizer  ---(※1)
import pyaudio

# Jsonファイルからウェイクワードとコマンドの配列を読み込む ---(※2)
with open(Path("data/command_data.json"), "rb") as f:
    data = json.load(f)

WAKE = data["wake"]
EXIT = data["exit"]

# Voskモデルの読み込み ---(※3)
model = Model(str(Path("vosk-model-small-ja-0.22").resolve()))

# マイクの初期化
recognizer = KaldiRecognizer(model, 16000)
mic = pyaudio.PyAudio()

# voskの設定 ---(※4)
def engine():
    stream = mic.open(format=pyaudio.paInt16,
                       channels=1, 
                       rate=16000, 
                       input=True, 
                       frames_per_buffer=8192)
    # ストリーミングデータを読み取り続けるループ---(※5)
    while True:
        stream.start_stream()
        try:
            data = stream.read(4096)
            if recognizer.AcceptWaveform(data):
                result = recognizer.Result()
                # jsonに変換---(※5)
                response_json = json.loads(result) 
                print("🖥️ SYSTEM: ", response_json)
                response = response_json["text"].replace(" ","")
                return response
            else:
                pass
        except OSError:
            pass

# ウェイクワード待機をlistening コマンド待機をhearingと設定 ---(※6)
listening = True
hearing = False

# listeningをループして音声認識 ウェイクワード認識でhearingループする
def bot_listen_hear():
    # グローバル変数 ---(※7)
    global listening, hearing
    
    if hearing == True: print("🖥️ SYSTEM: ","-"*22, "GPTに話しかけてください","-"*22)
    else: print("🖥️ SYSTEM: ","-"*22, "ウェイクワード待機中","-"*22)
    # listeningループ ---(※8)
    while listening:
        response = engine()
        if response in WAKE:
            listening = False
            hearing = True
            print("🖥️ SYSTEM: ","-"*22, "GPTに話しかけてください","-"*22)
        # 空白の場合はループを途中で抜ける  ---(※9)
        elif response.strip() == "":
            continue
        else:
            pass
    # hearingループ ---(※10)
    while hearing:
        response = engine()
        if response in EXIT:
            listening = True
            hearing = False
        # 空白の場合はループを途中で抜ける  ---(※11)
        elif response.strip() == "":
            continue
        else:
            pass
        return response 

if __name__ == "__main__":
    try:
        while True:
            # bot_listen_hear関数を実施してレスポンスを得る  ---(※12)
            user_input = bot_listen_hear()
            print("😀 USER: ",user_input)

            # ロボットの返信を設定  ---(※13)
            robot_reply = "回答テストです"
            print("🤖 GPT: ", robot_reply)
    except KeyboardInterrupt:
        # ctrl+c でループ終了  ---(※14)
        print("🖥️ SYSTEM: プログラムを終了します")

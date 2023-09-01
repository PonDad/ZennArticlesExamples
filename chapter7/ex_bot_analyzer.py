'''
bot_analyzer.py

音声認識で受け取ったコマンドを解析し、適切な応答を行う解析プログラムです。
ボイスアシスタントロボットの機能を制御するため、顔認識、時刻取得、モーター制御などの関数を呼び出します。
'''

from pathlib import Path # ---(※1)
import json, datetime
from ex_bot_wio_node import get_wio

# Jsonファイルからコマンドの配列を読み込む ---(※2)
with open(Path("data/command_data.json"), "rb") as f:
    data = json.load(f)

COMMAND = data["command"]

# コマンドを解析して適切な応答を行う関数 ---(※3)
def analyze(user_input):
    try:
        for word, phrases in COMMAND.items(): # ---(※4)
            command = "unknown"  # 初期値を "unknown" に設定
            for phrase in phrases:
                if user_input in phrase:
                    command = word
                    break  # 一致した場合にループを終了
            if command != "unknown":
                break  # コマンドが一致した場合に外側のループも終了

        if command == "unknown": # ---(※5)
            robot_reply =  "ごめんなさいよく分かりません"

        elif command == "greeting": # ---(※6)
            robot_reply = "ゆっくり霊夢です ゆっくりしていってね"

        elif command == "day_now": # ---(※7)
            # 現在時刻を取得して合成音声で出力
            day_now = datetime.datetime.today().strftime("%-Y年%-m月%-d日")
            robot_reply = "今日の日付は" + day_now + "です"

        elif command == "time_now": # ---(※8)
            # 現在時刻を取得して合成音声で出力
            time_now = datetime.datetime.now().strftime("%-H時%-M分")
            robot_reply = "現在時刻は" + time_now + "です"

        elif command == "room_data": # ---(※9)
            room_data = get_wio()
            robot_reply = "リビングの 気温は" + str(room_data[0]) + "度 湿度は" + str(room_data[1]) + "% 不快指数は" + str(room_data[2]) + " 明るさは" + str(room_data[3]) + "ルクス です"

        elif command == "pachira_data": # ---(※10)
            room_data = get_wio()
            robot_reply = "パキラの水分は" + str(room_data[4]) + "% です"

        elif command == "exit": # ---(※11)
            robot_reply = "会話を終了しました"

        else:
            pass

        return robot_reply

    except TypeError:
        pass

if __name__ == "__main__":
    print(analyze("今日の日付は"))
    print(analyze("今何時"))
    print(analyze("部屋の気温は"))
    print(analyze("パキラの水分は"))
    
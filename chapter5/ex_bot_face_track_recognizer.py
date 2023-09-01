'''
bot_face_track_recognizer.py

カメラ映像を取得し、顔を検出して認識する顔追跡システムのボット用スクリプトです
カメラで顔を検出し、顔の特徴を抽出して辞書と比較し、顔認識を行います
また、顔の中心を捉えてカメラのパンとチルトを制御し、顔の追跡も行います
'''

import cv2 # ---（※1）
import numpy as np
import time
from pathlib import Path
from collections import Counter

# カメラのクラスを定義 ---（※2）
class Camera():
    def __init__(self):
        self.cap = cv2.VideoCapture(0) 
        self.cap.set(3, 640)  
        self.cap.set(4, 480)

    def get_frame(self):
        ret, frame = self.cap.read()
        if ret: 
            return frame
        else:
            print("カメラからのフレーム取得に失敗しました。")
            return None

    def release_camera(self):
        self.cap.release()

def face_recognize(): # ---（※3）
    # モデルの読み込み
    face_detector_weights = str(Path("dnn_models/yunet.onnx").resolve())
    face_detector = cv2.FaceDetectorYN_create(face_detector_weights, "", (0, 0))

    # 顔識別モデルを読み込む
    face_recognizer_weights = str(Path("dnn_models/face_recognizer_fast.onnx").resolve())  # 顔認識用のweights
    face_recognizer = cv2.FaceRecognizerSF_create(face_recognizer_weights, "")

    COSINE_THRESHOLD = 0.363

    # 特徴を読み込み特徴量辞書をつくる ---（※4）
    dictionary = []
    files = Path("face_dataset").glob("*.npy")
    for file in files:
        feature = np.load(file)
        user_id = Path(file).stem
        dictionary.append((user_id, feature))

    # 特徴を辞書と比較してマッチしたユーザーとスコアを返す関数
    def match(recognizer, feature1, data_directory):
        for element in data_directory:
            user_id, feature2 = element
            score = recognizer.match(feature1, feature2, cv2.FaceRecognizerSF_FR_COSINE)
            if score > COSINE_THRESHOLD:
                return True, (user_id, score)
        return False, ("", 0.0)
    
    recognized_ids =[]
    
    cam = Camera()  # カメラオブジェクトを作成 ---（※5）

    time_start = time.perf_counter()
    time_end = 0

    while True: # ---（※6）
        frame = cam.get_frame()  # カメラからフレームを取得
        frame = cv2.flip(frame, -1)  # カメラ画像の上下を入れ替える

        # 入力サイズを指定する
        height, width, _ = frame.shape
        face_detector.setInputSize((width, height))

        # 顔を検出する
        _, faces = face_detector.detect(frame)
        faces = faces if faces is not None else []

        # 検出した顔のバウンディングボックスとランドマークを描画する
        frame_output = frame.copy()

        for face in faces:
            # 顔を切り抜き特徴を抽出する
            aligned_face = face_recognizer.alignCrop(frame, face)
            feature = face_recognizer.feature(aligned_face)

            # 辞書とマッチングする ---（※7）
            result, user = match(face_recognizer, feature, dictionary)

            # マッチングしたらボックスとテキストの色を変える
            if result is True:
                color = (0,255,0)
            else:
                color = (255,255,255)

            # バウンディングボックス
            x, y, w, h = list(map(int, face[:4]))
            thickness = 1
            cv2.rectangle(frame_output, (x, y), (x + w, y + h), color, thickness, cv2.LINE_AA)

            # ランドマーク（右目、左目、鼻、右口角、左口角）
            landmarks = list(map(int, face[4:len(face)-1]))
            landmarks = np.array_split(landmarks, len(landmarks) / 2)
            for landmark in landmarks:
                radius = 3
                thickness = -1
                cv2.circle(frame_output, landmark, radius, color, thickness, cv2.LINE_AA)
            
            # 認識の結果を描画する
            id, score = user if result else ("unknown", 0.0)
            text = "{0} ({1:.2f})".format(id, score)
            position = (x, y - 10)
            font = cv2.FONT_HERSHEY_SIMPLEX
            scale = 0.6
            thickness = 1
            cv2.putText(frame_output, text, position, font, scale, color, thickness, cv2.LINE_AA)

            # マッチングしたらIDを一度だけ追加する ---（※8）
            if result:
                recognized_ids.append(id)

            break
        
        if frame is not None:
            cv2.imshow("face detection", frame_output)

        time_end = time.perf_counter() - time_start  # ---（※9）
        if time_end > 5:
            break

        key = cv2.waitKey(1)
        if key == ord('q'):
            break

    cam.release_camera()   # カメラを解放   ---（※10）
    cv2.destroyAllWindows()
    return Counter(recognized_ids).most_common()[0][0]   # ---（※11）

if __name__ == '__main__':
    recognized_id = face_recognize()
    print(recognized_id)
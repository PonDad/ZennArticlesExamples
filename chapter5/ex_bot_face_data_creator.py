'''
bot_face_data_creator.py

ボイスアシスタントの顔認証と年齢性別データを作成するためのスクリプトです
カメラからユーザーの顔を検出し、顔画像を収集して特徴量を抽出し、性別と年齢を推論してJSONファイルに保存します
顔認証システムのトレーニングやデータ収集に使用します
'''

import cv2 # ---(※1)
import numpy as np
import json
from pathlib import Path

# カメラのクラスを定義 ---(※2)
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
            print("🖥️ SYSTEM: カメラからのフレーム取得に失敗しました。")
            return None
        

    def release_camera(self):
        self.cap.release()

# jsonファイルを作成する関数 ---(※3)
def save_json(id, name, image, feature, gender, age, category, interested):
    user = {id:{
        "id": id,
        "name": name,
        "image": image,
        "feature": feature,
        "gender": gender,
        "age": age,
        "category": category,
        "interested": interested
    }
    }

    isempty = Path("data/user_data.json").stat().st_size == 0

    if isempty is True:
        with open(Path("data/user_data.json"), "w") as file:
            json.dump(user, file, ensure_ascii=False, indent=4)
    else:
        with open(Path("data/user_data.json")) as file:
            load_user = json.load(file)

        save_user = dict(load_user, **user)
        
        with open(Path("data/user_data.json"), 'w') as file:
            json.dump(save_user, file, ensure_ascii=False, indent=4)

def face_date_create(): # ---(※4)
    # 顔認識モデルの読み込み
    face_detector_weights = str(Path("dnn_models/yunet.onnx").resolve())
    face_detector = cv2.FaceDetectorYN_create(face_detector_weights, "", (0, 0))

    # 顔識別モデルを読み込む
    face_recognizer_weights = str(Path("dnn_models/face_recognizer_fast.onnx").resolve())
    face_recognizer = cv2.FaceRecognizerSF_create(face_recognizer_weights, "")

    # 年齢識別モデルを読み込む
    ageProto = str(Path("dnn_models/age_deploy.prototxt").resolve())
    ageModel = str(Path("dnn_models/age_net.caffemodel").resolve())

    # 性別識別モデルを読み込む
    genderProto = str(Path("dnn_models/gender_deploy.prototxt").resolve())
    genderModel = str(Path("dnn_models/gender_net.caffemodel").resolve())

    MODEL_MEAN_VALUES = (78.4263377603, 87.7689143744, 114.895847746)
    ageList = ['(0-2)', '(4-6)', '(8-12)', '(15-20)', '(25-32)', '(38-43)', '(48-53)', '(60-100)']
    genderList = ['male', 'female']

    # DNNネットワークに接続
    ageNet = cv2.dnn.readNet(ageModel, ageProto)
    genderNet = cv2.dnn.readNet(genderModel, genderProto)

    # CPU使用を指定
    ageNet.setPreferableBackend(cv2.dnn.DNN_TARGET_CPU)
    genderNet.setPreferableBackend(cv2.dnn.DNN_TARGET_CPU)

    # ユーザーデータの初期化
    user_id = ""
    user_name = ""
    user_image = ""
    user_feature = ""
    user_gender = ""
    user_age = ""
    user_category = ""
    user_interested = ""

    # ユーザー名、ユーザーIDの入力 ---(※5)
    print("🖥️ SYSTEM: ユーザー名をひらがな(またはカタカナ)で入力してEterキーを押してください")
    user_name = input("> ")
    print("🖥️ SYSTEM: ユーザーIDをアルファベット(正規表現)で入力してEnterキーを押してください")
    user_id = input("> ")
    print("🖥️ SYSTEM: 興味のあることをひとつ入力してEnterキーを押してください")
    user_interested = input("> ")
    print("🖥️ SYSTEM: 画像データを 撮影します\n撮影はSキーを押してください\n終了はQキーを押してください")

    cam = Camera()  # カメラオブジェクトを作成 ---(※6)

    while(True): # ---(※7)
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
            # バウンディングボックス
            x, y, w, h = list(map(int, face[:4]))
            color = (255, 255, 255)
            thickness = 1
            cv2.rectangle(frame_output, (x, y), (x + w, y + h), color, thickness, cv2.LINE_AA)

            # ランドマーク(右目、左目、鼻、右口角、左口角)
            landmarks = list(map(int, face[4:len(face)-1]))
            landmarks = np.array_split(landmarks, len(landmarks) / 2)
            for landmark in landmarks:
                radius = 3
                thickness = -1
                cv2.circle(frame_output, landmark, radius, color, thickness, cv2.LINE_AA)
            
        # 画像を表示する
        cv2.imshow("face data create", frame_output)
        key = cv2.waitKey(10)

        # sキーでシャッターを切り、DNNモデルを使用しデータを取る ---(※8)
        if key == ord('s'):
            # 検出された顔を切り抜く
            aligned_faces = []
            if faces is not None:
                for face in faces:
                    aligned_face = face_recognizer.alignCrop(frame, face)
                    aligned_faces.append(aligned_face)

            # 画像を保存する
            for i, aligned_face in enumerate(aligned_faces):
                user_image = user_id + ".jpg"
                cv2.imwrite((str(Path("face_dataset/" + user_image))), aligned_face)
                cv2.imshow("aligned_face", aligned_face)
            
                # 特徴を抽出する
                aligned_face_img = cv2.imread(str(Path("face_dataset/" + user_image)))
                face_feature = face_recognizer.feature(aligned_face_img)

                # 特徴を保存する
                user_feature = user_id + ".npy"
                dictionary = Path("face_dataset/" + user_feature)
                np.save(dictionary , face_feature)

            # 性別を推論する
            blob = cv2.dnn.blobFromImage(frame_output, 1.0, (227, 227), MODEL_MEAN_VALUES, swapRB=False)
            genderNet.setInput(blob)
            genderPreds = genderNet.forward()
            user_gender = genderList[genderPreds[0].argmax()]
            print("🖥️ SYSTEM: 性別 : {}, conf = {:.3f}".format(user_gender, genderPreds[0].max()))

            # 年齢を推論する
            ageNet.setInput(blob)
            agePreds = ageNet.forward()
            user_age = ageList[agePreds[0].argmax()]
            print("🖥️ SYSTEM: 年齢 : {}, conf = {:.3f}".format(user_age, agePreds[0].max()))

            # カテゴリー分類
            if user_age in ageList[:4]:
                if user_gender == "male":
                    user_category = "boy"
                else:
                    user_category = "girl"
            elif user_age in ageList[4: 8]:
                if user_gender == "male":
                    user_category = "man"
                else:
                    user_category = "woman"

            # jsonファイルを保存する  ---(※9)
            save_json(user_id, user_name, user_image, user_feature, user_gender, user_age, user_category, user_interested)
            print("🖥️ SYSTEM: ユーザーデータ\n"
                  f"ID: {user_id} \n"
                  f"名前: {user_name} \n"
                  f"写真: {user_image} \n"
                  f"特徴量: {user_feature} \n"
                  f"性別: {user_gender} \n"
                  f"年齢: {user_age} \n"
                  f"分類: {user_category} \n"
                  f"興味: {user_interested} \n"
                  "を保存しました")

        if key == ord('q'):
            print("🖥️ SYSTEM: 撮影を終了します")
            break

    cam.release_camera()  # カメラを解放   ---(※10)
    cv2.destroyAllWindows()

if __name__ == '__main__':
    face_date_create()

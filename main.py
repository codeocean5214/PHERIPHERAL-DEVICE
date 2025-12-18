import cv2
import numpy as np
import time
import multiprocessing
from multiprocessing import Process, Value
import tensorflow as tf 
from Pheripherals.models import SecuritySystem 
from Pheripherals.models import Environment as EnvSystem  

MODEL_PATH = "mobilefacenet.tflite"
EMBEDDINGS_FILE = "embeddings.npy"
THRESHOLD = 0.5
FACE_STATUS = Value('i', 0)

def sensor_process(face_status):
    security = SecuritySystem(pir_pin=17) 
    env = EnvSystem()
    print("✅ Sensors Active...")
    
    while True:
        if security.motion_detected:
            who_is_it = face_status.value
            
            if who_is_it == 1:
                data = env.get_data()
                print(f"👋 Welcome Aditya! Body Temp: {data['body_temp']:.1f}°C")
                security.unlock_door()
                time.sleep(5)
                security.lock_door()
            elif who_is_it == 2:
                print("⛔ Alert: Unknown person at the door!")

        if int(time.time()) % 10 == 0:
            data = env.get_data()
            print(f"🌍 Status: {data['room_temp']:.1f}°C | {data['humidity']:.1f}% Hum")
            time.sleep(1.1)

        time.sleep(0.1)

def face_process(face_status):
    interpreter = tf.lite.Interpreter(model_path=MODEL_PATH)
    interpreter.allocate_tensors()
    input_idx = interpreter.get_input_details()[0]['index']
    output_idx = interpreter.get_output_details()[0]['index']
    
    try:
        data = np.load(EMBEDDINGS_FILE, allow_pickle=True).item()
        known_embeddings = np.array(data["embeddings"])
    except FileNotFoundError:
        print("❌ Error: embeddings.npy not found. Run the register script first!")
        return

    cap = cv2.VideoCapture(0)
    cap.set(3, 640)
    cap.set(4, 480)
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    print("✅ Camera Active...")

    while True:
        ret, frame = cap.read()
        if not ret: 
            continue

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.1, 4)
        current_status = 0

        for (x, y, w, h) in faces:
            face_img = frame[y:y+h, x:x+w]
            if face_img.size == 0: 
                continue
            
            img = cv2.resize(face_img, (112, 112))
            img = (img - 127.5) / 128.0
            img = img.astype(np.float32)
            img = np.expand_dims(img, axis=0)

            interpreter.set_tensor(input_idx, img)
            interpreter.invoke()
            emb = interpreter.get_tensor(output_idx)[0]

            diff = known_embeddings - emb
            dist = np.linalg.norm(diff, axis=1)
            min_dist = np.min(dist)

            if min_dist < THRESHOLD:
                current_status = 1
            else:
                current_status = 2

        face_status.value = current_status
        
        cv2.imshow('Face System', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'): 
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    p1 = Process(target=sensor_process, args=(FACE_STATUS,))
    p2 = Process(target=face_process, args=(FACE_STATUS,))

    p1.start()
    p2.start()

    p1.join()
    p2.join()
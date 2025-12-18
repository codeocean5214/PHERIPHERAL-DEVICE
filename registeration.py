import cv2 
import numpy as np 
import tensorflow as tf  

Model_path = "mobilefacenet.tflite"
save_location  = "embeddings.npy"
interpreter = tf.lite.Interpreter(model_path=Model_path)
interpreter.allocate_tensors()
input_indx  = interpreter.get_input_details()[0]['index']
ouput_idx   = interpreter.get_output_details()[0]['index']
Samples = 10
cap = cv2.VideoCapture(0)
cap.set(3,640)
cap.set(4,480)
#importing default face haar cascade classifier from open cv
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
embeddings  =  []
count = 0 
while count <Samples : 
    ret,frame = cap.read()
    if not ret :
        continue 
    gray  = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray,1.1,4)
    for(x,y,w,h) in faces : 
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
        
        cv2.putText(frame, f"Samples: {count}/{Samples}", (10, 30), 
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        cv2.putText(frame, "Press SPACE to capture", (10, 70), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
    cv2.imshow("Register Face", frame)
    key = cv2.waitKey(1) & 0xFF
    
    if key == ord(' ') and len(faces) > 0:
        x, y, w, h = faces[0]
        face_img = frame[y:y+h, x:x+w]
        
        img = cv2.resize(face_img, (112, 112))
        img = (img - 127.5) / 128.0
        img = img.astype(np.float32)
        img = np.expand_dims(img, axis=0)

        interpreter.set_tensor(input_indx, img)
        interpreter.invoke()
        emb = interpreter.get_tensor(ouput_idx)[0]
        
        embeddings.append(emb)
        count += 1
        print(f" Captured {count}/{Samples}")
        
    elif key == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
if len(embeddings) > 0 : 
    name = input("Enrer the name of the person: ") 
    data = { 
        "name" : name , 
        "embeddings" : embeddings
    }
    np.save(save_location,data)
    print(f"face data saved successfully at {save_location}")
else: 
    print("No face data captured.")


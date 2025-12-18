import os 
import requests  
#we are importing a pretrained deep learning model for face registrations 
#i have added the cusotm model that conv2d based along sequentail as well but annotating it could take a lot of time

Model_url = "https://github.com/MCarlomagno/FaceRecognitionAuth/raw/master/assets/mobilefacenet.tflite"
Model_path  = "mobilefacenet.tflite" 
if not os.path.exists(Model_path): 
    try : 
        r= requests.get(Model_url) 
        with open(Model_path,"wb") as f  : 
            f.write(r.content)
            print("Model downloaded successfully.")
    except Exception as e:
        print(f"Error is  : {e}")

    
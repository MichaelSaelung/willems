from cv2 import exp
import constan
import json
import numpy as np
import dataSet
from tensorflow.keras.models import load_model
from constan import region

def imagePrediction(REGION = region.CANINE):
    try:
        newImg = dataSet.createNewImage(imgPath = f'{constan.PATH_TESTING}{REGION}{constan.IMAGE_TYPE}')
        model = load_model(f'{constan.MODEL_FOLDER}{REGION}')
        arr_y_pred = model.predict(newImg)
        arr_y_pred = arr_y_pred.reshape(-1,) # Merubah 1D array
        y_pred = np.argmax(arr_y_pred)
        #y_class_pred = chr(y_pred +  constan.ASCII_A)
        return y_pred
    except:pass

# mencari Nilai klasifikasi dari gigi berdasarkan constantan perempuan atau laki2 dalam region yang sama
def imageClasification(gender, region, y_pred=None):
    with open(constan.TOOTH_JSON_PATH, 'r') as file:
        toothNumber = json.load(file)
        gender = "boy" if constan.gender.MALE == gender else "girl"
        toothNumber = toothNumber[gender][region][y_pred] if y_pred is not None else 0.00
        with open(constan.RESULT_JSON_PATH, 'r') as file:
            try: 
                Tooth = json.load(file) 
            except: 
                Tooth = {}
            
            Tooth[region] = toothNumber
            with open(constan.RESULT_JSON_PATH, 'w') as file: 
                json.dump(Tooth, file)    
    return toothNumber

def agePrediction():
    with open(constan.RESULT_JSON_PATH, 'r') as file:
        results = json.load(file)
        dictArray = list(results.values())
        finalRsuls = np.sum(dictArray)
    with open(constan.AGE_PREDICTION_JSON_PATH, 'w') as file: 
        json.dump({'agePrediction': finalRsuls}, file)
    return finalRsuls
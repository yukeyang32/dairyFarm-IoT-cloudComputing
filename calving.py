# This script generates the  file
# with the init and run functions needed to 
# operationalize the estrus prediction

import pickle
import json
import pandas
import joblib
from sklearn.linear_model import Ridge
from azureml.core.model import Model
from azureml.train.automl import AutoMLConfig

def init():
    global model
    # this is a different behavior than before when the code is run locally, even though the code is the same.
    model_path = Model.get_model_path('model.pkl')
    # deserialize the model file back into a sklearn model
    model = joblib.load(model_path)
    

def run(input_str):
    try:
        input_json = json.loads(input_str)
        input_df = pandas.DataFrame([[input_json['animal_activity'],input_json['temp_without_drink_cycles']]])
        pred = model.predict(data)
        pred = np.floor(pred[0])
        print("Prediction is ", pred)
    except Exception as e:
        result = str(e)
    
    if pred == 1:
        input_json['label']="> 24hrs"
    elif pred == 2:
        input_json['label']="> 12hrs"
    else:
        input_json['label']="> 6hrs"
        
    return [json.dumps(input_json)]

if __name__ == "__main__":
    test_sample = json.dumps({'data': [
    {
    "animal_activity": 10.31,
    "temp_without_drink_cycles": 40.22
    }
    ]})
    run(test_sample)

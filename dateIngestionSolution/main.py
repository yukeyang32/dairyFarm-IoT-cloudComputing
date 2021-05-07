# This script generates the  file
# with the init and run functions needed to 
# operationalize the estrus prediction

import pickle
import json
import pandas
import numpy as np
from sklearn.externals import joblib
from sklearn.linear_model import Ridge
from azureml.core.model import Model







def init():
    global model
    # this is a different behavior than before when the code is run locally, even though the code is the same.
    model_path = Model.get_model_path('model.pkl')
    # deserialize the model file back into a sklearn model
    model = joblib.load(model_path)
    
# input_sample = pd.DataFrame(data=[{
#     "animal_activity": 10.31,
#     "temp_without_drink_cycles": 40.22
# }])
# output_sample = np.array([1.19759538])

# note you can pass in multiple rows for scoring
def run(input_str):
    try:
        input_json = json.loads(input_str)
        input_df = pandas.DataFrame(data=[{
            "animal_activity": input_json['data'][0]['animal_activity'],
            "temp_without_drink_cycles": input_json['data'][0]['temp_without_drink_cycles']
        }])
        pred = model.predict(input_df)
        pred = np.floor(pred[0])
        print("Prediction is ", pred)
    except Exception as e:
        result = str(e)
    

    if pred == 0:
        input_json['calving_time']= "calving time > 36 hours"
    
    if pred == 1:
        input_json['calving_time']= "24 hours < calving time <= 36 hours"
    
    if pred == 2:
        input_json['calving_time']= "12 hours < calving time <= 24 hours"
    
    if pred == 3:
        input_json['calving_time']= "6 hours < calving time <= 12 hours"

        
    return [json.dumps(input_json)]
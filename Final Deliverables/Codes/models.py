import pickle

import requests


def local_model(values):
    model = pickle.load(open("models/RandomForestClassifier.pkl", "rb"))
    prediction = model.predict(values)
    return prediction

def ibm_model(values):
    API_KEY = "5tGOtJzbhIRefjroHYS7z0y9Gk-H88ygMXkj-lQ9UX0E"
    token_response = requests.post('https://iam.cloud.ibm.com/identity/token', data={"apikey": API_KEY, "grant_type": 'urn:ibm:params:oauth:grant-type:apikey'})
    mltoken = token_response.json()["access_token"]
    url = 'https://us-south.ml.cloud.ibm.com/ml/v4/deployments/f631af67-dd41-4357-a8c7-0a5c122c21f1/predictions?version=2022-11-11'
    array_of_input_fields = ["Ph", "Hardness", "Solids", "Turbidity"]

    payload_scoring = {"input_data": [{"fields": [array_of_input_fields], "values": [values]}]}
    response_scoring = requests.post(url, json=payload_scoring, headers={'Authorization': 'Bearer ' + mltoken})
    res = response_scoring.json()
    return res['predictions'][0]['values'][0][0]
    
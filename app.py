import pandas as pd
from flask import Flask, jsonify
import flask
import pickle
import pyrebase
from collections import OrderedDict
import urllib

config={
    "apiKey": "AIzaSyDeFLJFr2aqcAK40nZOmBtEDNYij49yyAk",
    "authDomain": "healdon-916dd.firebaseapp.com",
    "databaseURL": "https://healdon-916dd.firebaseio.com",
    "projectId": "healdon-916dd",
    "storageBucket": "healdon-916dd.appspot.com",
    "messagingSenderId": "756073662506",
    "appId": "1:756073662506:web:2f4cb2e5e93f1d4b9d1b53"
}
firebase=pyrebase.initialize_app(config)


model = pickle.load(open('model.pkl','rb'))

# app
app = Flask(__name__)

# routes
@app.route('/', methods=['POST'])

def predict():
    # get data
    data = flask.request.get_json(force=True)
    db = firebase.database()
    u_id="Utkarsh5470"
    game_data_dict = db.child("users").child(u_id).child("test").child("game_score").get()
    dict1=game_data_dict.val()
    print(dict1)
    
    d1=dict(OrderedDict(dict1))
    l1=list(d1.keys())
    l2=list(d1.values())
    df=pd.DataFrame(l2,l1)
    df=df.T

    data_df = df[["speed", "speed_time", "memory", "memory_time", "calculation", "calculation_time", "attention", "attention_time", "path_tracing_time"]]
        
    
    # convert data into dataframe
    #data.update((x, [y]) for x, y in data.items())
    #data_df = pd.DataFrame.from_dict(data)


    # predictions
    result = model.predict(data_df)

    
    
    # send back to browser
    output = {'Model_Prediction': str(int(result[0]))}
    json_data = json.dumps(output).encode()
    
    request = urllib.request.Request("https://healdon-916dd.firebaseio.com/users/"+u_id+"/test/game_score.json", data=json_data, method="PATCH")
    try:
        loader = urllib.request.urlopen(request)
    except urllib.error.URLError as e:
        message = json.loads(e.read())
    
    # return data
    return jsonify(results=output)

if __name__ == '__main__':
    app.run(port = 5000, debug=True,use_reloader=False)
    
    
    

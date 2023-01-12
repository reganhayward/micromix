#--------------------------------
#
# Heatmap designed by Titus Ebbecke 2021-2023
# Modifications by Regan Hayward 2023
#
#--------------------------------

from pymongo import MongoClient
from flask import Flask, request, Response
import os
from flask_cors import CORS
from bson.json_util import loads, dumps, ObjectId
import pandas as pd
from io import BytesIO

#client = MongoClient(os.environ.get("testend"))
client = MongoClient() # For offline testing.
db = client.test
visualizations = db.visualizations

DEBUG = True
app = Flask(__name__)
CORS(app)

#Testing
app.config.from_object(__name__)
app.config['CORS_HEADERS'] = 'Content-Type'
app.config['FLASK_DEBUG']=1
app.config['DEBUG'] = True

#Testing different config options - in the end not needed
#app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
#cors = CORS(app, resources={r"/*":{"origins": "*"}})
#cors = CORS(app, resources={r"/*":{"cors_allowed_origins": "*"}})
# CORS(app, resources={r'/*':{'origins': 'http://localhost:8080',"allow_headers": "Access-Control-Allow-Origin"}})
#CORS(app, resources={r'/*':{'origins': 'http://127.1.1.1:8081',"allow_headers": "Access-Control-Allow-Origin"}})


@app.route('/status', methods=['GET'])
def status():
  return 'alive'

@app.route('/config', methods=['GET', 'POST'])
def respond_config():
  #Print the ID to terminal
  print("DB Config=",request.form['url'])
  #Checking of a URL with DB id has been passed
  if request.form['url'] != 'undefined':
    #id identified and convert to ObjectId object
    print("id found in DB")
    db_entry_id = ObjectId(loads(request.form['url']))
    #Find the object id in the visualisations database
    db_entry = db.visualizations.find_one({"_id": db_entry_id})
    #Check if the df is filtered or transformed
    try:
      #Converts entry from .json into pandas parquet
      data = pd.read_parquet(BytesIO(db_entry['filtered_dataframe'])).to_json(orient='records')
    except:
      #The mockup db_entry stores the empty transformed_dataframe as a list, so don't convert that one.
      #Convert transformed into pandas parquet
      if type(db_entry['transformed_dataframe']) == bytes: 
        data = pd.read_parquet(BytesIO(db_entry['transformed_dataframe'])).to_json(orient='records')
      else:
        data = db_entry['transformed_dataframe']
  
  print("Data successfully passed to heatmap!")
  return Response(data, mimetype="application/json")
  

client.close()

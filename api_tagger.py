import flask
from flask import request
import pandas as pd 
import numpy as np
import h2o

from dncp import get_release, get_ocds_record
from data import get_pd_dataframe

app = flask.Flask(__name__)
app.config["DEBUG"] = True

@app.route('/home', methods=['GET'])
def api_home():
    
    id = request.args.get('id')
    
    record = get_ocds_record(id)
    ocid = record['records'][0]['compiledRelease']['id']
    release = get_release(ocid)
    compiled_release = release['releases'][0]
    df = get_pd_dataframe(compiled_release)

    pred_class = h2o.mojo_predict_pandas(df, "mojo.zip", 
                               genmodel_jar_path = 'jar/h2o-genmodel.jar', 
                               classpath = 'jar/*',
                               verbose = True
                               )
    pred_dict = pred_class.to_dict(orient = "records")[0]
    return {
        'prediction': pred_dict,
        'compiledRelease': compiled_release,
        'rows': 'df',
    }

@app.errorhandler(404)
def page_not_found(e):
    return "<h1>404</h1><p>No se encuentra el recurso.</p>", 404

app.run()

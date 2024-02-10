import flask
from flask import request
import h2o

from dncp import get_release, get_ocds_record
from data.frame import get_pd_dataframe

app = flask.Flask(__name__)
# app.config["DEBUG"] = True

@app.route('/', methods=['GET'])
def index():
	h2o.init()
	html =  '''
					<h1>Complaint scorer</h1>
					<p>Score de protestas -  API</p>
					<form action="/api/v1/predict">
                    
					ID licitacion: <input type="number" name="id" />
					<input type="submit" method="get" value="Calcular score"  />
                    <ul>
                    <li>
                        Ejemplo sin protestas: <a href="/api/v1/predict?id=415916" style="margin-right:5px;">415916</a> 
                        <a href="https://www.contrataciones.gov.py/licitaciones/adjudicacion/415916-construccion-ampliacion-edificio-conacyt-1/resumen-adjudicacion.html">Ver en pag. DNCP</a>
                    </li>
                    <li>
                        Ejemplo con protestas: <a href="/api/v1/predict?id=367291" style="margin-right:5px;">367291</a>
                        <a href="https://www.contrataciones.gov.py/licitaciones/convocatoria/367291-lpn-97-2019-adquisicion-certificados-servicios-ambientales-compensacion-ejecucion-ob-1.html#impugnaciones">Ver en pag. DNCP</a>
                    </li>
                    </ul>
					
				'''
	return html

@app.route('/api/v1/predict', methods=['GET'])
def api_home():
    h2o.init()
    id = request.args.get('id')
    
    record = get_ocds_record(id)
    if 'records' not in record:
        return {
			'error': 'No se encontró la licitación'
		}
    
    ocid = record['records'][0]['compiledRelease']['id']
    release = get_release(ocid)
    compiled_release = release['releases'][0]
    df = get_pd_dataframe(compiled_release)

    pred_class = h2o.mojo_predict_pandas(df, "GBM_grid_1_AutoML_1_20230927_154916_model_8.zip", 
                               genmodel_jar_path = 'jar/gbm-h2o-genmodel.jar', 
                               classpath = 'jar/*',
                               verbose = True
                               )
    
    pred_dict = pred_class.to_dict(orient = "records")[0]
    risk_percentage = pred_dict['True'] * 100
    return {
        # 'prediction': pred_dict,
        'riskScore': risk_percentage,
        'riskLevel': 'High' if risk_percentage >= 75 else 'Medium' if risk_percentage >= 50 else 'Low',
        'parameters': {
            'High': '>= 75%',
            'Medium': '>= 50%',
		}
        # 'compiledRelease': compiled_release,
        # 'rows': 'df',
    }

@app.errorhandler(404)
def page_not_found(e):
    return "<h1>404</h1><p>No se encuentra el recurso.</p>", 404

# if __name__ == "__main__"
# app.run()

if __name__ == "__main__":
    # serve(app, listen='*:80')
    app.run(debug=True, host='0.0.0.0', port=80)

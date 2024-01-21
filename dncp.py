import requests
import json

api_url = "https://www.contrataciones.gov.py/datos/api/v3/doc"

# /tender/415916
def get_tender(tender_id: int):
	try:
		response = requests.get(f'{api_url}/tender/{tender_id}')
		return json.loads(response.text)
	except Exception as e:
		print(e)
		return None
	# return response.json()

def get_planning(tender_id: int):
	# https://www.contrataciones.gov.py/datos/api/v3/doc/planning/415916
	try:
		response = requests.get(f'{api_url}/planning/{tender_id}')
		return json.loads(response.text)
	except Exception as e:
		print(e)
		return None
	
def get_awards(tender_id: int):
	# https://www.contrataciones.gov.py/datos/api/v3/doc/award/415916
	try:
		response = requests.get(f'{api_url}/award/{tender_id}')
		return json.loads(response.text)
	except Exception as e:
		print(e)
		return None
	
def search_processes(tender_id):
	# https://www.contrataciones.gov.py/datos/api/v3/doc/search/processes?q=licitacion
	try:
		response = requests.get(f'{api_url}/search/processes?ocid={tender_id}')
		return json.loads(response.text)
	except Exception as e:
		print(e)
		return None
	
def get_release(release_id):
	# https://www.contrataciones.gov.py/datos/api/v3/doc/release/415916
	try:
		response = requests.get(f'{api_url}/ocds/releases/id/{release_id}')
		return json.loads(response.text)
	except Exception as e:
		print(e)
		return None

def get_releases(release_id):
	# https://www.contrataciones.gov.py/datos/api/v3/doc/release/415916
	try:
		response = requests.get(f'{api_url}/ocds/releases/ocid/{release_id}')
		return json.loads(response.text)
	except Exception as e:
		print(e)
		return None
	
def get_ocds_record(id: int):
	# https://www.contrataciones.gov.py/datos/api/v3/doc/ocds/record/415916
	try:
		response = requests.get(f'{api_url}/ocds/record/{id}')
		return json.loads(response.text)
	except Exception as e:
		print(e)
		return None
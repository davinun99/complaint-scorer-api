from data.general_utils import count_length
from data.custom_pickle_methods import TenderDocumentsDocumentTypeDetail, TenderNotifiedSuppliers, TenderTenderers, TendersubmissionMethodDetails
from data.custom_pickle_methods import TenderEligibilityCriteria, TenderMainProcurementCategoryDetails, TenderProcuringEntityId, TenderProcuringEntityName
from data.custom_pickle_methods import BuyerId, BuyerName, AwardSuppliers
from data.custom_pickle_methods import N5TenderItemsClass, N4PlanningItemsClass, N3TenderItemsClass, N3PlanningItemsClass, N4PlanningItemsClass
from data.custom_pickle_methods import ContactInvestmentProjectsId, PartiesRoles, N1PlanningItemsClass, N2PlanningItemsClass, N1TenderItemsClass
from data.custom_pickle_methods import N2TenderItemsClass, N1_1TenderItemsClass, N1_1PlanningItemsClass, ContactInvestmentProjectsId

########## CUSTOM UTILS METHODS
def count_ammenments(ocds_data: dict):
	count = 0
	if 'contracts' in ocds_data:
		for contract in ocds_data['contracts']:
			if 'amendments' in contract:
				count += len(contract['amendments'])
	return count

def has_no_enquiry_answer(ocds_data: dict):
	if 'tender' in ocds_data:
		if 'enquiries' in ocds_data['tender']:
			for enquiry in ocds_data['tender']['enquiries']:
				if 'answer' not in enquiry:
					return False
	return True

def has_ammentment(ocds_data: dict):
	if 'contracts' in ocds_data:
		for contract in ocds_data['contracts']:
			if 'amendments' in contract:
				return True
	return False

def proveed_notificados_co(ocds_data: dict):
	result = False
	if 'tender' in ocds_data:
		if 'procurementMethodDetails' in ocds_data['tender']:
			if ocds_data['tender']['procurementMethodDetails'] != 'Concurso de Ofertas':
				result = False
	if result:
		if 'notifiedSuppliers' in  ocds_data['tender']:
			result = count_length(ocds_data['tender']['notifiedSuppliers']) < 5
	return result

def has_amount_missing(ocds_data: dict):
	if 'tender' in ocds_data:
		if 'value' in ocds_data['tender']:
			if type(ocds_data['tender']['value']['amount']) == int:
				return False
	return True

def has_criteria_missing(ocds_data: dict):
	if 'tender' in ocds_data:
		if 'awardCriteria' in ocds_data['tender']:
			if 'criteria' in ocds_data['tender']['awardCriteria']:
				return False
	return True

def get_contract_amount(ocds_data: dict) -> list[int]:
	amount_by_currency = {
		"USD": 0,
		"PYG": 0,
	}
	if 'contracts' in ocds_data:
		for contract in ocds_data['contracts']:
			if('value' in contract):
				currency = contract['value']['currency']
				amount_by_currency[currency] += contract['value']['amount']
	return [amount_by_currency["PYG"], amount_by_currency["USD"]]

def get_award_amount (ocds_data: dict) -> list[int]:
	amount_by_currency = {
		"USD": 0,
		"PYG": 0,
	}
	if 'awards' in ocds_data:
		for award in ocds_data['awards']:
			if('value' in award):
				currency = award['value']['currency']
				amount_by_currency[currency] += award['value']['amount']
	return [amount_by_currency["PYG"], amount_by_currency["USD"]]

def get_tender_doc_type_count(ocds_data: dict, doc_type: str) -> int:
	count = 0
	if 'tender' in ocds_data:
		if 'documents' in ocds_data['tender']:
			for doc in ocds_data['tender']['documents']:
				if 'documentTypeDetails' in doc and doc['documentTypeDetails'] == doc_type:
					count += 1
	return count

def get_tender_doc_type_count_others(ocds_data: dict) -> int:
	count = 0
	if 'tender' in ocds_data:
		if 'documents' in ocds_data['tender']:
			for doc in ocds_data['tender']['documents']:
				if 'documentTypeDetails' in doc and doc['documentTypeDetails'] not in TenderDocumentsDocumentTypeDetail:
					count += 1
	return count

def get_tender_enquiries_respondidos(ocds_data: dict) -> int:
	count = 0
	if 'tender' in ocds_data:
		if 'enquiries' in ocds_data['tender']:
			for enquiry in ocds_data['tender']['enquiries']:
				if 'answer' in enquiry:
					count += 1
	return count

def get_tender_enquiries_porcentaje(ocds_data: dict) -> float:
	if 'tender' in ocds_data:
		if 'enquiries' in ocds_data['tender']:
			return get_tender_enquiries_respondidos(ocds_data) / len(ocds_data['tender']['enquiries']) * 100
	return 0

def get_parties_legal_entity_type_detail(ocds_data: dict, role: str) -> list:
	values_map = ['Persona Física - Bienes y Servicios', 'Persona Física - Servicios Personales', 'S.A.', 'S.R.L.', 'S.A.C.I.', 'S.A.E.C.A.', 'Consorcio', 'Otros', 'S.A.I.C.', 'S.A.C.', 'Sociedad Simple', 'S.A.E.', 'C.I.S.A.', 'Sociedad Civil', 'E.I.R.L.', 'Cooperativas', 'Extranjeras', 'Sucursal', 'C.E.I.S.A.', 'Coaseguro', 'Empresa de Acciones Simplificada', 'Empresa sin fines de lucro', 'Asociación', 'S.A.C.I.G.', 'ADES']
	count_arr = [0] * len(values_map)
	if 'parties' in ocds_data:
		for party in ocds_data['parties']:
			if 'roles' in party:
				print(party['roles'], role, role in party['roles'])
				if 'details' in party and role in party['roles']:
					if 'legalEntityTypeDetail' in party['details']:
						count_arr[values_map.index(party['details']['legalEntityTypeDetail'])] += 1
	return count_arr

def get_awards_doc_type_details(ocds_data: dict):
	map_data = {
		"Informe de Evaluación": 0,
		"Notificación al Oferente": 1,
		"Resolución de Adjudicación": 2,
		"Cuadro Comparativo de Ofertas": 3,
		"Acta de Apertura": 4,
		"Nota de Observacion": 5, 
		"Otros - Exp. por Decreto 5174": 6,
		"Nota de Cancelación Adjudicación": 7,
		"Resolución de Cancelación Adjudicación": 8,
		"Resolución de Ratificación": 9,
		"Nota de Retención Adjudicación": 10,
		"Nota de Contestación": 11,
		"Nota de Observacion Adjudicacion": 12,
		"Orden de Compra o Contrato": 13,
		"Nota al Director": 14,
		"Nota de Suspensión": 15,
		"Nota Rechazo Solicitud de Cancelacion": 16,
		"Nota de Contestacion Adjudicacion": 17,
		"Nota de Contestacion Proveedor Adjudicado": 18,
		"Nota de Observación Proveedor Adjudicado": 19,
		"Nota de Aclaración": 20,
	}
	count_arr = [0] * len(list(map_data))
	if 'awards' in ocds_data:
		for award in ocds_data['awards']:
			if 'documents' in award:
				for doc in award['documents']:
					if 'documentTypeDetails' in doc:
						count_arr[map_data[doc['documentTypeDetails']]] += 1
	return count_arr

def get_tender_notified_suppliers_id(ocds_data: dict) -> int:
	count_arr = [0, 0, 0, 0]
	if 'tender' in ocds_data:
		if 'notifiedSuppliers' in ocds_data['tender']:
			for notified_supplier in ocds_data['tender']['notifiedSuppliers']:
				if notified_supplier['id'] in TenderNotifiedSuppliers[0]:
					count_arr[0] += 1
				elif notified_supplier['id'] in TenderNotifiedSuppliers[1]:
					count_arr[1] += 1
				elif notified_supplier['id'] in TenderNotifiedSuppliers[2]:
					count_arr[2] += 1
				else:
					count_arr[3] += 1
	return count_arr


def get_tender_elegibility_criteria(ocds_data: dict, index: int) -> int:
	if 'tender' in ocds_data:
		if 'eligibilityCriteria' in ocds_data['tender']:
			eligibilityCriteria = ocds_data['tender']['eligibilityCriteria']
			if eligibilityCriteria in TenderEligibilityCriteria[index]:
				return 1
			if len(eligibilityCriteria) != 0 and index == 3:
				return 1
	return 0

def get_tender_main_procurement_methods_details(ocds_data: dict, index: int) -> int:
	if 'tender' in ocds_data:
		if 'mainProcurementMethodDetails' in ocds_data['tender']:
			mainProcurementMethodDetails = ocds_data['tender']['mainProcurementCategoryDetails']
			if mainProcurementMethodDetails in TenderMainProcurementCategoryDetails[index]:
				return 1
			if len(mainProcurementMethodDetails) != 0 and index == 3:
				return 1
	return 0
				

def get_contract_doc_type_details(ocds_data):
	map_data = {
		"Orden de Compra o Contrato": 0,
		"Nota de Aclaración": 1,
		"Nota de Observacion": 2,
		"Nota de Contestación": 3,
		"Resolución Rescisión": 4,
		"Nota de Retención Adjudicación": 5, 
		"CDP Proveedor": 6,
		"Anexo Adjudicación": 7,
		"Nota de Contestacion Proveedor Adjudicado": 8,
		"Nota de Observacion Adjudicacion": 9,
		"Nota de Observación Proveedor Adjudicado": 10,
		"Nota de Contestacion Adjudicacion": 11,
	}
	count_arr = [0] * len(list(map_data))
	if 'contracts' in ocds_data:
		for contract in ocds_data['contracts']:
			if 'documents' in contract:
				for doc in contract['documents']:
					if 'documentTypeDetails' in doc:
						doc_type_details = doc['documentTypeDetails']
						if doc_type_details in map_data:
							ind = map_data[doc_type_details]
							count_arr[ind] += 1
	return count_arr

def get_tender_tenderers(ocds_data):
	count_arr = [0, 0, 0, 0]
	if 'tender' in ocds_data:
		if 'tenderers' in ocds_data['tender']:
			for tenderer in ocds_data['tender']['tenderers']:
				if tenderer['id'] in TenderTenderers[0]:
					count_arr[0] += 1
				elif tenderer['id'] in TenderTenderers[1]:
					count_arr[1] += 1
				elif tenderer['id'] in TenderTenderers[2]:
					count_arr[2] += 1
				else:
					count_arr[3] += 1
	return count_arr

def get_contracts_transactions_count(ocds_data: dict) -> int:
	count = 0
	if 'contracts' in ocds_data:
		for contract in ocds_data['contracts']:
			if 'implementation' in contract:
				if 'transactions' in contract['implementation']:
					count += len(contract['implementation']['transactions'])
	return count

def get_tender_submission_method_details(ocds_data: dict) -> int:
	count_arr = [0, 0, 0, 0]
	if 'tender' in ocds_data:
		if 'submissionMethodDetails' in ocds_data['tender']:
			method_details = ocds_data['tender']['submissionMethodDetails']
			if method_details in TendersubmissionMethodDetails[0]:
				count_arr[0] += 1
			elif method_details in TendersubmissionMethodDetails[1]:
				count_arr[1] += 1
			elif method_details in TendersubmissionMethodDetails[2]:
				count_arr[2] += 1
			else:
				count_arr[3] += 1
	return count_arr

def get_tender_procuring_entity_id(ocds_data: dict, index: int) -> int:
	if 'tender' in ocds_data:
		if 'procuringEntity' in ocds_data['tender']:
			procuring_entity_id = ocds_data['tender']['procuringEntity']['id']
			if procuring_entity_id and index == 3:
				return 1
			elif procuring_entity_id in TenderProcuringEntityId[index]:
				return 1
			
	return 0

def get_tender_procuring_entity_name(ocds_data: dict, index: int) -> int:
	if 'tender' in ocds_data:
		if 'procuringEntity' in ocds_data['tender']:
			procuring_entity_name = ocds_data['tender']['procuringEntity']['name']
			if procuring_entity_name and index == 3:
				return 1
			elif procuring_entity_name in TenderProcuringEntityName[index]:
				return 1
			
	return 0

def get_buyer_id(ocds_data: dict, index: int) -> int:
	if 'buyer' in ocds_data:
		buyer_id = ocds_data['buyer']['id']
		if buyer_id and index == 3:
			return 1
		if buyer_id in BuyerId[index]:
			return 1
	return 0

def get_buyer_name(ocds_data: dict, index: int) -> int:
	if 'buyer' in ocds_data:
		buyer_id = ocds_data['buyer']['id']
		if buyer_id and index == 3:
			return 1
		if buyer_id in BuyerName[index]:
			return 1
	return 0

def get_awards_supplier_id(ocds_data: dict) -> int:
	count_arr = [0, 0, 0, 0]
	if 'awards' in ocds_data:
		for award in ocds_data['awards']:
			if 'suppliers' in award:
				for supplier in award['suppliers']:
					if supplier['id'] in AwardSuppliers[0]:
						count_arr[0] += 1
					elif supplier['id'] in AwardSuppliers[1]:
						count_arr[1] += 1
					elif supplier['id'] in AwardSuppliers[2]:
						count_arr[2] += 1
					else:
						count_arr[3] += 1
	return count_arr
def get_contract_implementation_purchase_orders(ocds_data: dict) -> int:
	count = 0
	if 'contracts' in ocds_data:
		for contract in ocds_data['contracts']:
			if 'implementation' in contract:
				if 'purchaseOrders' in contract['implementation']:
					count += len(contract['implementation']['purchaseOrders'])
	return count

def get_tender_items_classification_id_n5(ocds_data: dict) -> list:
	count_arr = [0, 0, 0, 0]
	if 'tender' in ocds_data:
		if 'items' in ocds_data['tender']:
			for item in ocds_data['tender']['items']:
				if 'classification' in item:
					if 'id' in item['classification']:
						if item['classification']['id'] in N5TenderItemsClass[0]:
							count_arr[0] += 1
						elif item['classification']['id'] in N5TenderItemsClass[1]:
							count_arr[1] += 1
						elif item['classification']['id'] in N5TenderItemsClass[2]:
							count_arr[2] += 1
						else:
							count_arr[3] += 1
	return count_arr

def get_tender_items_classification_id_n3(ocds_data: dict) -> list:
	count_arr = [0, 0, 0, 0]
	if 'tender' in ocds_data:
		if 'items' in ocds_data['tender']:
			for item in ocds_data['tender']['items']:
				if 'classification' in item:
					if 'id' in item['classification']:
						id = item['classification']['id'][0:6]
						if id in N3TenderItemsClass[0]:
							count_arr[0] += 1
						elif id in N3TenderItemsClass[1]:
							count_arr[1] += 1
						elif id in N3TenderItemsClass[2]:
							count_arr[2] += 1
						else:
							count_arr[3] += 1
	return count_arr

def get_planing_items_classification_id_n3(ocds_data: dict) -> list:
	count_arr = [0, 0, 0, 0]
	if 'planning' in ocds_data:
		if 'items' in ocds_data['planning']:
			for item in ocds_data['planning']['items']:
				if 'classification' in item:
					if 'id' in item['classification']:
						id = item['classification']['id'][0:6]
						if id in N3PlanningItemsClass[0]:
							count_arr[0] += 1
						elif id in N3PlanningItemsClass[1]:
							count_arr[1] += 1
						elif id in N3PlanningItemsClass[2]:
							count_arr[2] += 1
						else:
							count_arr[3] += 1
	return count_arr

def get_contracts_investment_projects_id_q(ocds_data: dict) -> list:
	ContactInvestmentProjectsId
	count_arr = [0, 0, 0, 0]
	if 'contracts' in ocds_data:
		for contract in ocds_data['contracts']:
			if 'investmentProjects' in contract:
				if 'id' in contract['investmentProjects']:
					if contract['investmentProjects']['id'] in ContactInvestmentProjectsId[0]:
						count_arr[0] += 1
					elif contract['investmentProjects']['id'] in ContactInvestmentProjectsId[1]:
						count_arr[1] += 1
					elif contract['investmentProjects']['id'] in ContactInvestmentProjectsId[2]:
						count_arr[2] += 1
					else:
						count_arr[3] += 1
	return count_arr


def get_planing_items_classification_id_n4(ocds_data: dict) -> list:
	count_arr = [0, 0, 0, 0]
	if 'planning' in ocds_data:
		if 'items' in ocds_data['planning']:
			for item in ocds_data['planning']['items']:
				if 'classification' in item:
					if 'id' in item['classification']:
						id = item['classification']['id'][0:8]
						if id in N4PlanningItemsClass[0]:
							count_arr[0] += 1
						elif id in N4PlanningItemsClass[1]:
							count_arr[1] += 1
						elif id in N4PlanningItemsClass[2]:
							count_arr[2] += 1
						else:
							count_arr[3] += 1
	return count_arr

def get_tender_items_classification_id_n4(ocds_data: dict) -> list:
	count_arr = [0, 0, 0, 0]
	if 'tender' in ocds_data:
		if 'items' in ocds_data['tender']:
			for item in ocds_data['tender']['items']:
				if 'classification' in item:
					if 'id' in item['classification']:
						id = item['classification']['id'][0:8]
						if id in N4PlanningItemsClass[0]:
							count_arr[0] += 1
						elif id in N4PlanningItemsClass[1]:
							count_arr[1] += 1
						elif id in N4PlanningItemsClass[2]:
							count_arr[2] += 1
						else:
							count_arr[3] += 1
	return count_arr

def get_parties_roles(ocds_data, role: str) -> int:
	count_arr = [0, 0, 0, 0]
	# PartiesRoles
	if 'parties' in ocds_data:
		for party in ocds_data['parties']:
			if 'name' in party:
				party_name = party['name']
				if 'roles' in party and role in party['roles']:
					if party_name in PartiesRoles[role]['firstq_map']:
						count_arr[0] += 1
					elif party_name in PartiesRoles[role]['secondq_map']:
						count_arr[1] += 1
					elif party_name in PartiesRoles[role]['thirdq_map']:
						count_arr[2] += 1
					else:
						count_arr[3] += 1
						
	return count_arr

def get_contract_status(ocds_data: dict, status: str) -> int:
	count = 0
	if 'contracts' in ocds_data:
		for contract in ocds_data['contracts']:
			if 'status' in contract and contract['status'] == status:
				count += 1
	return count

def get_planning_items_class_id_n1_arr(ocds_data: dict) -> list:
	res = [0] * 16
	if 'planning' in ocds_data:
		if 'items' in ocds_data['planning']:
			for item in ocds_data['planning']['items']:
				if 'classification' in item:
					if 'id' in item['classification']:
						id = item['classification']['id'][0:2]
						if id in N1PlanningItemsClass:
							index = N1PlanningItemsClass[id]
							res[index] += 1
						else:
							res[15] += 1
	return res
def get_planning_items_class_id_n1_1_arr(ocds_data: dict) -> list:
	res = [0] * 58
	if 'planning' in ocds_data:
		if 'items' in ocds_data['planning']:
			for item in ocds_data['planning']['items']:
				if 'classification' in item:
					if 'id' in item['classification']:
						id = item['classification']['id'][0:2]
						if id in N1_1PlanningItemsClass:
							index = N1_1PlanningItemsClass[id]
							res[index] += 1
						else:
							res[57] += 1
	return res

def get_planning_items_class_id_n2_arr(ocds_data: dict) -> list:
	res = [0] * 44
	if 'planning' in ocds_data:
		if 'items' in ocds_data['planning']:
			for item in ocds_data['planning']['items']:
				if 'classification' in item:
					if 'id' in item['classification']:
						id = item['classification']['id'][0:4]
						if id in N2PlanningItemsClass:
							index = N2PlanningItemsClass[id]
							res[index] += 1
						else:
							res[43] += 1
	return res
# N2PlanningItemsClass

def get_tender_items_class_id_n1_arr(ocds_data: dict) -> list:
	res = [0] * 13
	if 'tender' in ocds_data:
		if 'items' in ocds_data['tender']:
			for item in ocds_data['tender']['items']:
				if 'classification' in item:
					if 'id' in item['classification']:
						id = item['classification']['id'][0:2]
						if id in N1TenderItemsClass:
							index = N1TenderItemsClass[id]
							res[index] += 1
						else:
							res[12] += 1
	return res
def get_tender_items_class_id_n1_1_arr(ocds_data: dict) -> list:
	res = [0] * 56
	if 'tender' in ocds_data:
		if 'items' in ocds_data['tender']:
			for item in ocds_data['tender']['items']:
				if 'classification' in item:
					if 'id' in item['classification']:
						id = item['classification']['id'][0:2]
						if id in N1_1TenderItemsClass:
							index = N1_1TenderItemsClass[id]
							res[index] += 1
						else:
							res[55] += 1
	return res
def get_tender_items_class_id_n2_arr(ocds_data: dict) -> list:
	res = [0] * 23
	if 'tender' in ocds_data:
		if 'items' in ocds_data['tender']:
			for item in ocds_data['tender']['items']:
				if 'classification' in item:
					if 'id' in item['classification']:
						id = item['classification']['id'][0:4]
						if id in N2TenderItemsClass:
							index = N2TenderItemsClass[id]
							res[index] += 1
						else:
							res[22] += 1
	return res

def get_parties_details_legalEntityTypeDetail(ocds_data: dict, role: str) -> list:
	values_map = ['Persona Física - Bienes y Servicios', 'Persona Física - Servicios Personales', 'S.A.', 'S.R.L.', 'S.A.C.I.', 'S.A.E.C.A.', 'Consorcio', 'Otros', 'S.A.I.C.', 'S.A.C.', 'Sociedad Simple', 'S.A.E.', 'C.I.S.A.', 'Sociedad Civil', 'E.I.R.L.', 'Cooperativas', 'Extranjeras', 'Sucursal', 'C.E.I.S.A.', 'Coaseguro', 'Empresa de Acciones Simplificada', 'Empresa sin fines de lucro', 'Asociación', 'S.A.C.I.G.', 'ADES']
	count_arr = [0] * len(values_map)
	if 'parties' in ocds_data:
		for party in ocds_data['parties']:
			if 'details' in party and 'roles' in party and role in party['roles']:
				if 'legalEntityTypeDetail' in party['details']:
					legal_entity_type = party['details']['legalEntityTypeDetail']
					count_arr[values_map.index(legal_entity_type)] += 1
	return count_arr


def get_parties_details_entity_type(ocds_data: dict, role: str) -> list:
	values_map = ['Municipalidades', 'NO CLASIFICADO', 'Organismos de la Administración Central', 'Entidades Descentralizadas']
	# roles = ['candidate','enquirer','payer', 'payee', 'supplier', 'procuringEntity', 'buyer', 'tenderer', 'notifiedSupplier']
	count_array = [0] * len(values_map)
	if 'parties' in ocds_data:
		parties = ocds_data['parties']
		for party in parties:
			if 'roles' in party:
				roles_llamados = party['roles']
				# será una columna para cada rol
				if role in roles_llamados:
					if 'details' in party:
						detail = party['details']
						if 'entityType' in detail:
							count_array[values_map.index(detail['entityType'])] += 1
            
			
	return count_array

def get_contract_status_details_arr(ocds_data: dict) -> list:
	possible_details = {
		"Adjudicado": 0,
		"Confirmado Orden de Compra": 1,
		"Orden de compra recibida": 2,
		"Orden de compra entregada": 3,
		"Cancelado": 4,
		"Cancelada de la Orden de Compra": 5,
		"Vencida Orden de Compra": 6,
		"Suspendido": 7,
		"Anulado": 8
	}
	arr = [0] * len(list(possible_details))
	if 'contracts' in ocds_data:
		for contract in ocds_data['contracts']:
			if('statusDetails' in contract):
				ind = possible_details[contract['statusDetails']]
				arr[ind] += 1
	return arr

def get_awards_status_details_arr(ocds_data:dict) -> list:
	map_data = {
		"Adjudicado": 0,
		"Confirmado Orden de Compra": 1,
		"Orden de compra recibida": 2,
		"Orden de compra entregada": 3,
		"Cancelado": 4,
		"Vencida Orden de Compra": 5,
		"Cancelada de la Orden de Compra": 6,
		"Suspendido": 7,
		"Anulado": 8,
		"Provisorio de la Orden de Compra": 9,
		"Notificado de la Orden de Compra": 10,
	}
	arr = [0] * len(list(map_data))
	if 'awards' in ocds_data:
		for award in ocds_data['awards']:
			if 'statusDetails' in award:
				ind = map_data[award['statusDetails']]
				arr[ind] += 1
	return arr

def get_awards_status_arr(ocds_data:dict) -> list:
	map_data = {
		"active": 0,
		"cancelled": 1,
		"pending": 2,
		"unsuccessful": 3,
	}
	arr = [0] * len(list(map_data))
	if 'awards' in ocds_data:
		for award in ocds_data['awards']:
			if 'status' in award:
				ind = map_data[award['status']]
				arr[ind] += 1
	return arr

def get_tender_covered_by_arr(ocds_data: dict) -> list:
	map_data = {
		"fonacide": 0,
		"produccion_nacional": 1,
		"urgencia_impostergable": 2,
		"adreferendum": 3,
		"agricultura_familiar": 4,
		"covid_19": 5,
		"almuerzo_escolar": 6,
		"seguridad_nacional": 7,
	}
	
	arr: list[int] = [0] * len(list(map_data))
	if 'tender' in ocds_data and 'coveredBy' in ocds_data['tender']:
		for cover in ocds_data['tender']['coveredBy']:
			ind = map_data[cover]
			arr[ind] += 1

	return arr


def get_contracts_guarantees_obligations_arr(ocds_data: dict) -> list:
	guarantee_type_map_data = {
		"fulfillment": 0,
		"Endoso - Fiel Cumplimiento": 1,
		"Endoso - Anticipo": 2,
		"Accidentes Personales": 3,
		"Todo Riesgos en Zona de Obras": 4,
		"Anticipo": 5,
		"Responsabilidad Civil General": 6,
		'Endoso - Accidentes Personales': 7,
		"Daños a Terceros": 8,
		"Responsabilidad Profesional": 9,
		"Endoso - Todo Riesgos en Zona de Obras": 10,
		"Endoso - Responsabilidad Civil General": 11,
		"Fondo de Reparo": 12,
		"Deshonestidad": 13,
		"Endoso - Daños a Terceros": 14,
		"Endoso - Responsabilidad Profesional": 15,
		"Endoso - Deshonestidad": 16,
		"Endoso - Fondo de Reparo": 17,
	}
	countArr = [0] * len(list(guarantee_type_map_data))
	if 'contracts' in ocds_data:
		for contract in ocds_data['contracts']:
			if'guarantees' in contract:
				for guarantee in contract['guarantees']:
					ind = guarantee_type_map_data[guarantee['obligations']]
					countArr[ind] += 1
	return countArr


def get_contracts_investment_projects_id(ocds_data: dict, index: int) -> int:
	if 'contracts' in ocds_data:
		for contract in ocds_data['contracts']:
			if 'investmentProjects' in contract:
				if 'id' in contract['investmentProjects']:
					if contract['investmentProjects']['id'] in ContactInvestmentProjectsId[index]:
						return 1
				elif index == 3:
					return 1
	return 0
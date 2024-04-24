from data.general_utils import count_length
from data.custom_pickle_methods import TenderDocumentsDocumentTypeDetail, TenderNotifiedSuppliers, TenderTenderers, TendersubmissionMethodDetails, TenderEligibilityCriteria, TenderMainProcurementCategoryDetails, TenderProcuringEntityId, TenderProcuringEntityName, BuyerId, BuyerName, AwardSuppliers
from data.custom_pickle_methods import N5TenderItemsClass, N4PlanningItemsClass, N3TenderItemsClass, N3PlanningItemsClass, N4PlanningItemsClass, ContactInvestmentProjectsId, PartiesRoles, N1PlanningItemsClass

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
						for i in range(15):
							if id in N1PlanningItemsClass:
								index = N1PlanningItemsClass[id]
								res[index] += 1
								break
						else:
							res[15] += 1
	return res

# --- REMAINING---

# parties.details.legalEntityTypeDetail supplier_3	90.5369	0.0222	0.0022

# tender.coveredBy_1	84.7357	0.0207	0.0020
# contracts.guarantees.obligations_1	83.9057	0.0205	0.0020

# planning.items.classification.id.n2_44	81.7232	0.0200	0.0020
# planning.items.classification.id.n2_11	80.4943	0.0197	0.0019

# planning.items.classification.id.n2_26	75.3552	0.0184	0.0018


# parties.details.EntityType buyer_3	69.5061	0.0170	0.0017


# parties.details.legalEntityTypeDetail supplier_1	58.8990	0.0144	0.0014
# parties.details.EntityType procuringEntity_4	58.3922	0.0143	0.0014
# parties.details.legalEntityTypeDetail payee_3	58.2384	0.0143	0.0014
# tender.items.classification.id.n2_1	57.3918	0.0140	0.0014


# tender.items.classification.id.n1_13	56.9272	0.0139	0.0014
# parties.details.legalEntityTypeDetail enquirer_3	56.1901	0.0138	0.0014

# tender.coveredBy_2	55.4019	0.0136	0.0013


# tender.items.classification.id.n2_22	51.7908	0.0127	0.0012
# awards.status_1	51.4833	0.0126	0.0012
# contracts.statusDetails_1	51.3826	0.0126	0.0012

# parties.details.EntityType procuringEntity_3	50.7915	0.0124	0.0012

# parties.details.EntityType buyer_1	49.4325	0.0121	0.0012

# parties.details.EntityType buyer_4	48.5794	0.0119	0.0012


# parties.details.EntityType procuringEntity_1	47.3632	0.0116	0.0011
# parties.details.EntityType payer_3	47.1255	0.0115	0.0011


# contracts.investmentProjects.id q1	45.2154	0.0111	0.0011




# tender.items.classification.id.n1_1_25	41.1033	0.0101	0.0010


# 
# contracts.guarantees.obligations_2	40.1719	0.0098	0.0010

# planning.items.classification.id.n1_1_9	37.2277	0.0091	0.0009
# planning.items.classification.id.n2_1	37.1796	0.0091	0.0009

# tender.items.classification.id.n1_1_1	36.0149	0.0088	0.0009
# tender.items.classification.id.n2_3	35.8347	0.0088	0.0009

# parties.details.legalEntityTypeDetail supplier_4	34.7273	0.0085	0.0008
# parties.details.EntityType payer_4	34.7144	0.0085	0.0008
# parties.details.legalEntityTypeDetail payee_1	34.5656	0.0085	0.0008
# parties.details.legalEntityTypeDetail payee_4	34.1374	0.0084	0.0008
# tender.coveredBy_5	34.1135	0.0083	0.0008
# planning.items.classification.id.n2_2	33.9110	0.0083	0.0008
# tender.items.classification.id.n1_1_21	33.8267	0.0083	0.0008

# planning.items.classification.id.n1_1_39	31.9398	0.0078	0.0008
# tender.items.classification.id.n1_1	31.7712	0.0078	0.0008
# planning.items.classification.id.n1_1_36	31.3219	0.0077	0.0008
# planning.items.classification.id.n1_1_32	30.1865	0.0074	0.0007

# tender.items.classification.id.n1_1_36	29.4745	0.0072	0.0007

# tender.items.classification.id.n1_1_41	29.0564	0.0071	0.0007
# awards.statusDetails_1	29.0442	0.0071	0.0007
# planning.items.classification.id.n1_1_22	28.9872	0.0071	0.0007
# tender.items.classification.id.n1_1_37	28.8278	0.0071	0.0007
# planning.items.classification.id.n2_5	28.6706	0.0070	0.0007
# planning.items.classification.id.n1_1_1	28.5288	0.0070	0.0007

# tender.items.classification.id.n2_17	28.1530	0.0069	0.0007


# planning.items.classification.id.n1_1	27.0247	0.0066	0.0007
# planning.items.classification.id.n1_1_25	26.9987	0.0066	0.0006

# contracts.guarantees.obligations_10	26.6178	0.0065	0.0006

# tender.items.classification.id.n1_1_4	25.6976	0.0063	0.0006
# tender.items.classification.id.n1_1_30	25.3838	0.0062	0.0006
# tender.items.classification.id.n2_6	25.2369	0.0062	0.0006
# parties.details.legalEntityTypeDetail supplier_8	25.0798	0.0061	0.0006
# planning.items.classification.id.n2_32	24.4227	0.0060	0.0006
# tender.items.classification.id.n1_1_18	24.2481	0.0059	0.0006
# planning.items.classification.id.n1_1_23	23.5629	0.0058	0.0006

# planning.items.classification.id.n1_1_21	21.5398	0.0053	0.0005
# tender.items.classification.id.n1_1_24	21.0230	0.0051	0.0005
# planning.items.classification.id.n1_1_17	20.9641	0.0051	0.0005
# parties.details.legalEntityTypeDetail supplier_2	20.4508	0.0050	0.0005
# planning.items.classification.id.n1_1_35	20.3380	0.0050	0.0005
# tender.items.classification.id.n1_1_16	20.3235	0.0050	0.0005

# tender.items.classification.id.n1_1_48	20.1819	0.0049	0.0005
# planning.items.classification.id.n1_1_29	19.9456	0.0049	0.0005
# planning.items.classification.id.n1_1_26	19.9153	0.0049	0.0005
# tender.items.classification.id.n2_2	19.8665	0.0049	0.0005


# tender.items.classification.id.n1_1_15	19.4336	0.0048	0.0005

# planning.items.classification.id.n1_1_19	19.3093	0.0047	0.0005
# tender.items.classification.id.n1_1_45	19.1834	0.0047	0.0005
# tender.items.classification.id.n1_4	19.1500	0.0047	0.0005
# tender.items.classification.id.n1_1_6	19.1473	0.0047	0.0005
# tender.items.classification.id.n1_1_19	19.0835	0.0047	0.0005
# planning.items.classification.id.n2_25	19.0346	0.0047	0.0005
# tender.items.classification.id.n2_21	19.0018	0.0047	0.0005

# tender.items.classification.id.n1_9	17.6333	0.0043	0.0004
# tender.items.classification.id.n1_1_26	17.5980	0.0043	0.0004
# planning.items.classification.id.n1_1_16	17.4628	0.0043	0.0004
# tender.items.classification.id.n1_1_9	17.2494	0.0042	0.0004

# tender.items.classification.id.n1_1_23	17.0656	0.0042	0.0004
# tender.items.classification.id.n2_11	16.8605	0.0041	0.0004
# planning.items.classification.id.n1_1_27	16.6700	0.0041	0.0004
# parties.details.EntityType buyer_2	16.1982	0.0040	0.0004
# planning.items.classification.id.n2_38	15.5572	0.0038	0.0004
# planning.items.classification.id.n2_12	15.4908	0.0038	0.0004
# contracts.guarantees.obligations_3	15.4459	0.0038	0.0004
# tender.items.classification.id.n2_16	15.3482	0.0038	0.0004
# tender.items.classification.id.n1_1_10	15.3355	0.0038	0.0004
# planning.items.classification.id.n2_28	14.5037	0.0035	0.0003
# tender.items.classification.id.n2_20	14.4849	0.0035	0.0003
# planning.items.classification.id.n1_1_24	14.4585	0.0035	0.0003
# tender.items.classification.id.n1_10	14.2062	0.0035	0.0003
# contracts.investmentProjects.id q3	13.9626	0.0034	0.0003
# planning.items.classification.id.n1_1_41	13.9047	0.0034	0.0003
# tender.items.classification.id.n1_1_13	13.8821	0.0034	0.0003
# planning.items.classification.id.n1_1_13	13.6182	0.0033	0.0003
# parties.details.legalEntityTypeDetail payee_2	13.5873	0.0033	0.0003
# planning.items.classification.id.n1_1_3	13.4268	0.0033	0.0003
# contracts.guarantees.obligations_14	13.3917	0.0033	0.0003

# planning.items.classification.id.n1_1_48	13.0610	0.0032	0.0003
# parties.details.legalEntityTypeDetail enquirer_4	12.9762	0.0032	0.0003

# planning.items.classification.id.n1_1_20	12.5356	0.0031	0.0003
# planning.items.classification.id.n2_6	12.4218	0.0030	0.0003

# parties.details.legalEntityTypeDetail enquirer_1	12.3165	0.0030	0.0003
# tender.items.classification.id.n1_1_43	12.1375	0.0030	0.0003
# planning.items.classification.id.n1_1_12	12.0458	0.0029	0.0003
# tender.awardCriteria_ratedCriteria	11.8094	0.0029	0.0003
# planning.items.classification.id.n2_13	11.6454	0.0029	0.0003
# tender.items.classification.id.n2_10	11.6251	0.0028	0.0003
# tender.items.classification.id.n1_2	11.5564	0.0028	0.0003
# Tiempo de Convocatoria CO	11.5323	0.0028	0.0003
# planning.items.classification.id.n1_1_37	11.3662	0.0028	0.0003
# awards.statusDetails_5	11.2291	0.0027	0.0003
# tender.items.classification.id.n1_6	11.0101	0.0027	0.0003
# planning.items.classification.id.n2_21	11.0	0.0027	0.0003
# planning.items.classification.id.n2_18	10.7721	0.0026	0.0003
# tender.statusDetails_Adjudicada	10.7079	0.0026	0.0003
# contracts.guarantees.obligations_4	10.7037	0.0026	0.0003
# planning.items.classification.id.n1_1_4	10.6924	0.0026	0.0003
# tender.items.classification.id.n1_1_31	10.6089	0.0026	0.0003
# tender.items.classification.id.n1_1_11	10.5567	0.0026	0.0003
# contracts.guarantees.obligations_7	10.5516	0.0026	0.0003
# tender.items.classification.id.n1_1_27	10.5373	0.0026	0.0003
# planning.items.classification.id.n1_1_8	10.4855	0.0026	0.0003

# tender.items.classification.id.n1_1_2	10.2633	0.0025	0.0002
# tender.items.classification.id.n1_1_29	10.2324	0.0025	0.0002
# tender.items.classification.id.n1_1_35	10.1280	0.0025	0.0002
# 
# tender.items.classification.id.n1_3	9.9613	0.0024	0.0002
# contracts.guarantees.obligations_5	9.9418	0.0024	0.0002


# contracts.investmentProjects.id q2	9.6662	0.0024	0.0002
# planning.items.classification.id.n1_1_30	9.4596	0.0023	0.0002

# planning.items.classification.id.n1_1_44	9.2963	0.0023	0.0002
# Preguntas Sin Respuesta	9.2762	0.0023	0.0002
# parties.details.legalEntityTypeDetail payee_9	9.1203	0.0022	0.0002
# tender.items.classification.id.n1_5	8.8385	0.0022	0.0002
# planning.items.classification.id.n2_36	8.6659	0.0021	0.0002
# planning.items.classification.id.n2_23	8.6479	0.0021	0.0002
# tender.coveredBy_4	8.6328	0.0021	0.0002
# tender.items.classification.id.n1_7	8.5705	0.0021	0.0002

# planning.items.classification.id.n2_42	8.5042	0.0021	0.0002
# planning.items.classification.id.n2_3	8.4994	0.0021	0.0002
# tender.items.classification.id.n1_1_34	8.3756	0.0020	0.0002

# tender.items.classification.id.n1_1_3	8.1909	0.0020	0.0002
# tender.items.classification.id.n1_1_5	8.1823	0.0020	0.0002
# tender.items.classification.id.n1_1_38	7.8390	0.0019	0.0002
# parties.details.EntityType procuringEntity_2	7.7643	0.0019	0.0002
# planning.items.classification.id.n1_1_43	7.6207	0.0019	0.0002
# tender.items.classification.id.n2_18	7.5834	0.0019	0.0002

# parties.details.legalEntityTypeDetail supplier_5	7.3900	0.0018	0.0002

# tender.coveredBy_6	7.0125	0.0017	0.0002
# parties.details.legalEntityTypeDetail enquirer_6	6.9285	0.0017	0.0002
# parties.details.legalEntityTypeDetail supplier_6	6.9148	0.0017	0.0002
# tender.items.classification.id.n1_1_7	6.7752	0.0017	0.0002
# tender.items.classification.id.n1_1_12	6.7644	0.0017	0.0002
# tender.items.classification.id.n1_12	6.7314	0.0016	0.0002

# tender.items.classification.id.n2_19	6.6951	0.0016	0.0002
# planning.items.classification.id.n1_1_2	6.4101	0.0016	0.0002
# planning.items.classification.id.n1_1_42	6.3331	0.0015	0.0002
# parties.details.EntityType payer_1	6.2328	0.0015	0.0002
# tender.items.classification.id.n1_1_22	6.1786	0.0015	0.0001
# planning.items.classification.id.n1_1_33	6.1402	0.0015	0.0001
# planning.items.classification.id.n1_1_18	6.0182	0.0015	0.0001
# tender.items.classification.id.n1_11	5.9809	0.0015	0.0001
# tender.items.classification.id.n2_13	5.9645	0.0015	0.0001
# planning.items.classification.id.n1_8	5.8471	0.0014	0.0001
# tender.items.classification.id.n1_1_40	5.8164	0.0014	0.0001
# tender.items.classification.id.n1_1_46	5.7642	0.0014	0.0001
# planning.items.classification.id.n2_20	5.6926	0.0014	0.0001

# planning.items.classification.id.n1_1_14	5.5570	0.0014	0.0001
# planning.items.classification.id.n2_8	5.5440	0.0014	0.0001
# planning.items.classification.id.n2_29	5.3910	0.0013	0.0001
# contracts.guarantees.obligations_6	5.3603	0.0013	0.0001
# planning.items.classification.id.n2_30	5.3017	0.0013	0.0001
# tender.items.classification.id.n1_1_33	5.2272	0.0013	0.0001
# planning.items.classification.id.n1_1_28	5.2170	0.0013	0.0001
# planning.items.classification.id.n1_6	5.1957	0.0013	0.0001
# planning.items.classification.id.n2_4	5.1373	0.0013	0.0001
# planning.items.classification.id.n1_1_31	5.1172	0.0013	0.0001
# planning.items.classification.id.n2_33	5.0358	0.0012	0.0001
# tender.items.classification.id.n2_14	5.0326	0.0012	0.0001
# planning.items.classification.id.n1_1_56	5.0113	0.0012	0.0001
# planning.items.classification.id.n1_1_7	4.9590	0.0012	0.0001
# planning.items.classification.id.n2_10	4.9409	0.0012	0.0001
# tender.items.classification.id.n1_1_17	4.9201	0.0012	0.0001

# tender.items.classification.id.n2_15	4.8286	0.0012	0.0001
# planning.items.classification.id.n1_1_40	4.8187	0.0012	0.0001

# tender.items.classification.id.n1_1_42	4.6983	0.0011	0.0001
# planning.items.classification.id.n2_34	4.6169	0.0011	0.0001
# planning.items.classification.id.n1_1_11	4.5642	0.0011	0.0001
# tender.items.classification.id.n1_1_52	4.5077	0.0011	0.0001
# planning.items.classification.id.n1_1_45	4.5071	0.0011	0.0001
# parties.details.legalEntityTypeDetail payee_8	4.4733	0.0011	0.0001
# planning.items.classification.id.n2_40	4.4597	0.0011	0.0001
# planning.items.classification.id.n1_1_5	4.4100	0.0011	0.0001
# planning.items.classification.id.n2_22	4.3869	0.0011	0.0001
# planning.items.classification.id.n2_19	4.3101	0.0011	0.0001
# planning.items.classification.id.n2_39	4.2995	0.0011	0.0001
# planning.items.classification.id.n2_35	4.2206	0.0010	0.0001
# planning.items.classification.id.n1_3	4.1716	0.0010	0.0001
# awards.status_2	4.0074	0.0010	0.0001
# planning.items.classification.id.n2_16	3.9476	0.0010	0.0001
# planning.items.classification.id.n1_1_38	3.9359	0.0010	0.0001
# planning.items.classification.id.n2_14	3.8720	0.0009	0.0001
# planning.items.classification.id.n2_37	3.6785	0.0009	0.0001
# contracts.investmentProjects.id q4	3.6286	0.0009	0.0001
# parties.details.legalEntityTypeDetail payee_17	3.5815	0.0009	0.0001
# planning.items.classification.id.n1_1_15	3.5633	0.0009	0.0001
# planning.items.classification.id.n1_1_50	3.4914	0.0009	0.0001
# tender.items.classification.id.n1_1_14	3.4627	0.0008	0.0001
# tender.items.classification.id.n2_4	3.3653	0.0008	0.0001
# planning.items.classification.id.n2_9	3.3006	0.0008	0.0001
# tender.items.classification.id.n2_7	3.2254	0.0008	0.0001
# tender.eligibilityCriteria q1	3.1358	0.0008	0.0001
# tender.items.classification.id.n1_1_44	3.1147	0.0008	0.0001
# planning.items.classification.id.n1_1_10	3.0388	0.0007	0.0001
# parties.details.EntityType payer_2	3.0379	0.0007	0.0001
# tender.items.classification.id.n1_1_32	2.9104	0.0007	0.0001

# tender.awardCriteria_qualityOnly	2.7746	0.0007	0.0001
# planning.budget.amount.currency_USD	2.7576	0.0007	0.0001
# planning.items.classification.id.n2_31	2.7156	0.0007	0.0001
# parties.details.legalEntityTypeDetail supplier_7	2.6828	0.0007	0.0001
# tender.items.classification.id.n2_9	2.6777	0.0007	0.0001
# parties.details.legalEntityTypeDetail payee_6	2.6485	0.0006	0.0001
# parties.details.legalEntityTypeDetail supplier_11	2.6347	0.0006	0.0001
# contracts.guarantees.obligations_11	2.6210	0.0006	0.0001

# tender.items.classification.id.n1_1_53	2.5216	0.0006	0.0001
# parties.details.legalEntityTypeDetail supplier_9	2.4959	0.0006	0.0001
# planning.items.classification.id.n1_1_46	2.3424	0.0006	0.0001
# parties.details.legalEntityTypeDetail supplier_12	2.3094	0.0006	0.0001
# parties.details.legalEntityTypeDetail enquirer_5	2.2786	0.0006	0.0001
# parties.details.legalEntityTypeDetail supplier_17	2.2727	0.0006	0.0001
# planning.items.classification.id.n2_7	2.2432	0.0005	0.0001
# parties.details.legalEntityTypeDetail payee_7	2.1188	0.0005	0.0001
# planning.items.classification.id.n1_1_34	2.0340	0.0005	0.0
# planning.items.classification.id.n2_15	1.9987	0.0005	0.0
# planning.items.classification.id.n2_27	1.9757	0.0005	0.0
# planning.items.classification.id.n1_1_54	1.9573	0.0005	0.0
# contracts.guarantees.obligations_17	1.8845	0.0005	0.0
# tender.items.classification.id.n2_8	1.8476	0.0005	0.0
# tender.items.classification.id.n1_8	1.8323	0.0004	0.0
# planning.items.classification.id.n2_24	1.8196	0.0004	0.0
# planning.items.classification.id.n1_1_49	1.8151	0.0004	0.0
# planning.items.classification.id.n1_1_53	1.7655	0.0004	0.0
# tender.items.classification.id.n1_1_20	1.7534	0.0004	0.0
# planning.items.classification.id.n2_17	1.7222	0.0004	0.0
# parties.details.legalEntityTypeDetail payee_5	1.7191	0.0004	0.0

# parties.details.legalEntityTypeDetail payee_11	1.5046	0.0004	0.0
# tender.items.classification.id.n1_1_8	1.3344	0.0003	0.0
# planning.items.classification.id.n1_1_6	1.2222	0.0003	0.0
# planning.items.classification.id.n2_43	1.1334	0.0003	0.0
# contracts.guarantees.obligations_8	1.1224	0.0003	0.0

# tender.items.classification.id.n1_1_47	1.0406	0.0003	0.0

# planning.items.classification.id.n1_1_55	0.9555	0.0002	0.0
# planning.items.classification.id.n1_1_47	0.9066	0.0002	0.0
# parties.details.legalEntityTypeDetail payee_13	0.8777	0.0002	0.0
# planning.items.classification.id.n2_41	0.8764	0.0002	0.0
# tender.items.classification.id.n2_5	0.7393	0.0002	0.0
# tender.eligibilityCriteria q4	0.6228	0.0002	0.0
# parties.details.legalEntityTypeDetail supplier_16	0.6140	0.0002	0.0
# planning.items.classification.id.n1_1_52	0.5876	0.0001	0.0
# tender.items.classification.id.n2_12	0.5597	0.0001	0.0


# parties.details.legalEntityTypeDetail enquirer_2	0.5358	0.0001	0.0
# parties.details.legalEntityTypeDetail enquirer_7	0.4606	0.0001	0.0
# contracts.value.amount_usd	0.4487	0.0001	0.0

# tender.items.classification.id.n1_1_39	0.4308	0.0001	0.0

# tender.items.classification.id.n1_1_28	0.3874	0.0001	0.0
# contracts.guarantees.obligations_12	0.3797	0.0001	0.0
# tender.awardCriteria_antecedentes_firma_consultora	0.3301	0.0001	0.0
# parties.details.legalEntityTypeDetail enquirer_17	0.3276	0.0001	0.0
# parties.details.legalEntityTypeDetail supplier_10	0.3119	0.0001	0.0
# parties.details.legalEntityTypeDetail supplier_14	0.3092	0.0001	0.0
# planning.budget.amount.currency_PYG	0.2638	0.0001	0.0
# contracts.guarantees.obligations_9	0.2527	0.0001	0.0
# tender.value.currency_PYG	0.2437	0.0001	0.0
# parties.details.legalEntityTypeDetail payee_16	0.2395	0.0001	0.0
# parties.details.legalEntityTypeDetail payee_10	0.2087	0.0001	0.0
# tender.items.classification.id.n1_1_50	0.1886	0.0	0.0

# parties.details.legalEntityTypeDetail payee_12	0.1069	0.0	0.0
# planning.items.classification.id.n1_1_51	0.0900	0.0	0.0
# contracts.statusDetails_5	0.0884	0.0	0.0
# parties.details.legalEntityTypeDetail supplier_19	0.0863	0.0	0.0
# parties.details.legalEntityTypeDetail enquirer_8	0.0854	0.0	0.0
# tender.items.classification.id.n1_1_55	0.0755	0.0	0.0
# tender.items.classification.id.n1_1_51	0.0751	0.0	0.0
# parties.details.legalEntityTypeDetail enquirer_19	0.0652	0.0	0.0
# parties.details.legalEntityTypeDetail supplier_13	0.0210	0.0	0.0
# tender.statusDetails_Inconsistente	0.0011	0.0	0.0
# tender.value.currency_USD	0.0002	0.0	0.0
# contracts.guarantees.obligations_13	0	0	0
# contracts.guarantees.obligations_15	0	0	0
# contracts.guarantees.obligations_16	0	0	0
# contracts.guarantees.obligations_18	0	0	0
# contracts.statusDetails_8	0	0	0

# awards.status_3	0	0	0
# awards.statusDetails_8	0	0	0
# tender.coveredBy_3	0	0	0
# tender.coveredBy_7	0	0	0
# tender.items.classification.id.n1_1_49	0	0	0
# tender.items.classification.id.n1_1_54	0	0	0
# tender.items.classification.id.n1_1_56	0	0	0
# parties.details.legalEntityTypeDetail enquirer_9	0	0	0
# parties.details.legalEntityTypeDetail enquirer_10	0	0	0
# parties.details.legalEntityTypeDetail enquirer_11	0	0	0
# parties.details.legalEntityTypeDetail enquirer_12	0	0	0
# parties.details.legalEntityTypeDetail enquirer_13	0	0	0
# parties.details.legalEntityTypeDetail enquirer_14	0	0	0
# parties.details.legalEntityTypeDetail enquirer_16	0	0	0
# parties.details.legalEntityTypeDetail payee_14	0	0	0
# parties.details.legalEntityTypeDetail payee_15	0	0	0
# parties.details.legalEntityTypeDetail payee_19	0	0	0
# parties.details.legalEntityTypeDetail payee_20	0	0	0
# parties.details.legalEntityTypeDetail payee_23	0	0	0
# parties.details.legalEntityTypeDetail supplier_15	0	0	0
# parties.details.legalEntityTypeDetail supplier_20	0	0	0
# parties.details.legalEntityTypeDetail supplier_23	0	0	0
# tender.procurementIntention.procuringEntity.id q2	0	0	0
# tender.procurementIntention.procuringEntity.id q4	0	0	0
# tender.procurementIntention.procuringEntity.name q2	0	0	0
# tender.procurementIntention.procuringEntity.name q4	0	0	0
# tender.ProcurementIntentionCategory q2	0	0	0
# tender.ProcurementIntentionCategory q4	0	0	0
# Proveedores Notificados CO	0	0	0
# tender.procurementMethodRationale_covid-19	0	0	0
# tender.procurementIntention.rationale_covid-19	0	0	0
# tender.procurementIntention.status_complete	0	0	0
# tender.procurementIntention.statusDetails_Ejecutada	0	0	0
import pandas as pd 
from data.general_utils import get_month, get_year, get_year_month, count_length
from data.custom_data_methods import count_ammenments, has_no_enquiry_answer, proveed_notificados_co, has_amount_missing, has_criteria_missing, get_contract_amount, get_award_amount, get_tender_doc_type_count, get_tender_doc_type_count_others, get_tender_enquiries_respondidos, get_tender_enquiries_porcentaje, get_parties_legal_entity_type_detail, get_awards_doc_type_details, get_tender_notified_suppliers_id, get_contract_doc_type_details, get_tender_tenderers, get_contracts_transactions_count, get_tender_submission_method_details, get_tender_elegibility_criteria, get_tender_main_procurement_methods_details, get_tender_procuring_entity_id, get_tender_procuring_entity_name, get_buyer_id, get_buyer_name, get_awards_supplier_id, get_contract_implementation_purchase_orders
from data.custom_data_methods import get_tender_items_classification_id_n5, get_tender_items_classification_id_n4, get_tender_items_classification_id_n3, get_planing_items_classification_id_n3, get_planing_items_classification_id_n4, get_parties_roles, get_contract_status, get_planning_items_class_id_n1_arr, get_parties_details_legalEntityTypeDetail, get_planning_items_class_id_n2_arr, get_tender_items_class_id_n1_arr, get_parties_details_entity_type, get_tender_items_class_id_n2_arr, get_tender_items_class_id_n1_1_arr, get_contract_status_details_arr, get_planning_items_class_id_n1_1_arr, get_awards_status_details_arr, get_tender_covered_by_arr

from data.custom_pickle_methods import TenderDocumentsDocumentTypeDetail

# https://www.contrataciones.gov.py/buscador/licitaciones.html?nro_nombre_licitacion=&fecha_desde=01-07-2023&fecha_hasta=31-08-2023&tipo_fecha=PUB&marcas%5B%5D=impugnado&convocante_tipo=&convocante_nombre_codigo=&codigo_contratacion=&catalogo%5Bcodigos_catalogo_n4%5D=&page=1&order=&convocante_codigos=&convocante_tipo_codigo=&unidad_contratacion_codigo=&catalogo%5Bcodigos_catalogo_n4_label%5D=
def get_pd_dataframe(ocds_data: dict):
	data = {
		'tender.value.amount': ocds_data['tender']['value']['amount'],
		'tender.datePublished.month': get_month(ocds_data['tender']['datePublished']),
		'tender.datePublished.year': get_year(ocds_data['tender']['datePublished']),
		'tender.datePublished.yearmonth': get_year_month(ocds_data['tender']['datePublished']),
		'tender.tenderPeriod.durationInDays': 0,
		'tender.tenderPeriod.startDate.month': 0,
		'tender.tenderPeriod.startDate.year': 0,
		'tender.tenderPeriod.startDate.yearmonth': 0,
		'tender.tenderPeriod.endDate.month': 0,
		'tender.tenderPeriod.endDate.year': 0,
		'tender.tenderPeriod.endDate.yearmonth': 0,
		'tender.awardPeriod.startDate.month': get_month(ocds_data['tender']['awardPeriod']['startDate']),
		'tender.awardPeriod.startDate.year': get_year(ocds_data['tender']['awardPeriod']['startDate']),
		'tender.awardPeriod.startDate.yearmonth': get_year_month(ocds_data['tender']['awardPeriod']['startDate']),
		'tender.status_cancelled': ocds_data['tender']['status'] == 'cancelled',
		'tender.status_complete': ocds_data['tender']['status'] == 'complete',
		'tender.status_unsuccessful': ocds_data['tender']['status'] == 'unsuccesful',
		'tender.awardCriteria_antecedentes_firma_consultora': ocds_data['tender']['awardCriteria'] == 'antecedentes_firma_consultora',
		'tender.awardCriteria_priceOnly': ocds_data['tender']['awardCriteria'] == 'priceOnly',
		'tender.awardCriteria_qualityOnly': ocds_data['tender']['awardCriteria'] == 'qualityOnly',
		'tender.awardCriteria_ratedCriteria': ocds_data['tender']['awardCriteria'] == 'ratedCriteria',
		'date.month': get_month(ocds_data['date']),
		'date.year': get_year(ocds_data['date']),
		'date.yearmonth': get_year_month(ocds_data['date']),
		'tender.awardCriteriaDetails_Combinado': ocds_data['tender']['awardCriteriaDetails'] == 'Combinado',
		'tender.awardCriteriaDetails_Por Item': ocds_data['tender']['awardCriteriaDetails'] == 'Por Item',
		'tender.awardCriteriaDetails_Por Lote': ocds_data['tender']['awardCriteriaDetails'] == 'Por Lote',
		'tender.awardCriteriaDetails_Por Total': ocds_data['tender']['awardCriteriaDetails'] == 'Por Total',
		'tender.statusDetails_Adjudicada': ocds_data['tender']['statusDetails'] == 'Adjudicada',
		'tender.statusDetails_Anulada o Cancelada': ocds_data['tender']['statusDetails'] == 'Anulada o Cancelada',
		'tender.statusDetails_Desierta': ocds_data['tender']['statusDetails'] == 'Desierta',
		'tender.statusDetails_En Evaluacion (Cerrada)': ocds_data['tender']['statusDetails'] == 'En Evaluacion (Cerrada)',
		'tender.statusDetails_Inconsistente': ocds_data['tender']['statusDetails'] == 'Inconsistente',
		'tender.statusDetails_Suspendida': ocds_data['tender']['statusDetails'] == 'Suspendida',
		'tender.hasEnquiries_False': ocds_data['tender']['hasEnquiries'] == 'false',
		'tender.hasEnquiries_True': ocds_data['tender']['hasEnquiries'] == 'true',
		'tender.value.currency_USD': ocds_data['tender']['value']['currency'] == 'USD',
		'tender.value.currency_PYG': ocds_data['tender']['value']['currency'] == 'PYG',
		'tender.mainProcurementCategory_goods': ocds_data['tender']['mainProcurementCategory'] == 'goods',
		'tender.mainProcurementCategory_services': ocds_data['tender']['mainProcurementCategory'] == 'services',
		'tender.mainProcurementCategory_works': ocds_data['tender']['mainProcurementCategory'] == 'works',
		# 'tender.procurementMethodRationale_covid-19': if procurementMethodRationale in ocds_data['tender']['procurementMethodRationale'] == 'covid-19',
		# 'tender.procurementIntention.rationale_covid-19': ocds_data['tender']['procurementIntention']['rationale'] == 'covid-19',
		'contracts.implementation.purchaseOrders.count': get_contract_implementation_purchase_orders(ocds_data),
		'contracts.implementation.transactions.count': get_contracts_transactions_count(ocds_data),
		'tender.enquiries respondidos': get_tender_enquiries_respondidos(ocds_data),
		'tender.enquiries porcentaje': get_tender_enquiries_porcentaje(ocds_data),
		'Preguntas Sin Respuesta': has_no_enquiry_answer(ocds_data),
		'Enmiendas  del contrato': count_ammenments(ocds_data) > 0,
		'Proveedores Notificados CO': proveed_notificados_co(ocds_data),
		'Monto faltante': has_amount_missing(ocds_data),
		'Criterio de evaluacion faltante': has_criteria_missing(ocds_data),
		'Tiempo de convocatoria LPN': False,
		'Oferente Unico': False,
		'Tiempo de Convocatoria CO': False,
		'award.count': 0,
		'contracts.count': 0,
		'tender.numberOfTenderers': 0,
		'tender.bidOpening.date.month': None,
		'tender.bidOpening.date.year': None,
		'tender.bidOpening.date.yearmonth': None,
		'tender.techniques.hasElectronicAuction': 0,
		'tender.enquiries total': 0,
		'tender.enquiries.count': 0,
		'contracts.amendments.count': 0,
		'tender.procurementIntention.status_complete': None,
		'tender.procurementIntention.statusDetails_Ejecutada': None,
		'tender.enquiryPeriod.durationInDays': None,
		'tender.enquiryPeriod.endDate.month': None,
		'tender.enquiryPeriod.endDate.year': None,
		'tender.enquiryPeriod.endDate.yearmonth': None,
		'tender.enquiryPeriod.startDate.month': None,
		'tender.enquiryPeriod.startDate.year': None,
		'tender.enquiryPeriod.startDate.yearmonth': None,
		'planning.identifier': None,
		'planning.budget.amount.amount': None,
		'planning.budget.amount.currency_PYG': 0,
		'planning.budget.amount.currency_USD': 0,
		'planning.estimatedDate.month': None,
		'planning.estimatedDate.year': None,
		'planning.estimatedDate.yearmonth': None,
		'tender.procurementMethodDetails q1': 0,
		'tender.procurementMethodDetails q2': 0,
		'tender.procurementMethodDetails q3': 0,
		'tender.procurementMethodDetails q4': 0,
		'tender.documents.documentTypeDetails_1': get_tender_doc_type_count(ocds_data, TenderDocumentsDocumentTypeDetail[0]),
		'tender.documents.documentTypeDetails_2': get_tender_doc_type_count(ocds_data, TenderDocumentsDocumentTypeDetail[1]),
		'tender.documents.documentTypeDetails_3': get_tender_doc_type_count(ocds_data, TenderDocumentsDocumentTypeDetail[2]),
		'tender.documents.documentTypeDetails_4': get_tender_doc_type_count(ocds_data, TenderDocumentsDocumentTypeDetail[3]),
		'tender.documents.documentTypeDetails_5': get_tender_doc_type_count(ocds_data, TenderDocumentsDocumentTypeDetail[4]),
		'tender.documents.documentTypeDetails_6': get_tender_doc_type_count(ocds_data, TenderDocumentsDocumentTypeDetail[5]),
		'tender.documents.documentTypeDetails_7': get_tender_doc_type_count(ocds_data, TenderDocumentsDocumentTypeDetail[6]),
		'tender.documents.documentTypeDetails_8': get_tender_doc_type_count(ocds_data, TenderDocumentsDocumentTypeDetail[7]),
		'tender.documents.documentTypeDetails_9': get_tender_doc_type_count(ocds_data, TenderDocumentsDocumentTypeDetail[8]),
		'tender.documents.documentTypeDetails_10': get_tender_doc_type_count(ocds_data, TenderDocumentsDocumentTypeDetail[9]),
		'tender.documents.documentTypeDetails_11': get_tender_doc_type_count(ocds_data, TenderDocumentsDocumentTypeDetail[10]),
		'tender.documents.documentTypeDetails_12': get_tender_doc_type_count(ocds_data, TenderDocumentsDocumentTypeDetail[11]),
		'tender.documents.documentTypeDetails_13': get_tender_doc_type_count_others(ocds_data),
		'parties.details.legalEntityTypeDetail tenderer_1': 0,
		'parties.details.legalEntityTypeDetail tenderer_2': 0,
		'parties.details.legalEntityTypeDetail tenderer_3': 0,
		'parties.details.legalEntityTypeDetail tenderer_4': 0,
		'parties.details.legalEntityTypeDetail tenderer_5': 0,
		'parties.details.legalEntityTypeDetail tenderer_6': 0,
		'parties.details.legalEntityTypeDetail tenderer_7': 0,
		'parties.details.legalEntityTypeDetail tenderer_8': 0,
		'parties.details.legalEntityTypeDetail tenderer_9': 0,
		'parties.details.legalEntityTypeDetail tenderer_10': 0,
		'parties.details.legalEntityTypeDetail tenderer_11': 0,
		'parties.details.legalEntityTypeDetail tenderer_12': 0,
		'parties.details.legalEntityTypeDetail tenderer_13': 0,
		'parties.details.legalEntityTypeDetail tenderer_14': 0,
		'parties.details.legalEntityTypeDetail tenderer_15': 0,
		'parties.details.legalEntityTypeDetail tenderer_16': 0,
		'parties.details.legalEntityTypeDetail tenderer_17': 0,
		'parties.details.legalEntityTypeDetail tenderer_18': 0,
		'parties.details.legalEntityTypeDetail tenderer_19': 0,
		'parties.details.legalEntityTypeDetail tenderer_20': 0,
		'parties.details.legalEntityTypeDetail tenderer_21': 0,
		'parties.details.legalEntityTypeDetail tenderer_22': 0,
		'parties.details.legalEntityTypeDetail tenderer_23': 0,
		'tender.notifiedSuppliers.id q1': 0,
		'tender.notifiedSuppliers.id q2': 0,
		'tender.notifiedSuppliers.id q3': 0,
		'tender.notifiedSuppliers.id q4': 0,
		'tender.eligibilityCriteria q1': 0,
		'tender.eligibilityCriteria q2': 0,
		'tender.eligibilityCriteria q3': 0,
		'tender.eligibilityCriteria q4': 0,
	}
	if 'awards' in ocds_data:
		data['awards.count'] = count_length(ocds_data['awards'])

	if 'contracts' in ocds_data:
		data['contracts.count'] = count_length(ocds_data['contracts'])

	if 'tenderPeriod' in ocds_data['tender']:
		data['Tiempo de convocatoria LPN'] = ocds_data['tender']['tenderPeriod']['durationInDays'] <= 19
		data['Tiempo de Convocatoria CO'] = ocds_data['tender']['tenderPeriod']['durationInDays'] <= 9
		data['tender.tenderPeriod.durationInDays'] = ocds_data['tender']['tenderPeriod']['durationInDays']
		data['tender.tenderPeriod.startDate.month'] = get_month(ocds_data['tender']['tenderPeriod']['startDate'])
		data['tender.tenderPeriod.startDate.year'] = get_year(ocds_data['tender']['tenderPeriod']['startDate'])
		data['tender.tenderPeriod.startDate.yearmonth'] = get_year_month(ocds_data['tender']['tenderPeriod']['startDate'])
		data['tender.tenderPeriod.endDate.month'] = get_month(ocds_data['tender']['tenderPeriod']['endDate'])
		data['tender.tenderPeriod.endDate.year'] = get_year(ocds_data['tender']['tenderPeriod']['endDate'])
		data['tender.tenderPeriod.endDate.yearmonth'] = get_year_month(ocds_data['tender']['tenderPeriod']['endDate'])

	if 'numberOfTenderers' in ocds_data['tender']:
		data['tender.numberOfTenderers'] = ocds_data['tender']['numberOfTenderers']
		data['Oferente Unico'] = ocds_data['tender']['numberOfTenderers'] == 1
	
	if 'bidOpening' in ocds_data['tender']:
		data['tender.bidOpening.date.month'] = get_month(ocds_data['tender']['bidOpening']['date'])
		data['tender.bidOpening.date.year'] = get_year(ocds_data['tender']['bidOpening']['date'])
		data['tender.bidOpening.date.yearmonth'] = get_year_month(ocds_data['tender']['bidOpening']['date'])

	if 'techniques' in ocds_data['tender'] and 'hasElectronicAuction' in ocds_data['tender']['techniques']:
		data['tender.techniques.hasElectronicAuction'] = 1 if ocds_data['tender']['techniques']['hasElectronicAuction'] else 0
	else:
		data['tender.techniques.hasElectronicAuction'] = None

	if 'enquiries' in ocds_data['tender']:
		data['tender.enquiries total'] = count_length(ocds_data['tender']['enquiries'])
		data['tender.enquiries.count'] = count_length(ocds_data['tender']['enquiries'])
	
	data['contracts.amendments.count']= count_ammenments(ocds_data)
	data['Enmiendas del contrato'] = count_ammenments(ocds_data) > 0
	if 'procurementIntention' in ocds_data['tender']:
		data['tender.procurementIntention.status_complete'] = ocds_data['tender']['procurementIntention']['status'] == 'complete'
		data['tender.procurementIntention.statusDetails_Ejecutada'] = ocds_data['tender']['procurementIntention']['statusDetails'] == 'Ejecutada'

	if 'enquiryPeriod' in ocds_data['tender']:
		data['tender.enquiryPeriod.durationInDays'] = ocds_data['tender']['enquiryPeriod']['durationInDays']
		data['tender.enquiryPeriod.endDate.month'] = get_month(ocds_data['tender']['enquiryPeriod']['endDate'])
		data['tender.enquiryPeriod.endDate.year'] = get_year(ocds_data['tender']['enquiryPeriod']['endDate'])
		data['tender.enquiryPeriod.endDate.yearmonth'] = get_year_month(ocds_data['tender']['enquiryPeriod']['endDate'])
		data['tender.enquiryPeriod.startDate.month'] = get_month(ocds_data['tender']['enquiryPeriod']['startDate'])
		data['tender.enquiryPeriod.startDate.year'] = get_year(ocds_data['tender']['enquiryPeriod']['startDate'])
		data['tender.enquiryPeriod.startDate.yearmonth'] = get_year_month(ocds_data['tender']['enquiryPeriod']['startDate'])
	
	if 'planning' in ocds_data:
		data['planning.identifier'] = ocds_data['planning']['identifier']
		data['planning.budget.amount.amount'] = ocds_data['planning']['budget']['amount']['amount']
		data['planning.budget.amount.currency_PYG'] = ocds_data['planning']['budget']['amount']['currency'] == 'PYG'
		data['planning.budget.amount.currency_USD'] = ocds_data['planning']['budget']['amount']['currency'] == 'USD'
		data['planning.estimatedDate.month'] = get_month(ocds_data['planning']['estimatedDate'])
		data['planning.estimatedDate.year'] = get_year(ocds_data['planning']['estimatedDate'])
		data['planning.estimatedDate.yearmonth'] = get_year_month(ocds_data['planning']['estimatedDate'])

	if 'lots' in ocds_data['tender']:
		data['tender.lots.count'] = count_length(ocds_data['tender']['lots'])
		data['tender.lots'] = count_length(ocds_data['tender']['lots'])

	if 'procurementMethodDetails' in ocds_data['tender']:

		if ocds_data['tender']['procurementMethodDetails'] == 'Contratación Directa':
			data['tender.procurementMethodDetails q1'] = 1

		elif ocds_data['tender']['procurementMethodDetails'] == '':
			data['tender.procurementMethodDetails q2'] = 1

		elif ocds_data['tender']['procurementMethodDetails'] == 'Concurso de Ofertas':
			data['tender.procurementMethodDetails q3'] = 1
		else:
			data['tender.procurementMethodDetails q4'] = 1
	else:
		data['tender.procurementMethodDetails q4'] = 1
	
	data['tender.eligibilityCriteria q1'] = get_tender_elegibility_criteria(ocds_data, 0)
	data['tender.eligibilityCriteria q2'] = get_tender_elegibility_criteria(ocds_data, 1)
	data['tender.eligibilityCriteria q3'] = get_tender_elegibility_criteria(ocds_data, 2)
	data['tender.eligibilityCriteria q4'] = get_tender_elegibility_criteria(ocds_data, 3)

	data['tender.mainProcurementCategoryDetails q1'] = get_tender_main_procurement_methods_details(ocds_data, 0)
	data['tender.mainProcurementCategoryDetails q2'] = get_tender_main_procurement_methods_details(ocds_data, 1)
	data['tender.mainProcurementCategoryDetails q3'] = get_tender_main_procurement_methods_details(ocds_data, 2)
	data['tender.mainProcurementCategoryDetails q4'] = get_tender_main_procurement_methods_details(ocds_data, 3)

	contract_amount = get_contract_amount(ocds_data)
	data['contracts.value.amount_pyg'] = contract_amount[0]
	data['contracts.value.amount_usd'] = contract_amount[1]
	# data['tender.procurementMethodDetails q4'] = ocds_data['tender']['procurementMethodDetails'] == 'Contratación Directa'
	# ocds_data['tender']['procurementMethodDetails']
	awards_amount = get_award_amount(ocds_data)
	data['awards.value.amount_pyg'] = awards_amount[0]
	data['awards.value.amount_usd'] = awards_amount[1]

	parties_tenderer = get_parties_legal_entity_type_detail(ocds_data, 'tenderer')
	data['parties.details.legalEntityTypeDetail tenderer_1'] = parties_tenderer[0]
	data['parties.details.legalEntityTypeDetail tenderer_2'] = parties_tenderer[1]
	data['parties.details.legalEntityTypeDetail tenderer_3'] = parties_tenderer[2]
	data['parties.details.legalEntityTypeDetail tenderer_4'] = parties_tenderer[3]
	data['parties.details.legalEntityTypeDetail tenderer_5'] = parties_tenderer[4]
	data['parties.details.legalEntityTypeDetail tenderer_6'] = parties_tenderer[5]
	data['parties.details.legalEntityTypeDetail tenderer_7'] = parties_tenderer[6]
	data['parties.details.legalEntityTypeDetail tenderer_8'] = parties_tenderer[7]
	data['parties.details.legalEntityTypeDetail tenderer_9'] = parties_tenderer[8]
	data['parties.details.legalEntityTypeDetail tenderer_10'] = parties_tenderer[9]
	data['parties.details.legalEntityTypeDetail tenderer_11'] = parties_tenderer[10]
	data['parties.details.legalEntityTypeDetail tenderer_12'] = parties_tenderer[11]
	data['parties.details.legalEntityTypeDetail tenderer_13'] = parties_tenderer[12]
	data['parties.details.legalEntityTypeDetail tenderer_14'] = parties_tenderer[13]
	data['parties.details.legalEntityTypeDetail tenderer_15'] = parties_tenderer[14]
	data['parties.details.legalEntityTypeDetail tenderer_16'] = parties_tenderer[15]
	data['parties.details.legalEntityTypeDetail tenderer_17'] = parties_tenderer[16]
	data['parties.details.legalEntityTypeDetail tenderer_18'] = parties_tenderer[17]
	data['parties.details.legalEntityTypeDetail tenderer_19'] = parties_tenderer[18]
	data['parties.details.legalEntityTypeDetail tenderer_20'] = parties_tenderer[19]
	data['parties.details.legalEntityTypeDetail tenderer_21'] = parties_tenderer[20]
	data['parties.details.legalEntityTypeDetail tenderer_22'] = parties_tenderer[21]
	data['parties.details.legalEntityTypeDetail tenderer_23'] = parties_tenderer[22]
	
	parties_notified_supplier = get_parties_legal_entity_type_detail(ocds_data, 'notifiedSupplier')
	data['parties.details.legalEntityTypeDetail notifiedSupplier_1'] = parties_notified_supplier[0]
	data['parties.details.legalEntityTypeDetail notifiedSupplier_2'] = parties_notified_supplier[1]
	data['parties.details.legalEntityTypeDetail notifiedSupplier_3'] = parties_notified_supplier[2]
	data['parties.details.legalEntityTypeDetail notifiedSupplier_4'] = parties_notified_supplier[3]
	data['parties.details.legalEntityTypeDetail notifiedSupplier_5'] = parties_notified_supplier[4]
	data['parties.details.legalEntityTypeDetail notifiedSupplier_6'] = parties_notified_supplier[5]
	data['parties.details.legalEntityTypeDetail notifiedSupplier_7'] = parties_notified_supplier[6]
	data['parties.details.legalEntityTypeDetail notifiedSupplier_8'] = parties_notified_supplier[7]
	data['parties.details.legalEntityTypeDetail notifiedSupplier_9'] = parties_notified_supplier[8]
	data['parties.details.legalEntityTypeDetail notifiedSupplier_10'] = parties_notified_supplier[9]
	data['parties.details.legalEntityTypeDetail notifiedSupplier_11'] = parties_notified_supplier[10]
	data['parties.details.legalEntityTypeDetail notifiedSupplier_12'] = parties_notified_supplier[11]
	data['parties.details.legalEntityTypeDetail notifiedSupplier_13'] = parties_notified_supplier[12]
	data['parties.details.legalEntityTypeDetail notifiedSupplier_14'] = parties_notified_supplier[13]
	data['parties.details.legalEntityTypeDetail notifiedSupplier_15'] = parties_notified_supplier[14]
	data['parties.details.legalEntityTypeDetail notifiedSupplier_16'] = parties_notified_supplier[15]
	data['parties.details.legalEntityTypeDetail notifiedSupplier_17'] = parties_notified_supplier[16]
	data['parties.details.legalEntityTypeDetail notifiedSupplier_18'] = parties_notified_supplier[17]
	data['parties.details.legalEntityTypeDetail notifiedSupplier_19'] = parties_notified_supplier[18]
	data['parties.details.legalEntityTypeDetail notifiedSupplier_20'] = parties_notified_supplier[19]
	data['parties.details.legalEntityTypeDetail notifiedSupplier_21'] = parties_notified_supplier[20]
	data['parties.details.legalEntityTypeDetail notifiedSupplier_22'] = parties_notified_supplier[21]
	data['parties.details.legalEntityTypeDetail notifiedSupplier_23'] = parties_notified_supplier[22]

	awards_doc_type_details = get_awards_doc_type_details(ocds_data)	
	data['awards.documents.DocumentTypeDetails_1'] = awards_doc_type_details[0]
	data['awards.documents.DocumentTypeDetails_2'] = awards_doc_type_details[1]
	data['awards.documents.DocumentTypeDetails_3'] = awards_doc_type_details[2]
	data['awards.documents.DocumentTypeDetails_4'] = awards_doc_type_details[3]
	data['awards.documents.DocumentTypeDetails_5'] = awards_doc_type_details[4]
	data['awards.documents.DocumentTypeDetails_6'] = awards_doc_type_details[5]
	data['awards.documents.DocumentTypeDetails_7'] = awards_doc_type_details[6]
	data['awards.documents.DocumentTypeDetails_8'] = awards_doc_type_details[7]
	data['awards.documents.DocumentTypeDetails_9'] = awards_doc_type_details[8]
	data['awards.documents.DocumentTypeDetails_10'] = awards_doc_type_details[9]
	data['awards.documents.DocumentTypeDetails_11'] = awards_doc_type_details[10]
	data['awards.documents.DocumentTypeDetails_12'] = awards_doc_type_details[11]
	data['awards.documents.DocumentTypeDetails_13'] = awards_doc_type_details[12]
	data['awards.documents.DocumentTypeDetails_14'] = awards_doc_type_details[13]
	data['awards.documents.DocumentTypeDetails_15'] = awards_doc_type_details[14]
	data['awards.documents.DocumentTypeDetails_16'] = awards_doc_type_details[15]

	tender_notified_suppliers = get_tender_notified_suppliers_id(ocds_data)
	data['tender.notifiedSuppliers.id q1'] = tender_notified_suppliers[0]
	data['tender.notifiedSuppliers.id q2'] = tender_notified_suppliers[1]
	data['tender.notifiedSuppliers.id q3'] = tender_notified_suppliers[2]
	data['tender.notifiedSuppliers.id q4'] = tender_notified_suppliers[3]

	contract_doc_type_details = get_contract_doc_type_details(ocds_data)

	data['contracts.documents.DocumentTypeDetails_1'] = contract_doc_type_details[0]
	data['contracts.documents.DocumentTypeDetails_2'] = contract_doc_type_details[1]
	data['contracts.documents.DocumentTypeDetails_3'] = contract_doc_type_details[2]
	data['contracts.documents.DocumentTypeDetails_4'] = contract_doc_type_details[3]
	data['contracts.documents.DocumentTypeDetails_5'] = contract_doc_type_details[4]
	data['contracts.documents.DocumentTypeDetails_6'] = contract_doc_type_details[5]
	data['contracts.documents.DocumentTypeDetails_7'] = contract_doc_type_details[6]
	data['contracts.documents.DocumentTypeDetails_8'] = contract_doc_type_details[7]
	data['contracts.documents.DocumentTypeDetails_9'] = contract_doc_type_details[8]
	data['contracts.documents.DocumentTypeDetails_10'] = contract_doc_type_details[9]
	data['contracts.documents.DocumentTypeDetails_11'] = contract_doc_type_details[10]
	data['contracts.documents.DocumentTypeDetails_12'] = contract_doc_type_details[11]
	
	tender_tenderers = get_tender_tenderers(ocds_data)
	data['tender.tenderers.id q1'] = tender_tenderers[0]
	data['tender.tenderers.id q2'] = tender_tenderers[1]
	data['tender.tenderers.id q3'] = tender_tenderers[2]
	data['tender.tenderers.id q4'] = tender_tenderers[3]

	tender_sub_method_details = get_tender_submission_method_details(ocds_data)
	data['tender.submissionMethodDetails q1'] = tender_sub_method_details[0]
	data['tender.submissionMethodDetails q2'] = tender_sub_method_details[1]
	data['tender.submissionMethodDetails q3'] = tender_sub_method_details[2]
	data['tender.submissionMethodDetails q4'] = tender_sub_method_details[3]

	data['tender.procuringEntity.id q1'] = get_tender_procuring_entity_id(ocds_data, 0)
	data['tender.procuringEntity.id q2'] = get_tender_procuring_entity_id(ocds_data, 1)
	data['tender.procuringEntity.id q3'] = get_tender_procuring_entity_id(ocds_data, 2)
	data['tender.procuringEntity.id q4'] = get_tender_procuring_entity_id(ocds_data, 3)
	
	data['tender.procuringEntity.name q1'] = get_tender_procuring_entity_name(ocds_data, 0)
	data['tender.procuringEntity.name q2'] = get_tender_procuring_entity_name(ocds_data, 1)
	data['tender.procuringEntity.name q3'] = get_tender_procuring_entity_name(ocds_data, 2)
	data['tender.procuringEntity.name q4'] = get_tender_procuring_entity_name(ocds_data, 3)
	
	data['buyer.id q1'] = get_buyer_id(ocds_data, 0)
	data['buyer.id q2'] = get_buyer_id(ocds_data, 1)
	data['buyer.id q3'] = get_buyer_id(ocds_data, 2)
	data['buyer.id q4'] = get_buyer_id(ocds_data, 3)

	data['buyer.name q1'] = get_buyer_name(ocds_data, 0)
	data['buyer.name q2'] = get_buyer_name(ocds_data, 1)
	data['buyer.name q3'] = get_buyer_name(ocds_data, 2)
	data['buyer.name q4'] = get_buyer_name(ocds_data, 3)

	award_supp_id = get_awards_supplier_id(ocds_data)
	data['awards.suppliers.id q1'] = award_supp_id[0]
	data['awards.suppliers.id q2'] = award_supp_id[1]
	data['awards.suppliers.id q3'] = award_supp_id[2]
	data['awards.suppliers.id q4'] = award_supp_id[3]

	tender_items_n5 = get_tender_items_classification_id_n5(ocds_data)
	tender_items_n3 = get_tender_items_classification_id_n3(ocds_data)
	tender_items_n4 = get_tender_items_classification_id_n4(ocds_data)

	data['tender.items.classification.id.n5 q1'] = tender_items_n5[0]
	data['tender.items.classification.id.n5 q2'] = tender_items_n5[1]
	data['tender.items.classification.id.n5 q3'] = tender_items_n5[2]
	data['tender.items.classification.id.n5 q4'] = tender_items_n5[3]

	data['tender.items.classification.id.n4 q1'] = tender_items_n4[0]
	data['tender.items.classification.id.n4 q2'] = tender_items_n4[1]
	data['tender.items.classification.id.n4 q3'] = tender_items_n4[2]
	data['tender.items.classification.id.n4 q4'] = tender_items_n4[3]

	data['tender.items.classification.id.n3 q1'] = tender_items_n3[0]
	data['tender.items.classification.id.n3 q2'] = tender_items_n3[1]
	data['tender.items.classification.id.n3 q3'] = tender_items_n3[2]
	data['tender.items.classification.id.n3 q4'] = tender_items_n3[3]
	
	planning_items_class_n3 = get_planing_items_classification_id_n3(ocds_data)
	data['planning.items.classification.id.n3 q1'] = planning_items_class_n3[0]
	data['planning.items.classification.id.n3 q2'] = planning_items_class_n3[1]
	data['planning.items.classification.id.n3 q3'] = planning_items_class_n3[2]
	data['planning.items.classification.id.n3 q4'] = planning_items_class_n3[3]

	planning_items_class_n4 = get_planing_items_classification_id_n4(ocds_data)
	data['planning.items.classification.id.n4 q1'] = planning_items_class_n4[0]
	data['planning.items.classification.id.n4 q2'] = planning_items_class_n4[1]
	data['planning.items.classification.id.n4 q3'] = planning_items_class_n4[2]
	data['planning.items.classification.id.n4 q4'] = planning_items_class_n4[3]

	parties_roles_notifiedSupplier = get_parties_roles(ocds_data, 'notifiedSupplier')
	data['parties.roles notifiedSupplier q1'] = parties_roles_notifiedSupplier[0]
	data['parties.roles notifiedSupplier q2'] = parties_roles_notifiedSupplier[1]
	data['parties.roles notifiedSupplier q3'] = parties_roles_notifiedSupplier[2]
	data['parties.roles notifiedSupplier q4'] = parties_roles_notifiedSupplier[3]
	
	parties_roles_tenderer = get_parties_roles(ocds_data, 'tenderer')
	data['parties.roles tenderer q1'] = parties_roles_tenderer[0]
	data['parties.roles tenderer q2'] = parties_roles_tenderer[1]
	data['parties.roles tenderer q3'] = parties_roles_tenderer[2]
	data['parties.roles tenderer q4'] = parties_roles_tenderer[3]
	
	parties_roles_procuring = get_parties_roles(ocds_data, 'procuringEntity')
	data['parties.roles procuringEntity q1'] = parties_roles_procuring[0]
	data['parties.roles procuringEntity q2'] = parties_roles_procuring[1]
	data['parties.roles procuringEntity q3'] = parties_roles_procuring[2]
	data['parties.roles procuringEntity q4'] = parties_roles_procuring[3]
	
	parties_roles_payee = get_parties_roles(ocds_data, 'payee')
	data['parties.roles payee q1'] = parties_roles_payee[0]
	data['parties.roles payee q2'] = parties_roles_payee[1]
	data['parties.roles payee q3'] = parties_roles_payee[2]
	data['parties.roles payee q4'] = parties_roles_payee[3]

	parties_roles_supplier = get_parties_roles(ocds_data, 'supplier')
	data['parties.roles supplier q1'] = parties_roles_supplier[0]
	data['parties.roles supplier q2'] = parties_roles_supplier[1]
	data['parties.roles supplier q3'] = parties_roles_supplier[2]
	data['parties.roles supplier q4'] = parties_roles_supplier[3]

	parties_roles_buyer = get_parties_roles(ocds_data, 'buyer')
	data['parties.roles buyer q1'] = parties_roles_buyer[0]
	data['parties.roles buyer q2'] = parties_roles_buyer[1]
	data['parties.roles buyer q3'] = parties_roles_buyer[2]
	data['parties.roles buyer q4'] = parties_roles_buyer[3]

	parties_roles_payer = get_parties_roles(ocds_data, 'payer')
	data['parties.roles payer q1'] = parties_roles_payer[0]
	data['parties.roles payer q2'] = parties_roles_payer[1]
	data['parties.roles payer q3'] = parties_roles_payer[2]
	data['parties.roles payer q4'] = parties_roles_payer[3]

	parties_roles_enquirer = get_parties_roles(ocds_data, 'enquirer')
	data['parties.roles enquirer q1'] = parties_roles_enquirer[0]
	data['parties.roles enquirer q2'] = parties_roles_enquirer[1]
	data['parties.roles enquirer q3'] = parties_roles_enquirer[2]
	data['parties.roles enquirer q4'] = parties_roles_enquirer[3]
	
	data['contracts.status_1'] = get_contract_status(ocds_data, "active")
	data['contracts.status_2'] = get_contract_status(ocds_data, "terminated")
	data['contracts.status_3'] = get_contract_status(ocds_data, "cancelled")
	data['contracts.status_4'] = get_contract_status(ocds_data, "pending")
	
	roles = ['candidate','enquirer','payer', 'payee', 'supplier', 'procuringEntity', 'buyer', 'tenderer', 'notifiedSupplier']
	for role in roles:
		arr = get_parties_details_legalEntityTypeDetail(ocds_data, role)
		legal_ent = f'parties.details.legalEntityTypeDetail {role}_'
		for i in range(len(arr)):
			data[f'{legal_ent}{i + 1}'] = arr[i]
	
	for role in roles:
		arr = get_parties_details_entity_type(ocds_data, role)
		legal_ent = f'parties.details.EntityType {role}_'
		for i in range(len(arr)):
			data[f'{legal_ent}{i + 1}'] = arr[i]


	planning_items_class_id_n1_arr = get_planning_items_class_id_n1_arr(ocds_data)
	for i in range(len(planning_items_class_id_n1_arr)):
		data[f'planning.items.classification.id.n1_{i + 1}'] = planning_items_class_id_n1_arr[i]
	
	planning_items_class_id_n1_1_arr = get_planning_items_class_id_n1_1_arr(ocds_data)
	for i in range(len(planning_items_class_id_n1_1_arr)):
		data[f'planning.items.classification.id.n1_1_{i + 1}'] = planning_items_class_id_n1_1_arr[i]

	planning_items_class_id_n2_arr = get_planning_items_class_id_n2_arr(ocds_data)
	for i in range(len(planning_items_class_id_n2_arr)):
		data[f'planning.items.classification.id.n2_{i + 1}'] = planning_items_class_id_n2_arr[i]

	tender_items_class_id_n1_arr = get_tender_items_class_id_n1_arr(ocds_data)
	for i in range(len(tender_items_class_id_n1_arr)):
		data[f'tender.items.classification.id.n1_{i + 1}'] = tender_items_class_id_n1_arr[i]

	tender_items_class_id_n2_arr = get_tender_items_class_id_n2_arr(ocds_data)
	for i in range(len(tender_items_class_id_n2_arr)):
		data[f'tender.items.classification.id.n2_{i + 1}'] = tender_items_class_id_n2_arr[i]
	
	tender_items_class_n1_1_arr = get_tender_items_class_id_n1_1_arr(ocds_data)
	for i in range(len(tender_items_class_n1_1_arr)):
		data[f'tender.items.classification.id.n1_1_{i + 1}'] = tender_items_class_n1_1_arr[i]

	contract_status_details_arr = get_contract_status_details_arr(ocds_data)
	for i in range(len(contract_status_details_arr)):
		data[f'contracts.statusDetails_{i + 1}'] = contract_status_details_arr[i]
	
	awards_status_details_arr = get_awards_status_details_arr(ocds_data)
	for i in range(len(awards_status_details_arr)):
		data[f'awards.statusDetails_{i + 1}'] = awards_status_details_arr[i]
	
	tender_covered_by_arr = get_tender_covered_by_arr(ocds_data)
	for i in range(len(tender_covered_by_arr)):
		data[f'tender.coveredBy_{i + 1}'] = tender_covered_by_arr[i]

	data_df = pd.DataFrame([data])
	return data_df, data


# missing data:
# tender.ProcurementIntentionCategory q1
# tender.ProcurementIntentionCategory q2
# tender.ProcurementIntentionCategory q3
# tender.ProcurementIntentionCategory q4
# tender.procuringEntity.id q1
# tender.procuringEntity.id q2
# tender.procuringEntity.id q3
# tender.procuringEntity.id q4
# tender.procuringEntity.name q1
# tender.procuringEntity.name q2
# tender.procuringEntity.name q3
# tender.procuringEntity.name q4
# tender.procurementIntention.procuringEntity.id q1
# tender.procurementIntention.procuringEntity.id q2
# tender.procurementIntention.procuringEntity.id q3
# tender.procurementIntention.procuringEntity.id q4
# tender.procurementIntention.procuringEntity.name q1
# tender.procurementIntention.procuringEntity.name q2
# tender.procurementIntention.procuringEntity.name q3
# tender.procurementIntention.procuringEntity.name q4


# secondStage.id q1
# secondStage.id q2
# secondStage.id q3
# secondStage.id q4

# tender.notifiedSuppliers.id q1
# tender.notifiedSuppliers.id q2
# tender.notifiedSuppliers.id q3
# tender.notifiedSuppliers.id q4
# tender.tenderers.id q1
# tender.tenderers.id q2
# tender.tenderers.id q3
# tender.tenderers.id q4




# contracts.guarantees.obligations_1
# contracts.guarantees.obligations_2
# contracts.guarantees.obligations_3
# contracts.guarantees.obligations_4
# contracts.guarantees.obligations_5
# contracts.guarantees.obligations_6
# contracts.guarantees.obligations_7
# contracts.guarantees.obligations_8
# contracts.guarantees.obligations_9
# contracts.guarantees.obligations_10
# contracts.guarantees.obligations_11
# contracts.guarantees.obligations_12
# contracts.guarantees.obligations_13
# contracts.guarantees.obligations_14
# contracts.guarantees.obligations_15
# contracts.guarantees.obligations_16
# contracts.guarantees.obligations_17
# contracts.guarantees.obligations_18
# contracts.investmentProjects.id q1
# contracts.investmentProjects.id q2
# contracts.investmentProjects.id q3
# contracts.investmentProjects.id q4
# contracts.amendments.amendsAmount_pyg
# contracts.amendments.amendsAmount_usd

# contracts.documents.DocumentTypeDetails_1
# contracts.documents.DocumentTypeDetails_2
# contracts.documents.DocumentTypeDetails_3
# contracts.documents.DocumentTypeDetails_4
# contracts.documents.DocumentTypeDetails_5
# contracts.documents.DocumentTypeDetails_6
# contracts.documents.DocumentTypeDetails_7
# contracts.documents.DocumentTypeDetails_8
# contracts.documents.DocumentTypeDetails_9
# contracts.documents.DocumentTypeDetails_10
# contracts.documents.DocumentTypeDetails_11
# contracts.documents.DocumentTypeDetails_12

# awards.documents.DocumentTypeDetails_1
# awards.documents.DocumentTypeDetails_2
# awards.documents.DocumentTypeDetails_3
# awards.documents.DocumentTypeDetails_4
# awards.documents.DocumentTypeDetails_5
# awards.documents.DocumentTypeDetails_6
# awards.documents.DocumentTypeDetails_7
# awards.documents.DocumentTypeDetails_8
# awards.documents.DocumentTypeDetails_9
# awards.documents.DocumentTypeDetails_10
# awards.documents.DocumentTypeDetails_11
# awards.documents.DocumentTypeDetails_12
# awards.documents.DocumentTypeDetails_13
# awards.documents.DocumentTypeDetails_14
# awards.documents.DocumentTypeDetails_15
# awards.documents.DocumentTypeDetails_16
# awards.documents.DocumentTypeDetails_17
# awards.documents.DocumentTypeDetails_18
# awards.documents.DocumentTypeDetails_19
# awards.documents.DocumentTypeDetails_20
# awards.documents.DocumentTypeDetails_21
# awards.status_1
# awards.status_2
# awards.status_3
# awards.status_4

# buyer.id q1
# buyer.id q2
# buyer.id q3
# buyer.id q4
# buyer.name q1
# buyer.name q2
# buyer.name q3
# buyer.name q4
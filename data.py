import pandas as pd 

def count_length (data):
	if type(data) == list:
		return len(data)
	return 0
	# return len(data) 
def get_month (data):
	if type(data) == str:
		return int(data.split('-')[1])
	return None
def get_year (data):
	if type(data) == str:
		return int(data.split('-')[0])
	return None
def get_year_month (data):
	if type(data) == str:
		return int(data.split('-')[0])*100 + int(data.split('-')[1])
	return None
def get_pd_dataframe(ocds_data: dict):
	data = {
		'tender.value.amount': ocds_data['tender']['value']['amount'],
		'tender.tenderPeriod.durationInDays': ocds_data['tender']['tenderPeriod']['durationInDays'],
		'tender.enquiryPeriod.durationInDays': ocds_data['tender']['enquiryPeriod']['durationInDays'],
		'tender.numberOfTenderers': ocds_data['tender']['numberOfTenderers'],
		'tender.techniques.hasElectronicAuction': 1 if ocds_data['tender']['techniques']['hasElectronicAuction'] else 0,
		'tender.lots.count': count_length(ocds_data['tender']['lots']),
		'tender.enquiries.count': count_length(ocds_data['tender']['enquiries']),
		'tender.bidOpening.date.month': get_month(ocds_data['tender']['bidOpening']['date']),
		'tender.bidOpening.date.year': get_year(ocds_data['tender']['bidOpening']['date']),
		'tender.bidOpening.date.yearmonth': get_year_month(ocds_data['tender']['bidOpening']['date']),
		'tender.datePublished.month': get_month(ocds_data['tender']['datePublished']),
		'tender.datePublished.year': get_year(ocds_data['tender']['datePublished']),
		'tender.datePublished.yearmonth': get_year_month(ocds_data['tender']['datePublished']),
		'tender.tenderPeriod.startDate.month': get_month(ocds_data['tender']['tenderPeriod']['startDate']),
		'tender.tenderPeriod.startDate.year': get_year(ocds_data['tender']['tenderPeriod']['startDate']),
		'tender.tenderPeriod.startDate.yearmonth': get_year_month(ocds_data['tender']['tenderPeriod']['startDate']),
		'tender.tenderPeriod.endDate.month': get_month(ocds_data['tender']['tenderPeriod']['endDate']),
		'tender.tenderPeriod.endDate.year': get_year(ocds_data['tender']['tenderPeriod']['endDate']),
		'tender.tenderPeriod.endDate.yearmonth': get_year_month(ocds_data['tender']['tenderPeriod']['endDate']),
		'tender.awardPeriod.startDate.month': get_month(ocds_data['tender']['awardPeriod']['startDate']),
		'tender.awardPeriod.startDate.year': get_year(ocds_data['tender']['awardPeriod']['startDate']),
		'tender.awardPeriod.startDate.yearmonth': get_year_month(ocds_data['tender']['awardPeriod']['startDate']),
		'tender.enquiryPeriod.endDate.month': get_month(ocds_data['tender']['enquiryPeriod']['endDate']),
		'tender.enquiryPeriod.endDate.year': get_year(ocds_data['tender']['enquiryPeriod']['endDate']),
		'tender.enquiryPeriod.endDate.yearmonth': get_year_month(ocds_data['tender']['enquiryPeriod']['endDate']),
		'tender.enquiryPeriod.startDate.month': get_month(ocds_data['tender']['enquiryPeriod']['startDate']),
		'tender.enquiryPeriod.startDate.year': get_year(ocds_data['tender']['enquiryPeriod']['startDate']),
		'tender.enquiryPeriod.startDate.yearmonth': get_year_month(ocds_data['tender']['enquiryPeriod']['startDate']),
		'tender.status_active': ocds_data['tender']['status'] == 'active',
		'tender.status_cancelled': ocds_data['tender']['status'] == 'cancelled',
		'tender.status_complete': ocds_data['tender']['status'] == 'complete',
		'tender.status_unsuccessful': ocds_data['tender']['status'] == 'unsuccesful',
		'tender.awardCriteria_antecedentes_firma_consultora': ocds_data['tender']['awardCriteria'] == 'antecedentes_firma_consultora',
		'tender.awardCriteria_priceOnly': ocds_data['tender']['awardCriteria'] == 'priceOnly',
		'tender.awardCriteria_qualityOnly': ocds_data['tender']['awardCriteria'] == 'qualityOnly',
		'tender.awardCriteria_ratedCriteria': ocds_data['tender']['awardCriteria'] == 'ratedCriteria',
		'planning.identifier': ocds_data['planning']['identifier'],
		'planning.budget.amount.amount': ocds_data['planning']['budget']['amount']['amount'],
		'planning.budget.amount.currency_PYG': ocds_data['planning']['budget']['amount']['currency'] == 'PYG',
		'planning.budget.amount.currency_USD': ocds_data['planning']['budget']['amount']['currency'] == 'USD',
		'planning.estimatedDate.month': get_month(ocds_data['planning']['estimatedDate']),
		'planning.estimatedDate.year': get_year(ocds_data['planning']['estimatedDate']),
		'planning.estimatedDate.yearmonth': get_year_month(ocds_data['planning']['estimatedDate']),
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
		'tender.statusDetails_En Convocatoria (Abierta)': ocds_data['tender']['statusDetails'] == 'En Convocatoria (Abierta)',
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
		'tender.procurementMethod_open': ocds_data['tender']['procurementMethod'] == 'open',
		# 'tender.procurementMethodRationale_covid-19': if procurementMethodRationale in ocds_data['tender']['procurementMethodRationale'] == 'covid-19',
		# 'tender.procurementIntention.rationale_covid-19': ocds_data['tender']['procurementIntention']['rationale'] == 'covid-19',
		'awards.count': count_length(ocds_data['awards']),
		'contracts.count': count_length(ocds_data['contracts']),
		# 'contracts.amendments.count': count_length(ocds_data['contracts']['amendments']), es un array
		# 'contracts.implementation.purchaseOrders.count': count_length(ocds_data['contracts']['implementation']['purchaseOrders']),, es un array
		# 'contracts.implementation.transactions.count': count_length(ocds_data['contracts']['implementation']['transactions']),, es un array
		# 'tender.criteria.id': ocds_data['tender']['criteria']['id'], es un array
 		'tender.enquiries total': count_length(ocds_data['tender']['enquiries']),
		# tender.enquiries respondidos
		# tender.enquiries porcentaje
	}
	data = pd.DataFrame([data])
	return data



# missing data:

# tender.procurementIntention.status_complete
# tender.procurementIntention.statusDetails_Ejecutada

# tender.eligibilityCriteria q1
# tender.eligibilityCriteria q2
# tender.eligibilityCriteria q3
# tender.eligibilityCriteria q4
# tender.mainProcurementCategoryDetails q1
# tender.mainProcurementCategoryDetails q2
# tender.mainProcurementCategoryDetails q3
# tender.mainProcurementCategoryDetails q4
# tender.submissionMethodDetails q1
# tender.submissionMethodDetails q2
# tender.submissionMethodDetails q3
# tender.submissionMethodDetails q4
# tender.ProcurementIntentionCategory q1
# tender.ProcurementIntentionCategory q2
# tender.ProcurementIntentionCategory q3
# tender.ProcurementIntentionCategory q4
# tender.procurementMethodDetails q1
# tender.procurementMethodDetails q2
# tender.procurementMethodDetails q3
# tender.procurementMethodDetails q4
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


# Preguntas Sin Respuesta
# Enmiendas  del contrato
# Proveedores Notificados CO
# Monto faltante
# Criterio de evaluacion faltante
# Tiempo de convocatoria LPN
# Oferente Unico
# Tiempo de Convocatoria CO


# tender.coveredBy_1
# tender.coveredBy_2
# tender.coveredBy_3
# tender.coveredBy_4
# tender.coveredBy_5
# tender.coveredBy_6
# tender.coveredBy_7
# tender.coveredBy_8
# tender.notifiedSuppliers.id q1
# tender.notifiedSuppliers.id q2
# tender.notifiedSuppliers.id q3
# tender.notifiedSuppliers.id q4
# tender.tenderers.id q1
# tender.tenderers.id q2
# tender.tenderers.id q3
# tender.tenderers.id q4
# tender.items.classification.id.n5 q1
# tender.items.classification.id.n5 q2
# tender.items.classification.id.n5 q3
# tender.items.classification.id.n5 q4
# tender.items.classification.id.n4 q1
# tender.items.classification.id.n4 q2
# tender.items.classification.id.n4 q3
# tender.items.classification.id.n4 q4
# tender.items.classification.id.n3 q1
# tender.items.classification.id.n3 q2
# tender.items.classification.id.n3 q3
# tender.items.classification.id.n3 q4
# tender.items.classification.id.n2_1
# tender.items.classification.id.n2_2
# tender.items.classification.id.n2_3
# tender.items.classification.id.n2_4
# tender.items.classification.id.n2_5
# tender.items.classification.id.n2_6
# tender.items.classification.id.n2_7
# tender.items.classification.id.n2_8
# tender.items.classification.id.n2_9
# tender.items.classification.id.n2_10
# tender.items.classification.id.n2_11
# tender.items.classification.id.n2_12
# tender.items.classification.id.n2_13
# tender.items.classification.id.n2_14
# tender.items.classification.id.n2_15
# tender.items.classification.id.n2_16
# tender.items.classification.id.n2_17
# tender.items.classification.id.n2_18
# tender.items.classification.id.n2_19
# tender.items.classification.id.n2_20
# tender.items.classification.id.n2_21
# tender.items.classification.id.n2_22
# tender.items.classification.id.n1_1
# tender.items.classification.id.n1_2
# tender.items.classification.id.n1_3
# tender.items.classification.id.n1_4
# tender.items.classification.id.n1_5
# tender.items.classification.id.n1_6
# tender.items.classification.id.n1_7
# tender.items.classification.id.n1_8
# tender.items.classification.id.n1_9
# tender.items.classification.id.n1_10
# tender.items.classification.id.n1_11
# tender.items.classification.id.n1_12
# tender.items.classification.id.n1_13
# tender.items.classification.id.n1_1_1
# tender.items.classification.id.n1_1_2
# tender.items.classification.id.n1_1_3
# tender.items.classification.id.n1_1_4
# tender.items.classification.id.n1_1_5
# tender.items.classification.id.n1_1_6
# tender.items.classification.id.n1_1_7
# tender.items.classification.id.n1_1_8
# tender.items.classification.id.n1_1_9
# tender.items.classification.id.n1_1_10
# tender.items.classification.id.n1_1_11
# tender.items.classification.id.n1_1_12
# tender.items.classification.id.n1_1_13
# tender.items.classification.id.n1_1_14
# tender.items.classification.id.n1_1_15
# tender.items.classification.id.n1_1_16
# tender.items.classification.id.n1_1_17
# tender.items.classification.id.n1_1_18
# tender.items.classification.id.n1_1_19
# tender.items.classification.id.n1_1_20
# tender.items.classification.id.n1_1_21
# tender.items.classification.id.n1_1_22
# tender.items.classification.id.n1_1_23
# tender.items.classification.id.n1_1_24
# tender.items.classification.id.n1_1_25
# tender.items.classification.id.n1_1_26
# tender.items.classification.id.n1_1_27
# tender.items.classification.id.n1_1_28
# tender.items.classification.id.n1_1_29
# tender.items.classification.id.n1_1_30
# tender.items.classification.id.n1_1_31
# tender.items.classification.id.n1_1_32
# tender.items.classification.id.n1_1_33
# tender.items.classification.id.n1_1_34
# tender.items.classification.id.n1_1_35
# tender.items.classification.id.n1_1_36
# tender.items.classification.id.n1_1_37
# tender.items.classification.id.n1_1_38
# tender.items.classification.id.n1_1_39
# tender.items.classification.id.n1_1_40
# tender.items.classification.id.n1_1_41
# tender.items.classification.id.n1_1_42
# tender.items.classification.id.n1_1_43
# tender.items.classification.id.n1_1_44
# tender.items.classification.id.n1_1_45
# tender.items.classification.id.n1_1_46
# tender.items.classification.id.n1_1_47
# tender.items.classification.id.n1_1_48
# tender.items.classification.id.n1_1_49
# tender.items.classification.id.n1_1_50
# tender.items.classification.id.n1_1_51
# tender.items.classification.id.n1_1_52
# tender.items.classification.id.n1_1_53
# tender.items.classification.id.n1_1_54
# tender.items.classification.id.n1_1_55
# tender.items.classification.id.n1_1_56
# tender.items.classification.id.n1_1_57
# tender.lots
# tender.documents.documentTypeDetails_1
# tender.documents.documentTypeDetails_2
# tender.documents.documentTypeDetails_3
# tender.documents.documentTypeDetails_4
# tender.documents.documentTypeDetails_5
# tender.documents.documentTypeDetails_6
# tender.documents.documentTypeDetails_7
# tender.documents.documentTypeDetails_8
# tender.documents.documentTypeDetails_9
# tender.documents.documentTypeDetails_10
# tender.documents.documentTypeDetails_11
# tender.documents.documentTypeDetails_12
# tender.documents.documentTypeDetails_13
# planning.items.classification.id.n4 q1
# planning.items.classification.id.n4 q2
# planning.items.classification.id.n4 q3
# planning.items.classification.id.n4 q4
# planning.items.classification.id.n3 q1
# planning.items.classification.id.n3 q2
# planning.items.classification.id.n3 q3
# planning.items.classification.id.n3 q4
# planning.items.classification.id.n2_1
# planning.items.classification.id.n2_2
# planning.items.classification.id.n2_3
# planning.items.classification.id.n2_4
# planning.items.classification.id.n2_5
# planning.items.classification.id.n2_6
# planning.items.classification.id.n2_7
# planning.items.classification.id.n2_8
# planning.items.classification.id.n2_9
# planning.items.classification.id.n2_10
# planning.items.classification.id.n2_11
# planning.items.classification.id.n2_12
# planning.items.classification.id.n2_13
# planning.items.classification.id.n2_14
# planning.items.classification.id.n2_15
# planning.items.classification.id.n2_16
# planning.items.classification.id.n2_17
# planning.items.classification.id.n2_18
# planning.items.classification.id.n2_19
# planning.items.classification.id.n2_20
# planning.items.classification.id.n2_21
# planning.items.classification.id.n2_22
# planning.items.classification.id.n2_23
# planning.items.classification.id.n2_24
# planning.items.classification.id.n2_25
# planning.items.classification.id.n2_26
# planning.items.classification.id.n2_27
# planning.items.classification.id.n2_28
# planning.items.classification.id.n2_29
# planning.items.classification.id.n2_30
# planning.items.classification.id.n2_31
# planning.items.classification.id.n2_32
# planning.items.classification.id.n2_33
# planning.items.classification.id.n2_34
# planning.items.classification.id.n2_35
# planning.items.classification.id.n2_36
# planning.items.classification.id.n2_37
# planning.items.classification.id.n2_38
# planning.items.classification.id.n2_39
# planning.items.classification.id.n2_40
# planning.items.classification.id.n2_41
# planning.items.classification.id.n2_42
# planning.items.classification.id.n2_43
# planning.items.classification.id.n2_44
# planning.items.classification.id.n1_1
# planning.items.classification.id.n1_2
# planning.items.classification.id.n1_3
# planning.items.classification.id.n1_4
# planning.items.classification.id.n1_5
# planning.items.classification.id.n1_6
# planning.items.classification.id.n1_7
# planning.items.classification.id.n1_8
# planning.items.classification.id.n1_9
# planning.items.classification.id.n1_10
# planning.items.classification.id.n1_11
# planning.items.classification.id.n1_12
# planning.items.classification.id.n1_13
# planning.items.classification.id.n1_14
# planning.items.classification.id.n1_15
# planning.items.classification.id.n1_16
# planning.items.classification.id.n1_1_1
# planning.items.classification.id.n1_1_2
# planning.items.classification.id.n1_1_3
# planning.items.classification.id.n1_1_4
# planning.items.classification.id.n1_1_5
# planning.items.classification.id.n1_1_6
# planning.items.classification.id.n1_1_7
# planning.items.classification.id.n1_1_8
# planning.items.classification.id.n1_1_9
# planning.items.classification.id.n1_1_10
# planning.items.classification.id.n1_1_11
# planning.items.classification.id.n1_1_12
# planning.items.classification.id.n1_1_13
# planning.items.classification.id.n1_1_14
# planning.items.classification.id.n1_1_15
# planning.items.classification.id.n1_1_16
# planning.items.classification.id.n1_1_17
# planning.items.classification.id.n1_1_18
# planning.items.classification.id.n1_1_19
# planning.items.classification.id.n1_1_20
# planning.items.classification.id.n1_1_21
# planning.items.classification.id.n1_1_22
# planning.items.classification.id.n1_1_23
# planning.items.classification.id.n1_1_24
# planning.items.classification.id.n1_1_25
# planning.items.classification.id.n1_1_26
# planning.items.classification.id.n1_1_27
# planning.items.classification.id.n1_1_28
# planning.items.classification.id.n1_1_29
# planning.items.classification.id.n1_1_30
# planning.items.classification.id.n1_1_31
# planning.items.classification.id.n1_1_32
# planning.items.classification.id.n1_1_33
# planning.items.classification.id.n1_1_34
# planning.items.classification.id.n1_1_35
# planning.items.classification.id.n1_1_36
# planning.items.classification.id.n1_1_37
# planning.items.classification.id.n1_1_38
# planning.items.classification.id.n1_1_39
# planning.items.classification.id.n1_1_40
# planning.items.classification.id.n1_1_41
# planning.items.classification.id.n1_1_42
# planning.items.classification.id.n1_1_43
# planning.items.classification.id.n1_1_44
# planning.items.classification.id.n1_1_45
# planning.items.classification.id.n1_1_46
# planning.items.classification.id.n1_1_47
# planning.items.classification.id.n1_1_48
# planning.items.classification.id.n1_1_49
# planning.items.classification.id.n1_1_50
# planning.items.classification.id.n1_1_51
# planning.items.classification.id.n1_1_52
# planning.items.classification.id.n1_1_53
# planning.items.classification.id.n1_1_54
# planning.items.classification.id.n1_1_55
# planning.items.classification.id.n1_1_56
# planning.items.classification.id.n1_1_57
# planning.items.classification.id.n1_1_58

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
# contracts.value.amount_pyg
# contracts.value.amount_usd
# contracts.status_1
# contracts.status_2
# contracts.status_3
# contracts.status_4
# contracts.statusDetails_1
# contracts.statusDetails_2
# contracts.statusDetails_3
# contracts.statusDetails_4
# contracts.statusDetails_5
# contracts.statusDetails_6
# contracts.statusDetails_7
# contracts.statusDetails_8
# contracts.statusDetails_9
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
# awards.suppliers.id q1
# awards.suppliers.id q2
# awards.suppliers.id q3
# awards.suppliers.id q4
# awards.value.amount_pyg
# awards.value.amount_usd
# awards.status_1
# awards.status_2
# awards.status_3
# awards.status_4
# awards.statusDetails_1
# awards.statusDetails_2
# awards.statusDetails_3
# awards.statusDetails_4
# awards.statusDetails_5
# awards.statusDetails_6
# awards.statusDetails_7
# awards.statusDetails_8
# awards.statusDetails_9
# awards.statusDetails_10
# awards.statusDetails_11
# parties.details.EntityType candidate_1
# parties.details.EntityType candidate_2
# parties.details.EntityType candidate_3
# parties.details.EntityType candidate_4
# parties.details.EntityType enquirer_1
# parties.details.EntityType enquirer_2
# parties.details.EntityType enquirer_3
# parties.details.EntityType enquirer_4
# parties.details.EntityType payer_1
# parties.details.EntityType payer_2
# parties.details.EntityType payer_3
# parties.details.EntityType payer_4
# parties.details.EntityType payee_1
# parties.details.EntityType payee_2
# parties.details.EntityType payee_3
# parties.details.EntityType payee_4
# parties.details.EntityType supplier_1
# parties.details.EntityType supplier_2
# parties.details.EntityType supplier_3
# parties.details.EntityType supplier_4
# parties.details.EntityType procuringEntity_1
# parties.details.EntityType procuringEntity_2
# parties.details.EntityType procuringEntity_3
# parties.details.EntityType procuringEntity_4
# parties.details.EntityType buyer_1
# parties.details.EntityType buyer_2
# parties.details.EntityType buyer_3
# parties.details.EntityType buyer_4
# parties.details.EntityType tenderer_1
# parties.details.EntityType tenderer_2
# parties.details.EntityType tenderer_3
# parties.details.EntityType tenderer_4
# parties.details.EntityType notifiedSupplier_1
# parties.details.EntityType notifiedSupplier_2
# parties.details.EntityType notifiedSupplier_3
# parties.details.EntityType notifiedSupplier_4
# parties.details.legalEntityTypeDetail candidate_1
# parties.details.legalEntityTypeDetail candidate_2
# parties.details.legalEntityTypeDetail candidate_3
# parties.details.legalEntityTypeDetail candidate_4
# parties.details.legalEntityTypeDetail candidate_5
# parties.details.legalEntityTypeDetail candidate_6
# parties.details.legalEntityTypeDetail candidate_7
# parties.details.legalEntityTypeDetail candidate_8
# parties.details.legalEntityTypeDetail candidate_9
# parties.details.legalEntityTypeDetail candidate_10
# parties.details.legalEntityTypeDetail candidate_11
# parties.details.legalEntityTypeDetail candidate_12
# parties.details.legalEntityTypeDetail candidate_13
# parties.details.legalEntityTypeDetail candidate_14
# parties.details.legalEntityTypeDetail candidate_15
# parties.details.legalEntityTypeDetail candidate_16
# parties.details.legalEntityTypeDetail candidate_17
# parties.details.legalEntityTypeDetail candidate_18
# parties.details.legalEntityTypeDetail candidate_19
# parties.details.legalEntityTypeDetail candidate_20
# parties.details.legalEntityTypeDetail candidate_21
# parties.details.legalEntityTypeDetail candidate_22
# parties.details.legalEntityTypeDetail candidate_23
# parties.details.legalEntityTypeDetail candidate_24
# parties.details.legalEntityTypeDetail candidate_25
# parties.details.legalEntityTypeDetail enquirer_1
# parties.details.legalEntityTypeDetail enquirer_2
# parties.details.legalEntityTypeDetail enquirer_3
# parties.details.legalEntityTypeDetail enquirer_4
# parties.details.legalEntityTypeDetail enquirer_5
# parties.details.legalEntityTypeDetail enquirer_6
# parties.details.legalEntityTypeDetail enquirer_7
# parties.details.legalEntityTypeDetail enquirer_8
# parties.details.legalEntityTypeDetail enquirer_9
# parties.details.legalEntityTypeDetail enquirer_10
# parties.details.legalEntityTypeDetail enquirer_11
# parties.details.legalEntityTypeDetail enquirer_12
# parties.details.legalEntityTypeDetail enquirer_13
# parties.details.legalEntityTypeDetail enquirer_14
# parties.details.legalEntityTypeDetail enquirer_15
# parties.details.legalEntityTypeDetail enquirer_16
# parties.details.legalEntityTypeDetail enquirer_17
# parties.details.legalEntityTypeDetail enquirer_18
# parties.details.legalEntityTypeDetail enquirer_19
# parties.details.legalEntityTypeDetail enquirer_20
# parties.details.legalEntityTypeDetail enquirer_21
# parties.details.legalEntityTypeDetail enquirer_22
# parties.details.legalEntityTypeDetail enquirer_23
# parties.details.legalEntityTypeDetail enquirer_24
# parties.details.legalEntityTypeDetail enquirer_25
# parties.details.legalEntityTypeDetail payer_1
# parties.details.legalEntityTypeDetail payer_2
# parties.details.legalEntityTypeDetail payer_3
# parties.details.legalEntityTypeDetail payer_4
# parties.details.legalEntityTypeDetail payer_5
# parties.details.legalEntityTypeDetail payer_6
# parties.details.legalEntityTypeDetail payer_7
# parties.details.legalEntityTypeDetail payer_8
# parties.details.legalEntityTypeDetail payer_9
# parties.details.legalEntityTypeDetail payer_10
# parties.details.legalEntityTypeDetail payer_11
# parties.details.legalEntityTypeDetail payer_12
# parties.details.legalEntityTypeDetail payer_13
# parties.details.legalEntityTypeDetail payer_14
# parties.details.legalEntityTypeDetail payer_15
# parties.details.legalEntityTypeDetail payer_16
# parties.details.legalEntityTypeDetail payer_17
# parties.details.legalEntityTypeDetail payer_18
# parties.details.legalEntityTypeDetail payer_19
# parties.details.legalEntityTypeDetail payer_20
# parties.details.legalEntityTypeDetail payer_21
# parties.details.legalEntityTypeDetail payer_22
# parties.details.legalEntityTypeDetail payer_23
# parties.details.legalEntityTypeDetail payer_24
# parties.details.legalEntityTypeDetail payer_25
# parties.details.legalEntityTypeDetail payee_1
# parties.details.legalEntityTypeDetail payee_2
# parties.details.legalEntityTypeDetail payee_3
# parties.details.legalEntityTypeDetail payee_4
# parties.details.legalEntityTypeDetail payee_5
# parties.details.legalEntityTypeDetail payee_6
# parties.details.legalEntityTypeDetail payee_7
# parties.details.legalEntityTypeDetail payee_8
# parties.details.legalEntityTypeDetail payee_9
# parties.details.legalEntityTypeDetail payee_10
# parties.details.legalEntityTypeDetail payee_11
# parties.details.legalEntityTypeDetail payee_12
# parties.details.legalEntityTypeDetail payee_13
# parties.details.legalEntityTypeDetail payee_14
# parties.details.legalEntityTypeDetail payee_15
# parties.details.legalEntityTypeDetail payee_16
# parties.details.legalEntityTypeDetail payee_17
# parties.details.legalEntityTypeDetail payee_18
# parties.details.legalEntityTypeDetail payee_19
# parties.details.legalEntityTypeDetail payee_20
# parties.details.legalEntityTypeDetail payee_21
# parties.details.legalEntityTypeDetail payee_22
# parties.details.legalEntityTypeDetail payee_23
# parties.details.legalEntityTypeDetail payee_24
# parties.details.legalEntityTypeDetail payee_25
# parties.details.legalEntityTypeDetail supplier_1
# parties.details.legalEntityTypeDetail supplier_2
# parties.details.legalEntityTypeDetail supplier_3
# parties.details.legalEntityTypeDetail supplier_4
# parties.details.legalEntityTypeDetail supplier_5
# parties.details.legalEntityTypeDetail supplier_6
# parties.details.legalEntityTypeDetail supplier_7
# parties.details.legalEntityTypeDetail supplier_8
# parties.details.legalEntityTypeDetail supplier_9
# parties.details.legalEntityTypeDetail supplier_10
# parties.details.legalEntityTypeDetail supplier_11
# parties.details.legalEntityTypeDetail supplier_12
# parties.details.legalEntityTypeDetail supplier_13
# parties.details.legalEntityTypeDetail supplier_14
# parties.details.legalEntityTypeDetail supplier_15
# parties.details.legalEntityTypeDetail supplier_16
# parties.details.legalEntityTypeDetail supplier_17
# parties.details.legalEntityTypeDetail supplier_18
# parties.details.legalEntityTypeDetail supplier_19
# parties.details.legalEntityTypeDetail supplier_20
# parties.details.legalEntityTypeDetail supplier_21
# parties.details.legalEntityTypeDetail supplier_22
# parties.details.legalEntityTypeDetail supplier_23
# parties.details.legalEntityTypeDetail supplier_24
# parties.details.legalEntityTypeDetail supplier_25
# parties.details.legalEntityTypeDetail procuringEntity_1
# parties.details.legalEntityTypeDetail procuringEntity_2
# parties.details.legalEntityTypeDetail procuringEntity_3
# parties.details.legalEntityTypeDetail procuringEntity_4
# parties.details.legalEntityTypeDetail procuringEntity_5
# parties.details.legalEntityTypeDetail procuringEntity_6
# parties.details.legalEntityTypeDetail procuringEntity_7
# parties.details.legalEntityTypeDetail procuringEntity_8
# parties.details.legalEntityTypeDetail procuringEntity_9
# parties.details.legalEntityTypeDetail procuringEntity_10
# parties.details.legalEntityTypeDetail procuringEntity_11
# parties.details.legalEntityTypeDetail procuringEntity_12
# parties.details.legalEntityTypeDetail procuringEntity_13
# parties.details.legalEntityTypeDetail procuringEntity_14
# parties.details.legalEntityTypeDetail procuringEntity_15
# parties.details.legalEntityTypeDetail procuringEntity_16
# parties.details.legalEntityTypeDetail procuringEntity_17
# parties.details.legalEntityTypeDetail procuringEntity_18
# parties.details.legalEntityTypeDetail procuringEntity_19
# parties.details.legalEntityTypeDetail procuringEntity_20
# parties.details.legalEntityTypeDetail procuringEntity_21
# parties.details.legalEntityTypeDetail procuringEntity_22
# parties.details.legalEntityTypeDetail procuringEntity_23
# parties.details.legalEntityTypeDetail procuringEntity_24
# parties.details.legalEntityTypeDetail procuringEntity_25
# parties.details.legalEntityTypeDetail buyer_1
# parties.details.legalEntityTypeDetail buyer_2
# parties.details.legalEntityTypeDetail buyer_3
# parties.details.legalEntityTypeDetail buyer_4
# parties.details.legalEntityTypeDetail buyer_5
# parties.details.legalEntityTypeDetail buyer_6
# parties.details.legalEntityTypeDetail buyer_7
# parties.details.legalEntityTypeDetail buyer_8
# parties.details.legalEntityTypeDetail buyer_9
# parties.details.legalEntityTypeDetail buyer_10
# parties.details.legalEntityTypeDetail buyer_11
# parties.details.legalEntityTypeDetail buyer_12
# parties.details.legalEntityTypeDetail buyer_13
# parties.details.legalEntityTypeDetail buyer_14
# parties.details.legalEntityTypeDetail buyer_15
# parties.details.legalEntityTypeDetail buyer_16
# parties.details.legalEntityTypeDetail buyer_17
# parties.details.legalEntityTypeDetail buyer_18
# parties.details.legalEntityTypeDetail buyer_19
# parties.details.legalEntityTypeDetail buyer_20
# parties.details.legalEntityTypeDetail buyer_21
# parties.details.legalEntityTypeDetail buyer_22
# parties.details.legalEntityTypeDetail buyer_23
# parties.details.legalEntityTypeDetail buyer_24
# parties.details.legalEntityTypeDetail buyer_25
# parties.details.legalEntityTypeDetail tenderer_1
# parties.details.legalEntityTypeDetail tenderer_2
# parties.details.legalEntityTypeDetail tenderer_3
# parties.details.legalEntityTypeDetail tenderer_4
# parties.details.legalEntityTypeDetail tenderer_5
# parties.details.legalEntityTypeDetail tenderer_6
# parties.details.legalEntityTypeDetail tenderer_7
# parties.details.legalEntityTypeDetail tenderer_8
# parties.details.legalEntityTypeDetail tenderer_9
# parties.details.legalEntityTypeDetail tenderer_10
# parties.details.legalEntityTypeDetail tenderer_11
# parties.details.legalEntityTypeDetail tenderer_12
# parties.details.legalEntityTypeDetail tenderer_13
# parties.details.legalEntityTypeDetail tenderer_14
# parties.details.legalEntityTypeDetail tenderer_15
# parties.details.legalEntityTypeDetail tenderer_16
# parties.details.legalEntityTypeDetail tenderer_17
# parties.details.legalEntityTypeDetail tenderer_18
# parties.details.legalEntityTypeDetail tenderer_19
# parties.details.legalEntityTypeDetail tenderer_20
# parties.details.legalEntityTypeDetail tenderer_21
# parties.details.legalEntityTypeDetail tenderer_22
# parties.details.legalEntityTypeDetail tenderer_23
# parties.details.legalEntityTypeDetail tenderer_24
# parties.details.legalEntityTypeDetail tenderer_25
# parties.details.legalEntityTypeDetail notifiedSupplier_1
# parties.details.legalEntityTypeDetail notifiedSupplier_2
# parties.details.legalEntityTypeDetail notifiedSupplier_3
# parties.details.legalEntityTypeDetail notifiedSupplier_4
# parties.details.legalEntityTypeDetail notifiedSupplier_5
# parties.details.legalEntityTypeDetail notifiedSupplier_6
# parties.details.legalEntityTypeDetail notifiedSupplier_7
# parties.details.legalEntityTypeDetail notifiedSupplier_8
# parties.details.legalEntityTypeDetail notifiedSupplier_9
# parties.details.legalEntityTypeDetail notifiedSupplier_10
# parties.details.legalEntityTypeDetail notifiedSupplier_11
# parties.details.legalEntityTypeDetail notifiedSupplier_12
# parties.details.legalEntityTypeDetail notifiedSupplier_13
# parties.details.legalEntityTypeDetail notifiedSupplier_14
# parties.details.legalEntityTypeDetail notifiedSupplier_15
# parties.details.legalEntityTypeDetail notifiedSupplier_16
# parties.details.legalEntityTypeDetail notifiedSupplier_17
# parties.details.legalEntityTypeDetail notifiedSupplier_18
# parties.details.legalEntityTypeDetail notifiedSupplier_19
# parties.details.legalEntityTypeDetail notifiedSupplier_20
# parties.details.legalEntityTypeDetail notifiedSupplier_21
# parties.details.legalEntityTypeDetail notifiedSupplier_22
# parties.details.legalEntityTypeDetail notifiedSupplier_23
# parties.details.legalEntityTypeDetail notifiedSupplier_24
# parties.details.legalEntityTypeDetail notifiedSupplier_25
# parties.roles candidate q1
# parties.roles candidate q2
# parties.roles candidate q3
# parties.roles candidate q4
# parties.roles enquirer q1
# parties.roles enquirer q2
# parties.roles enquirer q3
# parties.roles enquirer q4
# parties.roles payer q1
# parties.roles payer q2
# parties.roles payer q3
# parties.roles payer q4
# parties.roles payee q1
# parties.roles payee q2
# parties.roles payee q3
# parties.roles payee q4
# parties.roles supplier q1
# parties.roles supplier q2
# parties.roles supplier q3
# parties.roles supplier q4
# parties.roles procuringEntity q1
# parties.roles procuringEntity q2
# parties.roles procuringEntity q3
# parties.roles procuringEntity q4
# parties.roles buyer q1
# parties.roles buyer q2
# parties.roles buyer q3
# parties.roles buyer q4
# parties.roles tenderer q1
# parties.roles tenderer q2
# parties.roles tenderer q3
# parties.roles tenderer q4
# parties.roles notifiedSupplier q1
# parties.roles notifiedSupplier q2
# parties.roles notifiedSupplier q3
# parties.roles notifiedSupplier q4
# buyer.id q1
# buyer.id q2
# buyer.id q3
# buyer.id q4
# buyer.name q1
# buyer.name q2
# buyer.name q3
# buyer.name q4
from data.general_utils import count_length
from data.custom_pickle_methods import TenderDocumentsDocumentTypeDetail

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




# VARIABLE IMPORTANCE
# --- DONE ---
# tender.procurementMethodDetails q4	4085.9177	1.0	0.0983
# tender.documents.documentTypeDetails_1	2482.5088	0.6076	0.0597
# tender.value.amount	2446.6934	0.5988	0.0589
# planning.budget.amount.amount	2038.4487	0.4989	0.0491
# tender.numberOfTenderers	1720.2838	0.4210	0.0414
# tender.documents.documentTypeDetails_2	1164.0098	0.2849	0.0280
# date.yearmonth	895.8250	0.2192	0.0216
# tender.tenderPeriod.durationInDays	765.1774	0.1873	0.0184
# date.month	622.0535	0.1522	0.0150
# planning.identifier	496.0822	0.1214	0.0119
# tender.enquiryPeriod.endDate.yearmonth	492.8662	0.1206	0.0119
# tender.enquiryPeriod.durationInDays	475.4081	0.1164	0.0114
# tender.hasEnquiries_False	445.3940	0.1090	0.0107
# tender.enquiryPeriod.endDate.year	438.8650	0.1074	0.0106
# tender.hasEnquiries_True	438.3706	0.1073	0.0106
# contracts.value.amount_pyg	423.9971	0.1038	0.0102
# tender.documents.documentTypeDetails_13	420.1869	0.1028	0.0101
# date.year	392.4234	0.0960	0.0094
# planning.estimatedDate.month	391.1234	0.0957	0.0094
# awards.value.amount_pyg	386.3469	0.0946	0.0093
# tender.tenderPeriod.endDate.yearmonth	382.8535	0.0937	0.0092
# tender.datePublished.yearmonth	382.4442	0.0936	0.0092
# tender.tenderPeriod.startDate.yearmonth	381.6205	0.0934	0.0092
# tender.documents.documentTypeDetails_3	381.5552	0.0934	0.0092
# Oferente Unico	364.2455	0.0891	0.0088
# tender.enquiryPeriod.startDate.yearmonth	322.2376	0.0789	0.0078
# tender.enquiries porcentaje	316.2770	0.0774	0.0076
# tender.procurementMethodDetails q1	303.6610	0.0743	0.0073
# tender.enquiryPeriod.endDate.month	261.9514	0.0641	0.0063
# tender.documents.documentTypeDetails_6	243.7191	0.0596	0.0059
# tender.bidOpening.date.month	225.4909	0.0552	0.0054
# tender.awardPeriod.startDate.month	221.1198	0.0541	0.0053
# --- REMAINING---

# parties.details.legalEntityTypeDetail tenderer_3	206.6613	0.0506	0.0050
# parties.details.legalEntityTypeDetail notifiedSupplier_1	196.5828	0.0481	0.0047
# parties.details.legalEntityTypeDetail notifiedSupplier_3	196.1885	0.0480	0.0047
# tender.documents.documentTypeDetails_7	181.3734	0.0444	0.0044
# awards.documents.DocumentTypeDetails_3	173.5098	0.0425	0.0042
# tender.documents.documentTypeDetails_11	166.4568	0.0407	0.0040
# tender.notifiedSuppliers.id q4	166.1698	0.0407	0.0040
# parties.roles notifiedSupplier q2	165.2717	0.0404	0.0040
# parties.details.legalEntityTypeDetail tenderer_1	164.6845	0.0403	0.0040
# tender.datePublished.year	160.5135	0.0393	0.0039
# tender.notifiedSuppliers.id q2	160.0062	0.0392	0.0039
# tender.tenderPeriod.endDate.month	154.5209	0.0378	0.0037
# tender.enquiryPeriod.startDate.month	150.2691	0.0368	0.0036
# contracts.documents.DocumentTypeDetails_2	149.9422	0.0367	0.0036
# tender.datePublished.month	148.6000	0.0364	0.0036
# tender.mainProcurementCategory_services	144.0898	0.0353	0.0035
# parties.roles notifiedSupplier q3	142.7743	0.0349	0.0034
# parties.roles notifiedSupplier q4	140.5254	0.0344	0.0034
# tender.notifiedSuppliers.id q1	138.6548	0.0339	0.0033
# parties.roles tenderer q3	137.9390	0.0338	0.0033
# tender.enquiryPeriod.startDate.year	136.6498	0.0334	0.0033
# awards.documents.DocumentTypeDetails_2	131.0876	0.0321	0.0032
# tender.statusDetails_Suspendida	130.0047	0.0318	0.0031
# tender.tenderPeriod.startDate.month	129.2932	0.0316	0.0031
# awards.documents.DocumentTypeDetails_8	128.9490	0.0316	0.0031
# tender.notifiedSuppliers.id q3	128.2529	0.0314	0.0031
# tender.awardCriteriaDetails_Por Total	124.8761	0.0306	0.0030
# tender.enquiries total	124.5149	0.0305	0.0030
# parties.roles notifiedSupplier q1	120.8446	0.0296	0.0029
# parties.details.legalEntityTypeDetail notifiedSupplier_4	119.2093	0.0292	0.0029
# planning.estimatedDate.yearmonth	118.4092	0.0290	0.0028
# contracts.documents.DocumentTypeDetails_1	117.8243	0.0288	0.0028
# awards.documents.DocumentTypeDetails_1	116.9902	0.0286	0.0028
# tender.enquiries.count	115.0681	0.0282	0.0028
# tender.tenderers.id q2	114.1641	0.0279	0.0027
# contracts.implementation.transactions.count	110.8425	0.0271	0.0027
# tender.enquiries respondidos	109.7275	0.0269	0.0026
# tender.submissionMethodDetails q4	108.6431	0.0266	0.0026
# tender.tenderPeriod.endDate.year	107.6786	0.0264	0.0026
# tender.mainProcurementCategoryDetails q1	98.5033	0.0241	0.0024
# awards.documents.DocumentTypeDetails_6	95.7040	0.0234	0.0023
# tender.documents.documentTypeDetails_8	95.3221	0.0233	0.0023
# parties.roles tenderer q1	95.3214	0.0233	0.0023
# tender.tenderers.id q4	95.3037	0.0233	0.0023
# contracts.documents.DocumentTypeDetails_3	94.2618	0.0231	0.0023
# parties.roles tenderer q4	93.9049	0.0230	0.0023
# tender.documents.documentTypeDetails_10	93.5317	0.0229	0.0023
# planning.items.classification.id.n1_16	91.7993	0.0225	0.0022
# tender.tenderers.id q3	91.7348	0.0225	0.0022
# parties.roles tenderer q2	91.6072	0.0224	0.0022
# tender.mainProcurementCategory_works	91.5821	0.0224	0.0022
# parties.details.legalEntityTypeDetail tenderer_4	90.8835	0.0222	0.0022
# parties.details.legalEntityTypeDetail supplier_3	90.5369	0.0222	0.0022
# tender.tenderers.id q1	89.1096	0.0218	0.0021
# contracts.amendments.count	88.5945	0.0217	0.0021
# tender.mainProcurementCategory_goods	88.1713	0.0216	0.0021
# tender.statusDetails_Anulada o Cancelada	87.4196	0.0214	0.0021
# tender.submissionMethodDetails q3	87.3354	0.0214	0.0021
# contracts.status_1	86.9856	0.0213	0.0021
# tender.awardCriteriaDetails_Por Item	85.5137	0.0209	0.0021
# tender.coveredBy_1	84.7357	0.0207	0.0020
# contracts.guarantees.obligations_1	83.9057	0.0205	0.0020
# tender.awardPeriod.startDate.year	83.6274	0.0205	0.0020
# parties.roles procuringEntity q1	83.2735	0.0204	0.0020
# planning.items.classification.id.n2_44	81.7232	0.0200	0.0020
# tender.tenderPeriod.startDate.year	81.1438	0.0199	0.0020
# tender.procuringEntity.name q1	80.5938	0.0197	0.0019
# planning.items.classification.id.n2_11	80.4943	0.0197	0.0019
# tender.bidOpening.date.year	80.1329	0.0196	0.0019
# tender.bidOpening.date.yearmonth	79.2195	0.0194	0.0019
# awards.documents.DocumentTypeDetails_5	75.6677	0.0185	0.0018
# tender.awardCriteriaDetails_Por Lote	75.5907	0.0185	0.0018
# planning.items.classification.id.n2_26	75.3552	0.0184	0.0018
# parties.details.legalEntityTypeDetail notifiedSupplier_2	75.0005	0.0184	0.0018
# tender.items.classification.id.n5 q4	73.6508	0.0180	0.0018
# Enmiendas del contrato	73.6042	0.0180	0.0018
# parties.details.EntityType buyer_3	69.5061	0.0170	0.0017
# tender.submissionMethodDetails q1	69.5037	0.0170	0.0017
# tender.status_cancelled	69.2665	0.0170	0.0017
# tender.status_complete	68.8670	0.0169	0.0017
# tender.documents.documentTypeDetails_9	67.3494	0.0165	0.0016
# tender.awardPeriod.startDate.yearmonth	67.2612	0.0165	0.0016
# planning.estimatedDate.year	66.2734	0.0162	0.0016
# tender.mainProcurementCategoryDetails q3	65.1773	0.0160	0.0016
# tender.procurementMethodDetails q3	65.1128	0.0159	0.0016
# tender.procuringEntity.id q1	63.6584	0.0156	0.0015
# planning.items.classification.id.n3 q2	63.4044	0.0155	0.0015
# tender.submissionMethodDetails q2	63.1321	0.0155	0.0015
# tender.items.classification.id.n5 q3	60.6512	0.0148	0.0015
# awards.documents.DocumentTypeDetails_12	59.9219	0.0147	0.0014
# planning.items.classification.id.n4 q3	59.3996	0.0145	0.0014
# parties.roles procuringEntity q2	59.2857	0.0145	0.0014
# parties.details.legalEntityTypeDetail supplier_1	58.8990	0.0144	0.0014
# parties.details.EntityType procuringEntity_4	58.3922	0.0143	0.0014
# parties.details.legalEntityTypeDetail payee_3	58.2384	0.0143	0.0014
# tender.documents.documentTypeDetails_5	57.6838	0.0141	0.0014
# tender.items.classification.id.n2_1	57.3918	0.0140	0.0014
# awards.documents.DocumentTypeDetails_4	57.3804	0.0140	0.0014
# awards.suppliers.id q2	57.0019	0.0140	0.0014
# tender.items.classification.id.n1_13	56.9272	0.0139	0.0014
# parties.details.legalEntityTypeDetail enquirer_3	56.1901	0.0138	0.0014
# tender.mainProcurementCategoryDetails q4	56.1185	0.0137	0.0014
# tender.coveredBy_2	55.4019	0.0136	0.0013
# tender.items.classification.id.n5 q2	54.4952	0.0133	0.0013
# tender.items.classification.id.n3 q4	53.9766	0.0132	0.0013
# parties.roles procuringEntity q3	53.9075	0.0132	0.0013
# planning.items.classification.id.n3 q4	53.3700	0.0131	0.0013
# planning.items.classification.id.n4 q4	53.3195	0.0130	0.0013
# parties.details.legalEntityTypeDetail tenderer_2	52.4096	0.0128	0.0013
# awards.documents.DocumentTypeDetails_9	52.1007	0.0128	0.0013
# tender.items.classification.id.n2_22	51.7908	0.0127	0.0012
# tender.procuringEntity.name q2	51.4905	0.0126	0.0012
# awards.status_1	51.4833	0.0126	0.0012
# contracts.statusDetails_1	51.3826	0.0126	0.0012
# parties.roles payee q2	51.0022	0.0125	0.0012
# parties.details.EntityType procuringEntity_3	50.7915	0.0124	0.0012
# tender.statusDetails_En Evaluacion (Cerrada)	49.8098	0.0122	0.0012
# parties.details.EntityType buyer_1	49.4325	0.0121	0.0012
# parties.roles supplier q3	49.1994	0.0120	0.0012
# parties.details.EntityType buyer_4	48.5794	0.0119	0.0012
# parties.roles payee q3	48.4246	0.0119	0.0012
# tender.documents.documentTypeDetails_4	47.7385	0.0117	0.0011
# parties.roles supplier q4	47.5671	0.0116	0.0011
# parties.details.EntityType procuringEntity_1	47.3632	0.0116	0.0011
# parties.details.EntityType payer_3	47.1255	0.0115	0.0011
# planning.items.classification.id.n4 q1	46.5220	0.0114	0.0011
# planning.items.classification.id.n4 q2	46.3638	0.0113	0.0011
# buyer.id q1	46.3491	0.0113	0.0011
# parties.roles supplier q2	45.9971	0.0113	0.0011
# tender.items.classification.id.n4 q3	45.7239	0.0112	0.0011
# contracts.investmentProjects.id q1	45.2154	0.0111	0.0011
# parties.roles procuringEntity q4	45.0510	0.0110	0.0011
# awards.suppliers.id q3	44.8417	0.0110	0.0011
# buyer.name q1	44.3699	0.0109	0.0011
# planning.items.classification.id.n3 q1	43.9676	0.0108	0.0011
# parties.roles buyer q2	43.8875	0.0107	0.0011
# tender.items.classification.id.n4 q4	43.5209	0.0107	0.0010
# tender.items.classification.id.n5 q1	43.4647	0.0106	0.0010
# planning.items.classification.id.n3 q3	42.8678	0.0105	0.0010
# tender.procuringEntity.id q4	42.4966	0.0104	0.0010
# contracts.implementation.purchaseOrders.count	41.9523	0.0103	0.0010
# tender.items.classification.id.n1_1_25	41.1033	0.0101	0.0010
# tender.statusDetails_Desierta	40.8804	0.0100	0.0010
# tender.items.classification.id.n3 q2	40.8509	0.0100	0.0010
# parties.roles supplier q1	40.5900	0.0099	0.0010
# tender.items.classification.id.n3 q3	40.3265	0.0099	0.0010
# contracts.guarantees.obligations_2	40.1719	0.0098	0.0010
# awards.suppliers.id q4	39.6343	0.0097	0.0010
# tender.procuringEntity.name q3	39.3985	0.0096	0.0009
# parties.roles payer q2	38.9314	0.0095	0.0009
# contracts.status_2	38.8012	0.0095	0.0009
# contracts.count	38.3238	0.0094	0.0009
# tender.techniques.hasElectronicAuction	38.2015	0.0093	0.0009
# parties.roles payer q3	38.0953	0.0093	0.0009
# parties.roles buyer q1	37.9550	0.0093	0.0009
# tender.procuringEntity.id q2	37.7254	0.0092	0.0009
# planning.items.classification.id.n1_9	37.5250	0.0092	0.0009
# awards.suppliers.id q1	37.4722	0.0092	0.0009
# planning.items.classification.id.n1_1_9	37.2277	0.0091	0.0009
# planning.items.classification.id.n2_1	37.1796	0.0091	0.0009
# tender.items.classification.id.n4 q2	36.7683	0.0090	0.0009
# parties.roles payer q4	36.5670	0.0089	0.0009
# parties.roles payee q1	36.2886	0.0089	0.0009
# tender.items.classification.id.n1_1_1	36.0149	0.0088	0.0009
# tender.items.classification.id.n2_3	35.8347	0.0088	0.0009
# awards.count	35.7265	0.0087	0.0009
# parties.roles buyer q3	35.6841	0.0087	0.0009
# parties.roles buyer q4	35.2000	0.0086	0.0008
# parties.details.legalEntityTypeDetail supplier_4	34.7273	0.0085	0.0008
# parties.details.EntityType payer_4	34.7144	0.0085	0.0008
# parties.details.legalEntityTypeDetail payee_1	34.5656	0.0085	0.0008
# buyer.name q2	34.3341	0.0084	0.0008
# parties.details.legalEntityTypeDetail payee_4	34.1374	0.0084	0.0008
# tender.coveredBy_5	34.1135	0.0083	0.0008
# planning.items.classification.id.n2_2	33.9110	0.0083	0.0008
# parties.roles enquirer q4	33.8374	0.0083	0.0008
# tender.items.classification.id.n1_1_21	33.8267	0.0083	0.0008
# tender.mainProcurementCategoryDetails q2	33.7712	0.0083	0.0008
# tender.documents.documentTypeDetails_12	32.3286	0.0079	0.0008
# planning.items.classification.id.n1_1_39	31.9398	0.0078	0.0008
# tender.items.classification.id.n1_1	31.7712	0.0078	0.0008
# planning.items.classification.id.n1_1_36	31.3219	0.0077	0.0008
# planning.items.classification.id.n1_1_32	30.1865	0.0074	0.0007
# tender.status_unsuccessful	29.7670	0.0073	0.0007
# buyer.id q2	29.5432	0.0072	0.0007
# tender.items.classification.id.n1_1_36	29.4745	0.0072	0.0007
# parties.roles payer q1	29.3840	0.0072	0.0007
# buyer.id q3	29.2707	0.0072	0.0007
# tender.items.classification.id.n1_1_41	29.0564	0.0071	0.0007
# awards.statusDetails_1	29.0442	0.0071	0.0007
# planning.items.classification.id.n1_1_22	28.9872	0.0071	0.0007
# tender.items.classification.id.n1_1_37	28.8278	0.0071	0.0007
# buyer.name q4	28.7626	0.0070	0.0007
# planning.items.classification.id.n2_5	28.6706	0.0070	0.0007
# planning.items.classification.id.n1_1_1	28.5288	0.0070	0.0007
# parties.roles payee q4	28.3609	0.0069	0.0007
# buyer.id q4	28.2376	0.0069	0.0007
# tender.items.classification.id.n2_17	28.1530	0.0069	0.0007
# tender.procuringEntity.name q4	28.0404	0.0069	0.0007
# tender.lots.count	27.8663	0.0068	0.0007
# contracts.documents.DocumentTypeDetails_5	27.5922	0.0068	0.0007
# planning.items.classification.id.n1_1	27.0247	0.0066	0.0007
# planning.items.classification.id.n1_1_25	26.9987	0.0066	0.0006
# tender.items.classification.id.n4 q1	26.8589	0.0066	0.0006
# contracts.guarantees.obligations_10	26.6178	0.0065	0.0006
# Tiempo de convocatoria LPN	26.3607	0.0065	0.0006
# tender.items.classification.id.n1_1_4	25.6976	0.0063	0.0006
# buyer.name q3	25.4083	0.0062	0.0006
# tender.items.classification.id.n1_1_30	25.3838	0.0062	0.0006
# parties.details.legalEntityTypeDetail tenderer_8	25.3771	0.0062	0.0006
# tender.items.classification.id.n2_6	25.2369	0.0062	0.0006
# parties.details.legalEntityTypeDetail supplier_8	25.0798	0.0061	0.0006
# planning.items.classification.id.n2_32	24.4227	0.0060	0.0006
# tender.items.classification.id.n1_1_18	24.2481	0.0059	0.0006
# tender.procuringEntity.id q3	23.7985	0.0058	0.0006
# planning.items.classification.id.n1_1_23	23.5629	0.0058	0.0006
# parties.details.legalEntityTypeDetail tenderer_6	22.7069	0.0056	0.0005
# tender.awardCriteria_priceOnly	21.9174	0.0054	0.0005
# planning.items.classification.id.n1_1_21	21.5398	0.0053	0.0005
# awards.documents.DocumentTypeDetails_11	21.1400	0.0052	0.0005
# tender.items.classification.id.n3 q1	21.0348	0.0051	0.0005
# tender.items.classification.id.n1_1_24	21.0230	0.0051	0.0005
# planning.items.classification.id.n1_1_17	20.9641	0.0051	0.0005
# parties.details.legalEntityTypeDetail supplier_2	20.4508	0.0050	0.0005
# planning.items.classification.id.n1_1_35	20.3380	0.0050	0.0005
# tender.items.classification.id.n1_1_16	20.3235	0.0050	0.0005
# contracts.documents.DocumentTypeDetails_4	20.2327	0.0050	0.0005
# tender.items.classification.id.n1_1_48	20.1819	0.0049	0.0005
# planning.items.classification.id.n1_1_29	19.9456	0.0049	0.0005
# planning.items.classification.id.n1_1_26	19.9153	0.0049	0.0005
# tender.items.classification.id.n2_2	19.8665	0.0049	0.0005
# parties.details.legalEntityTypeDetail notifiedSupplier_8	19.7297	0.0048	0.0005
# tender.lots	19.4563	0.0048	0.0005
# tender.items.classification.id.n1_1_15	19.4336	0.0048	0.0005
# parties.roles enquirer q3	19.3364	0.0047	0.0005
# planning.items.classification.id.n1_1_19	19.3093	0.0047	0.0005
# tender.items.classification.id.n1_1_45	19.1834	0.0047	0.0005
# tender.items.classification.id.n1_4	19.1500	0.0047	0.0005
# tender.items.classification.id.n1_1_6	19.1473	0.0047	0.0005
# tender.items.classification.id.n1_1_19	19.0835	0.0047	0.0005
# planning.items.classification.id.n2_25	19.0346	0.0047	0.0005
# tender.items.classification.id.n2_21	19.0018	0.0047	0.0005
# parties.details.legalEntityTypeDetail notifiedSupplier_6	18.3568	0.0045	0.0004
# tender.items.classification.id.n1_9	17.6333	0.0043	0.0004
# tender.items.classification.id.n1_1_26	17.5980	0.0043	0.0004
# planning.items.classification.id.n1_1_16	17.4628	0.0043	0.0004
# tender.items.classification.id.n1_1_9	17.2494	0.0042	0.0004
# parties.details.legalEntityTypeDetail notifiedSupplier_5	17.1522	0.0042	0.0004
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
# parties.details.legalEntityTypeDetail notifiedSupplier_11	13.2806	0.0033	0.0003
# planning.items.classification.id.n1_1_48	13.0610	0.0032	0.0003
# parties.details.legalEntityTypeDetail enquirer_4	12.9762	0.0032	0.0003
# planning.items.classification.id.n1_5	12.6877	0.0031	0.0003
# planning.items.classification.id.n1_1_20	12.5356	0.0031	0.0003
# planning.items.classification.id.n2_6	12.4218	0.0030	0.0003
# planning.items.classification.id.n1_12	12.3429	0.0030	0.0003
# parties.details.legalEntityTypeDetail enquirer_1	12.3165	0.0030	0.0003
# tender.items.classification.id.n1_1_43	12.1375	0.0030	0.0003
# planning.items.classification.id.n1_1_12	12.0458	0.0029	0.0003
# tender.awardCriteria_ratedCriteria	11.8094	0.0029	0.0003
# planning.items.classification.id.n2_13	11.6454	0.0029	0.0003
# tender.items.classification.id.n2_10	11.6251	0.0028	0.0003
# tender.items.classification.id.n1_2	11.5564	0.0028	0.0003
# Tiempo de Convocatoria CO	11.5323	0.0028	0.0003
# planning.items.classification.id.n1_1_37	11.3662	0.0028	0.0003
# parties.roles enquirer q1	11.2491	0.0028	0.0003
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
# planning.items.classification.id.n1_13	10.3981	0.0025	0.0003
# tender.items.classification.id.n1_1_2	10.2633	0.0025	0.0002
# tender.items.classification.id.n1_1_29	10.2324	0.0025	0.0002
# tender.items.classification.id.n1_1_35	10.1280	0.0025	0.0002
# parties.details.legalEntityTypeDetail notifiedSupplier_16	10.0396	0.0025	0.0002
# tender.items.classification.id.n1_3	9.9613	0.0024	0.0002
# contracts.guarantees.obligations_5	9.9418	0.0024	0.0002
# parties.details.legalEntityTypeDetail notifiedSupplier_14	9.8088	0.0024	0.0002
# planning.items.classification.id.n1_2	9.6985	0.0024	0.0002
# contracts.investmentProjects.id q2	9.6662	0.0024	0.0002
# planning.items.classification.id.n1_1_30	9.4596	0.0023	0.0002
# parties.details.legalEntityTypeDetail notifiedSupplier_9	9.4150	0.0023	0.0002
# parties.details.legalEntityTypeDetail tenderer_5	9.3408	0.0023	0.0002
# planning.items.classification.id.n1_1_44	9.2963	0.0023	0.0002
# Preguntas Sin Respuesta	9.2762	0.0023	0.0002
# parties.details.legalEntityTypeDetail tenderer_7	9.2231	0.0023	0.0002
# parties.details.legalEntityTypeDetail payee_9	9.1203	0.0022	0.0002
# tender.items.classification.id.n1_5	8.8385	0.0022	0.0002
# parties.details.legalEntityTypeDetail tenderer_12	8.7510	0.0021	0.0002
# planning.items.classification.id.n2_36	8.6659	0.0021	0.0002
# planning.items.classification.id.n2_23	8.6479	0.0021	0.0002
# tender.coveredBy_4	8.6328	0.0021	0.0002
# tender.items.classification.id.n1_7	8.5705	0.0021	0.0002
# planning.items.classification.id.n1_7	8.5574	0.0021	0.0002
# planning.items.classification.id.n2_42	8.5042	0.0021	0.0002
# planning.items.classification.id.n2_3	8.4994	0.0021	0.0002
# tender.items.classification.id.n1_1_34	8.3756	0.0020	0.0002
# planning.items.classification.id.n1_15	8.3344	0.0020	0.0002
# tender.items.classification.id.n1_1_3	8.1909	0.0020	0.0002
# parties.roles enquirer q2	8.1890	0.0020	0.0002
# tender.items.classification.id.n1_1_5	8.1823	0.0020	0.0002
# tender.items.classification.id.n1_1_38	7.8390	0.0019	0.0002
# parties.details.EntityType procuringEntity_2	7.7643	0.0019	0.0002
# planning.items.classification.id.n1_1_43	7.6207	0.0019	0.0002
# tender.items.classification.id.n2_18	7.5834	0.0019	0.0002
# planning.items.classification.id.n1_14	7.5557	0.0018	0.0002
# parties.details.legalEntityTypeDetail tenderer_9	7.4918	0.0018	0.0002
# parties.details.legalEntityTypeDetail supplier_5	7.3900	0.0018	0.0002
# parties.details.legalEntityTypeDetail tenderer_11	7.3009	0.0018	0.0002
# planning.items.classification.id.n1_10	7.1310	0.0017	0.0002
# tender.coveredBy_6	7.0125	0.0017	0.0002
# parties.details.legalEntityTypeDetail enquirer_6	6.9285	0.0017	0.0002
# parties.details.legalEntityTypeDetail supplier_6	6.9148	0.0017	0.0002
# parties.details.legalEntityTypeDetail tenderer_17	6.8123	0.0017	0.0002
# tender.items.classification.id.n1_1_7	6.7752	0.0017	0.0002
# tender.items.classification.id.n1_1_12	6.7644	0.0017	0.0002
# tender.items.classification.id.n1_12	6.7314	0.0016	0.0002
# parties.details.legalEntityTypeDetail tenderer_14	6.6996	0.0016	0.0002
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
# parties.details.legalEntityTypeDetail tenderer_16	5.8372	0.0014	0.0001
# tender.items.classification.id.n1_1_40	5.8164	0.0014	0.0001
# tender.items.classification.id.n1_1_46	5.7642	0.0014	0.0001
# planning.items.classification.id.n2_20	5.6926	0.0014	0.0001
# parties.details.legalEntityTypeDetail notifiedSupplier_7	5.6308	0.0014	0.0001
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
# parties.details.legalEntityTypeDetail notifiedSupplier_15	4.8484	0.0012	0.0001
# tender.items.classification.id.n2_15	4.8286	0.0012	0.0001
# planning.items.classification.id.n1_1_40	4.8187	0.0012	0.0001
# parties.details.legalEntityTypeDetail notifiedSupplier_13	4.8157	0.0012	0.0001
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
# planning.items.classification.id.n1_4	3.4033	0.0008	0.0001
# tender.items.classification.id.n2_4	3.3653	0.0008	0.0001
# planning.items.classification.id.n2_9	3.3006	0.0008	0.0001
# tender.items.classification.id.n2_7	3.2254	0.0008	0.0001
# tender.eligibilityCriteria q1	3.1358	0.0008	0.0001
# tender.items.classification.id.n1_1_44	3.1147	0.0008	0.0001
# planning.items.classification.id.n1_1_10	3.0388	0.0007	0.0001
# parties.details.EntityType payer_2	3.0379	0.0007	0.0001
# tender.items.classification.id.n1_1_32	2.9104	0.0007	0.0001
# contracts.documents.DocumentTypeDetails_8	2.8210	0.0007	0.0001
# tender.awardCriteria_qualityOnly	2.7746	0.0007	0.0001
# planning.budget.amount.currency_USD	2.7576	0.0007	0.0001
# planning.items.classification.id.n2_31	2.7156	0.0007	0.0001
# parties.details.legalEntityTypeDetail supplier_7	2.6828	0.0007	0.0001
# tender.items.classification.id.n2_9	2.6777	0.0007	0.0001
# parties.details.legalEntityTypeDetail payee_6	2.6485	0.0006	0.0001
# parties.details.legalEntityTypeDetail supplier_11	2.6347	0.0006	0.0001
# contracts.guarantees.obligations_11	2.6210	0.0006	0.0001
# awards.documents.DocumentTypeDetails_13	2.6097	0.0006	0.0001
# tender.items.classification.id.n1_1_53	2.5216	0.0006	0.0001
# parties.details.legalEntityTypeDetail supplier_9	2.4959	0.0006	0.0001
# planning.items.classification.id.n1_1_46	2.3424	0.0006	0.0001
# parties.details.legalEntityTypeDetail supplier_12	2.3094	0.0006	0.0001
# parties.details.legalEntityTypeDetail enquirer_5	2.2786	0.0006	0.0001
# parties.details.legalEntityTypeDetail supplier_17	2.2727	0.0006	0.0001
# planning.items.classification.id.n2_7	2.2432	0.0005	0.0001
# parties.details.legalEntityTypeDetail payee_7	2.1188	0.0005	0.0001
# parties.details.legalEntityTypeDetail notifiedSupplier_12	2.1120	0.0005	0.0001
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
# parties.details.legalEntityTypeDetail notifiedSupplier_10	1.7131	0.0004	0.0
# contracts.status_3	1.6861	0.0004	0.0
# awards.value.amount_usd	1.5187	0.0004	0.0
# parties.details.legalEntityTypeDetail payee_11	1.5046	0.0004	0.0
# contracts.documents.DocumentTypeDetails_6	1.4312	0.0004	0.0
# planning.items.classification.id.n1_11	1.3535	0.0003	0.0
# tender.items.classification.id.n1_1_8	1.3344	0.0003	0.0
# planning.items.classification.id.n1_1_6	1.2222	0.0003	0.0
# planning.items.classification.id.n2_43	1.1334	0.0003	0.0
# contracts.guarantees.obligations_8	1.1224	0.0003	0.0
# tender.awardCriteriaDetails_Combinado	1.0837	0.0003	0.0
# parties.details.legalEntityTypeDetail tenderer_19	1.0820	0.0003	0.0
# tender.items.classification.id.n1_1_47	1.0406	0.0003	0.0
# parties.details.legalEntityTypeDetail tenderer_13	1.0114	0.0002	0.0
# planning.items.classification.id.n1_1_55	0.9555	0.0002	0.0
# planning.items.classification.id.n1_1_47	0.9066	0.0002	0.0
# parties.details.legalEntityTypeDetail payee_13	0.8777	0.0002	0.0
# planning.items.classification.id.n2_41	0.8764	0.0002	0.0
# tender.items.classification.id.n2_5	0.7393	0.0002	0.0
# tender.eligibilityCriteria q4	0.6228	0.0002	0.0
# parties.details.legalEntityTypeDetail supplier_16	0.6140	0.0002	0.0
# planning.items.classification.id.n1_1_52	0.5876	0.0001	0.0
# tender.items.classification.id.n2_12	0.5597	0.0001	0.0
# parties.details.legalEntityTypeDetail tenderer_10	0.5596	0.0001	0.0
# contracts.documents.DocumentTypeDetails_7	0.5532	0.0001	0.0
# parties.details.legalEntityTypeDetail enquirer_2	0.5358	0.0001	0.0
# parties.details.legalEntityTypeDetail enquirer_7	0.4606	0.0001	0.0
# contracts.value.amount_usd	0.4487	0.0001	0.0
# parties.details.legalEntityTypeDetail tenderer_15	0.4350	0.0001	0.0
# tender.items.classification.id.n1_1_39	0.4308	0.0001	0.0
# parties.details.legalEntityTypeDetail notifiedSupplier_19	0.3997	0.0001	0.0
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
# parties.details.legalEntityTypeDetail notifiedSupplier_22	0.1525	0.0	0.0
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
# contracts.documents.DocumentTypeDetails_9	0	0	0
# contracts.documents.DocumentTypeDetails_10	0	0	0
# contracts.documents.DocumentTypeDetails_11	0	0	0
# contracts.statusDetails_8	0	0	0
# awards.documents.DocumentTypeDetails_7	0	0	0
# awards.documents.DocumentTypeDetails_10	0	0	0
# awards.documents.DocumentTypeDetails_15	0	0	0
# awards.documents.DocumentTypeDetails_16	0	0	0
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
# parties.details.legalEntityTypeDetail tenderer_20	0	0	0
# parties.details.legalEntityTypeDetail tenderer_21	0	0	0
# parties.details.legalEntityTypeDetail tenderer_22	0	0	0
# parties.details.legalEntityTypeDetail tenderer_23	0	0	0
# parties.details.legalEntityTypeDetail notifiedSupplier_17	0	0	0
# parties.details.legalEntityTypeDetail notifiedSupplier_18	0	0	0
# parties.details.legalEntityTypeDetail notifiedSupplier_21	0	0	0
# parties.details.legalEntityTypeDetail notifiedSupplier_23	0	0	0
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
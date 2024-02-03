from data.general_utils import count_length

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
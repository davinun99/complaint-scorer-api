########## GENERAL UTILS
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
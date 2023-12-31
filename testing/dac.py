import numpy as np
from pprint import pprint

def calc_gain(code_data_dict):
	'''
	Inputs:
		code_data_dict: Mapping with key:value of digital code:collection of 
			analog measurements taken for that code. For example
			{0: [0, 1e-3],
			 1: [1, 1.1, 2, 0]}
	Returns:
		Float. DAC gain (volts/LSB).
	'''
	code_max = max(code_data_dict.keys())
	code_min = min(code_data_dict.keys())
	dy = np.mean(code_data_dict[code_max])-np.mean(code_data_dict[code_min])
	dx = code_max - code_min
	return dy/dx

def calc_fsr(code_data_dict):
	'''
	Inputs:
		code_data_dict: Mapping with key:value of digital code:collection of 
			analog measurements taken for that code. For example
			{0: [0, 1e-3],
			 1: [1, 1.1, 2, 0]}
	Returns:
		Float. The full-scale range (V) of the DAC in question.
	Notes:
		This is only calculated using the endpoints of the DAC codes!
		This will not warn you if there are skipped codes--use DNL for that.
	'''
	code_max = max(code_data_dict.keys())
	code_min = min(code_data_dict.keys())
	return np.mean(code_data_dict[code_max])-np.mean(code_data_dict[code_min])

def calc_noise(code_data_dict):
	'''
	Inputs:
		code_data_dict: Mapping with key:value of digital code:collection of 
			analog measurements taken for that code. For example
			{0: [0, 1e-3],
			 1: [1, 1.1, 2, 0]}
	Returns:
		Dictionary. Key:value is code:RMS noise voltage.
	'''
	code_noise_dict = dict()
	for code, val_vec in code_data_dict.items():
		code_noise_dict[code] = np.std(val_vec)
	return code_noise_dict

def calc_dnl(code_data_dict):
	'''
	Inputs:
		code_data_dict: Mapping with key:value of digital code:collection of 
			analog measurements taken for that code. For example
			{0: [0, 1e-3],
			 1: [1, 1.1, 2, 0]}
	Returns:
		dnl_dict: Mapping with key:value of code:DNL
	Raises:
		ValueError: If the included codes are missing any intermediate
			integer values. 
	'''
	# Stop the user if a digital code wasn't tested
	code_max = max(code_data_dict.keys())
	for i in range(code_max):
		if i not in code_data_dict.keys():
			raise ValueError(f'Code {i} not found in data.')

	# Use the average of the analog readings
	avg_dict = {code:np.mean(vals) for (code,vals) in code_data_dict.items()}

	# Calculate steps (and account for the fact that DNL@0 is undefined)
	step_vec = [avg_dict[c+1]-avg_dict[c] for c in range(code_max)]
	step_avg = np.mean(step_vec)
	step_vec = [float('nan')] + step_vec

	# DNL undefined @ code 0
	dnl_dict = {code:(step_vec[code]-step_avg)/step_avg 
		for code in range(1, code_max)}

	return dnl_dict

def calc_inl(code_data_dict):
	'''
	Inputs:
		code_data_dict: Mapping with key:value of digital code:collection of 
			analog measurements taken for that code. For example
			{0: [0, 1e-3],
			 1: [1, 1.1, 2, 0]}
	Returns:
		inl_dict: Mapping with key:value of code:INL
	Raises:
		See dac_dnl.
	'''
	dnl_dict = calc_dnl(code_data_dict)

	code_max = max(code_data_dict.keys())
	inl_dict = dict()
	for code in dnl_dict.keys():
		inl_dict[code] = sum([dnl_dict[c] for c in range(1,code)])

	inl_dict[code_max] = 0

	return inl_dict

if __name__ == '__main__':
	code_data_dict = {0:0,
					1:1,
					2:2,
					3:2.5,
					4:4,
					5:5}
	pprint(dac_dnl(code_data_dict))
	pprint(dac_inl(code_data_dict))
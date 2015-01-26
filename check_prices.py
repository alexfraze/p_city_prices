import json

with open('okay','r') as f:
	_i = json.load(f)


	# if 'units' in i['scraped']:
	# 	if len(i['scraped']) == 2:
	# 		continue
	# 	if len(i['scraped']) > 2:
	# 		print("\n")
for i in _i:
	print("\n")
	for key in i.keys():
		print("{0}: {1}".format(key,i[key]))
		if 'scraped' in key:
			print("{0} : {1}".format("len: "+str(len(i['scraped'])), type(i['scraped'])))
			if 'units' in i['scraped']:
				print("    uom: {0}".format(i['scraped']['unit_of_measure']))
				print("    units: {0}".format(i['scraped']['units']))
				print("    prices: {0}".format(i['scraped']['prices']))
			if 'scraped_price' in i['scraped']:
				print("    price: {0}".format(i['scraped']['scraped_price']))
				print("    name: {0}".format(i['scraped']['scraped_name']))
		if 'csv_info' in key:
			for _key in i['csv_info'].keys():
				print("    {0}: {1}".format(_key,i['csv_info'][_key]))

			#for s in i['scraped']:
			#	print(s)
    


import pdb;pdb.set_trace()
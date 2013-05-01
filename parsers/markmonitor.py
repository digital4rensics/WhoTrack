def parse(data):
	extracted = {}
	temp = data.split('\n')
	#print temp
	for line in temp:
		if line.strip() == "Registrant:":
			offset = temp.index(line) + 1
			for i in range(6):
				if i == 0:
					extracted['name'] = temp[offset+i].strip()
				elif i == 1:
					extracted['organization'] = temp[offset+i].strip()
				elif i == 2:
					add = temp[offset+i].strip() + " " + temp[offset+i+1].strip() + " " + temp[offset+i+2].strip()
					extracted['address'] = add
				elif i == 5:
					temp2 = temp[offset+i].strip().split()
					extracted['email'] = temp2[0]
					extracted['phone'] = temp2[1]
					extracted['fax'] = temp2[3]

	if extracted:
		return extracted
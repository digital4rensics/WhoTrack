def parse(data):
	extracted = {}
	temp = data.split('\n')
	#print temp
	for line in temp:
		if line.strip() == "owner-c:":
			offset = temp.index(line) + 2
			for i in range(11):
				if i == 0:
					extracted['name'] = temp[offset+i].split(":")[1].strip()
				elif i == 1:
					extracted['organization'] = temp[offset+i].split(":")[1].strip()
				elif i == 3:
					add = temp[offset+i].split(":")[1].strip() + " " + temp[offset+i+1].split(":")[1].strip() + " " + temp[offset+i+2].split(":")[1].strip() + " " + temp[offset+i+3].split(":")[1].strip() + " " + temp[offset+i+4].split(":")[1].strip()
					extracted['address'] = add
				elif i == 8:
					extracted['phone'] = temp[offset+i].split(":")[1].strip()
				elif i == 9:		
					extracted['fax'] = temp[offset+i].split(":")[1].strip()
				elif i == 10:
					extracted['email'] = temp[offset+i].split(":")[1].strip()
	if extracted:
		return extracted
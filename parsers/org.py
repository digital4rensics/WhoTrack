def parse(data):
	extracted = {}
	temp = data.split('\n')
	for line in temp:
		if line.startswith("Registrant Name:"):
			temp2 = line.split(":")
			extracted['name'] = temp2[1].strip()
		elif line.startswith("Registrant Organization:"):
			temp2 = line.split(":")
			extracted['organization'] = temp2[1].strip()	
		elif line.startswith("Registrant Email:"):
			temp2 = line.split(":")
			extracted['email'] = temp2[1].strip()	
		elif line.startswith("Registrant FAX:"):
			temp2 = line.split(":")
			extracted['fax'] = temp2[1].strip()	
		elif line.startswith("Registrant Phone:"):
			temp2 = line.split(":")
			extracted['phone'] = temp2[1].strip()
		elif line.startswith("Registrant Street1:"):
			offset = temp.index(line)
			temp2 = []
			for i in range(7):
				temp3 = temp[offset+i].split(":")
				try:
					temp2.append(temp3[1].strip())
				except:
					temp2.append(None)
			add = ''.join(temp2)
			extracted['address'] = add
	if extracted:
		return extracted
def parse(data):
	extracted = {}
	temp = data.split('\n')
	#print temp
	for line in temp:
		if line.startswith("Registrant Info:"):
			offset = temp.index(line) + 1
			if temp[offset+9].strip() == "":
				for i in range(8):
					if i == 0:
						extracted['organization'] = temp[offset+i].strip()
					elif i == 1:
						extracted['name'] = temp[offset+i].strip()
					elif i == 2:
						add = temp[offset+i].strip() + " " + temp[offset+i+1].strip() + " " + temp[offset+i+2].strip()
						extracted['address'] = add
					elif i == 5:
						temp2 = temp[offset+i].strip().split()
						extracted['phone'] = temp2[1]
					elif i == 6:
						try:
							temp3 = temp[offset+i].strip().split()
							extracted['fax'] = temp3[1]
						except:
							extracted['fax'] = None
					elif i == 7:
						temp4 = temp[offset+i].strip().split()
						extracted['email'] = temp4[1]
			else:
				for i in range(7):
					if i == 0:
						extracted['name'] = temp[offset+i].strip()
					elif i == 1:
						add = temp[offset+i].strip() + " " + temp[offset+i+1].strip() + " " + temp[offset+i+2].strip()
						extracted['address'] = add
					elif i == 4:
						temp2 = temp[offset+i].strip().split()
						extracted['phone'] = temp2[1]
					elif i == 5:
						try:
							temp3 = temp[offset+i].strip().split()
							extracted['fax'] = temp3[1]
						except:
							extracted['fax'] = None
					elif i == 6:
						temp4 = temp[offset+i].strip().split()
						extracted['email'] = temp4[1]
						
	if extracted:
		return extracted
def parse(data):
	extracted = {}
	temp = data.split('\n')
	for line in temp:
		if line.startswith("person:"):
			temp2 = line.split(":")
			extracted['name'] = temp2[1].strip()
			extracted['organization'] = None
		elif line.startswith("org:"):
			temp2 = line.split(":")
			extracted['organization'] = temp2[1].strip()	
			extracted['name'] = None
			
	extracted['address'] = None
	extracted['email'] = None
	extracted['phone'] = None
	extracted['fax'] = None

	if extracted:
		return extracted
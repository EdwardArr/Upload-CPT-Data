filename = 'MODUL.txt'

def upload_modifiers(doc_ref):
	modifier_text_results = read_modifier_file()
	listOfTuples = create_list_of_tuples(modifier_text_results[1])
	write_to_firebase(listOfTuples, modifier_text_results[0], doc_ref)

def read_modifier_file():
	modifierIndexList = []
	f = open(filename, encoding='UTF-8', errors='ignore')
	lines = f.readlines()
	count = 0
	for line in lines:
		count += 1
		# hard coded to only look at lines that contains modifier info
		if count >= 44 and count < 415:
			if line.isspace():
				modifierIndexList.append(count+1)
	f.close()
	return [lines, modifierIndexList]

def create_list_of_tuples(modifierIndexList):
	modifierCount = 0
	listOfTuples = []
	for startOfLine in modifierIndexList:
		modifierCount += 1
		if startOfLine != modifierIndexList[-1]:
			endOfLine = modifierIndexList[modifierCount]-2
			listOfTuples.append((startOfLine,endOfLine))
	return listOfTuples

def write_to_firebase(listOfTuples, lines, doc_ref):
	for lineRange in listOfTuples:
		modifier = ""
		heading = ""
		description = ""
		note = ""
		joinedLine = ""
		count = 0
		for line in lines:
			count += 1
			# if line is between tuple range then...
			if count >= lineRange[0] and count <= lineRange[1]:
				# join all lines to one string
				joinedLine += line
		# grab the first two characters and save as modifier number
		modifier = joinedLine[0:2]
		# grab substring between modifier number and colon
		firstColonIndex = joinedLine.find(':')
		# grab substring after colon
		heading = joinedLine[3:firstColonIndex]	
		# find index of "Note"
		noteIndex = joinedLine[firstColonIndex+3:].find('Note')
		if noteIndex != -1:
			description = joinedLine[firstColonIndex+2:]
			note = description[noteIndex+7:]
			description = description[:noteIndex]
			modifier_dict = {
	            u'number':modifier,
	            u'heading':heading,
	            u'description':description,
	            u'note':note,
	            u'year': "2022"
	      }
			# doc_ref.document().set(modifier_dict)
			print("Modifier: {} ".format(modifier))
			print("Heading: {}".format(heading))
			print("Description: {}".format(description))
			print("Note: {}".format(note))
		else:
			description = joinedLine[firstColonIndex+2:]
			modifier_dict = {
	            u'number':modifier,
	            u'heading':heading,
	            u'description':description,
	            u'year': "2022" 
	      }
			# doc_ref.document().set(modifier_dict)
			print("Modifier: {} ".format(modifier))
			print("Heading: {}".format(heading))
			print("Description: {}".format(description))

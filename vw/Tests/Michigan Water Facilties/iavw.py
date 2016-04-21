		
def getIDsFromFile( filename: str):
	""" Opens a file whose name is specified in the 
	input and returns the list of IDs in that file. The 
	IDs in the file must be separated by linebreaks."""
	import json
	IDs = []
	print("Openning ID file...")
	file = open(filename, 'r')
	print("Reading IDs from file...")
	for line in file:
		IDs.append(line.rstrip())
	print("Finished reading " + str(len(IDs)) + \
		" IDs from file. Closing file...")
	file.close()
	print("ID File closed!")
	return IDs


def downloadMetaFiles( IDs: list, directoryToSave: str):
	""" Downloads the metadata file for each ID in the passed
	list of IDs in the directory specified."""

	import json
	import internetarchive as ia
	import os

	print("Downloading " + str(len(IDs)) + " item metadatas...")
	if not directoryToSave.endswith("/"):
		directoryToSave += "/"
	if not os.path.exists(directoryToSave):
		os.makedirs(directoryToSave)
	count = 1
	for ID in IDs:
		file = open(directoryToSave + ID + ".txt", 'w')
		meta = ia.get_item(ID).metadata
		json.dump(meta, file)
		if(count % 31 == 0):
			print('downloaded ' + str(count) + ' metadata files so far!')
		count += 1
	print("Successefully downloaded " + str(len(IDs)) + " metadatas!")



def getMetaFromFile(fileDir: str):
	"""Reads the metadata from a json file whose name is passed.
	If the file could not be read, an error is printed and the 
	file is skipped."""

	import json
	file = open(fileDir, 'r')
	try:
		jObject = json.load(file)
		return jObject
	except ValueError:
		print("Error reading JSON from " + fileDir)


def readMetaTextInDirectory( directory: str):
	"""Reads all the metadata files ending in .txt
	in the passed directory"""
	import os
	return [getMetaFromFile(directory + os.sep + f) 
			for f in os.listdir(directory)
			if  f.endswith('.txt')]

def proccessText( text: str):
	"""Accepts a string and returns a proccessed string ready for vw 
	proccessing"""
	newText = text.replace(':', 'COLON').replace('|', 'PIPE').replace('\n', ' ').replace('\r', ' ').replace("@", ' ')
	newText = newText.replace('<br>', ' ').replace("<\br>", ' ')
	newText = newText.replace('الدولة الاسلامية', ' ')
	newText = newText.replace('سكر', ' ')
	n2 = []
	for word in newText.split():
		if len(word) < 50:
			n2.append(word)
	return ' '.join(n2[:500])

def metadataToVWline( metadata: dict, positive: bool):
	ignored_keys = ['mediatype', 'sound', 'color', 'curation']
	data = ''
	if metadata is None:
		print('Found null metadata. Skipping.')
	else:
		for key in metadata:
			if key in ignored_keys:
				continue
			else:
				if(type(metadata[key]) == list):
					string = ' '.join(metadata[key])
					data += key + ' ' + proccessText(string) + " |"
				else:
					data += key + ' ' + proccessText(metadata[key]) + " |"
		#remove last trailing pipe and add new line
		data = data.rstrip('|')
		data += '\n'

		if(positive):
			data = "+1 |" + data
		else:
			data = "-1 |" + data
		
		return data

def writeVWlinesToFile(vwLines: list, filename: str):
	file = open(filename, 'w')
	print("opening Vwneg.txt file to write metadata")
	print("Writing lines to file...")
	for line in vwLines:
		file.write(line)
	print("Closing file...")
	file.close()
	print("File closed!")


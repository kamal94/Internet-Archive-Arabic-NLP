import internetarchive as ia
import json
from time import gmtime, strftime
import subprocess

# searches for the term and returns search results not in exisitingIDs
def findNewIDs(searchTerm, existingIDs):
	newIDs = []
	for result in ia.search_items(searchTerm):
		if result['identifier'] not in existingIDs:
			newIDs.append(result['identifier'])
	print('found ' + str(len(newIDs)) + " new results for query: " + searchTerm)
	return newIDs

# saves metadata in /metadata/IDNAME.txt
def downloadMetaFiles(IDs):
    print("Downloading " + str(len(IDs)) + " item metadatas...")
    count = 1
    for ID in IDs:
        file = open("metadata/"+ID+".txt", 'w')
        meta = ia.get_item(ID).metadata
        json.dump(meta, file)
        if(count % 31 == 0):
            print('downloaded ' + str(count) + ' metadata files so far!')
        count += 1
    print("Successefully downloaded " + str(len(IDs)) + " metadatas!")

#sort existing ID file
subprocess.call(['sort', 'existingIDs.txt'], stderr=subprocess.DEVNULL)
# read existing IDs from the ID file
IDFile = open("existingIDs.txt", 'r')
existingIDs = []
for line in IDFile:
	existingIDs.append(line.rstrip('\n'))

IDFile.close()

# find new IDs with the search query and download their meta files
query = "سكر"
print("searching for new IDs for query: " + query)
newIDs = findNewIDs(query, existingIDs)
downloadMetaFiles(newIDs)

# add the new IDs to the list of current IDs
IDFile = open("existingIDs.txt", 'a')
for ID in newIDs:
	IDFile.write(ID+"\n")

#log what has been added
logFile = open("logfile", 'a')
logFile.write(strftime("%Y-%m-%d %H:%M:%S", gmtime()) + " " + str(len(newIDs)) + " new IDs found.")
if(len(newIDs) > 0):
	for ID in newIDs:
		logFile.write("\t" + ID + "\n")
else:
	logFile.write("\n")
logFile.write("********")
logFile.close()
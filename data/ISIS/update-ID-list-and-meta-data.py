import internetarchive as ia
import json

# searches for the term and returns search results not in exisitingIDs
def findNewIDs(searchTerm, existingIDs):
	search = ia.search.Search(searchTerm)
	newIDs = []
	print('found ' + str(search.num_found) + " overall results for query: " + searchTerm)
	for result in search:
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


# read existing IDs from the 
IDFile = open("existingIDs.txt", 'r')
existingIDs = []
for line in IDFile:
	existingIDs.append(line.rstrip('\n'))

IDFile.close()

# find new IDs with the search query and download their meta files
query = "الدولة الاسلامية"
print("searching for new IDs for query: " + query)
newIDs = findNewIDs(query, existingIDs)
downloadMetaFiles(newIDs)

# add the new IDs to the list of current IDs
IDFile = open("existingIDs.txt", 'a')
for ID in newIDs:
	IDFile.write(ID+"\n")
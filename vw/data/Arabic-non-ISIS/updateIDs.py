import internetarchive as ia
import json, os, subprocess
from time import gmtime, strftime
import iavw

# read existing IDs from the ID file
searchTerm = "سكر"
downloadedIDs = []
print("looking for " + searchTerm)
for r in ia.search_items(searchTerm, params=dict(size=1000)):
	downloadedIDs.append(r['identifier'])

print("A total of " + str(len(downloadedIDs)) +" was found")

existingIDs = []

if os.path.exists('metadata/'):
	for f in os.listdir('metadata/'):
		if  f.endswith('.txt'):
			#remove file extension. split('.txt') doesn't work with 
			#ids that end in t
			existingIDs.append(f[:-4])


print("Number of existing IDs: " + str(len(existingIDs)))
newIDs = set(downloadedIDs) - (set(existingIDs))
print(str(len(newIDs)) + " new IDs were found")
# print(newIDs)
iavw.downloadMeta(newIDs, 'metadata', True)

# #log what has been added
logFile = open(".logfile", 'a')
logFile.write(strftime("%Y-%m-%d %H:%M:%S", gmtime()) + " " + str(len(newIDs)) + " new IDs found.\n")
if(len(newIDs) > 0):
	for ID in newIDs:
		logFile.write("\t" + ID + "\n")
else:
	logFile.write("\n")
logFile.write("********")
logFile.close()
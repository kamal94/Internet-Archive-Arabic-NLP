import iavw
ids = iavw.getIDsFromFile(filename='IDList.txt')
iavw.downloadMetaFiles(ids, 'metadata')
metadata = iavw.readMetaTextInDirectory('metadata')
posVwLines = []
for meta in metadata:
    posVwLines.append(iavw.metadataToVWline(meta, True))
    
iavw.writeVWlinesToFile(posVwLines, "testdata.te")
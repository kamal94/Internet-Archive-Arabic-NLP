from iavw import iavw
helper = iavw()
ids = helper.getIDsFromFile(filename='IDList.txt')
helper.downloadMetaFiles(ids, 'metadata')
metadata = helper.readMetaTextInDirectory('metadata')
posVwLines = []
for meta in metadata:
    posVwLines.append(helper.metadataToVWline(meta, True))
    
helper.writeVWlinesToFile(posVwLines, "testdata.te")
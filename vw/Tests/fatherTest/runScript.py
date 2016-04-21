import iavw
metadata = iavw.readMetaTextInDirectory('metadata')
negVwLines = []
for meta in metadata:
    negVwLines.append(iavw.metadataToVWline(meta, False))
    
iavw.writeVWlinesToFile(negVwLines, "testdata.te")
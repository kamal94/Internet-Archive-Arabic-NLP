import iavw
import subprocess
posMeta = iavw.readMetaTextInDirectory("../../data/ISIS/metadata")
negMeta = iavw.readMetaTextInDirectory('metadata')
negVwLines = []
posVwLines = []
posWeight = round(len(negMeta)/len(posMeta), 2)
for meta in negMeta:
    negVwLines.append(iavw.metadataToVWline(meta, ['تاريخ', 'الاسلام'], False))
for meta in posMeta:
    posVwLines.append(iavw.metadataToVWline(meta, ['الدولة الاسلامية'], True))

allVWLines = posVwLines + negVwLines
import random
random.seed(1234)
random.shuffle(allVWLines)
mid = int(len(allVWLines)/2)
iavw.writeVWlinesToFile(allVWLines[:mid], 'data.tr')
iavw.writeVWlinesToFile(allVWLines[mid:], 'data.te')
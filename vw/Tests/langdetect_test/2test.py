from iavw import *
from langdetect import detect_langs, lang_detect_exception
import types

meta = readMetaTextInDirectory("../../data/ISIS/metadata")
def separateMetaByLanaguage(metadata, keys):
	languages = {"error":[]}
	print(languages["error"])
	for m in metadata:
		probs = {}
		for key in keys:
			# print("probs:" + str(probs))
			if key in m:
				# print(type(m['identifier']))
				try:
					langs = detect_langs(m[key])
					for l in langs:
						if l.lang in probs:
							probs[l.lang] += l.prob
						else:
							probs[l.lang] = l.prob
				except lang_detect_exception.LangDetectException:
					try:
						print("langdetect had no data to work with on item " + m['identifier'])
					except:
						print("fatal error: item with no identifier")
				# except:
				# 	try:
				# 		print("some unknown error occurred when detecting item " + m['identifier'])
				# 	except:
				# 		print("fatal error: item with no identifier")
		if probs == {}:
			languages["error"].append(m)
		else:
			lang = max(probs, key=probs.get)
			if lang in languages:
				languages[lang].append(m)
			else:
				languages[lang] = [m]
	return languages

def showLangCount(langaugesInMeta):
	for l in langaugesInMeta:
		print(l + ": " + str(len(langaugesInMeta[l])))

byTitles = separateMetaByLanaguage(meta, ['title'])
print("******************************************\nresults for " + 'titles')
showLangCount(byTitles)

bySubject = separateMetaByLanaguage(meta, ['subject'])
print("******************************************\nresults for " + 'subject')
showLangCount(bySubject)

byTitleAndSubject = separateMetaByLanaguage(meta, ['title', 'subject'])
print("******************************************\nresults for " + 'title and subject')
showLangCount(byTitleAndSubject)

byTitlesAndDescription = separateMetaByLanaguage(meta, ['title', 'description'])
print("******************************************\nresults for " + 'title and description')
showLangCount(byTitlesAndDescription)

bySubjectAndDescription = separateMetaByLanaguage(meta, ['subject', 'description'])
print("******************************************\nresults for " + 'subject and description')
showLangCount(bySubjectAndDescription)

bySubjectAndTitleAndDescription = separateMetaByLanaguage(meta, ['subject', 'description', 'title'])
print("******************************************\nresults for " + 'subject and title and description')
showLangCount(bySubjectAndTitleAndDescription)
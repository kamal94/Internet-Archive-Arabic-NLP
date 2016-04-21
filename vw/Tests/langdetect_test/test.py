from iavw import *
from langdetect import detect, lang_detect_exception
import types

debug = False
meta = readMetaTextInDirectory("../../data/ISIS/metadata")
def separateMetaByLanaguage(metadata, keys):
	languages = dict(zip("", []))
	for m in metadata:
		sample = ""
		for key in keys:
			if key in m:
				if type(m[key]) is list:
					sample += " " + ' '.join(m[key])
				else:
					sample += " " + m[key]
		# print(type(m['identifier']))
		lang = "error"
		try:
			lang = detect(sample)
		except lang_detect_exception.LangDetectException:
			if debug:
				try:
					print("langdetect had no data to work with on item " + m['identifier'])
				except:
					print("fatal error when throwing langDetectException: item with no identifier")
		except:
			if debug:
				try:
					print("some unknown error occurred when detecting item " + m['identifier'])
				except:
					print("fatal error: item with no identifier")

		if lang in languages:
			# print(str(lang) + " exists: " + str(type(languages[lang])))
			# print("adding to list")
			# print("type(m): " + str(type(m)))
			languages[lang].append(m)
		else:
			# print(lang + " is new")
			# print("creating new list")
			languages[lang] = [m]
			# print(str(lang) + ": " + str(type(languages[lang])))
			# 
	return languages

def showLangCount(langaugesInMeta):
	for l in langaugesInMeta:
		print(l + ": " + str(len(langaugesInMeta[l])))

print("##########################################\ntesting language recognition by title")
byTitles = separateMetaByLanaguage(meta, ['title'])
print("******************************************\nresults for " + 'titles')
showLangCount(byTitles)

print("##########################################\ntesting language recognition by subject")
bySubject = separateMetaByLanaguage(meta, ['subject'])
print("******************************************\nresults for " + 'subject')
showLangCount(bySubject)

print("##########################################\ntesting language recognition by description")
bySubject = separateMetaByLanaguage(meta, ['description'])
print("******************************************\nresults for " + 'description')
showLangCount(bySubject)

print("##########################################\ntesting language recognition by title and subject")
byTitleAndSubject = separateMetaByLanaguage(meta, ['title', 'subject'])
print("******************************************\nresults for " + 'title and subject')
showLangCount(byTitleAndSubject)

print("##########################################\ntesting language recognition by title and description")
byTitlesAndDescription = separateMetaByLanaguage(meta, ['title', 'description'])
print("******************************************\nresults for " + 'title and description')
showLangCount(byTitlesAndDescription)

print("##########################################\ntesting language recognition by subject and description")
bySubjectAndDescription = separateMetaByLanaguage(meta, ['subject', 'description'])
print("******************************************\nresults for " + 'subject and description')
showLangCount(bySubjectAndDescription)

print("##########################################\ntesting language recognition by subject and title and description")
bySubjectAndTitleAndDescription = separateMetaByLanaguage(meta, ['subject', 'description', 'title'])
print("******************************************\nresults for " + 'subject and title and description')
showLangCount(bySubjectAndTitleAndDescription)
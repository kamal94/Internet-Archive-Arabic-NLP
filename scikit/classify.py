import iavw
import nltk
import random
import pickle
import sys, getopt

classifierFileName = None;
dataSetFileName = None
#parse arguments
try:
 	opts, args = getopt.getopt(sys.argv[1:], "c:d:", ["classifier=","data="])
except getopt.GetoptError:
	print('classify.py -c <classifier> -d <dataSet>')

#test for argument existance
for opt, arg in opts:
  if opt in ("-c", "--classifier"):
     classifierFileName = arg
  if opt in ("-d", "--data"):
     dataSetFileName = arg



def proccessText( text: str, removePhrases: list):
	"""Accepts a string and returns a cleaner version of it.
	Any unnecessary characters or hyperlinks are removed from the string, and the
	string is truncated to a 1000 words if it is longer than that. Any words larger
	than 20 characters in length are removed."""
	import re
	# newText = text.replace(':', 'COLON').replace('|', 'PIPE')
	newText = text.replace('\n', ' ').replace('\r', ' ').replace("@", ' ')
	newText = newText.replace('<br>', ' ').replace("<\br>", ' ').replace("<span>", " ").replace("</span>", " ")
	newText = re.sub('<[^>]*>', '', newText)
	newText = newText.replace("gmail.com", "").replace("hotmail.com", "").replace("yahoo.com", "")
	for phrase in removePhrases:
		newText = newText.replace(phrase, "")
	n2 = []
	for word in newText.split():
		if len(word) < 20:
			n2.append(word)
	return ' '.join(n2[:1000])


# def word_features(words):
# 	return dict((word, True) for word in nltk.word_tokenize(words))

def cleanMetadata(metadata: dict):
	ignored_keys = ['mediatype', 'sound', 'color', 'curation', 'creator', 'scanner', 'collection', 'language']
	data = {}
	if metadata is None:
		return{}
	else:
		for key in metadata:
			if key in ignored_keys:	#remove ignored keys
				continue
			else:
				if(type(metadata[key]) == list):
					string = ' '.join(metadata[key])
					data[key] = proccessText(string, ['الدولة الاسلامية', 'سكر', 'الاسلامية', 'الدولة'])
				else:
					data[key] = proccessText(metadata[key],  ['الدولة الاسلامية', 'سكر', 'الاسلامية', 'الدولة'])
	return data

# def metaToString(metadata:dict):
# 	string = ""
# 	if metadata==None:
# 		return string
# 	string += ' '.join(metadata.values())
# 	return string

def metaToFeatureDict(metadata:dict):
	d = dict()
	if metadata==None:
		return d
	#create a list of section:word binding features
	for key in metadata:
		for st in nltk.word_tokenize(metadata[key]):\
			d[key+":"+st] = True
	return d

def getFeaturesWithLabel(metadata:dict, label:str):
	return [(wordFeatures, label) 
		for wordFeatures in [metaToFeatureDict(cleanedMeta) 
		for cleanedMeta in [cleanMetadata(item) 
		for item in metadata ]]]

if dataSetFileName==None:
	posMeta  = iavw.readMetaTextInDirectory("data/metadata/ISIS")
	negMeta = iavw.readMetaTextInDirectory("data/metadata/non-isis")

	posSet = getFeaturesWithLabel(posMeta, 'isis')
	negSet = getFeaturesWithLabel(negMeta, 'neutral')

	totalSet =  posSet + negSet
else:
	print("pre-loading dataset from " + dataSetFileName)
	dataSetFile = open(dataSetFileName, 'rb')
	totalSet = pickle.load(dataSetFile)
	dataSetFile.close()


random.shuffle(totalSet)
train_set = totalSet[:int(len(totalSet)/2)+1]
test_set = totalSet[int(len(totalSet)/2)+1:]

if classifierFileName==None:
	classifier = nltk.NaiveBayesClassifier.train(train_set)
else:
	print("pre-loading classifier from " + classifierFileName)
	classifierFile = open(classifierFileName, 'rb')
	classifier = pickle.load(classifierFile)
	classifierFile.close()

classifier.show_most_informative_features(50)
print("classifier accuracy: " + str(nltk.classify.accuracy(classifier, test_set)))

print("Saving classifier")
fi = open("classifier.pickle", 'wb')
pickle.dump(classifier, fi)
fi.close()

print("savind dataset")
fi = open("dataset.pickle", 'wb')
pickle.dump(totalSet, fi)
fi.close()

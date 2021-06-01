#calculate WER from CER

#average number of chars in training transcripotions
#calculated with avg.py
languages = {
	'ady':5.9925,
	'gre':6.73125,
	'ice':5.72,
	'ita':6.625,
	'khm':5.5125,
	'lav':5.94375,
	'mlt_latn':5.1675,
	'rum':6.1475,
	'slv':5.7475,
	'wel_sw':5.18375
}

import sys
import numpy as np

#cer
val = float(sys.argv[1])

#sample size in words
size = int(sys.argv[2])

accuracies = np.zeros(len(languages))
for n,language in enumerate(languages):
	#word length
	length = int(languages[language])
	#make array for all letters
	x = np.zeros(size*length)
	#generate the right number of errors
	ones = round(val*size*length)
	#put errors in array
	x[:ones] = 1
	#randommize errors
	x = np.random.permutation(x)
	#break array into word lengths
	x = x.reshape(size,length)
	#calculate number of correct words
	correct = np.where(x.sum(axis=1) == 0)[0].shape[0]
	#calculate percent accuracy
	accuracy = correct/size
	accuracies[n] = accuracy
	print(f'\t{language}: {accuracy:.3f}')
print(f'accuracy overall: {accuracies.sum()/len(languages):.3f}')


#do stats

import numpy as np
from scipy.stats import ttest_ind
import re

#val=100
v100 = [
	[94.6073,74.6],
	[94.7088,75],
	[94.3535,73.8],
	[94.4804,74],
	[94.4804,74],
	[94.5058,74.2],
	[94.5946,74.5],
	[94.7088,75],
	[94.7976,75.4],
	[94.5946,74.5]
]
#val=20
v20 = [
	[94.8383,75.6],
	[94.7761,75.3],
	[94.4652,74],
	[94.8383,75.5],
	[94.7139,75],
	[94.5896,74.5],
	[94.9005,75.8],
	[94.5274,74.2],
	[94.5274,74.2],
	[94.7139,75]
]

#no substring runs
vns = [
	[95.1493,    76.9],
	[94.403,     73.7],
	[95.1493,    76.8],
	[94.5896,    74.5],
	[94.6517,    74.8],
	[95.2736,    77.4],
	[94.5274,    74.2],
	[94.7761,    75.2],
	[95.0871,    76.6],
	[94.5896,    74.5]
]

lge = '''ady         95.2663 91.1243 93.4911 94.6746 93.4911
gre         97.2527 98.3516 98.3516 98.9011 98.9011
ice         91.1565 94.5578 93.8776 90.4762 94.5578
ita         93.5135 94.5946 94.5946 94.5946 94.5946
khm         94.1935 90.3226 90.9677 90.9677 90.9677
lav         94      90.6667 89.3333 92      90.6667
mlt\_latn   91.8919 94.5946 91.8919 92.5676 93.2432
rum         95.2941 96.4706 94.7059 95.8824 95.2941
slv         94.012  94.6108 94.6108 94.6108 94.012
wel\_sw     96.2963 97.037  96.2963 97.037  96.2963'''

v100c = [v[0] for v in v100]
v20c = [v[0] for v in v20]

print('validation 20 vs. 100 (chars)',ttest_ind(v100c,v20c),'\n')

v100w = [v[1] for v in v100]
v20w = [v[1] for v in v20]

print('validation 20 vs. 100 (words)',ttest_ind(v100w,v20w),'\n')

vnsc = [v[0] for v in vns]
vnsw = [v[1] for v in vns]

print('validation 20 vs. no substrings (words)',ttest_ind(vnsw,v20w),'\n')
print('validation 20 vs no substrings (chars)',ttest_ind(vnsc,v20c),'\n')

lge = lge.split('\n')

vals = []
languages = []
for l in lge:
	bits = re.split(' +',l)
	languages.append(bits[0])
	res = [float(bit) for bit in bits[1:]]
	vals.append(res)

vals = np.array(vals)

print(vals.mean(axis=0))

print(
	'validation 20 vs separate (chars)',
	ttest_ind(vals.mean(axis=0),v20c),
	'\n'
)


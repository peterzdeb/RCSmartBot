from __future__ import print_function
import numpy
from matplotlib.mlab import csv2rec
import matplotlib.pyplot as plt
import matplotlib.cbook as cbook

import itertools


r = csv2rec('actions.log')[-40:]

y1 = [v[0] for v in r]

plt.plot(numpy.arange(len(r)), y1,'-')
plt.plot(numpy.arange(len(r)), [v[1] for v in r],'-')
plt.plot(numpy.arange(len(r)), [v[2] for v in r],'-')

labels = [v[3] for v in r]

for i, txt in enumerate(labels):
    plt.annotate(txt, (i,y1[i]))

plt.show()

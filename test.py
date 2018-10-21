import randscanner
import random
import numpy as np
import matplotlib.pyplot as plt


custom = np.empty(0)
normal = np.empty(0)

for i in range(0, 100):
    custom = np.append(custom, randscanner.random())
    normal = np.append(normal, random.random())
    print(i)

custcorr = np.correlate(custom, custom, "same")
normcorr = np.correlate(normal, normal, "same")
# use only second half
custcorr = custcorr[int(len(custcorr)/2):]
normcorr = normcorr[int(len(normcorr)/2):]

plt.plot(custcorr, label="Skyscanner")
plt.plot(normcorr, label="Python")
plt.legend();
plt.show()

import numpy as np
import matplotlib.pyplot as plt
import math

def f(t):
    return t * np.sin(2*np.pi*t)

t1 = np.arange(0.0, 10.0, 0.1)

plt.plot(t1, f(t1), 'b-')
plt.xlabel('x')
plt.ylabel('f(t)=tsint')
plt.show()

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np




x = [1,1,2,2,3,3]
y = [6,6,5,5,4,4]

dx = 0.5
dy = 0.5

base = [0,1,0,0,0,0]
z = [1,2,3,5,3,6]

list_color = ['r','b','b','r','r','b']




fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.bar3d(x,y,base,dx,dy,z,color = list_color)

plt.show()

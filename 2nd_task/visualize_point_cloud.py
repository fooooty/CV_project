# visualize_point_cloud.py
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

points = np.load("2nd_task/result/point_cloud.npy")  

H, W, _ = points.shape
points_flat = points.reshape(-1, 3)

X = points_flat[:, 0]
Y = points_flat[:, 1]
Z = points_flat[:, 2]

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.scatter(X, Y, Z, c=Z, cmap='jet', s=0.5)
ax.set_title("3D Point Cloud from Depth Map")
plt.show()

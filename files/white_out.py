import matplotlib.pyplot as plt
import matplotlib.patches as patches
from PIL import Image
import numpy as np

x = np.array(Image.open('geek.png'), dtype=np.uint8)
plt.imshow(x)
  
# Create figure and axes
fig, ax = plt.subplots(1)
  
# Display the image
ax.imshow(x)
  
# Create a Rectangle patch
rect = patches.Rectangle((50, 100), 40, 30, linewidth=1,
                         edgecolor='r', facecolor="g")
  
# Add the patch to the Axes
ax.add_patch(rect)
plt.show()
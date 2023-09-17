import matplotlib.pyplot as plt
import matplotlib.patches as patches
from PIL import Image
import numpy as np

def white(anchorX,anchorY,width,height,path):
    x = np.array(Image.open(path), dtype=np.uint8)
    plt.imshow(x)
  
    # Create figure and axes
    fig, ax = plt.subplots(1)
  
    # Display the image
    ax.imshow(x)
  
    # Create a Rectangle patch
    rect = patches.Rectangle((anchorX, anchorY), width, height, linewidth=1, edgecolor='w', facecolor="w")
  
    # Add the patch to the Axes
    ax.add_patch(rect)
    plt.show()
    
    
        
white(50,50,100,100,'images\download.jpg')        
        
        
        
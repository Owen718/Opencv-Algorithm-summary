import matplotlib.pyplot as plt
from matplotlib import animation 
import numpy as np

ims = []
fig = plt.figure("Animation")
ax = fig.add_subplot(111)

for imgNum in range(10):
    img = np.random.rand(10,10) #random image for an example

    frame =  ax.imshow(img)  
    t = ax.annotate(imgNum,(1,1)) # add text

    ims.append([frame,t]) # add both the image and the text to the list of artists 

anim = animation.ArtistAnimation(fig, ims, interval=350, blit=True, repeat_delay=350)

plt.show()
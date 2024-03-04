import matplotlib.pyplot as plt
import numpy as np
import time

# Initialize plot
plt.ion()
fig, ax = plt.subplots()
line, = ax.plot(np.random.rand(100))
ax.set_ylim(0, 1)
ax.set_title('Random Array Plot')

# Main loop
while True:
    # Generate random array of length 100
    random_array = np.random.rand(100)
    
    # Update plot
    line.set_ydata(random_array)
    plt.draw()
    plt.pause(0.1)  # Adjust the pause duration as needed
    
    # Optional: Print the generated array
    print("Generated array:", random_array)

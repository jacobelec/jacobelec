import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import sys, time, math
import serial
import platform
import os

# Configure the serial port 
xsize = 50
ser = serial.Serial(
    port='COM3',
    baudrate=115200,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_TWO,
    bytesize=serial.EIGHTBITS
) 
ser.isOpen()

# Moving average filter window size
window_size = 5
temp_buffer = []

# Temperature threshold (adjust as needed)
TEMP_THRESHOLD = 45  # Alert if temperature exceeds 45°C

# Beep function for different OS
def beep():
    if platform.system() == "Windows":
        import winsound
        winsound.Beep(1000, 500)  # 1000 Hz for 500ms
    


# Generator function to read serial data
def data_gen():
    t = data_gen.t
    while True:
        num = ser.readline().decode('utf-8').strip()
        try:
            temp = float(num)

            # Moving Average Filter
            temp_buffer.append(temp)
            if len(temp_buffer) > window_size:
                temp_buffer.pop(0)
            filtered_temp = np.mean(temp_buffer)

            # Temperature Alert + Beep Sound + Voice Alert
            if filtered_temp > TEMP_THRESHOLD:
                print(f" Warning: High Temperature! ")
                beep()  # Beep alert
                  # Voice alert

            t += 1
            print(f"Raw: {temp:.2f}, Filtered: {filtered_temp:.2f}")
            yield t, filtered_temp  # Use filtered value

        except ValueError:
            print("Invalid data received")

data_gen.t = -1

def run(data):
    t, y = data
    if t > -1:
        xdata.append(t)
        ydata.append(y)

        # Keep the last xsize points
        if t > xsize:
            ax.set_xlim(t - xsize, t)

        # Auto-adjust Y-axis for better visibility
        ax.set_ylim(min(ydata) - 2, max(ydata) + 2)

        # Change background color based on temperature
        if y > TEMP_THRESHOLD:
            ax.set_facecolor("red")  # High temp = red
        else:
            ax.set_facecolor("lightblue")  # Normal temp = blue

        line.set_data(xdata, ydata)

    return line,

def on_close_figure(event):
    sys.exit(0)

fig = plt.figure()
fig.canvas.mpl_connect('close_event', on_close_figure)
ax = fig.add_subplot(111)
line, = ax.plot([], [], lw=2, color='b', label="Temperature (°C)")
ax.set_xlim(0, xsize)
ax.set_ylim(0, 60)
ax.grid()
ax.legend()

xdata, ydata = [], []

ani = animation.FuncAnimation(fig, run, data_gen, blit=False, interval=100, repeat=False)
plt.show()

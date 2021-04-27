import time
import board
import busio
import adafruit_mlx90640

import cv2
import numpy as np



PRINT_TEMPERATURES = False
PRINT_ASCIIART = False
PRINT_OPENCV = True

i2c = busio.I2C("GEN2_I2C_SCL", "GEN2_I2C_SDA", frequency=800000)
mlx = adafruit_mlx90640.MLX90640(i2c)
print("MLX addr detected on I2C")
print([hex(i) for i in mlx.serial_number])
 
mlx.refresh_rate = adafruit_mlx90640.RefreshRate.REFRESH_2_HZ
 
frame = [0] * 768
blank_image = np.zeros((24,32,3), np.uint8)
while True:
    stamp = time.monotonic()
    try:
        mlx.getFrame(frame)
    except ValueError:
        # these happen, no biggie - retry
        continue
    print("Read 2 frames in %0.2f s" % (time.monotonic() - stamp))
    Max = 20.0
    point = (0,0)
    for h in range(24):
        for w in range(32):
            t = frame[h * 32 + w]
            if t > Max:
                Max = t
                point = (w*20 -10,h*20 - 10)
            if PRINT_TEMPERATURES:
                print("%0.1f, " % t, end="")
            if PRINT_ASCIIART:
                c = "&"
                # pylint: disable=multiple-statements
                if t < 20:
                    c = " "
                elif t < 23:
                    c = "."
                elif t < 25:
                    c = "-"
                elif t < 27:
                    c = "*"
                elif t < 29:
                    c = "+"
                elif t < 31:
                    c = "x"
                elif t < 33:
                    c = "%"
                elif t < 35:
                    c = "#"
                elif t < 37:
                    c = "X"
                # pylint: enable=multiple-statements
                print(c, end="")
            if PRINT_OPENCV:
                #BGR
                c = [255,255,255]
                if t < 20:
                    c = [143,0,255]
                elif t < 23:
                    c = [75,0,130]
                elif t < 25:
                    c = [255,0,0]
                elif t < 27:
                    c = [255,125,0]
                elif t < 29:
                    c = [255,255,0]
                elif t < 31:
                    c = [0,127,255]
                elif t < 33:
                    c = [0,0,150]
                elif t < 35:
                    c = [0,0,200]
                elif t < 37:
                    c = [0,0,255]
                blank_image[h][w] = c

      #  print()
    #print()
    if PRINT_OPENCV:
        resized = cv2.resize(blank_image, (640,480), interpolation = cv2.INTER_AREA)
        cv2.circle(resized,point, 5, (0, 0, 0), -1)
        cv2.putText(resized, str(round(Max,1)),point, cv2.FONT_HERSHEY_SIMPLEX,1, (0, 255, 255), 1, cv2.LINE_AA)
        print("Max = ", Max)
        cv2.imshow("Mlx90640_example",resized)
        cv2.waitKey(1)
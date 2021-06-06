# import cv2 as cv
# import numpy as np
# import csv
# import glob
# from matplotlib import pyplot as plt
#
# pictureFolder = glob.glob("temp.jpg")
# imageList = []
#
# for img in pictureFolder:
#     image = cv.imread(img)
#     new_width = 28
#     new_height = 28
#     img_resized = cv.resize(src=image, dsize=(new_width, new_height))
#     # imageList.append(image)
#     print('reisze_img_name', img_resized.shape)
#     imageList.append(img_resized)
#
# with open ('pixel.csv', 'r+') as outFile:
#     outFile.readline()
#     outFile.truncate(outFile.tell())
#
# for img in imageList:
#     image = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
#     imageData2D = np.array(image)
# #    print(imageData2D.shape)
#     imageData1D = imageData2D.flatten()
# #    print(imageData1D.shape)
# #    tryimg = imageData1D.reshape((28,28))
# #   plt.imshow(tryimg, cmap="grey")
# #   plt.show()
#     with open ('pixel.csv', 'a', newline='\n') as outFile:
#         writer = csv.writer(outFile)
#         writer.writerow(imageData1D)
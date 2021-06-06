import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from tkinter import *
import cv2
from tkinter import filedialog
from PIL import Image, ImageDraw
import tkinter as tk
import cv2 as cv
import numpy as np
import csv
import glob

trainDataSet = pd.read_csv("train_data.csv")

dataTrain = trainDataSet.values

xTrain, yTrain = dataTrain[:, 1:], dataTrain[:, 0]

print(xTrain.shape, yTrain.shape)


def knn(xTrain, yTrain, testPoint, k=11):
    distances = []

    for dataPoint, label in zip(xTrain, yTrain):
        distances.append((euclidean(testPoint, dataPoint), label))

    sortedDistances = sorted(distances, key=lambda x: x[0])
    k_nearest_neighbors = np.array(sortedDistances[:k])
    freq = np.unique(k_nearest_neighbors[:, 1], return_counts=True)
    labels, counts = freq
    majorityVote = labels[counts.argmax()]
    return majorityVote


def euclidean(p1, p2):
    return np.sqrt(np.sum((p1 - p2) ** 2))


testDataSet = pd.read_csv("pixel.csv")

testData = testDataSet.values
testImages = testData[:20]


# root= Tk()
# root.resizable(0,0)
# root.title('window')
#
# canvas= Canvas(root, width=640, height=480, bg='white');
# canvas.pack()
# canvas.grid(row=0, column=0,pady=2,sticky=W,columnspan=2)
# root.mainloop()


class ImageGenerator:

    def __init__(self, parent, posx, posy,testImages2, *kwargs):
        self.parent = parent
        self.posx = posx
        self.testImages2 = testImages2
        self.posy = posy
        self.sizex = 200
        self.sizey = 200
        self.b1 = "up"
        self.xold = None
        self.yold = None
        self.drawing_area = tk.Canvas(self.parent, width=self.sizex, height=self.sizey, bg='black')
        self.drawing_area.place(x=self.posx, y=self.posy)
        self.drawing_area.bind("<Motion>", self.motion)
        self.drawing_area.bind("<ButtonPress-1>", self.b1down)
        self.drawing_area.bind("<ButtonRelease-1>", self.b1up)
        self.button = tk.Button(self.parent, text="Done!", width=10, bg='white', command=self.save)
        self.button.place(x=self.sizex / 7, y=self.sizey + 20)
        self.button1 = tk.Button(self.parent, text="Clear!", width=10, bg='white', command=self.clear)
        self.button1.place(x=(self.sizex / 7) + 80, y=self.sizey + 20)
        self.button2 = tk.Button(self.parent, text="Convert Excel!", width=10, bg='white', command=self.convertExcel)
        self.button2.place(x=(self.sizex / 7) , y=self.sizey + 45)
        self.button3 = tk.Button(self.parent, text="Screen!", width=10, bg='white', command=self.screen)
        self.button3.place(x=(self.sizex / 7) + 80, y=self.sizey + 45)

        self.image = Image.new("RGB", (200, 200), (0, 0, 0))
        self.draw = ImageDraw.Draw(self.image)


    def save(self):
        filename = "temp.jpg"
        self.image.save(filename)

    def convertExcel(self):

        pictureFolder = glob.glob("temp.jpg")
        imageList = []

        for img in pictureFolder:
            image = cv.imread(img)
            new_width = 28
            new_height = 28
            img_resized = cv.resize(src=image, dsize=(new_width, new_height))
            # imageList.append(image)
            print('image size', img_resized.shape)
            # imageList.append(img_resized)

        with open('pixel.csv', 'r+') as outFile:
            outFile.readline()
            outFile.truncate(outFile.tell())

        # for img in imageList:
            image = cv.cvtColor(img_resized, cv.COLOR_BGR2GRAY)
            imageData2D = np.array(image)
            #    print(imageData2D.shape)
            imageData1D = imageData2D.flatten()
            #    print(imageData1D.shape)
            #    tryimg = imageData1D.reshape((28,28))
            #   plt.imshow(tryimg, cmap="grey")
            #   plt.show()
            with open('pixel.csv', 'a', newline='\n') as outFile:
                writer = csv.writer(outFile)
                writer.writerow(imageData1D)






    def screen(self):
        testDataSet = pd.read_csv("pixel.csv")

        testData = testDataSet.values
        self.testImages2 = testData[:20]
        print(self.testImages2)
        for test in self.testImages2:
            im = test.reshape((28, 28))
            plt.figure()
            plt.imshow(im, cmap='gray')
            plt.show()
            label = knn(xTrain, yTrain, test)
            print("Label:", label)


    def clear(self):
        self.drawing_area.delete("all")
        self.image = Image.new("RGB", (200, 200), (255, 255, 255))
        self.draw = ImageDraw.Draw(self.image)

    def b1down(self, event):
        self.b1 = "down"

    def b1up(self, event):
        self.b1 = "up"
        self.xold = None
        self.yold = None

    def motion(self, event):
        if self.b1 == "down":
            if self.xold is not None and self.yold is not None:
                event.widget.create_line(self.xold, self.yold, event.x, event.y, smooth='true', width=15, fill='white')
                self.draw.line(((self.xold, self.yold), (event.x, event.y)), (255, 255, 255), width=15)

        self.xold = event.x
        self.yold = event.y


if __name__ == "__main__":
    root = tk.Tk()
    root.wm_geometry("%dx%d+%d+%d" % (400, 400, 10, 10))
    root.config(bg='white')
    ImageGenerator(root, 10, 10, testImages)
    root.mainloop()

# for test in testImages:
#     im = test.reshape((28, 28))
#     plt.figure()
#     plt.imshow(im, cmap='gray')
#     plt.show()
#     label = knn(xTrain, yTrain, test)
#     print("Label:", label)

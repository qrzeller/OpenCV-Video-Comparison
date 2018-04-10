import cv2
import numpy as np
from matplotlib import pyplot as plt

init = True
fig = None
hist_plotted = None
h = None
ax2 = None
ax3 = None
ax4 = None

color = ('b', 'g', 'r')
previous_hist = {}
current_hist = {}

comparison_list_correl = []
comparison_list_chi = []
comparison_list_hell = []

def calc_histo(img):
    global init,fig,hist_plotted,h,previous_hist,current_hist,ax2,ax3,ax4
    if init:
        # interactive mode
        plt.ion()

        fig, ((h, ax2), (ax3, ax4)) = plt.subplots(nrows=2, ncols=2)
        fig.set_size_inches((60, 60))

        for channel, col in enumerate(color):
            histr = cv2.calcHist([img], [channel], None, [256], [4, 256])
            previous_hist[col] = histr

        init = False
        fig.canvas.draw()

    h.cla()
    ax2.cla()
    ax3.cla()
    ax4.cla()

    h.set_title("Histogram of colors")
    for channel, col in enumerate(color):
        current_hist[col] = cv2.calcHist([img], [channel], None, [256], [4, 256])
        hist_plotted = h.plot(current_hist[col], color=col)


        #comp.bar()
        #h.xlim([0, 256])


    # Correlation
    ax2.set_title("Covariance between 2 contiguous frame")
    a = cv2.compareHist(current_hist[col], previous_hist[col], cv2.HISTCMP_CORREL)
    comparison_list_correl.append(a)
    ax2.plot(comparison_list_correl)
    if a < 0.5:
        print(a)

    ax3.set_title("CHISQR between 2 contiguous frame")
    a = cv2.compareHist(current_hist[col], previous_hist[col], cv2.HISTCMP_CHISQR)
    comparison_list_chi.append(a)
    ax3.plot(comparison_list_chi)

    ax4.set_title("HELLINGER between 2 contiguous frame")
    a = cv2.compareHist(current_hist[col], previous_hist[col], cv2.HISTCMP_HELLINGER)
    comparison_list_hell.append(a)
    ax4.plot(comparison_list_hell)



    previous_hist = current_hist.copy()
    plt.pause(0.0001)
    #fig.canvas.draw()



def main():
    vidcap = cv2.VideoCapture('15 - Nesquik Nesquik 1366404005.mpg')

    count = 0
    success = 1
    while success:
        success, image = vidcap.read()
        hist = calc_histo(image)
        cv2.imshow('frame',image)
        # cv2.imwrite("frame%d.jpg" % count, image)     # save frame as JPEG file
        if cv2.waitKey(10) == 27:  # exit if Escape is hit
            break
        count += 1

        #cv2.destroyAllWindows()

if __name__ == "__main__":
    main()




# some ref :
# https://www.pyimagesearch.com/2014/07/14/3-ways-compare-histograms-using-opencv-python/
# https://docs.opencv.org/2.4.13.5/doc/tutorials/imgproc/histograms/histogram_comparison/histogram_comparison.html

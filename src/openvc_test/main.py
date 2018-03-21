import cv2
import numpy as np
from matplotlib import pyplot as plt
from os import listdir
init = True
fig = None
hist_plotted = None
h = None
ax2 = None
ax3 = None
ax4 = None
a = 0
frame_counter = 0

color = ('b', 'g', 'r')
previous_hist = {}
current_hist = {}

comparison_list_correl = []
comparison_list_chi = []
comparison_list_hell = []
storage_reference = []

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


    a = cv2.compareHist(current_hist[col], previous_hist[col], cv2.HISTCMP_CORREL)
    if a < 0.5:
        print(a)

    ax2.set_title("Covariance between 2 contiguous frame")
    comparison_list_correl.append(a)
    ax2.plot(comparison_list_correl)



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



def calculate_correlation(img):
    global init, fig, hist_plotted, h, previous_hist, current_hist, ax2, ax3, ax4,a, prev_hist_added,frame_counter
    for channel, col in enumerate(color):
        current_hist[col] = cv2.calcHist([img], [channel], None, [256], [4, 256])

    hist_added = current_hist['b']

    if init:
        init = False
    else :
        a = cv2.compareHist(hist_added, prev_hist_added, cv2.HISTCMP_CORREL)

    ## Of 1 color only
    if a < 0.3:
        storage_reference.append(frame_counter)
        #print(str(frame_counter)+ " " + str(a))

    prev_hist_added = hist_added.copy()


def main():
    global frame_counter,storage_reference
    list_of_dir = listdir('./video')
    for f in list_of_dir:
        #clear
        frame_counter=0
        storage_reference = []

        vidcap = cv2.VideoCapture('./video/'+f)

        count = 0
        success = 1
        while success:
            frame_counter+=1
            success, image = vidcap.read()
            if not success: break
            ####hist = calc_histo(image)
            calculate_correlation(image)
            #cv2.imshow('frame',image)
            # cv2.imwrite("frame%d.jpg" % count, image)     # save frame as JPEG file
            if cv2.waitKey(10) == 27:  # exit if Escape is hit
                break
            count += 1

            #cv2.destroyAllWindows()

        # post traitement
        print("Total frame count  : " + str(frame_counter))
        for i in storage_reference:
            to_print  = int(i*100/frame_counter)
            if to_print != 0:
                print(to_print)

if __name__ == "__main__":
    main()



# some ref :
# https://www.pyimagesearch.com/2014/07/14/3-ways-compare-histograms-using-opencv-python/
# https://docs.opencv.org/2.4.13.5/doc/tutorials/imgproc/histograms/histogram_comparison/histogram_comparison.html

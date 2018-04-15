import cv2
import numpy as np
from matplotlib import pyplot as plt
import os
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
vidcap = None

color = ('b', 'g', 'r')
previous_hist = {}
current_hist = {}

comparison_list_correl = []
comparison_list_chi = []
comparison_list_hell = []
storage_reference = []
data = {}
data['cur'] = None

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
    global init, fig, hist_plotted, h, previous_hist, current_hist, ax2, ax3, ax4,a, prev_hist_added,frame_counter,data
    for channel, col in enumerate(color):
        current_hist[col] = cv2.calcHist([img], [channel], None, [256], [4, 256])

    hist_added = current_hist['b']

    if init:
        init = False
    else :
        a = cv2.compareHist(hist_added, prev_hist_added, cv2.HISTCMP_CORREL)

        ## Of 1 color only
        if a < 0.7:
            storage_reference.append(frame_counter)
            #cv2.imwrite('./image/sc_detect/' + data['file'][:2] + "_" + str(frame_counter-1) + "_1" + ".jpg", data['prev'])
            #cv2.imwrite('./image/sc_detect/' + data['file'][:2] + "_" + str(frame_counter) + "_2" + ".jpg", data['cur'])
            #print(str(frame_counter)+ " " + str(a))

    prev_hist_added = hist_added.copy()

def im_ref(d) :
    im_keys = []
    for i in range(1,len(d)):
        if(d[i]-(d[i-1])>10): # arbitrary diff to be sure is not a fading.
            im_keys.append( int((d[i]-d[i-1])/2) + d[i-1] )
    return im_keys

path_to_image_scene = './image/sc_temp/'
def store_im_keys(frames):

    path_folder_tocreate = os.path.join(path_to_image_scene, os.path.splitext(data['file'])[0])
    print(path_folder_tocreate)
    if not os.path.exists(path_folder_tocreate):
        os.makedirs(path_folder_tocreate)
    tempvid = cv2.VideoCapture('./video/' + data['file'])

    print("-----------------------------------" + str(frames))
    for i in frames :
        tempvid.set(cv2.CAP_PROP_POS_FRAMES,i) # 2 mean set frame
        ret, im_to_store = tempvid.read()
        if ret:
            #cv2.imshow("test", im_to_store)
            print("writing" + str(i))
            cv2.imwrite(os.path.join(path_folder_tocreate,  data['file'][:2] + "_frame" + str(i) + ".jpg"), im_to_store)



def main():
    global frame_counter,storage_reference,data,init,vidcap
    list_of_dir = listdir('./video')
    for f in list_of_dir:
        #clear
        init = True
        frame_counter = 1
        storage_reference = []

        vidcap = cv2.VideoCapture('./video/'+f)

        success = 1
        data['file'] = f;

        # init
        success, image = vidcap.read()
        data['cur'] = image
        calculate_correlation(image)
        while success:
            frame_counter += 1
            success, image = vidcap.read()
            data['prev'] = data['cur']
            data['cur'] = image
            if not success: break
            ####hist = calc_histo(image)
            calculate_correlation(image)
            #cv2.imshow('frame',image)
            # cv2.imwrite("frame%d.jpg" % count, image)     # save frame as JPEG file

            if cv2.waitKey(10) == 27:  # exit if Escape is hit
                break

            #cv2.destroyAllWindows()

        # post traitement
        print("Total frame count  : " + str(frame_counter) + " Name : " + f)
        im_keys = im_ref(storage_reference)
        store_im_keys(im_keys)
        for i in storage_reference:
            to_print  = int(i*100/frame_counter)
            if to_print != 0:
                print(to_print)

if __name__ == "__main__":
    main()


# some ref :
# https://www.pyimagesearch.com/2014/07/14/3-ways-compare-histograms-using-opencv-python/
# https://docs.opencv.org/2.4.13.5/doc/tutorials/imgproc/histograms/histogram_comparison/histogram_comparison.html

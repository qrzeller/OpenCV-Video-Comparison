from time import sleep

import cv2
from os import listdir


# USAGE
# python image_diff.py --first images/original_01.png --second images/modified_01.png

# import the necessary packages
import numpy as np
from skimage.measure import compare_ssim
import argparse
import imutils
import cv2
import networkx as nx
import matplotlib.pyplot as plt


G = nx.MultiGraph()
"""
def pyimage():
    # construct the argument parse and parse the arguments

    global images
    list_of_dir = listdir('./image/sc_key/')
    for f in list_of_dir:
        
    # load the two input images
    imageA = cv2.imread(list_of_dir[i])
    imageB = cv2.imread(list_of_dir)
    
    # convert the images to grayscale
    grayA = cv2.cvtColor(imageA, cv2.COLOR_BGR2GRAY)
    grayB = cv2.cvtColor(imageB, cv2.COLOR_BGR2GRAY)
    
    # compute the Structural Similarity Index (SSIM) between the two
    # images, ensuring that the difference image is returned
    (score, diff) = compare_ssim(grayA, grayB, full=True)
    diff = (diff * 255).astype("uint8")
    print("SSIM: {}".format(score))
    
    # threshold the difference image, followed by finding contours to
    # obtain the regions of the two input images that differ
    thresh = cv2.threshold(diff, 0, 255,
        cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
    cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if imutils.is_cv2() else cnts[1]
    
    # loop over the contours
    for c in cnts:
        # compute the bounding box of the contour and then draw the
        # bounding box on both input images to represent where the two
        # images differ
        (x, y, w, h) = cv2.boundingRect(c)
        cv2.rectangle(imageA, (x, y), (x + w, y + h), (0, 0, 255), 2)
        cv2.rectangle(imageB, (x, y), (x + w, y + h), (0, 0, 255), 2)
    
    # show the output images
    cv2.imshow("Original", imageA)
    cv2.imshow("Modified", imageB)
    cv2.imshow("Diff", diff)
    cv2.imshow("Thresh", thresh)
    cv2.waitKey(0)
"""
def diff(img, img1):  # returns just the difference of the two images

    return cv2.absdiff(img, img1)


def diff_remove_bg(img0, img, img1):  # removes the background but requires three images

    d1 = diff(img0, img)

    d2 = diff(img, img1)

    return cv2.bitwise_and(d1, d2)
path = './image/sc_key/'
images = []
images_name = []
def main():
    global images, images_name, G, GG
    list_of_dir = listdir(path)
    for f in list_of_dir:
        im_ref = cv2.imread(path+f,0)
        images_name.append(f)
        images.append(im_ref)
    print(list_of_dir)
    # compute
    colors = []
    for i in range(0, len(images)):
        for j in range(i+1,len(images)-1):



            # compute the Structural Similarity Index (SSIM) between the two
            # images, ensuring that the difference image is returned
            (score, diff) = compare_ssim(images[i], images[j], full=True)
            diff = (diff * 255).astype("uint8")

            if score > 0.8:
                str_comp = images_name[i] +"  ||  " + images_name[j] + " SSIM: {}".format(score)
                print(str_comp)
                G.add_edge(images_name[i][:2], images_name[j][:2] , weight=score)
                colors.append(score)

                #concat = np.concatenate((images[i], images[j]), axis=0)
                #cv2.imshow(str_comp, concat)

            #res = diff(images[i], images[j])
    #print(G.adj)
    #plt.subplot(121)
    pos = nx.spring_layout(G, k=0.4)
    edges, weights = zip(*nx.get_edge_attributes(G, 'weight').items())
    nx.draw(G,pos, node_color='#A0CBE2', edgelist=edges, edge_color=weights,
        width=4, edge_cmap=plt.cm.Blues)
    labels = nx.get_edge_attributes(G, 'weight')
    #n_label = nx.get_edge_attributes(G,'labels')
    nx.draw_networkx_labels(G, pos, font_size=6)
    #nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)
    plt.show()


if __name__ == '__main__':
    main()
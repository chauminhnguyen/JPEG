import numpy as np
import cv2
import scipy.fftpack as fftpack
import matplotlib.pyplot as plt
from dahuffman import HuffmanCodec
from utils import *
import os
import time

HEIGHT_BITS = 16
WIDTH_BITS = 16
DC_BITS = 16
AC_BITS = 16

def main(string):
    QF = 1
    start = time.time()
    B = 8   
    im = cv2.imread(string)
    h,w=np.array(im.shape[:2])/B * B
    h = int(h)
    w = int(w)
    jpg_len = 0

    b = b""
    b += h.to_bytes(HEIGHT_BITS, byteorder='big')
    b += w.to_bytes(WIDTH_BITS, byteorder='big')


    block=np.array([[B,B]]) #first component is col, second component is row
    scol=block[0,0]
    srow=block[0,1]

    imYCC=cv2.cvtColor(im, cv2.COLOR_BGR2YCR_CB)

    #*Subsample Chrominance Channels======================
    SSV=2
    SSH=2
    crf=cv2.boxFilter(imYCC[:,:,1],ddepth=-1,ksize=(2,2))
    cbf=cv2.boxFilter(imYCC[:,:,2],ddepth=-1,ksize=(2,2))
    
    y = imYCC[:,:,0]
    crsub=crf[::SSV,::SSH]
    cbsub=cbf[::SSV,::SSH]
    imSub=[y,crsub,cbsub]
    #*=====================================================

    ch=['Y','Cr','Cb']
    it = 0
    for idx,channel in enumerate(imSub):
        channelrows=channel.shape[0]
        channelcols=channel.shape[1]

        TransQuant = np.zeros((channelrows,channelcols), np.float32)
        blocksV=channelrows/B
        blocksH=channelcols/B
        vis0 = np.zeros((channelrows,channelcols), np.float32)
        
        vis0[:channelrows, :channelcols] = channel
        vis0=vis0 - 128
        
        dc_c = []
        ac_c = []
        rle_ecoded = []

        for row in range(int(blocksV)):
            for col in range(int(blocksH)):

                #* Using DCT
                currentblock = cv2.dct(vis0[row*B:(row+1)*B,col*B:(col+1)*B])
                
                #*Quantization
                TransQuant[row*B:(row+1)*B,col*B:(col+1)*B]=np.round(currentblock/Q[idx])

                #*Zigzag
                zz = zigzag(TransQuant[row*B:(row+1)*B,col*B:(col+1)*B])

                #*DPCM - Vectorizing
                dc_c.append(zz[0])
                ac_c.append(zz[1:])
                

                #*RLE on ac encoded as (skip, value)
                #*(0, 0) end the block
                rle_ecoded.extend(rle(ac_c[-1]))


        #Save dc table
        dc_codec = HuffmanCodec.from_data(dc_c)
        dc_codec.save("dc_table/dc_table{0}.tb" .format(it))
        jpg_len += os.stat("dc_table/dc_table{0}.tb" .format(it)).st_size

        encoded = dc_codec.encode(dc_c)

        l = len(encoded)
        b += l.to_bytes(DC_BITS, byteorder='big')
        b += encoded
        
        #Save ac table
        
        ac_codec = HuffmanCodec.from_data(rle_ecoded)
        
        ac_codec.save("ac_table/ac_table{0}.tb" .format(it))
        jpg_len += os.stat("ac_table/ac_table{0}.tb" .format(it)).st_size

        encoded = ac_codec.encode(rle_ecoded)

        
        #string += encoded
        l = len(encoded)
        b += l.to_bytes(AC_BITS, byteorder='big')
        b += encoded

        it += 1

    file = open("encoded.jpg", "wb")
    file.write(b)

    end = time.time()

    r = (len(b) + jpg_len) / (w * h)
    #print("Hệ số nén r : {0}" .format(r))
    #print("time: {0}s" .format(end - start))
    return r, end - start

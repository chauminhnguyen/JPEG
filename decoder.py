import numpy as np
from dahuffman import HuffmanCodec
import cv2
from utils import *
import time

HEIGHT_BITS = 16
WIDTH_BITS = 16
DC_BITS = 16
AC_BITS = 16

def main():

    start = time.time()

    dc = [] # 3, [12288, 3072, 3027]
    ac = [] # 3, [12288, 3072, 3027], [63, .., 63]

    f = open("encoded.jpg", "rb")
    h = f.read(HEIGHT_BITS)
    w = f.read(WIDTH_BITS)
    h = int.from_bytes( h, byteorder = "big")
    w = int.from_bytes( w, byteorder = "big")

    D = w * h / 64
    TransAllQuant = []

    #*Inverse Huffman
    for it in range(3):
        #* DC Table and file
        t = HuffmanCodec.load("dc_table/dc_table{0}.tb" .format(it))
        length = int.from_bytes(f.read(DC_BITS), byteorder = "big")
        dc.append(t.decode(f.read(length)))

        #* AC Table and file
        t = HuffmanCodec.load("ac_table/ac_table{0}.tb" .format(it))
        length = int.from_bytes(f.read(AC_BITS), byteorder = "big")
        ac.append(t.decode(f.read(length)))
    
        #* RLD
        ac_rld = from_rle(ac[it].copy())
        
        temp = np.hstack((np.asarray([dc[it]]).T, np.asarray(ac_rld)))
        zigzag_arr = []

        #* inverse zigzag
        for item in temp:
            zigzag_arr.append(inverse_zigzag(item, B, B))
        TransAllQuant.append(zigzag_arr)

    #*Decoding==========================================
    DecAll=np.zeros((h,w,3), np.uint8)
    reImg = []
    for idx,channel in enumerate(TransAllQuant):
        blocksV=h / B if idx == 0 else h /(B * 2)
        blocksH=w / B if idx == 0 else w /(B * 2)
        back0 = np.zeros((int(blocksV) * 8, int(blocksH) * 8), np.uint8)
        for row in range(int(blocksV)):
            for col in range(int(blocksH)):
                
                dequantblock=channel[col + int(blocksH) * row]*Q[idx]
                #*Inverse DCT + 128
                currentblock = np.round(cv2.idct(dequantblock))+128
                #*clamp to 255 for pixel that exceed 255 and below 0
                currentblock[currentblock>255]=255
                currentblock[currentblock<0]=0
                
                back0[row*B:(row+1)*B,col*B:(col+1)*B]=currentblock
        
        
        #*
        back1=cv2.resize(back0,(w,h))
        #*
        DecAll[:,:,idx]=np.round(back1)

    reImg=cv2.cvtColor(DecAll, cv2.COLOR_YCrCb2BGR)
    cv2.imshow('Decoded Image', reImg)
    
    end = time.time()

    return end - start

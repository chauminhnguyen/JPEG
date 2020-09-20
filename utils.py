from itertools import groupby
import numpy as np

B =  8

QY=np.array([ [16,11,10,16,24,40,51,61],
                [12,12,14,19,26,48,60,55],
                [14,13,16,24,40,57,69,56],
                [14,17,22,29,51,87,80,62],
                [18,22,37,56,68,109,103,77],
                [24,35,55,64,81,104,113,92],
                [49,64,78,87,103,121,120,101],
                [72,92,95,98,112,100,103,99]])

QC=np.array([ [17,18,24,47,99,99,99,99],
                [18,21,26,66,99,99,99,99],
                [24,26,56,99,99,99,99,99],
                [47,66,99,99,99,99,99,99],
                [99,99,99,99,99,99,99,99],
                [99,99,99,99,99,99,99,99],
                [99,99,99,99,99,99,99,99],
                [99,99,99,99,99,99,99,99]])


QF=49
if QF < 50 and QF > 1:
        scale = np.floor(5000/QF)
elif QF < 100:
        scale = 200-2*QF
else:
        print("Quality Factor must be in the range [1..99]")
scale=scale/100.0
Q=[QY*scale,QC*scale,QC*scale]

def rle(arr):
  rle_arr = []
  zero_counter = 0
  for item in [(len(list(group)), i) for i, group in groupby(arr)]:

    if item[1] == -0.0 or item[1] == 0.0:
      zero_counter = item[0]
      continue

    #rle_arr.extend((zero_counter, item[1]) * item[0])
    rle_arr += (zero_counter, item[1])
    for i in range(item[0] - 1):
        rle_arr.extend((0, item[1]))
    if zero_counter != 0:
      zero_counter = 0

  if zero_counter != 0:
    rle_arr.extend((zero_counter, 0))
    zero_counter = 0
  rle_arr.extend((0,0))
  
  return rle_arr

def from_rle(s):
    ac = []
    temp = []
    for i,k in zip(s[0::2], s[1::2]):
        i = int(i)
        temp += ([0] * i)
        if k == 0:
            if i == 0:
                ac.append(temp.copy())
                temp.clear()
        else:
            temp.append(k)
    return ac



def zigzag(input):
    #initializing the variables
    #----------------------------------
    h = 0
    v = 0

    vmin = 0
    hmin = 0

    vmax = input.shape[0]
    hmax = input.shape[1]
    
    #print(vmax ,hmax )

    i = 0

    output = np.zeros(( vmax * hmax))
    #----------------------------------

    while ((v < vmax) and (h < hmax)):
    	
        if ((h + v) % 2) == 0:                 # going up
            
            if (v == vmin):
            	#print(1)
                output[i] = input[v, h]        # if we got to the first line

                if (h == hmax):
                    v = v + 1
                else:
                    h = h + 1                        

                i = i + 1

            elif ((h == hmax -1 ) and (v < vmax)):   # if we got to the last column
            	#print(2)
            	output[i] = input[v, h] 
            	v = v + 1
            	i = i + 1

            elif ((v > vmin) and (h < hmax -1 )):    # all other cases
            	#print(3)
            	output[i] = input[v, h] 
            	v = v - 1
            	h = h + 1
            	i = i + 1

        
        else:                                    # going down

        	if ((v == vmax -1) and (h <= hmax -1)):       # if we got to the last line
        		#print(4)
        		output[i] = input[v, h] 
        		h = h + 1
        		i = i + 1
        
        	elif (h == hmin):                  # if we got to the first column
        		#print(5)
        		output[i] = input[v, h] 

        		if (v == vmax -1):
        			h = h + 1
        		else:
        			v = v + 1

        		i = i + 1

        	elif ((v < vmax -1) and (h > hmin)):     # all other cases
        		#print(6)
        		output[i] = input[v, h] 
        		v = v + 1
        		h = h - 1
        		i = i + 1




        if ((v == vmax-1) and (h == hmax-1)):          # bottom right element
        	#print(7)        	
        	output[i] = input[v, h] 
        	break

    #print ('v:',v,', h:',h,', i:',i)
    return output



def inverse_zigzag(input, vmax, hmax):
	
	#print input.shape

	# initializing the variables
	#----------------------------------
	h = 0
	v = 0

	vmin = 0
	hmin = 0

	output = np.zeros((vmax, hmax))

	i = 0
    #----------------------------------

	while ((v < vmax) and (h < hmax)): 
		#print ('v:',v,', h:',h,', i:',i)   	
		if ((h + v) % 2) == 0:                 # going up
            
			if (v == vmin):
				#print(1)
				
				output[v, h] = input[i]        # if we got to the first line

				if (h == hmax):
					v = v + 1
				else:
					h = h + 1                        

				i = i + 1

			elif ((h == hmax -1 ) and (v < vmax)):   # if we got to the last column
				output[v, h] = input[i] 
				v = v + 1
				i = i + 1

			elif ((v > vmin) and (h < hmax -1 )):    # all other cases
				output[v, h] = input[i] 
				v = v - 1
				h = h + 1
				i = i + 1

        
		else:                                    # going down

			if ((v == vmax -1) and (h <= hmax -1)):       # if we got to the last line
				output[v, h] = input[i] 
				h = h + 1
				i = i + 1
        
			elif (h == hmin):                  # if we got to the first column
				output[v, h] = input[i] 
				if (v == vmax -1):
					h = h + 1
				else:
					v = v + 1
				i = i + 1
        		        		
			elif((v < vmax -1) and (h > hmin)):     # all other cases
				output[v, h] = input[i] 
				v = v + 1
				h = h - 1
				i = i + 1




		if ((v == vmax-1) and (h == hmax-1)):          # bottom right element  	
			output[v, h] = input[i] 
			break


	return output
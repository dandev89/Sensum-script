'''
Created on Apr 30, 2013

@author: daniele
'''
import cv2
from cv2 import cv
import osgeo.gdal, os, sys, osgeo.osr, math
from osgeo.gdalconst import *
import numpy as np
import scipy as sp
import time
from scipy import signal
from numpy import unravel_index
from myFeatureExtraction import Extraction 

starttime=time.time()
path = '/Users/daniele/Documents/Sensum/Bishkek/'
folder1 = 'LT51510302006213IKR00/'
name1 = 'LT51510302006213IKR00_B2_city.TIF'
folder2 = 'LT51510302009189KHC01/'
name2 = 'LT51510302009189KHC01_B2_city.TIF'
outname='LT51510302009189KHC01_B2_city_adj.TIF'

osgeo.gdal.AllRegister()
os.chdir(path)

#open the image
inputimg1 = osgeo.gdal.Open(folder1+name1,GA_ReadOnly)
if inputimg1 is None:
    print 'Could not open ' + name1
    sys.exit(1)
#number of rows and columns are printed out 
print 'Image 1'   
cols1=inputimg1.RasterXSize
rows1=inputimg1.RasterYSize
transform1=inputimg1.GetGeoTransform()
xOrigin1 = transform1[0] 
print xOrigin1
yOrigin1 = transform1[3] 
print yOrigin1
pixelWidth1 = transform1[1] 
print pixelWidth1
pixelHeight1 = transform1[5]
print pixelHeight1
print rows1,cols1

inputimg2 = osgeo.gdal.Open(folder2+name2,GA_ReadOnly)
if inputimg2 is None:
    print 'Could not open ' + name2
    sys.exit(1)
#number of rows and columns are printed out    
cols2=inputimg2.RasterXSize
rows2=inputimg2.RasterYSize
print 'Image 2'
transform2=inputimg2.GetGeoTransform()
xOrigin2 = transform2[0] 
print xOrigin2
yOrigin2 = transform2[3] 
print yOrigin2
pixelWidth2 = transform2[1] 
print pixelWidth2
pixelHeight2 = transform2[5]
print pixelHeight2
print rows2,cols2

k = Extraction(path+folder1+name1,path+folder2+name2)
print k

for l in range(0,len(k)):
    xoff=k[l][2]-k[l][0]
    yoff=k[l][3]-k[l][1]
xoff.mean()
yoff.mean()

print xoff,yoff

inband1=inputimg1.GetRasterBand(1)
print 'Image 1 correctly opened'
inband2=inputimg2.GetRasterBand(1)
print 'Image 2 correctly opened'

driver=inputimg1.GetDriver()
rows_out=rows1+rows2-1
cols_out=cols1+cols2-1
output=driver.Create(folder2+outname,cols2,rows2,1)
outband=output.GetRasterBand(1)
print 'Output image created'

# register all of the drivers
osgeo.gdal.AllRegister()

data1 = inband1.ReadAsArray()
print 'image 1 read'
data2 = inband2.ReadAsArray()
print 'image 2 read'

out=np.zeros(shape=(rows2,cols2))

for i in range(0,rows2):
    for j in range(0,cols2):
        if ((i+yoff)<=0) or ((j+xoff)<=0):
            out[i][j]=0
        else:
            out[i][j]=data2[i+yoff][j+xoff]

#tras=np.matrix([[1,0,0,xoff],[0,1,0,yoff],[0,0,1,0],[0,0,0,1]])
#out=tras*data2
       

'''
print unravel_index(np.argmax(autocorr),autocorr.shape)
print np.where(autocorr == autocorr.max())
print autocorr.max()
print autocorr.max()/autocorr.mean()
print unravel_index(np.argmax(out),out.shape)
print np.where(out==out.max())
print out.max()
print out.max()/out.mean()
#out=(out-np.mean(out))*255
#out=(out/np.mean(out))*255
'''
            
outband.WriteArray(out,0,0)
geotransform=inputimg2.GetGeoTransform()
output.SetGeoTransform(geotransform)
inprj=inputimg2.GetProjection()
output.SetProjection(inprj)   

endtime=time.time()
print 'Total time= ' + str(endtime-starttime)
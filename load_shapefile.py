#!/usr/local/bin//python3.9
##!/Users/jfuerst/anaconda/bin/python

import shapefile
import numpy as np
import sys
import os
import pyproj
import subprocess
import datetime

def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

#from make_directory import makeDIR

day       = 28  # measurements were carried out 19-20 May 2019 (also encoded in attribute table)
month     = 4
year      = 2022
inventory_path = 'C:/Users/mu92vogu/Desktop/Ground Penetrating Radar/REFLEX/shapefiles/'
inventory_fname = 'Perito_Moreno_Ice_Thickness'
#day       = 27
#month     = 4
#year      = 2012
#inventory_path = './raw/NPI/IV_Espesor_de_hielo/Colonia-Esp/'
#inventory_fname = 'Colonia_perfiles.shp'
storage_path = 'C:/Users/mu92vogu/Desktop/Thickness Modelling/processed_shp'
output_path = storage_path
output_fname = inventory_fname+'.csv'

p18 = pyproj.Proj(proj='utm', zone=18, ellps='WGS84')
p33 = pyproj.Proj(proj='utm', zone=33, ellps='WGS84',inverse=True)

unc = 10.0/100.0

#################################################################
#################################################################
#                        MAIN PROGRAMME                         #
#################################################################
#################################################################

#pid=subprocess.call('rm -rf '+storage_path,shell=True)

#ctr = shapefile.Reader(shp=myshp,dbf=mydbf)
ctr = shapefile.Reader(inventory_path+inventory_fname+".shp")
geomet = ctr.shapeRecords() # attributes + geometries

k=0
l=0
ll=0
lll=0
areas = np.zeros((np.size(geomet),1))

#while k < np.size(geomet):
for k in range(0,np.size(geomet)):
    aday      = datetime.date(year,month,day)
    #print 'Ordinal Day nummber',aday.toordinal()
    #print( k,geomet[k].record[8-1],geomet[k].record[3-1])
    #if(is_number(str(geomet[k].record[8-1]))):
    #    print(k)
    #print(geomet[k].record[3-1],geomet[k].record[4-1],geomet[k].record[5-1],geomet[k].record[6-1],geomet[k].record[7-1])
    #print(type(geomet[k].record[3-1]),type(geomet[k].record[6-1]))
    #print(k,type(geomet[k].record[6-1]),isinstance(geomet[k].record[6-1], str))
    if(isinstance(geomet[k].record[6-1], str)):
        #sur       = float(geomet[k].record[8-1])
        #print(geomet[k].record[3-1],geomet[k].record[4-1],geomet[k].record[5-1],geomet[k].record[6-1],geomet[k].record[7-1])
        xx        = float(geomet[k].shape.points[0][0])
        yy        = float(geomet[k].shape.points[0][1])
        sur       = float(geomet[k].record[3-1])
        thi       = float(geomet[k].record[5-1])
        bed       = -9999
        #print sur,thi,unc
        #print thi
        #dthi      = unc*thi

        lamb      = 20e6
        vv        = 168.5*1e6 # verified in Cassassa 1998
        deltat    = 2.0*thi/vv
        dthi      = 0.5*((vv/lamb)**2+(deltat*0.02*vv)**2)**0.5

        [ni,nj]   = np.shape(geomet[k].shape.points)

        #xx        = np.zeros(ni)
        #yy        = np.zeros(ni)
        #lat       = np.zeros(ni)
        #lon       = np.zeros(ni)


        #for ii in range(0, ni):
        #xx      = geomet[k].shape.points[0][0]
        #yy      = geomet[k].shape.points[0][1]
        lon,lat = p18(xx,yy,inverse=True)

        #xxx,yyy = p18(lon,lat)

        #command = 'echo '+str(lat)+' '+str(lon)+'| GeoidEval'
        ##command = 'echo '+str(xx)+' '+str(yy)+'| GeoidEval -z 35n'
        #proc    = subprocess.Popen(command,shell=True,stdout=subprocess.PIPE)
        #output  = proc.stdout.read()
        #output  = output.strip()
        ##print 'First geoid correction : ',output,' m','; at location ',xx,xxx,yy,yyy

        if k == 0:
            proc=subprocess.call('rm -f '+output_path+'/'+output_fname,shell=True)
            with open(output_path+'/'+output_fname,'w') as thefile:
                thefile.write("%16.8f\t%16.8f\t%9.4f\t%9.4f\t%9.4f\t%i\n" % (float(xx),float(yy),float(thi),float(sur),float(dthi),int(aday.toordinal())))
        else:
            with open(output_path+'/'+output_fname,'a') as thefile:
                thefile.write("%16.8f\t%16.8f\t%9.4f\t%9.4f\t%9.4f\t%i\n" % (float(xx),float(yy),float(thi),float(sur),float(dthi),int(aday.toordinal())))
#    k += 1



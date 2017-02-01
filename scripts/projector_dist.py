#################################################################################
#################################################################################
#################################################################################
#######                                                                   #######
#######                     RADON TRANSFORM DISTANCE-DRIVEN               #######
#######                                                                   #######
#######        Author: Filippo Arcadu, arcusfil@gmail.com, 08/07/2016     #######
#######                                                                   #######
#################################################################################
#################################################################################
#################################################################################




####  PYTHON MODULES
from __future__ import division,print_function
import time
import datetime
import argparse
import sys
import os
import numpy as np




####  MY PYTHON MODULES
import myImageIO as io
import myPrint as pp
import myImageDisplay as dis
import myImageProcess as proc

sys.path.append( 'pymodule_radon_distance_driven/' )
import radon_distance_driven as rdd




####  MY FORMAT VARIABLES
myfloat = np.float32




####  CONSTANTS
eps = 1e-8




##########################################################
##########################################################
####                                                  ####
####             GET INPUT ARGUMENTS                  ####
####                                                  ####
##########################################################
##########################################################

def getArgs():
    parser = argparse.ArgumentParser(description='Radon Transform distance-driven',
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    
    parser.add_argument('-Di', '--pathin', dest='pathin', default='./',
                        help='Specify path to input data')    
    
    parser.add_argument('-i', '--image', dest='image',
                        help='Specify name of input image')
    
    parser.add_argument('-Do', '--pathout', dest='pathout',
                        help='Specify path to output data') 
    
    parser.add_argument('-o', '--sino', dest='sino',
                        help='Specify name of output sinogram')
    
    parser.add_argument('-n', '--nang', dest='nang', type=int,
                        help='Select the number of projection angles') 
    
    parser.add_argument('-g', '--geometry', dest='geometry',default='0',
                        help='Specify projection geometry; @@@@@@@@@@@@@@@@@@@@@@@'
                             +' -g 0 --> equiangular projections in [0,180)')

    parser.add_argument('-p',dest='plot', action='store_true',
                        help='Display check-plots during the run of the code')

    args = parser.parse_args()
    

    ##  Exit of the program in case the compulsory arguments, 
    ##  are not specified
    if args.image is None:
        parser.print_help()
        print('ERROR: Input image name not specified!')
        sys.exit()  
        
    return args




##########################################################
##########################################################
####                                                  ####
####                    SAVE SINOGRAM                 ####
####                                                  ####
##########################################################
##########################################################

def save_sino( sino , angles , args ):
    ##  Save sinogram
    if args.pathout is None:
        pathout = args.pathin
    else:
        pathout = args.pathout
    
    if args.sino is None:
        filename = args.image
        filename = filename[:len(filename)-4]

        if args.nang < 10:
            str_ang = '000' + str( args.nang )
        elif args.nang < 100:
            str_ang = '00' + str( args.nang )
        elif args.nang < 1000:
            str_ang = '0' + str( args.nang )
        else:
            str_ang = str( args.nang ) 

        filename += '_ang' + str_ang + '_radon_distdriv'
        filename += '_sino.DMP' 
        filename = pathout + filename
    else:
        filename = pathout + args.sino

    io.writeImage( filename , sino )
    print( '\nOutput file written in:\n', filename )





##########################################################
##########################################################
####                                                  ####
####                       MAIN                       ####
####                                                  ####
##########################################################
##########################################################

def main():
    ##  Initial print
    print('\n')
    print('##########################################')  
    print('##########################################')
    print('####                                  ####') 
    print('#### RADON TRANSFORM DISTANCE-DRIVEN  ####') 
    print('####                                  ####')    
    print('##########################################')
    print('##########################################')      
    print('\n')


    
    ##  Get input arguments
    args = getArgs()


    
    ##  Get path to input sino
    pathin = args.pathin


    
    ##  Get input image
    ##  You assume the image to be square
    image_name = pathin + args.image
    image = io.readImage( image_name ).astype( myfloat )
    npix = image.shape[1]
    nang = args.nang

    print('\nInput image:\n', image_name)
    print('Number of projection angles: ', nang)
    print('Number of pixels: ', npix)


    ##  Check plot
    if args.plot is True:
        dis.plot( image , 'Input image' )



    ##  Get projection geometry  
    angles = np.arange( nang )
    angles = ( angles * np.pi )/myfloat( nang )
    print('\nDealing with equally angularly spaced projections in [0,180)')


    
    ##  Compute forward projection
    print( '\nRun forward projection ...', end='' )
    time1 = time.time()
    sino = rdd.forwproj( image.astype( myfloat ) , angles.astype( myfloat ) )
    time2 = time.time()
    print( ' done!' )



    ##  Show sino     
    if args.plot is True:
        dis.plot( sino , 'Sinogram' )    


    
    ##  Save sino
    save_sino( sino , angles , args )

    
    
    ##  Time elapsed for the computation of the radon transform
    dt = time2 - time1
    print('\nTime elapsed to run radon pixel-driven: ', dt/60.0,' min.   ', dt,' sec.') 
    print('\n')




###########################################################
###########################################################
####                                                   #### 
####                      CALL TO MAIN                 ####
####                                                   ####
###########################################################
###########################################################

if __name__ == '__main__':
    main()

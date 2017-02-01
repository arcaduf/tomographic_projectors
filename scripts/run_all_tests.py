###########################################################
###########################################################
####                                                   ####
####                     TEST ROUTINE                  ####
####                                                   ####
###########################################################
###########################################################




####  PYTHON MODULES
from __future__ import division , print_function
import sys
import numpy as np
import filters as fil

sys.path.append( '../common/' )
import my_image_io as io
import my_image_display as dis

import class_projectors_radon as cpr
import class_projectors_bspline as cpb




####  MY VARIABLE FORMAT
myfloat = np.float32



####  ABBREVIATIONS FOR PROJECTORS
####    dd  --->  distance-driven
####    pd  --->  pixel-driven
####    rd  --->  ray-driven
####    ss  --->  slant-stacking
####    bsp --->  bspline
list_proj = [ 'dd' , 'pd' , 'rd' , 'ss' , 'bsp' ]




###########################################################
###########################################################
####                                                   ####
####                       TEST 1                      ####
####                                                   ####
###########################################################
########################################################### 

##  Check whether each backprojector is really adjoint to the
##  corresponding forward projector by using the definition of
##  adjoint operator.
##  A: U --> V  thus A^{T}: V --> U
##  A is the linear operator, A^{T} is the adjoint operator, 
##  U and V are vector spaces.
##  For all x in U and y in V, it holds that:
##  < y , Ax > = < A^{T}y , x >

def test1( abbr ):
    ##  Pick up a random number in [0,256] and make sure it is even
    n = np.int( np.random.rand( 1 ) * 256 )
    if n == 0:
        n = 20
    if n % 2 != 0:
        n += 1
    print( 'Number of pixels: ' , n )

    ##  Construct an array of random angles in rad
    a  = np.random.random( n ).astype( myfloat )

    ##  Construct a random object
    y1 = np.random.random( ( n , n ) ).astype( myfloat )

    ##  Construct a random sinogram
    x2 = np.random.random( ( n , n ) ).astype(myfloat)
    
    ##  Load selected projectors
    if abbr != 'bsp':
        tp = cpr.projectors( n , a , oper=abbr )
    else:
        tp = cpb.projectors( n , a , bspline_degree=3 , proj_support_y=4 ,
                             nsamples_y=2048 , radon_degree=0 , filt='ramp' , 
                             back = False , plot=True  ) 

    ##  Create A^{T}y
    x1 = tp.At( y1 )

    ##  Create Ax
    y2 = tp.A( x2 )

    ##  Compute inner product < A^{T}y , x >
    inn_prod = np.sum( np.conjugate( x2 ) * x1 )

    ##  Compute inner product < y , Ax >
    inn_prod = np.sum( np.conjugate( y2 ) * y1 )

    print( '< b , Tt( a ) >  = ', inn_prod )
    print( '< T( b ) , a >  = ', inn_prod )  




###########################################################
###########################################################
####                                                   ####
####                       TEST 2                      ####
####                                                   ####
###########################################################
###########################################################

##  Test forward projector only

def test2( abbr ):
    ##  Read Shepp-Logan image in folder "../data/"
    image = io.readImage( '../data/shepp_logan_pix0256.DMP' )
    n = image.shape[0]

    ##  Create array of 200 angularly equispaced angles in [0,180) (degrees)
    nang = 200
    a = np.arange( nang ) * 180.0 / nang

    ##  Compute forward projection
    if abbr != 'bsp':
        tp = cpr.projectors( n , a , oper=abbr )
    else:
        a *= np.pi/180.0
        tp = cpb.projectors( n , a , bspline_degree=3 , proj_support_y=4 ,
                             nsamples_y=2048 , radon_degree=0 , filt='ramp' , 
                             back = False , plot=True  )    
    sino = tp.A( image )

    return sino




###########################################################
###########################################################
####                                                   ####
####                       TEST 3                      ####
####                                                   ####
###########################################################
###########################################################

##  Test backprojector only

def test3( abbr, sino ):
    ##  Get sinogram size
    nang , n = sino.shape

    ##  Create array of 200 angularly equispaced angles in [0,180) (degrees)
    a = np.arange( nang ) * 180.0 / nang

    ##  Compute non-filtered backprojection
    if abbr != 'bsp':
        tp = cpr.projectors( n , a , oper=abbr )
    else:
        a *= np.pi/180.0
        tp = cpb.projectors( n , a , bspline_degree=3 , proj_support_y=4 ,
                             nsamples_y=2048 , radon_degree=0 , filt='ramp' , 
                             back = False , plot=True  )    
    reco_nf = tp.At( sino )

    return reco_nf




###########################################################
###########################################################
####                                                   ####
####                       TEST 4                      ####
####                                                   ####
###########################################################
###########################################################

##  Test filtered backprojection

def test4( abbr , sino ):
    ##  Get sinogram size
    nang , n = sino.shape

    ##  Create array of 200 angularly equispaced angles in [0,180) (degrees)
    a = np.arange( nang ) * 180.0 / nang

    ##  Compute non-filtered backprojection
    if abbr != 'bsp':
        tp = cpr.projectors( n , a , oper=abbr )
    else:
        a *= np.pi/180.0
        tp = cpb.projectors( n , a , bspline_degree=3 , proj_support_y=4 ,
                             nsamples_y=2048 , radon_degree=0 , filt='ramp' , 
                             back = False , plot=True  )    
    reco = tp.fbp( sino )

    return reco




###########################################################
###########################################################
####                                                   ####
####                         MAIN                      ####
####                                                   ####
###########################################################
###########################################################  

def main():
    ##  Initial print
    print( '''\nThe program will execute in order 4 tests for the various implementation of the forward and backprojector''' )

    print( '''\nEvery time an image is displayed the code is temporarily halted. To the successive tests close the image''')


    #############################################################
    ##  Test n.1
    #############################################################
    inp = raw_input( '\n\nProceed with test n.1? (y/n) ' )
    if inp == 'n':
        exit()

    print( '###################################################' )
    print( '###                                             ###' )
    print( '###        TEST 1: Test adjoint operator        ###' )
    print( '###                                             ###' ) 
    print( '###################################################' ) 

    print( '\nTest adjoint for DISTANCE-DRIVEN:' )
    test1( 'dd' )
    print( '\nTest adjoint for PIXEL-DRIVEN:' )
    test1( 'pd' ) 
    print( '\nTest adjoint for RAY-DRIVEN:' )
    test1( 'rd' ) 
    print( '\nTest adjoint for SLANT-STACKING:' )
    test1( 'ss' ) 
    print( '\nTest adjoint for BSPLINE:' )
    test1( 'bsp' )



    #############################################################
    ##  Test n.2
    #############################################################
    inp = raw_input( '\n\nProceed with test n.2? (y/n) ' )
    if inp == 'n':
        exit()

    print( '###################################################' )
    print( '###                                             ###' )
    print( '###        TEST 2: Test forward operator        ###' )
    print( '###                                             ###' ) 
    print( '###################################################' ) 

    print( '\nTest forward operator for DISTANCE-DRIVEN:' )
    sino1 = test2( 'dd' )
    print( '\nTest forward operator for PIXEL-DRIVEN:' )
    sino2 = test2( 'pd' ) 
    print( '\nTest forward operator for RAY-DRIVEN:' )
    sino3 = test2( 'rd' ) 
    print( '\nTest forward operator for SLANT-STACKING:' )
    sino4 = test2( 'ss' ) 
    print( '\nTest forward operator for BSPLINE:' )
    sino5 = test2( 'bsp' )

    dis.plot_multi( [ sino1 , sino2 , sino3 , sino4 , sino5 ] ,
                    [ 'DIST-DRIV' , 'PIX-DRIV' , 'RAY-DRIV' , 
                      'SLANT-STACK' , 'BSPLINE' ] )



    #############################################################
    ##  Test n.3
    ############################################################# 
    inp = raw_input( '\n\nProceed with test n.3? (y/n) ' )
    if inp == 'n':
        exit()

    print( '###################################################' )
    print( '###                                             ###' )
    print( '###          TEST 3: Test backprojector         ###' )
    print( '###                                             ###' ) 
    print( '###################################################' ) 

    print( '\nTest non-filtered backprojection for DISTANCE-DRIVEN:' )
    reco1 = test3( 'dd' , sino1 )
    print( '\nTest non-filtered backprojection for PIXEL-DRIVEN:' )
    reco2 = test3( 'pd' , sino2 ) 
    print( '\nTest non-filtered backprojection for RAY-DRIVEN:' )
    reco3 = test3( 'rd' , sino3 ) 
    print( '\nTest non-filtered backprojection for SLANT-STACKING:' )
    reco4 = test3( 'ss' , sino4 ) 
    print( '\nTest non-filtered backprojection for BSPLINE:' )
    reco5 = test3( 'bsp' , sino5 )

    dis.plot_multi( [ reco1 , reco2 , reco3 , reco4 , reco5 ] ,
                    [ 'DIST-DRIV' , 'PIX-DRIV' , 'RAY-DRIV' , 
                      'SLANT-STACK' , 'BSPLINE' ] )



    #############################################################
    ##  Test n.4
    ############################################################# 
    inp = raw_input( '\n\nProceed with test n.4? (y/n) ' )
    if inp == 'n':
        exit()

    print( '###################################################' )
    print( '###                                             ###' )
    print( '###              TEST 4: Test FBP               ###' )
    print( '###                                             ###' ) 
    print( '###################################################' ) 

    print( '\nTest filtered backprojection for DISTANCE-DRIVEN:' )
    reco1 = test4( 'dd' , sino1 )
    print( '\nTest filtered backprojection for PIXEL-DRIVEN:' )
    reco2 = test4( 'pd' , sino2 ) 
    print( '\nTest filtered backprojection for RAY-DRIVEN:' )
    reco3 = test4( 'rd' , sino3 ) 
    print( '\nTest filtered backprojection for SLANT-STACKING:' )
    reco4 = test4( 'ss' , sino4 ) 
    print( '\nTest filtered backprojection for BSPLINE:' )
    reco5 = test4( 'bsp' , sino5 )

    dis.plot_multi( [ reco1 , reco2 , reco3 , reco4 , reco5 ] ,
                    [ 'DIST-DRIV' , 'PIX-DRIV' , 'RAY-DRIV' , 
                      'SLANT-STACK' , 'BSPLINE' ] )  




###########################################################
###########################################################
####                                                   ####
####                    CALL TO MAIN                   ####
####                                                   ####
###########################################################
###########################################################

if __name__ == '__main__':
    main()

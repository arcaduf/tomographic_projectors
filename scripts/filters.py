##########################################################
##########################################################
####                                                  ####
####       SINOGRAM FILTERING FOR BACKPROJECTION      ####
####                                                  ####
##########################################################
##########################################################




####  PYTHON MODULES
import sys
import numpy as np




####  MY FORMAT VARIABLES
myfloat   = np.float32
myint     = np.int
mycomplex = np.complex64




##########################################################
##########################################################
####                                                  ####
####              CALCULATE FILTERING ARRAY           ####
####                                                  ####
##########################################################
##########################################################

def ramp( n ):
    nh = np.int( n * 0.5 )
    ramp = np.zeros( n )

    for i in range( n ):
        c = i - ( nh - 1 )
        if c == 0:
            ramp[i] = 0.25
        elif c % 2 == 0:
            ramp[i] = 0.0
        else:
            ramp[i] = -1.0 / ( np.pi * c )**2
    return ramp

            

def hann( k ):
    return 0.5 * ( 1 + np.cos( np.pi * k / 0.5 ) )



def shlo( k ):
    arr = np.zeros( len( k ) )
    arr[0] = 1.0
    arr[1:] = np.sin( np.pi * k[1:] ) / ( np.pi * k[1:] )
    return arr



def parz( k ):
    arr = np.zeros( len( k ) )

    ii = np.argwhere( k <= 0.25 )
    arr[ii] = 1 - 6 * ( k[ii]/0.5 )**2 * ( 1 - k[ii]/0.5 )

    ii = np.argwhere( k > 0.25 )
    arr[ii] = 2 * ( 1 - k[ii]/0.5 )**3

    return arr



def calc_filter( n , ftype='ramp' , dpc=False ):
    nh = np.int( n * 0.5 )   
                                                                
    if ftype is not None and dpc is False:
        filt = np.abs( np.fft.fft( ramp( n ) ) )[:nh]
        k    = np.arange( nh ) / myfloat( n )
        
        if ftype=='ramp' or ftype=='ram-lak' or ftype=='Ram-Lak':
            wind = np.ones( len( k ) )

        elif ftype=='hann' or ftype=='hanning' or ftype=='Hann' or ftype=='Hanning':
            wind = hann( k )

        elif ftype=='shlo' or ftype=='shepp-logan' or ftype=='Shepp-Logan':
            wind = shlo( k )

        elif ftype=='parz' or ftype=='parzen' or ftype=='Parzen':   
            wind = parz( k )

        filt *= wind
        filt  = np.hstack( ( filt , filt[nh-1:0:-1] ) )
        #print( filt )

    elif ftype is None and dpc is False:
        filt = np.ones( 2 * n )

    return filt      




##########################################################
##########################################################
####                                                  ####
####                 PROJECTION FILTERING             ####
####                                                  ####
##########################################################
##########################################################

def filter_proj( sino , ftype='ramp' , dpc=False ):
    ##  Compute oversamples array length
    nang , npix = sino.shape
    norm  = np.pi / myfloat( nang )
    nfreq = 2 * int( 2**( int( np.ceil( np.log2( npix ) ) ) ) )


    ##  Compute filtering array
    filtarr  = calc_filter( nfreq , ftype=ftype , dpc=dpc )
    #print( 'filtarr:')
    #for i in range( len( filtarr ) ):
    #    print( 'i = ', i,'  filt = ' , filtarr[i] )


    ##  Zero-pad projections
    sino_filt = np.concatenate( ( sino , np.zeros( ( nang , nfreq - npix - 1 ) ) ) , axis=1 )


    ##  Filtering in Fourier space
    for i in range( nang ):
        #sys.stdout.write( 'Filtering projection number %d\r' % ( i + 1 , ) )
        #sys.stdout.flush()
        sino_filt[i,:] = np.real( np.fft.ifft( np.fft.fft( sino_filt[i,:] ) * filtarr ) )


    ##  Replace values in the original array
    sino[:,:] = norm * sino_filt[:,:npix]

    return sino


2D TOMOGRAPHIC PROJECTORS
=========================



##  Brief description
This repository contains different implementations of the 2D X-ray transform 
its adjoint operator, the backprojector, for parallel beam geometry. 

The following algorithms are included:

* the **Pixel-Driven** projectors;

* the **Ray-Driven** projectors;

* the **Distance-Driven** projectors;

* the **Slant-Stacking** projectors;

* the **Radon Transform based on cubic B-spline tensor product**.


##  Installation
Basic compilers like gcc and g++ are required.
The simplest way to use the code is with an Anaconda environment equipped with
python-2.7, scikit-image and Cython.

Procedure:

1. Create Anaconda environment (if not already existing): `conda create -n test-repo python=2.7 anaconda`.
2. Install necessary Python packages: `conda install -n test-repo scikit-image Cython`.
3. Activate environment: `source activate test-repo`.
4. Download the repo: `git clone git@github.com:arcaduf/tomographic_projectors.git`.
5. Install C code for the projectors: `python setup.py`.

If setup.py runs without giving any error all subroutines in C have been installed and
your python version meets all dependencies.

If you run `python setup.py 1` (you can use any other character than 1), the 
all executables, temporary and build folders are deleted, the test data are 
placed in .zip files. In this way, the repository is restored to its original
status, right after the download.



##  Test the package
Go inside the folder "scripts/" and run: `python run_all_tests.py`.
Every time this script creates an image, the script is halted. To run the successive tests
just close the image.


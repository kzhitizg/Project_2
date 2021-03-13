# Project_2
Repo for Project 2, Osteosarcoma detection

## cython_files
Contains the cython sample files

## Region_Growing
Contains images, with scripts to run region growing algorithms

## modules
Contains the cython modules

### NbrRegionSegment
Contains Region Growing through neighbours, implemented in cpp

**Note** To build a cython module, follow the following steps :-
* Run the build.ps1 (Windows) or build.sh (Linux) in source directory. It will build the cpp + header files to use
* .pyd file should be created along with build directory
* The pyd file can be imported as a normal python file (import xyz). The functions defined in the .pyx file (in src/cython folder) can be used as normal python functions
* For better usability, the .pyd functions are wrapped by module itself, so importing the folder in a script will provide all required functions with better IDE suggestions. Its usage can be found in Segmentation.ipynb








### GLCM Features
* Energy
* Contrast
* Inverse difference moment
* Entropy
* Correlation
* Variance
* Sum average
* Sum variance
* sum entropy
* Difference Entropy
* Difference Variance
* Inverse measure of Correlation 1
* Inverse measure of Correlation 2
* Maximal correlation of correlation

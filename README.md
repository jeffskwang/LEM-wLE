# LEM-wLE
A landscape evolution model that incorporates lateral erosion written in the python coding language. Animations of simulations can be found here: https://www.youtube.com/playlist?list=PLnBjO1cu4qCQOc38ptFVAJ4id2gZ6drm3

The lateral erosion sub-model is an implementation of the algorithm detailed in Langston and Tucker (2018) (https://esurf.copernicus.org/articles/6/1/2018/). 

The model is located in the LEM-wLE subfolder, which contains the following folders and files:

[folders]

-input - contains initial topography .asc raster files 
-modules - contains functions used for the model
-output - this is where data is saved for the model runs
-parameters - this contains the driver files that the code uses

[files]

-main.py - this is the main code for the model that calls the functions in the modules folder
-plot_output.py - this is the main plotting routine that plots the .asc files as matplotlib pcolor plots
-run_example_pypy.sh - this is an example bash script that runs the code using pypy
-run_example_python.sh - this is an example bash script that runs the code using python
-run_example_python.bat - this is an example windows batch file that runs the code using python

I strongly recommend utilizing the pypy to run the main code and python to run the plotting routine. Using pypy increases the speed of the code dramatically. PyPy is found here: https://www.pypy.org/

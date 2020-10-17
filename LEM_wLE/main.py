#LEM written by Jeffrey Kwang 11/16/2014
#This reduced complexity model contains codes for a detachment limited & transport limited model
#importing libaries
import time
import os
import csv
import sys
import importlib
import shutil

#intialize
#start time
start_time = time.time()

#parent folder
parent_folder = os.getcwd()
sys.path.append(parent_folder +'/modules')
sys.path.append(parent_folder +'/parameters')

#cleanup
for files_temp in os.listdir(parent_folder+'/modules'):
    if files_temp.endswith('.pyc'):
        os.remove(parent_folder+'/modules/'+files_temp)
for files_temp in os.listdir(parent_folder+'/parameters'):
    if files_temp.endswith('.pyc'):
        os.remove(parent_folder+'/parameters/'+files_temp)

#parameters
parameters = importlib.import_module(sys.argv[1])
globals().update(parameters.__dict__)
if os.path.isdir(parent_folder+'/output/'+output_folder):
    shutil.rmtree(parent_folder+'/output/'+output_folder)
    time.sleep(5)
os.makedirs(parent_folder+'/output/'+output_folder)
os.makedirs(parent_folder+'/output/'+output_folder+'/input')
shutil.copyfile(parent_folder+'/parameters/'+sys.argv[1]+'.py',parent_folder+'/output/'+output_folder+'/input/'+sys.argv[1]+'.py')
if input_file != '':
    shutil.copyfile(parent_folder+'/input/'+input_file,parent_folder+'/output/'+output_folder+'/input/'+input_file)

#modules
from variables import *
from F_initial import *
from BC1 import *
from BC2 import *
from F_direction import *
from F_hole import *
from F_hole_update import *
from F_discharge import *
from F_forward_vertical import *
from F_lateral import *
from F_update import *
from F_print import *

#Basic outline---functions
eta_old = f_initial(eta_old,parent_folder)

#main loop
number_of_holes = 0
for t in xrange (1,cellst+1):
    #boundary condition function 1
    eta_old,direction = f_bc1(eta_old,direction)
    #flow direction
    direction,slope,hole = f_direction(eta_old,direction,slope,hole)
    #if there is a closed depression, run the hole function
    if hole[0] == 1 and hole_function == 1:
        number_of_holes += 1 #keeps track of timesteps w/ holes
        eta_ghost = f_hole(eta_old,eta_ghost,direction) #makes a synthetic filled landscape which we run the flow direction algorithm on
    	eta_ghost,direction = f_bc1(eta_ghost,direction)
        direction,slope,hole= f_direction(eta_ghost,direction,slope,hole)
        # if fill_holes = 1, the holes will be filled, and slope will be set to zero
        eta_old,slope = f_hole_update(eta_old,eta_ghost,slope)
    #routes flow        
    discharge, area = f_discharge(discharge,area,direction,precipitation,incision,diffusion,lateral_incision)
    #boundary condition function 2
    eta_old = f_bc2(eta_old)
    #vertical incision
    eta_new,incision,diffusion= f_forward_vertical(eta_old,eta_new,discharge,slope,uplift,incision,diffusion,area)
    #lateral incision
    if lateral_incision_boolean == 1:
        lateral_incision,lateral_incision_cumulative,lateral_incision_threshold_total,lateral_discharge,eta_new\
        = f_lateral(discharge,lateral_incision,lateral_incision_cumulative,area,slope,direction,lateral_incision_threshold_total,lateral_discharge,eta_old,eta_new)        

    #this plots arrays as .asc files
    if plot_array[t] != 0 or t == 1:
        if elevation_plot == 1:
            f_print(eta_new,'elevation',plot_array[t],parent_folder)
        if area_plot == 1:
            f_print(area,'area',plot_array[t],parent_folder)
        if uplift_plot == 1:
            f_print(uplift,'uplift',plot_array[t],parent_folder)
        if slope_plot == 1:
            f_print(slope,'slope',plot_array[t],parent_folder)
        if direction_plot == 1:
            f_print(direction,'direction',plot_array[t],parent_folder)
        if discharge_plot == 1:
            f_print(discharge,'discharge',plot_array[t],parent_folder)
        if incision_plot == 1:
            f_print(incision,'incision',plot_array[t],parent_folder)
        if lateral_incision_plot == 1:
            f_print(lateral_incision,'lateral_incision',plot_array[t],parent_folder)
        if diffusion_plot == 1:
            f_print(diffusion,'diffusion',plot_array[t],parent_folder)
        if precipitation_plot == 1:
            f_print(precipitation,'precipitation',plot_array[t],parent_folder)
        print str(int(float(t)/float(cellst) * 1000.) / 10.) +'% done'
    #updates old arrays as new arrays and erases some arrays
    eta_old,eta_new,lateral_discharge,area,discharge = f_update(eta_old,eta_new,lateral_discharge,area,discharge,t)

#cleanup
for files_temp in os.listdir(parent_folder+'/modules'):
    if files_temp.endswith('.pyc'):
        os.remove(parent_folder+'/modules/'+files_temp)
for files_temp in os.listdir(parent_folder+'/parameters'):
    if files_temp.endswith('.pyc'):
        os.remove(parent_folder+'/parameters/'+files_temp)

#print run time
stop_time = time.time()
print str(round((stop_time -start_time )/60.,1))+' mins'

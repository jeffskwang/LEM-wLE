import sys
import os
import importlib
import numpy as np
import matplotlib
matplotlib.use('Agg') 
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

from matplotlib.colors import LightSource
ls = LightSource(azdeg=315, altdeg=15)

#parent folder
output_folder = sys.argv[1]
parent_folder = os.getcwd()
sys.path.append(parent_folder +'/output/'+output_folder+'/input')
os.chdir(parent_folder +'/output/'+output_folder)

#get parameters file
for files_temp in os.listdir(parent_folder +'/output/'+output_folder+'/input'):
    if files_temp.endswith('.py'):
        parameters = importlib.import_module(files_temp[:-3])
        globals().update(parameters.__dict__)

def fmt(x, pos):
    a, b = '{:.2e}'.format(x).split('e')
    b = int(b)
    return r'${}\times 10^{{{}}}$'.format(a, b)

#change of time unit
def time_unit_function(time_unit, time_unit_plot):
    if time_unit == 'sec' and time_unit_plot == 'sec':
        time_rescale = 1.0
    elif time_unit == 'sec' and time_unit_plot == 'hr':
        time_rescale = 1. / 3600.
    elif time_unit == 'sec' and time_unit_plot == 'day':
        time_rescale = 1. / 3600. / 24. 
    elif time_unit == 'sec' and time_unit_plot == 'yr':
        time_rescale = 1. / 3600. / 24. / 365.25
    elif time_unit == 'sec' and time_unit_plot == 'kyr':
        time_rescale = 1. / 3600. / 24. / 365.25 / 1000.
    elif time_unit == 'sec' and time_unit_plot == 'Myr':
        time_rescale = 1. / 3600. / 24. / 365.25 / 1000000.
    elif time_unit == 'sec' and time_unit_plot == 'Byr':
        time_rescale = 1. / 3600. / 24. / 365.25 / 1000000000.
        
    elif time_unit == 'hr' and time_unit_plot == 'sec':
        time_rescale = 3600.
    elif time_unit == 'hr' and time_unit_plot == 'hr':
        time_rescale = 1.
    elif time_unit == 'hr' and time_unit_plot == 'day':
        time_rescale = 1. / 24. 
    elif time_unit == 'hr' and time_unit_plot == 'yr':
        time_rescale = 1.  / 24. / 365.25
    elif time_unit == 'hr' and time_unit_plot == 'kyr':
        time_rescale = 1.  / 24. / 365.25 / 1000.
    elif time_unit == 'hr' and time_unit_plot == 'Myr':
        time_rescale = 1.  / 24. / 365.25 / 1000000.
    elif time_unit == 'hr' and time_unit_plot == 'Byr':
        time_rescale = 1.  / 24. / 365.25 / 1000000000.
        
    elif time_unit == 'day' and time_unit_plot == 'sec':
        time_rescale = 24. * 3600.
    elif time_unit == 'day' and time_unit_plot == 'hr':
        time_rescale = 24.
    elif time_unit == 'day' and time_unit_plot == 'day':
        time_rescale = 1.
    elif time_unit == 'day' and time_unit_plot == 'yr':
        time_rescale = 1. / 365.25
    elif time_unit == 'day' and time_unit_plot == 'kyr':
        time_rescale = 1. / 365.25 / 1000.
    elif time_unit == 'day' and time_unit_plot == 'Myr':
        time_rescale = 1. / 365.25 / 1000000.
    elif time_unit == 'day' and time_unit_plot == 'Byr':
        time_rescale = 1. / 365.25 / 1000000000.
        
    elif time_unit == 'yr' and time_unit_plot == 'sec':
        time_rescale = 3600. * 24. * 365.25
    elif time_unit == 'yr' and time_unit_plot == 'hr':
        time_rescale = 24. * 365.25
    elif time_unit == 'yr' and time_unit_plot == 'day':
        time_rescale = 365.25
    elif time_unit == 'yr' and time_unit_plot == 'yr':
        time_rescale = 1.
    elif time_unit == 'yr' and time_unit_plot == 'kyr':
        time_rescale = 1. / 1000.
    elif time_unit == 'yr' and time_unit_plot == 'Myr':
        time_rescale = 1. / 1000000.
    elif time_unit == 'yr' and time_unit_plot == 'Byr':
        time_rescale = 1. / 1000000000.
        
    return time_rescale
#plot_function
def plot(plot_type,plot_num,slabel,normalize,log_scale):
    if os.path.isfile(plot_type + '_'+ '%06d' % plot_num + '.png'):
        dumdum = 1
    else:
        s = np.loadtxt(plot_type + '_'+ '%06d' % plot_num + '.asc', skiprows=6)
        if plot_type == 'elevation':    
            s[s==-9999.]=0.0
        else:
            s[s==-9999.]=np.nan
        if plot_type == 'lateral_incision' or plot_type == 'migration_rate':
           s[:,0] = np.nan
        fig = plt.figure(1,figsize = (10.,8.),facecolor='white')
        ax = fig.add_axes([0.0, 0.075, .85, .85])
        cax = fig.add_axes([0.8, 0.075, 0.02, 0.85])
        if log_scale == 0:
                im = ax.imshow(np.rot90(s)/normalize,extent=[x_plot[0]/length_conversion,x_plot[1]/length_conversion,y_plot[0]/length_conversion,y_plot[1]/length_conversion],cmap=cmap)
        elif log_scale == 1:
                s[s==0.0]=np.nan
                im = ax.imshow(np.rot90(np.log10(s/normalize)),extent=[x_plot[0]/length_conversion,x_plot[1]/length_conversion,y_plot[0]/length_conversion,y_plot[1]/length_conversion],cmap=cmap)
        ax.set_xlabel('x ['+length_unit+']')
        ax.set_ylabel('y ['+length_unit+']')

        time_rescale = time_unit_function(time_unit, time_unit_plot)
        
        ax.set_title('Simulation time = ' + str(float(plot_num) * float(dt_plot) * time_rescale)  + ' ' + time_unit_plot)

        fig.colorbar(im, cax=cax, label = slabel, format=ticker.FuncFormatter(fmt),fraction=0.046, pad=0.04)
        plt.savefig(plot_type + '_'+ '%06d' % plot_num + '.png',dpi=300)
        plt.clf()
        plt.clf()
        plt.close('all')
        
print 'plotting...'
cmap = matplotlib.cm.viridis
cmap.set_bad('k',1.)

for plot_num in xrange(0, num_plots):
    print 'plot ' + str(plot_num),'/',str(num_plots-1)
    if elevation_plot == 1:
        plot('elevation',plot_num,r'$\eta$ ['+length_unit+']',length_conversion,0)
    if area_plot == 1:
        plot('area',plot_num,r'$A$ ['+length_unit+r'$^2$]',length_conversion * length_conversion,1)       
    if uplift_plot == 1:
        plot('uplift',plot_num,r'$\upsilon$ ['+length_unit+'/'+time_unit+']',length_conversion/time_conversion,0)
    if slope_plot == 1:
        plot('slope',plot_num,r'$S$ [-]',1.0,0)
    if direction_plot == 1:
        plot('direction',plot_num,r'$direction$ [-]',1.0,0)
    if discharge_plot == 1:
        plot('discharge',plot_num,r'log($Q$) [-]',length_conversion * length_conversion* length_conversion / time_conversion,1)
    if incision_plot == 1:
        plot('incision',plot_num,r'$\epsilon/\upsilon$ [-]',U,0)
    if lateral_incision_plot == 1:
        plot('lateral_incision',plot_num,r'$\epsilon_l/\upsilon$ [-]',U*dx*dy,0)
    if diffusion_plot == 1:
        plot('diffusion',plot_num,r'$D/\upsilon$ [-]',U,0)
    if precipitation_plot == 1:
        plot('precipitation',plot_num,r'$P$ ['+length_unit+'/'+time_unit+']',length_conversion/time_conversion,0)

print 'done'

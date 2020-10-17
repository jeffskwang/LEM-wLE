import importlib
import sys
parameters = importlib.import_module(sys.argv[1])
globals().update(parameters.__dict__)
import os
import numpy as np

#This function prints arrays as .asc files.

def f_print(data,datatype,plot_number,parent_folder):
        data_print = np.zeros((cellsx,cellsy))
        for x in xrange(0,cellsx):
                for y in xrange(0,cellsy):
                        data_print[x,y] = data[x+1][y+1]
        np.savetxt(parent_folder+'/output/'+output_folder+'/'+datatype+'_'+ '%06d' % plot_number + '.asc',data_print,delimiter='\t',newline='\n',header= 'nrows\t'+str(cellsx)+'\ncellsize\t'+str(dx)+'\nxllcorner\t0\nncols\t'+str(cellsy)+'\nyllcorner\t0\nNODATA_value\t-9999', comments='')
        return

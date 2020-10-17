import importlib
import sys
parameters = importlib.import_module(sys.argv[1])
globals().update(parameters.__dict__)

#This function fills sets slope to zero, inhibiting fluvial incision in the closed depressions.

def f_hole_update(eta_old,eta_ghost,slope):
        for x in xrange(0,cellsx+2):
                for y in xrange(0,cellsy+2):
                        if eta_old[x][y] < eta_ghost[x][y]:
                                slope[x][y] = 0.0                
        return eta_old, slope

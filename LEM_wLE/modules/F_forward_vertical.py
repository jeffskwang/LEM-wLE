import importlib
import sys
parameters = importlib.import_module(sys.argv[1])
globals().update(parameters.__dict__)

#This function calculates the vertical components of elevation change,  i.e. fluvial erosion, uplift, and hillslope diffusion.

def f_forward_vertical(eta_old,eta_new,discharge,slope,uplift,incision,diffusion,area):
        
        for x in xrange(1,cellsx+1):
                eta_new[x][1] = eta_old[x][1]
                eta_new[x][cellsy] = eta_old[x][cellsy]
        for y in xrange(1,cellsy+1):
                eta_new[1][y] = eta_old[1][y]
                eta_new[cellsx][y] = eta_old[cellsx][y]
        
        for x in xrange(x_lower,x_upper):
                for y in xrange(y_lower,y_upper):
                        diffusion[x][y]= D / (dx * dy)* \
                        ((eta_old[x-1][y]-2.*eta_old[x][y]+eta_old[x+1][y])+ \
                        (eta_old[x][y-1]-2.*eta_old[x][y]+eta_old[x][y+1]))
                        incision[x][y] = K *(area[x][y]**m)*(slope[x][y]**n)
                        eta_new[x][y] = eta_old[x][y] + dt * (uplift[x][y] + diffusion[x][y] - incision[x][y])
        return eta_new,incision,diffusion
			

import importlib
import sys
parameters = importlib.import_module(sys.argv[1])
globals().update(parameters.__dict__)

#This function calculates drainage area and flow discharge.

def f_discharge(discharge,area,direction,precipitation,incision,diffusion,lateral_incision):
        for x in xrange(x_lower,x_upper):
                for y in xrange(y_lower,y_upper):
                        xloc = x
                        yloc = y
                        area[xloc][yloc] += dx * dy
                        discharge[xloc][yloc] += precipitation[x][y] * dx * dy
                        bingo = 0
                        while bingo ==0:
                                i=direction[xloc][yloc]
                                if yloc == cellsy and BC[0] == 1:
                                        bingo = 1
                                elif yloc == 1 and BC[1] == 1:
                                        bingo = 1
                                elif xloc == 1 and BC[2] == 1:
                                        bingo = 1
                                elif xloc == cellsx and BC[3] == 1:
                                        bingo = 1
                                elif i == -9999:
                                        bingo = 1
                                else:
                                        xloc = xloc + xn[i]
                                        yloc = yloc + yn[i]
                                        if BC[0] == 2 and BC[1] == 2:
                                                if yloc == cellsy+1:
                                                        yloc = 1
                                                elif yloc == 0:
                                                        yloc = cellsy
                                        elif BC[2] == 2 and BC[3] == 2:
                                                if xloc == cellsx+1:
                                                        xloc = 1
                                                elif xloc == 0:
                                                        xloc = cellsx
                                        area[xloc][yloc] += dx * dy
                                        discharge[xloc][yloc] += precipitation[x][y] * dx * dy
        return discharge, area

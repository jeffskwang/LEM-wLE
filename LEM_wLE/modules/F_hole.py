import importlib
import sys
parameters = importlib.import_module(sys.argv[1])
globals().update(parameters.__dict__)

#This function creates a temporary landscape where holes are filled.

def f_hole(eta_old,eta_ghost,direction):
        #based on Planchon and Darboux 2001
        #stage 1
        for x in xrange(0,cellsx+2):
		for y in xrange(0,cellsy+2):
                        eta_ghost[x][y] = eta_old[x][y]
	for x in xrange(x_lower,x_upper):
		for y in xrange(y_lower,y_upper):
                        eta_ghost[x][y] = 1. * 10. ** (20.)
        
        #stage 2
        epsilon = dx * hole_adjustment
        bingo = 0
        go = 0
        while bingo == 0:
                bingo = 1
                for y in xrange(y_lower,y_upper):
                        for x in xrange(x_lower,x_upper):
                                if eta_ghost[x][y] > eta_old[x][y]:
                                        for i in xrange (0,8):
                                                x_ghost = x+xn[i]
                                                y_ghost = y+yn[i]
                                                if BC[0] == 2 and BC[1] == 2 and y_ghost == cellsy + 1:
                                                    y_ghost  = 1
                                                if BC[0] == 2 and BC[1] == 2 and y_ghost == 0:
                                                    y_ghost  = cellsy
                                                if BC[2] == 2 and BC[3] == 2 and x_ghost == cellsx + 1:
                                                    x_ghost  = 1
                                                if BC[2] == 2 and BC[3] == 2 and x_ghost == 0:
                                                    x_ghost  = cellsx
                                                if eta_old[x][y] >= eta_ghost[x_ghost][y_ghost] + epsilon:
                                                        bingo = 2
                                        if bingo == 1:
                                                for i in xrange (0,8):
                                                        x_ghost = x+xn[i]
                                                        y_ghost = y+yn[i]
                                                        if BC[0] == 2 and BC[1] == 2 and y_ghost == cellsy + 1:
                                                            y_ghost  = 1
                                                        if BC[0] == 2 and BC[1] == 2 and y_ghost == 0:
                                                            y_ghost  = cellsy
                                                        if BC[2] == 2 and BC[3] == 2 and x_ghost == cellsx + 1:
                                                            x_ghost  = 1
                                                        if BC[2] == 2 and BC[3] == 2 and x_ghost == 0:
                                                            x_ghost  = cellsx
                                                        if eta_ghost[x][y] > eta_ghost[x_ghost][y_ghost] + epsilon:
                                                                eta_ghost[x][y] = eta_ghost[x_ghost][y_ghost] + epsilon
                                                                bingo = 0
                                        elif bingo == 2:
                                                eta_ghost[x][y] = eta_old[x][y]
                                                go += 1
                                                break
                        if bingo == 2:
                                break
                if bingo == 2:
                        bingo = 0
        
	return eta_ghost

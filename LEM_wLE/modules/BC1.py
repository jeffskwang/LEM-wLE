import importlib
import sys
parameters = importlib.import_module(sys.argv[1])
globals().update(parameters.__dict__)

#The boundary condition function handles three boundary condition types on each of the four sides.
#BC = 0: represents a wall boundary, where flow cannot cross.
#BC = 1: represents an outlet boundary, where flow leaves the domain.
#BC = 2: represents a periodic boundary, where flow leaving the left enters the right and where flow leaving the bottom enters the top, and vice versa.

def f_bc1(eta,direction):
        for i in xrange(0,4):
                if BC[i] == 0:
                        if i == 0:
                                for x in xrange(0,cellsx+2):
                                        eta[x][-1] = 1. * 10. ** (20.)
                        elif i == 1:
                                for x in xrange(0,cellsx+2):
                                        eta[x][0] = 1. * 10. ** (20.)
                        elif i == 2:
                                for y in xrange(0,cellsy+2):
                                        eta[0][y] =1. * 10. ** (20.)
                        elif i == 3:
                                for y in xrange(0,cellsy+2):
                                        eta[-1][y] = 1. * 10. ** (20.)
                if BC[i] == 1:
                        if i == 0:
                                for x in xrange(2,cellsx):
                                        direction[x][-2] = 1
                                direction[1][-2] = 0
                                direction[-2][-2] = 2
                        elif i == 1:
                                for x in xrange(2,cellsx):
                                        direction[x][1] = 6
                                direction[1][1] = 5
                                direction[-2][1] = 7
                        elif i == 2:
                                for y in xrange(2,cellsy):
                                        direction[1][y] = 3
                                direction[1][1] = 5
                                direction[1][-2] = 0
                        elif i == 3:
                                for y in xrange(2,cellsy):
                                        direction[-2][y] = 4
                                direction[-2][1] = 7
                                direction[-2][-2] = 2
                elif BC[i] == 2:
                        if i == 0:
                                for x in xrange(0,cellsx+2):
                                        eta[x][-1] = eta[x][1]
                        elif i == 1:
                                for x in xrange(0,cellsx+2):
                                        eta[x][0] = eta[x][-2]
                        elif i == 2:
                                for y in xrange(0,cellsy+2):
                                        eta[0][y] = eta[-2][y]
                        elif i == 3:
                                for y in xrange(0,cellsy+2):
                                        eta[-1][y] = eta[1][y]
                
	return eta,direction

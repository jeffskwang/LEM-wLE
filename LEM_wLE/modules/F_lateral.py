import importlib
import sys
import random
parameters = importlib.import_module(sys.argv[1])
globals().update(parameters.__dict__)

#These functions implement Langston and Tucker (2018) lateral incision algorithm.

#   o  | o  | x1
# --------------
#   o  | x2 | o
# --------------
# xlat | x3 | o


def direction_single(x_in,y_in,d_in):
        proceed = 1
        x_out, y_out = -9999, -9999
        if y_in == cellsy and BC[0] == 1:
                proceed = 0
        elif y_in == 1 and BC[1] == 1:
                proceed = 0
        elif x_in == 1 and BC[2] == 1:
                proceed = 0
        elif x_in == cellsx and BC[3] == 1:
                proceed = 0
        elif d_in == -9999:
                proceed = 0
        else:
                x_out = x_in + xn[d_in]
                y_out = y_in + yn[d_in]    
                if BC[0] == 2 and BC[1] == 2:
                        if y_out == cellsy+1:
                                y_out = 1
                        elif y_out == 0:
                                y_out = cellsy
                elif BC[2] == 2 and BC[3] == 2:
                        if x_out == cellsx+1:
                                x_out = 1
                        elif x_out == 0:
                                x_out = cellsx
        return x_out, y_out, proceed

def f_lateral(discharge,lateral_incision,lateral_incision_cumulative,area,slope,direction,lateral_incision_threshold_total,lateral_discharge,eta_old,eta_new):
        for x in xrange(x_lower,x_upper):
                for y in xrange(y_lower,y_upper):
                        lateral_incision[x][y] = 0.0
        
        for x in xrange(x_lower,x_upper):
                for y in xrange(y_lower,y_upper):
                        d_in_max = - 9999
                        discharge_in_max = 0.0
                        for i in xrange (0,8):
                                x_in_max,y_in_max,proceed = direction_single(x,y,i)
                                if proceed == 1 and direction[x_in_max][y_in_max] == dop[i]:#checks that neighbor node flows into primary node
                                        if discharge_in_max < discharge[x_in_max][y_in_max]:
                                                discharge_in_max = discharge[x_in_max][y_in_max]
                                                d_in_max = dop[i]
                                        elif discharge_in_max == discharge[x_in_max][y_in_max]: #if there are two incoming discharges that are the same, choose one randomly
                                                if random.random() < 0.5:
                                                        d_in_max = dop[i]

                        if d_in_max != - 9999:
                                x_out,y_out,proceed = direction_single(x,y,direction[x][y])
                                if proceed == 1:
                                        curve = str(d_in_max) + str(direction[x][y])
                                        if curve in lateral_nodes:
                                                lateral_node_direction = lateral_nodes[curve][int(0.5 + random.random())]
                                                xlat,ylat,proceed = direction_single(x,y,lateral_node_direction)
                                                if proceed == 1 and eta_old[xlat][ylat] > eta_old[x][y]:
                                                        flow_depth = discharge_constant * discharge[x][y] ** discharge_exponent
                                                        inverse_radius_curvature = lateral_nodes[curve][2]
                                                        if discharge[x][y] < lateral_discharge[xlat][ylat]:
                                                                lateral_discharge[xlat][ylat] = discharge[x][y]
                                                                lateral_incision_threshold_total[xlat][ylat] = (eta_old[xlat][ylat] - eta_old[x_out][y_out]) * dx * dy
                                                        lateral_incision[xlat][ylat] += Kl *(area[x][y]**m_l)*(slope[x][y]**n_l) * inverse_radius_curvature * (flow_depth * dx)
                                                        lateral_incision_cumulative[xlat][ylat] +=  dt * Kl *(area[x][y]**m_l)*(slope[x][y]**n_l) * inverse_radius_curvature * (flow_depth * dx)

#if the cumulative lateral incision >= the amount needs to remove the lateral cell, incision occurs                                                        
        for x in xrange(x_lower,x_upper):
                for y in xrange(y_lower,y_upper):
                        if lateral_incision_cumulative[x][y] > 0.0:
                                if lateral_incision_cumulative[x][y] > lateral_incision_threshold_total[x][y]:
                                        eta_new[x][y] -= lateral_incision_threshold_total[x][y] / dx / dy
                                        lateral_incision_cumulative[x][y] = 0.0
                                
        return lateral_incision,lateral_incision_cumulative,lateral_incision_threshold_total,lateral_discharge,eta_new

import numpy as np
from scipy.optimize import linprog
from math import ceil

class MainSolver:
    def __init__(self,
                 route_len, number_of_vehicles, passenger_capacity, route_time,
                 first_guard, guard_duration, number_of_guards,
                 area_population, area_square):
        self.route_len = route_len
        self.number_of_vehicles = number_of_vehicles
        self.passenger_capacity = passenger_capacity
        self.route_time = route_time
        self.first_guard = first_guard
        self.guard_duration = guard_duration
        self.number_of_guards = number_of_guards
        self.density = area_population/area_square

    def time_converter(self, unformatted_time):
        hours = int(unformatted_time[:-3])
        minutes = int(unformatted_time[-2:])
        return hours*60 + minutes

    def A(self, Qmax, to, q, L):
        print("Qmax: ", Qmax)
        return ceil(Qmax*to*L/L/q/2)

    def time_intervals(self, first_g, duration, num):
        first_g = self.time_converter(first_g)
        output_time_intervals = [first_g]
        for i in range(num-1):
            output_time_intervals.append(output_time_intervals[i] + duration*60/2)
        return output_time_intervals

    def minimization_bounds(self, time_intervals_list, population_density, to, q, L):
        peak_hours = [7*60, 8*60, 9*60, 17*60, 18*60, 19*60]
        output_minimization_bounds = []
        for i in time_intervals_list:
            if i < peak_hours[0]-30:
                output_minimization_bounds.append(self.A(ceil(population_density/8), to, q, L))
            elif i >= peak_hours[0]-30 and i < peak_hours[1]-30:
                output_minimization_bounds.append(self.A(ceil(population_density/2), to, q, L))
            elif i >= peak_hours[1]-30 and i < peak_hours[2]-30:
                output_minimization_bounds.append(self.A(ceil(population_density*3/4), to, q, L))
            elif i >= peak_hours[2]-30 and i < peak_hours[3]-30:
                output_minimization_bounds.append(self.A(ceil(population_density/3), to, q, L))
            elif i >= peak_hours[3]-30 and i < peak_hours[4]-30:
                output_minimization_bounds.append(self.A(ceil(population_density*3/4), to, q, L))
            elif i >= peak_hours[4]-30 and i <= peak_hours[5]:
                output_minimization_bounds.append(self.A(ceil(population_density/2), to, q, L))
            elif i > peak_hours[5] and i < 23*60:
                output_minimization_bounds.append(self.A(ceil(population_density/4), to, q, L))
        return output_minimization_bounds

    def optimization_task(self):
        DepartHours = self.time_intervals(self.first_guard, self.guard_duration, self.number_of_guards)
        bounds = self.minimization_bounds(DepartHours,
                                          self.density,
                                          self.time_converter(self.route_time)/60,
                                          self.passenger_capacity,
                                          self.route_len)
        c = [1 for ci in range(len(DepartHours))]
        A = [[] for ai in range(len(DepartHours))]
        counter = 0
        for i in range(len(DepartHours)):
            A[i] = [0 for z in range(len(DepartHours))]
            while counter < len(DepartHours):
                A[i][counter] = 1
                A[i][counter - 1] = 1
                break
            counter += 1
        print('DepartHours:', DepartHours)
        print('c:', c)
        print('A:', A)
        print('bounds:', bounds)
        c = np.array(c)
        A_ub = -np.array(A)
        b_ub = -np.array(bounds)
        solution = linprog(c, A_ub=A_ub, b_ub=b_ub, method='simplex')
        print(solution)
        return ["%d:%02d" % (int(i/60), i%60) for i in DepartHours], \
               abs(ceil(solution['fun'])), \
               solution['status'], \
               [ceil(abs(i)) for i in solution['x']], \
               self.number_of_vehicles > abs(ceil(solution['fun']))
    """A = [[1, 0, 0, 0, 0, 1], [1, 1, 0, 0, 0, 0], [0, 1, 1, 0, 0, 0], [0, 0, 1, 1, 0, 0], [0, 0, 0, 1, 1, 0], [0, 0, 0, 0, 1, 1]]
        b = [4, 8, 10, 7, 12, 4]
        c = np.array([1,1,1,1,1,1])
        A_ub = -np.array(A)
        b_ub = -np.array(b)
        print("b_ub:", b_ub)
        solution = linprog(c, A_ub=A_ub, b_ub=b_ub, method='simplex')"""









import numpy as np
import math
import sys
import time

class SAnnealing(object):

    def __init__(self, domain, step = 1, final_temperature=0.1, temperature = 100, alpha=0.95, equilibrium=10, time = 0):
        self.domain = domain
        self.step = step
        self.temperature = temperature
        self.final_temperature = final_temperature
        self.alpha = alpha
        self.equilibrium = equilibrium
        self.time = time


    def cost_function(self, f, x):
        return f(x)


    def create_first_solution(self):
        #return np.array([float(np.random.randint(self.domain[i][0], self.domain[i][1])) for i in range(len(self.domain))])
         return np.array([1, 0, 0, 1, 1])


    def create_neighbor_solution(self, actual_solution, epoch):
        neighbor = actual_solution.copy()
        idx = np.random.randint(5)
        if neighbor[idx] == 0:
            neighbor[idx] = 1
        else:
            neighbor[idx] = 0
        return neighbor


    def aceptance_probability(self, deltaE, temperature):
        try:
            r = math.exp(-deltaE/temperature)
        except OverflowError:
            r = float("inf") 
        return r


    def update_temperature(self, temperature):
        return self.alpha * temperature


    def fit(self, objetive):
        self.cost_ = []
        actual_solution = self.create_first_solution()
        best_solution = actual_solution.copy()
        epoch = 0
        number_tested_solution = 0
        aceptanced = 100
        while (self.temperature > self.final_temperature):
            
            number_worst_solution_acepted = 0
            i = 0
            while (i < self.equilibrium):
                random_solution = self.create_neighbor_solution(actual_solution, epoch)
                number_tested_solution += 1
                delta_E = self.cost_function(objetive, random_solution)[1] - self.cost_function(objetive, actual_solution)[1]
                #print(f'Valor deltaE = {delta_E}')
                if delta_E > 0:
                    actual_solution = random_solution.copy()
                    #print("Solución vecina aceptada por mejora")
                else:
                    #print("Solución veicina no aceptada... genearar probabilidad")
                    deg_deltaE = self.aceptance_probability(-delta_E, self.temperature)
                    if(np.random.uniform(0, 1) < deg_deltaE):
                        actual_solution = random_solution.copy()
                        number_worst_solution_acepted += 1
                        #print("La solución vecina fue aceptada por probabilidad")
                x, y = self.cost_function(objetive, actual_solution)
                self.cost_.append((x,y))
                epoch_strlen = len(str(epoch))
                sys.stderr.write('\r%0*d Epoch | Equilibrium %d | Temperature %.2f '
                                '| Actual solution %.2f | Cost function: %.2f | Aceptance : %.2f' 
                        %
                        (epoch_strlen, epoch+1, i+1, self.temperature, 
                        x, y, aceptanced ))
                time.sleep(self.time)
                sys.stderr.flush()
                i += 1
                epoch += 1
                #actualizar best_solution
            #print("Punto de equilibrio alcanzado..")
            aceptanced = number_worst_solution_acepted * 100 /number_tested_solution
            self.temperature = self.update_temperature(self.temperature)
            #print(f"Temperatura actualizada: {temperature}")
            
        
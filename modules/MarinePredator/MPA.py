import numpy as np
from scipy.special import gamma
from numpy import random
from numpy.lib.function_base import percentile

class MPA:
    """Implements Marine Predators Algorithm

    Args:
        agentsCount (int): number of search agents
        maxItr (int): maximum number of iteratios
        lb (List[float]): lower bounds of all variables
        ub (List[float]): upper bounds of all variables
        dim (int): number of variables
        func (function pointer): fitness function name

    Methods:
        initialize(): Initializes the variables for simulation
        run(): Run Simulation
    """
    def __init__(self, agentsCount, maxItr, lb, ub, dim, func):
        self.search_agents_no   = agentsCount
        self.maxItr             = maxItr
        self.lb                 = lb
        self.ub                 = ub
        self.dim                = dim
        self.func               = func

    def initialize(self):
        # Initialize variables for one run
        self.Top_predator_pos = np.zeros((1, self.dim))
        self.Top_predator_fit = np.inf

        self.convergence_curve = []
        self.step_size = np.zeros((self.search_agents_no, self.dim))
        self.fitness = np.full((self.search_agents_no, 1), np.inf)

        self.__init_positions()

        self.Xmin = np.ones((self.search_agents_no, self.dim)) * self.lb
        self.Xmax = np.ones((self.search_agents_no, self.dim)) * self.ub

    def __init_positions(self):
        # initialize positions of preys
        self.Prey = np.empty((self.search_agents_no, self.dim))
        for i in range(self.dim):
            self.Prey[:, i] = np.random.rand(self.search_agents_no)*(self.ub[i]-self.lb[i]) + self.lb[i]

    def get_fitness(self, vals):
        return self.func(*tuple(np.split(vals, self.dim, 0)))
    
    def run(self):
        # It will act as a memory for previously used parameters
        self.memory = {}

        #Initialize
        self.initialize()

        iter = 0
        FADs = 0.2
        P = 0.5

        while iter < self.maxItr:

            #------------------ Detecting Top Predator ----------------------
            for i in range(self.Prey.shape[0]):
                Flag4ub = self.Prey[i, :] > self.ub
                Flag4lb = self.Prey[i, :] < self.lb
                self.Prey[i,:] = (self.Prey[i, :] * (~(Flag4ub + Flag4lb))) + self.ub * Flag4ub + self.lb * Flag4lb;                    
        
                self.fitness[i] = self.get_fitness(self.Prey[i, :])
                                
                if self.fitness[i] < self.Top_predator_fit:
                    self.Top_predator_fit = self.fitness[i]
                    self.Top_predator_pos = self.Prey[i,:]

            # -------------------Marine Memory Saving ------------------------
            if iter == 0:
                fit_old = self.fitness
                Prey_old = self.Prey
            
            Inx = (fit_old < self.fitness)
            Indx = np.tile(Inx, (1, self.dim))

            # Set fitness of previous iteration, if it was better
            print(self.fitness)
            self.Prey = Indx*Prey_old + (~Indx)*self.Prey
            self.fitness = Inx*fit_old + (~Inx)*self.fitness

            print(self.fitness)
            fit_old = self.fitness
            Prey_old = self.Prey

            #-----------------------------------------------------------------

            Elite = np.tile(self.Top_predator_pos,(self.search_agents_no,1)) 
            CF = (1 - iter/self.maxItr)** (2*iter/self.maxItr)

            RL = 0.05 * self.levy(self.search_agents_no, self.dim, 1.5)   #Levy random number vector
            RB = np.random.randn(self.search_agents_no, self.dim)          #Brownian random number vector
                    
            for i in range (self.Prey.shape[0]):
                for j in range(self.Prey.shape[1]):        
                    R = np.random.rand()
                    #------------------ Phase 1 (Eq.12) ------------------- 
                    if iter<self.maxItr/3:
                        self.step_size[i,j] = RB[i,j] * (Elite[i,j]-RB[i,j]*self.Prey[i,j])                
                        self.Prey[i,j] = self.Prey[i,j] + P * R * self.step_size[i,j]
                            
                    #--------------- Phase 2 (Eqs. 13 & 14)----------------
                    elif iter>self.maxItr/3 and iter < 2*self.maxItr/3:
                        
                        if i > self.Prey.shape[0] / 2:
                            self.step_size[i,j] = RB[i,j] * (RB[i,j] * Elite[i,j] - self.Prey[i,j])
                            self.Prey[i,j] = Elite[i,j] + P*CF*self.step_size[i,j] 
                        else:
                            self.step_size[i,j] = RL[i,j] * (Elite[i,j] - RL[i,j] * self.Prey[i,j])                     
                            self.Prey[i,j] = self.Prey[i,j] + P * R * self.step_size[i,j]
                    
                    #----------------- Phase 3 (Eq. 15)-------------------
                    else:
                        self.step_size[i,j] = RL[i,j] * (RL[i,j] * Elite[i,j] - self.Prey[i,j]) 
                        self.Prey[i,j] = Elite[i,j] + P*CF*self.step_size[i,j]

            
            #------------------ Detecting top predator ------------------        
            for i in range(self.Prey.shape[0]):
                Flag4ub = self.Prey[i,:] > self.ub
                Flag4lb = self.Prey[i,:] < self.lb
                self.Prey[i,:] = (self.Prey[i,:]*(~(Flag4ub+Flag4lb))) + self.ub*Flag4ub + self.lb*Flag4lb
            
                self.fitness[i] = self.get_fitness(self.Prey[i,:])
                    
                if self.fitness[i] < self.Top_predator_fit:
                    self.Top_predator_fit = self.fitness[i]
                    self.Top_predator_pos = self.Prey[i,:]

            # -------------------Marine Memory Saving ------------------------
            if iter == 0:
                fit_old = self.fitness
                Prey_old = self.Prey
            
            Inx = (fit_old < self.fitness)
            Indx = np.tile(Inx, (1, self.dim))

            # Set fitness of previous iteration, if it was better
            self.Prey = Indx*Prey_old + (~Indx)*self.Prey
            self.fitness = Inx*fit_old + (~Inx)*self.fitness

            fit_old = self.fitness
            Prey_old = self.Prey

            #---------- Eddy formation and FADs effect (Eq 16) ----------- 
                                        
            if np.random.rand() < FADs:
                U = np.random.rand(self.search_agents_no,self.dim) < FADs                                                                                              
                self.Prey = self.Prey + CF*((self.Xmin+np.random.rand(self.search_agents_no, self.dim) *(self.Xmax - self.Xmin)) *U)

            else:
                r = np.random.rand()  
                Rs = self.Prey.shape[0]
                self.step_size = (FADs * (1-r)+r) * (self.Prey [np.random.permutation(Rs), : ]- self.Prey[np.random.permutation(Rs),:])
                self.Prey = self.Prey + self.step_size

            iter=iter+1 
            self.convergence_curve.append(self.Top_predator_fit)

    def levy(self, n, m, beta):
        num = gamma(1+beta) * np.sin(np.pi * beta/2)
    
        den = gamma((1+beta)/2)*beta*2 ** ((beta-1)/2)

        sigma_u = (num/den)**(1/beta)

        u = np.random.normal(0,sigma_u,(n,m))
        
        v = np.random.normal(0,1,(n,m))

        z = u / (abs(v)**(1/beta))

        return z
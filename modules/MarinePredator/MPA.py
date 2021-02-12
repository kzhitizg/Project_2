import numpy as np

class MPA:
    def __init__(self, agentsCount, maxItr, lb, ub, dim, func):
        """Implements Marine Predators Algorithm

        Args:
            agentsCount (int): number of search agents
            maxItr (int): maximum number of iteratios
            lb (List[float]): lower bounds of all variables
            ub (List[float]): upper bounds of all variables
            dim (int): number of variables
            func (function pointer): fitness function name
        """
        self.search_agents_no   = agentsCount
        self.maxItr             = maxItr
        self.lb                 = lb
        self.ub                 = ub
        self.dim                = dim
        self.func               = func

    def initialize(self):
        # Initialize variables for one run
        self.top_predator_pos = np.zeros((1, self.dim))
        self.top_predator_fit = np.inf

        self.convergence_curve = []
        self.step_size = np.zeros((self.search_agents_no, self.maxItr))
        self.fitness = np.full((self.search_agents_no), np.inf)

        self.init_positions()

        self.Xmin = np.ones(self.search_agents_no, self.dim) @ self.lb
        self.Xmax = np.ones(self.search_agents_no, self.dim) @ self.ub

    def init_positions(self):
        # initialize positions of preys
        self.Prey = np.empty((self.search_agents_no, self.dim))
        for i in range(self.dim):
            self.Prey[:, i] = np.random.rand(self.search_agents_no, 1)*(self.ub[i]-self.lb[i]) + self.lb[i]

    def run(self):
        # It will act as a memory for previously used parameters
        self.memory = {}

        #Initialize
        self.initialize()
        self.init_positions()

        iter = 0
        FADs = 0.2
        P = 0.5

        while iter < self.maxItr:

            #------------------ Detecting Top Predator ----------------------
            for i in range(self.Prey.shape[0]):
                Flag4ub = self.Prey[i, :] > self.ub
                Flag4lb = self.Prey[i, :] < self.lb
                self.Prey[i,:] = (self.Prey[i, :] * (~(Flag4ub + Flag4lb))) + self.ub * Flag4ub + self.lb * Flag4lb;                    
        
                self.fitness[i,1] = self.func(self.Prey[i,:])
                                
                if self.fitness[i,1] < self.Top_predator_fit:
                    self.Top_predator_fit = self.fitness[i,1]
                    self.Top_predator_pos = self.Prey[i,:]

            # -------------------Marine Memory Saving ------------------------
            if iter == 0:
                fit_old = self.fitness
                Prey_old = self.Prey
            
            Inx = (fit_old < self.fitness)
            
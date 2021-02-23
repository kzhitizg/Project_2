import numpy as np
from scipy.special import gamma
from numpy import random
from numpy.lib.function_base import percentile
import logging
import matplotlib.pyplot as plt
import pickle


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

    @staticmethod
    def load_mpa(file_name):
        f = open(file_name, "rb")
        m = pickle.load(f)
        f.close()
        return m

    def __init__(self, agentsCount, maxItr, lb, ub, dim, func):
        self.search_agents_no = agentsCount
        self.maxItr = maxItr
        self.lb = lb
        self.ub = ub
        self.dim = dim
        self.func = func

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

        self.curr_itr = 0
        self.FADs = 0.2
        self.P = 0.5

        # It will act as a memory for previously used parameters
        self.memory = {}

    def save_mpa(self, file_name):
        f = open(file_name, "wb")
        pickle.dump(self, f)
        f.close()

    def __init_positions(self):
        # initialize positions of preys
        self.Prey = np.empty((self.search_agents_no, self.dim))
        for i in range(self.dim):
            self.Prey[:, i] = np.random.rand(
                self.search_agents_no)*(self.ub[i]-self.lb[i]) + self.lb[i]

    # func to write to the file
    def file_write(self, msg):
        file = open(
            "/content/drive/My Drive/8thSem/BTP_Metaheuristic/scripts/Abhishek/checkpoints/out.txt", "a")
        file.write(msg)
        file.close()

    def get_fitness(self, vals):
        vals = tuple(map(float, np.split(vals, self.dim, 0)))
        self.file_write("Pos {}\n".format(str(vals)))
        if vals in self.memory.keys():
            return self.memory[vals]
        else:
            fit = self.func(*vals)
            self.memory[vals] = fit
            return fit

    def levy(self, n, m, beta):
        num = gamma(1+beta) * np.sin(np.pi * beta/2)

        den = gamma((1+beta)/2)*beta*2 ** ((beta-1)/2)

        sigma_u = (num/den)**(1/beta)

        u = np.random.normal(0, sigma_u, (n, m))

        v = np.random.normal(0, 1, (n, m))

        z = u / (abs(v)**(1/beta))

        return z

    def run_once(self):
        if self.curr_itr < self.maxItr:

            # ------------------ Detecting Top Predator ----------------------
            for i in range(self.Prey.shape[0]):
                Flag4ub = self.Prey[i, :] > self.ub
                Flag4lb = self.Prey[i, :] < self.lb
                self.Prey[i, :] = (
                    self.Prey[i, :] * (~(Flag4ub + Flag4lb))) + self.ub * Flag4ub + self.lb * Flag4lb

                self.fitness[i] = self.get_fitness(self.Prey[i, :])
                self.file_write("Fitness of {} individual {}\n".format(
                    i, self.fitness[i]))

                if self.fitness[i] < self.Top_predator_fit:
                    self.Top_predator_fit = self.fitness[i]
                    self.Top_predator_pos = self.Prey[i, :]

            # -------------------Marine Memory Saving ------------------------
            if self.curr_itr == 0:
                self.fit_old = self.fitness
                self.Prey_old = self.Prey

            Inx = (self.fit_old < self.fitness)
            Indx = np.tile(Inx, (1, self.dim))

            # Set fitness of previous iteration, if it was better
            self.Prey = Indx*self.Prey_old + (~Indx)*self.Prey
            self.fitness = Inx*self.fit_old + (~Inx)*self.fitness

            self.fit_old = self.fitness
            self.Prey_old = self.Prey

            # -----------------------------------------------------------------

            Elite = np.tile(self.Top_predator_pos, (self.search_agents_no, 1))
            CF = (1 - self.curr_itr/self.maxItr) ** (2*self.curr_itr/self.maxItr)

            # Levy random number vector
            RL = 0.05 * self.levy(self.search_agents_no, self.dim, 1.5)
            # Brownian random number vector
            RB = np.random.randn(self.search_agents_no, self.dim)

            for i in range(self.Prey.shape[0]):
                for j in range(self.Prey.shape[1]):
                    R = np.random.rand()
                    # ------------------ Phase 1 (Eq.12) -------------------
                    if self.curr_itr < self.maxItr/3:
                        self.step_size[i, j] = RB[i, j] * \
                            (Elite[i, j]-RB[i, j]*self.Prey[i, j])
                        self.Prey[i, j] = self.Prey[i, j] + \
                            self.P * R * self.step_size[i, j]

                    # --------------- Phase 2 (Eqs. 13 & 14)----------------
                    elif self.curr_itr > self.maxItr/3 and self.curr_itr < 2*self.maxItr/3:

                        if i > self.Prey.shape[0] / 2:
                            self.step_size[i, j] = RB[i, j] * \
                                (RB[i, j] * Elite[i, j] - self.Prey[i, j])
                            self.Prey[i, j] = Elite[i, j] + \
                                self.P*CF*self.step_size[i, j]
                        else:
                            self.step_size[i, j] = RL[i, j] * \
                                (Elite[i, j] - RL[i, j] * self.Prey[i, j])
                            self.Prey[i, j] = self.Prey[i, j] + \
                                self.P * R * self.step_size[i, j]

                    # ----------------- Phase 3 (Eq. 15)-------------------
                    else:
                        self.step_size[i, j] = RL[i, j] * \
                            (RL[i, j] * Elite[i, j] - self.Prey[i, j])
                        self.Prey[i, j] = Elite[i, j] + \
                            self.P*CF*self.step_size[i, j]

            # ------------------ Detecting top predator ------------------
            for i in range(self.Prey.shape[0]):
                Flag4ub = self.Prey[i, :] > self.ub
                Flag4lb = self.Prey[i, :] < self.lb
                self.Prey[i, :] = (
                    self.Prey[i, :]*(~(Flag4ub+Flag4lb))) + self.ub*Flag4ub + self.lb*Flag4lb

                self.fitness[i] = self.get_fitness(self.Prey[i, :])
                self.file_write("Fitness of {} individual {} round 2\n".format(
                    i, self.fitness[i]))

                if self.fitness[i] < self.Top_predator_fit:
                    self.Top_predator_fit = self.fitness[i]
                    self.Top_predator_pos = self.Prey[i, :]

            # -------------------Marine Memory Saving ------------------------
            if self.curr_itr == 0:
                self.fit_old = self.fitness
                self.Prey_old = self.Prey

            Inx = (self.fit_old < self.fitness)
            Indx = np.tile(Inx, (1, self.dim))

            # Set fitness of previous iteration, if it was better
            self.Prey = Indx*self.Prey_old + (~Indx)*self.Prey
            self.fitness = Inx*self.fit_old + (~Inx)*self.fitness

            self.fit_old = self.fitness
            self.Prey_old = self.Prey

            # ---------- Eddy formation and FADs effect (Eq 16) -----------

            if np.random.rand() < self.FADs:
                U = np.random.rand(self.search_agents_no, self.dim) < self.FADs
                self.Prey = self.Prey + CF * \
                    ((self.Xmin+np.random.rand(self.search_agents_no,
                                               self.dim) * (self.Xmax - self.Xmin)) * U)

            else:
                r = np.random.rand()
                Rs = self.Prey.shape[0]
                self.step_size = (self.FADs * (1-r)+r) * (
                    self.Prey[np.random.permutation(Rs), :] - self.Prey[np.random.permutation(Rs), :])
                self.Prey = self.Prey + self.step_size

            self.curr_itr += 1
            self.convergence_curve.append(self.Top_predator_fit)
            self.file_write("Top Predator: {} and pos {}\n".format(
                self.Top_predator_fit, self.Top_predator_pos))
            print("Top Predator: {} and pos {}".format(
                self.Top_predator_fit, self.Top_predator_pos))
            plt.plot(self.convergence_curve)
            plt.show()
            return True

        else:
            print("Maximum iterations done")
            return False

    def iter_gen(self):
        # self.initialize()
        while self.curr_itr < self.maxItr:
            self.file_write(
                "--------------Iteration {}------------\n".format(self.curr_itr + 1))
            print("Iteration {}".format(self.curr_itr+1))
            yield self.run_once()

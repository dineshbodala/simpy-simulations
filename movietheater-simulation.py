#goal is to make the avg waiting period to 10 min or less

import simpy
import random
import statistics
env=simpy.Environment()

class Theater(object):

    def __init__(self, env) -> None:
        self.env=env
        self.cashier=simpy.Resource(env, num_cashiers)


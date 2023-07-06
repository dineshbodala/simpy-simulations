import simpy
import numpy as np

env=simpy.Environment()

def car(env):
    while True:
        print('Start Parking', env.now)
        yield env.timeout(5)

        print('Start Driving', env.now)
        yield env.timeout(2)



print(car(env))
env.process(car(env))
env.run(until=15)

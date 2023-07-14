import simpy
import random
import numpy as np

NUM_EMPLOYEES = 160
AVG_SUPPORT_TIME = 3
CUSTOMER_INTERVAL = 0.02
SIM_TIME = 60
customers_handled = 0

class Supermarket:
    def __init__(self, env, num_employees, support_time) -> None:
        self.env = env
        self.staff = simpy.Resource(env, num_employees)
        self.support_time = support_time

    def support(self, customer):
        yield self.env.timeout(self.support_time)
        print(f"Support finished for {customer} at {self.env.now:.2f}")


def worker(env, name, supermarket):
    while True:
        print(f"Worker {name} starts work at {env.now:.2f}")
        with supermarket.staff.request() as request:
            yield request
            print(f"Worker {name} is assisting a customer at {env.now:.2f}")
            yield env.process(supermarket.support(name))
            print(f"Worker {name} finished assisting a customer at {env.now:.2f}")

        # Workers go on a break for 30 seconds every 0.5 seconds
        if env.now % 0.5 == 0:
            print(f"Worker {name} is on break at {env.now:.2f}")
            yield env.timeout(30)
            print(f"Worker {name} returns from break at {env.now:.2f}")


def customer(env, name, supermarket):
    global customers_handled
    print(f"Customer {name} enters the waiting queue at {env.now:.2f}!")
    with supermarket.staff.request() as request:
        yield request
        print(f"Customer {name} enters checkout at {env.now:.2f}")
        yield env.process(supermarket.support(name))
        print(f"Customer {name} left checkout at {env.now:.2f}")
        customers_handled += 1


def setup(env, num_employees, support_time, customer_interval):
    supermarket = Supermarket(env, num_employees, support_time)

    for i in range(1, 6):
        env.process(customer(env, i, supermarket))

    for i in range(num_employees):
        env.process(worker(env, i, supermarket))

    while True:
        yield env.timeout(customer_interval)
        i += 1
        env.process(customer(env, i, supermarket))


print('Starting supermarket simulation')
env = simpy.Environment()
env.process(setup(env, NUM_EMPLOYEES, AVG_SUPPORT_TIME, CUSTOMER_INTERVAL))
env.run(until=SIM_TIME)

print(customers_handled)
 
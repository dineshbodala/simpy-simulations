import simpy
import random
import numpy as np

NUM_EMPLOYEES = 2
AVG_SUPPORT_TIME = 5
CUSTOMER_INTERVAL = 2
SIM_TIME = 120
customers_handled = 0


class Supermarket:

    def __init__(self, env, num_employees, support_time) -> None:
        self.env = env
        self.staff = simpy.Resource(env, num_employees)
        self.support_time = support_time

    def support(self, customer):
        random_time = max(1, np.random.normal(self.support_time, 4))
        yield self.env.timeout(random_time)
        print(f"Support finished for {customer} at {self.env.now:.2f}")


def customer(env, name, supermarket):
    global customers_handled
    print(f"Customer {name} enters waiting queue at {env.now:.2f}!")
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

    while True:
        yield env.timeout(random.randint(customer_interval - 1, customer_interval + 1))
        i += 1
        env.process(customer(env, i, supermarket))


print('Starting supermarket simulation')
env = simpy.Environment()
env.process(setup(env, NUM_EMPLOYEES, AVG_SUPPORT_TIME, CUSTOMER_INTERVAL))
env.run(until=SIM_TIME)

print(customers_handled)

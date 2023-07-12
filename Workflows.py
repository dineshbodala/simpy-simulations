import simpy
import random

NUM_CUSTOMERS = 3000
AVG_SUPPORT_TIME = 1
CUSTOMER_INTERVAL = 0.02
SIM_TIME = 60
employees_needed = None


class Supermarket:

    def __init__(self, env, num_employees, support_time, break_time) -> None:
        self.env = env
        self.staff = simpy.Resource(env, num_employees)
        self.support_time = support_time
        self.break_time = break_time

    def support(self, customer):
        yield self.env.timeout(self.support_time)

    def employee_break(self):
        while True:
            yield self.env.timeout(1) 
            for _ in range(54):  
                yield self.env.timeout(0.5)  


def customer(env, name, supermarket):
    global customers_handled
    with supermarket.staff.request() as request:
        yield request
        yield env.process(supermarket.support(name))
        customers_handled += 1


def setup(env, num_employees, support_time, customer_interval):
    global customers_handled
    supermarket = Supermarket(env, num_employees, support_time, break_time=0.5)
    customers_handled = 0

    env.process(supermarket.employee_break())

    for i in range(1, NUM_CUSTOMERS + 1):
        env.process(customer(env, i, supermarket))

    while customers_handled < NUM_CUSTOMERS:
        yield env.timeout(customer_interval)
        i += 1
        env.process(customer(env, i, supermarket))

        if env.now >= SIM_TIME:
            break

    employees_needed = num_employees


print('Starting supermarket simulation')
for num_employees in range(1, NUM_CUSTOMERS + 1):
    env = simpy.Environment()
    env.process(setup(env, num_employees, AVG_SUPPORT_TIME, CUSTOMER_INTERVAL))
    env.run(until=SIM_TIME)

    if customers_handled >= NUM_CUSTOMERS:
        employees_needed = num_employees
        break

print(f"Minimum number of employees needed to process {NUM_CUSTOMERS} customers in one hour: {employees_needed}")

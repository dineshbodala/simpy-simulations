import simpy
env=simpy.Environment()

class Car(object):
    def __init__(self,env) -> None:
        self.env=env

        self.action=env.process(self.run())

    def run(self):

        while True:
            print('Start parking and charging at ', self.env.now)
            yield self.env.process(self.charge(5))

            print('start driving', self.env.now)
            yield self.env.timeout(2)

    def charge(self, duration):
    
        yield self.env.timeout(duration)

car=Car(env)
env.run(until=15)



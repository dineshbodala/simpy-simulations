
import simpy
env=simpy.Environment()

def driver(env, car):
    yield env.timeout(3)
    car.action.interrupt()
class Car(object):
    def __init__(self,env) -> None:
        self.env=env

        self.action=env.process(self.run())

    def run(self):

        while True:
            print('Start parking and charging at ', self.env.now)
            try:
                yield self.env.process(self.charge(5))
            except simpy.Interrupt:
                print('Battery is full enough')
            
            print('start driving', self.env.now)
            yield self.env.timeout(2)

    def charge(self, duration):
    
        yield self.env.timeout(duration)

car=Car(env)
env.process(driver(env, car))
env.run(until=15)

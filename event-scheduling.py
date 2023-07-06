
import numpy as np
class simulation:
    def __init__(self) -> None:
        self.num_in_system=0
        self.clock=0.0
        self.t_arrival=self.generate_interarrival()
        self.t_depparture=float('inf')
        self.num_arrivals=0
        self.num_departures=0.0
        self.total_wait=0.0

    def advance_time(self):
        t_event=min(self.t_arrival, self.t_depparture)
        self.total_wait=self.num_in_system*(t_event-self.clock)
        self.clock = t_event

        if self.t_arrival <= self.t_depparture:
             self.handle_arrival_event()
        else:
             self.handle_depart_event()
             
    
    def handle_arrival_event(self):
         self.num_in_system+=1
         self.num_arrivals+=1
         if self.num_in_system <=1:
              self.t_depparture= self.clock + self.generate_service()
         
         self.t_arrival=self.clock + self.generate_interarrival()
              
    def handle_depart_event(self):
         self.num_in_system-=1
         self.num_departures+=1
         if self.num_in_system>0:
              self.t_depparture=self.clock + self.generate_service()

         else:
              self.t_depparture=float('inf')
    
    def generate_interarrival(self):
         return np.random.exponential(1./3)
    
    def generate_service(self):
         return np.random.exponential(1./4)
    

np.random.seed(0)
s=simulation()
s.advance_time()
print(s.clock)
print(s.num_in_system)
print(s.t_depparture)
s.advance_time()
print(s.num_in_system)
print(s.total_wait)
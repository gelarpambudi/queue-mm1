import numpy as np
import pandas as pd
import argparse

class Simulation:
    def __init__(self, lam, miu):
        self.Lambda = lam                   #Arrival Rate
        self.miu = miu                      #Service Rate 
        self.clock=0.0                      #simulation clock
        self.num_arrivals=0                 #total number of arrivals
        self.t_arrival=self.gen_int_arr()   #time of next arrival
        self.t_departure1=float('inf')      #departure time from server 1
        self.dep_sum1=0                     #Sum of service times by server
        self.state_T1=0                     #current state of server1 (binary)
        self.total_wait_time=0.0            #total wait time
        self.num_in_q=0                     #current number in queue
        self.number_in_queue=0              #customers who had to wait in line(counter)
        self.num_of_departures1=0           #number of customers served by server
        self.lost_customers=0               #customers who left without service
        self.num_in_system=0                #number of customers inside the system
        

    def time_adv(self):                                                       
        t_next_event=min(self.t_arrival,self.t_departure1)  
        self.total_wait_time += (self.num_in_q*(t_next_event-self.clock))
        self.clock=t_next_event
                
        if self.t_arrival < self.t_departure1:
            self.arrival()
        else:
            self.server()

    def arrival(self):              
        self.num_arrivals += 1
        self.num_in_system += 1

        #schedule next departure or arrival depending on state of servers
        if self.num_in_q == 0:                                 
            if self.state_T1==1:
                self.num_in_q+=1
                self.number_in_queue+=1
                self.t_arrival=self.clock+self.gen_int_arr()
            elif self.state_T1==0:
                self.state_T1=1
                self.dep1= self.gen_service_time()
                self.dep_sum1 += self.dep1
                self.t_departure1=self.clock + self.dep1
                self.t_arrival=self.clock+self.gen_int_arr()

        #if queue length is less than 4 generate next arrival and make customer join queue
        elif self.num_in_q < 4 and self.num_in_q >= 1:       
            self.num_in_q+=1
            self.number_in_queue+=1                             
            self.t_arrival=self.clock + self.gen_int_arr()
        
        #if queue length is 4 equal prob to leave or stay
        elif self.num_in_q == 4:                             
            if np.random.choice([0,1])==0: 
                self.num_in_q+=1 
                self.number_in_queue+=1                 
                self.t_arrival=self.clock + self.gen_int_arr()
            else:
                self.lost_customers+=1

        #if queue length is more than 5 60% chance of leaving
        elif self.num_in_q >= 5:                            
            if np.random.choice([0,1],p=[0.4,0.6])==0:
                self.t_arrival=self.clock+self.gen_int_arr()
                self.num_in_q+=1 
                self.number_in_queue+=1 
            else:
                self.lost_customers+=1

    #departure
    def server(self):               
        self.num_of_departures1 += 1
        if self.num_in_q>0:
            self.dep1= self.gen_service_time()
            self.dep_sum1 += self.dep1
            self.t_departure1=self.clock + self.dep1
            self.num_in_q-=1
        else:
            self.t_departure1=float('inf') 
            self.state_T1=0

    #generate arrival time (rate = lamda)
    def gen_int_arr(self):                                             
        return (-np.log(1-(np.random.uniform(low=0.0,high=1.0))) * self.Lambda)
    
    #generate service time (rate = miu)
    def gen_service_time(self):                               
        return (-np.log(1-(np.random.uniform(low=0.0,high=1.0))) * self.miu)


def args_parser():
    parser = argparse.ArgumentParser(description="M/M/1 Queue Simulation")
    parser.add_argument("--num_experiment", help="Number of experiment", type=int, default=10)
    parser.add_argument("--out", help="output file (*.xlsx)", type=str, default='simulation-result.xlsx')
    parser.add_argument("--lamda", help="arrival rate", type=float, default=3)
    parser.add_argument("--miu", help="service rate", type=float, default=1.2)
    parser.add_argument("--duration", help="simulation duration (in minutes)", type=float, default=2)
    return parser.parse_args()



if __name__ == "__main__":
    args = args_parser()
    s = Simulation(lam=args.lamda, miu=args.miu)

    df=pd.DataFrame(columns=[
        'Average interarrival time',
        'Average service time',
        'Utilization',
        'People who had to wait in line',
        'Total average wait time',
        'Lost Customers'])

    for i in range(args.num_experiment):
        np.random.seed(i)
        s.__init__(lam=args.lamda, miu=args.miu)
        while s.clock <= args.duration :
            s.time_adv() 
        a=pd.Series([
            s.clock/s.num_arrivals,
            s.dep_sum1/s.num_of_departures1,
            s.dep_sum1/s.clock,
            s.number_in_queue,
            s.total_wait_time,
            s.lost_customers],
            index=df.columns)
        df=df.append(a,ignore_index=True)   
        
    df.to_excel(args.out)
    print("Simulation done")         
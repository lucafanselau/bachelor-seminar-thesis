from math import floor
from typing import Tuple
import simpy
from simpy.core import SimTime
import pandas as pd
import numpy as np

classes = ['L', 'M', 'S', 'XS']

def cost(c: str, t: float):
    s = 0
    b = 0
    match c:
        case "L":
            s = 0.34
            b = 0.99
        case "M":
            s = 0.31
            b = 0.99
        case "S":
            s = 0.28
        case "XS":
            s = 0.09
    
    return t * s + b


class Station:
    def __init__(self, env: simpy.Environment, name: str, area_data) -> None:
        self.env = env
        self.store = { c: 0 for c in classes}
        self.store_history = { c: np.array([[0, 0]]) for c in classes }
        self.name = name
        self.area_data = area_data

        self.history_df = None

    def __str__(self) -> str:
        return f"{self.name}: ${self.area_data}"

    def reduce_stock(self, c: str, t: SimTime):
        current = self.store[c]
        self.store_history[c] = np.append(self.store_history[c], [[t, current - 1]], axis=0)
        self.store[c] -= 1

    def increase_stock(self, c: str, t: SimTime):
        current = self.store[c]
        self.store_history[c] = np.append(self.store_history[c], [[t, current + 1]], axis=0)
        self.store[c] += 1

    def to_dataframes(self):
        def to_df(c: str): 
            d = self.store_history[c]
            tdf = pd.DataFrame(data=d, columns=["time", "amount"])
            tdf.set_index("time", inplace=True)
            return tdf
        self.history_df = { c: to_df(c) for c in classes }

# simulation_districts = ["Pankow", "Reinickendorf", "Friedrichshain-Kreuzberg", "Charlottenburg-Wilmersdorf"]

def order_independant_distance(a: Tuple[Station, Station]):
        match a:
            case (Station(name="Pankow"), Station(name="Reinickendorf")):
                return 9.08
            case (Station(name="Pankow"), Station(name="Friedrichshain-Kreuzberg")):
                return 9.38
            case (Station(name="Pankow"), Station(name="Charlottenburg-Wilmersdorf")):
                return 14.18
            case (Station(name="Reinickendorf"), Station(name="Friedrichshain-Kreuzberg")):
                return 12.39
            case (Station(name="Reinickendorf"), Station(name="Charlottenburg-Wilmersdorf")):
                return 8.46
            case (Station(name="Friedrichshain-Kreuzberg"), Station(name="Charlottenburg-Wilmersdorf")):
                return 10.05
        return None

def station_distance(start: Station, end: Station):
    t = (start, end)
    r_1 = order_independant_distance(t)
    if r_1 is not None:
        return r_1
    return order_independant_distance(t[::-1])

class Simulation:

    def __init__(self,station_data: pd.DataFrame, p: pd.Series, alpha: float, capacity: float, pred):
        env = simpy.Environment()# Create the stations
        self.stations = [Station(env, n, d) for (n, d) in station_data.iterrows()]
        self.p = p

        self.alpha = alpha
        self.capacity = capacity
        self.pred = pred

        self.unsatisfied = np.array([])
        self.satisfied = np.array([])
        self.pi = 0
        self.td = 0

        env.process(self.spawner(env))

        env.run(until=60 * 24)

        # After execution compute metrics
        for s in self.stations:
            s.to_dataframes()
        
        self.urr = self.unsatisfied.size / (self.unsatisfied.size + self.satisfied.size)
        
    def customer(self, env: simpy.Environment, start: Station, dest: Station):

        # - Distance
        # TODO: Maybe this should be controllable by the outside environment
        distance = station_distance(start, dest)
        if distance is None:
            print(f"{distance} from: {start.name} to: {dest.name}")
        # - Area data
        X = [distance, *start.area_data]
        
        probabilities = self.pred([X])[0]
        max_p = probabilities.max()

        # print(probabilities)

        # Calculate D'
        D = filter(lambda a: a[1] >= max_p - self.alpha, zip(classes, probabilities))
        D = filter(lambda a: start.store[a[0]]  > -self.capacity, D)

        D = list(D)
        # print(D)

        C = [a[0] for a in D]

        if len(C) == 0:
            self.unsatisfied = np.append(self.unsatisfied, [X])
            return

        # Select the actual vehicle
        c = np.random.choice(C)

        # Update start state
        start.reduce_stock(c, env.now)
        

        # Travel
        speed = 126.39280907696697 # in m/min
        t = (distance * 1000) / speed
        # print(f"decided on {c} traveling for {t}min")
        yield env.timeout(t)

        # Update end state
        dest.increase_stock(c, env.now)

        # Add to satisfied customers
        self.satisfied = np.append(self.satisfied, [X])
        # Increase total profit
        self.pi += cost(c, t)
        self.td += distance


    def spawner(self, env: simpy.Environment):
        while True:
            hour = floor(env.now / 60)
            period = self.p[hour]

            wait_for = period * 60
            yield env.timeout(wait_for)

            # WAAUW a new customer appears
            (start, destination) = np.random.choice(self.stations, size=2, replace=False)
            env.process(self.customer(env, start, destination))
            
    def print_metrics(self):
        print("URR: {:.2f}%".format(self.urr * 100))
        print("Profit: {:.3f}€".format(self.pi))
        print("Total distance driven: {:.3f}km".format(self.td))





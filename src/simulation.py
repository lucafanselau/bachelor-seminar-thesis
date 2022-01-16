from math import floor
import simpy
import pandas as pd

classes = ["XS", "S", "M", "L"]


class Station:
    def __init__(self, env: simpy.Environment, name: str, area_data) -> None:
        self.env = env
        self.store = { c: 0 for c in classes}
        self.name = name
        self.area_data = area_data

    def __str__(self) -> str:
        return f"{self.name}: ${self.area_data}"
        
def customer(env: simpy.Environment):
    while True:
        print(f"start parking at {env.now}")
        parking_duration = 5
        yield env.timeout(parking_duration)

        print("Start driving at %d" % env.now)
        trip_duration = 2
        yield env.timeout(trip_duration)


def spawner(env: simpy.Environment):
    while True:
        hour = floor(env.now / 60)
        


def setup(station_data: pd.DataFrame):
    env = simpy.Environment()
    
    # Create the stations
    stations = [Station(env, n, d) for (n, d) in station_data.iterrows()]

    env.process(spawner(env))

    # env.run(until=24 * 60)






import simpy

classes = ["XS", "S", "M", "L"]


class Station:

    def __init__(self, env: simpy.Environment) -> None:
        self.env = env
        self.store = { c: 0 for c in classes}

def customer(env: simpy.Environment):
    while True:
        print(f"start parking at {env.now}")
        parking_duration = 5
        yield env.timeout(parking_duration)

        print("Start driving at %d" % env.now)
        trip_duration = 2
        yield env.timeout(trip_duration)


def setup(env: simpy.Environment):
    # Create the stations

env = simpy.Environment()
env.process(setup(env))


env.run(until=24 * 60)

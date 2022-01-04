import simpy


def car(env: simpy.Environment):
    while True:
        print(f"start parking at {env.now}")
        parking_duration = 5
        yield env.timeout(parking_duration)

        print("Start driving at %d" % env.now)
        trip_duration = 2
        yield env.timeout(trip_duration)


env = simpy.Environment()
env.process(car(env))


env.run(until=15)

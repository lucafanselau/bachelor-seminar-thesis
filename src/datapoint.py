from person import Datapoint, Person, random_person
import pandas as pd
import numpy as np

categories = ["XS", "S", "M", "L"]
size_hsg = [0.000000, 0.200000, 0.255556, 0.333333]

sizes = {"XS": [0], "S": [0, 1], "M": [1, 2], "L": [2, 3]}

# income_weight = {
#     "XS": 0.2,
#     "S": 0.3,
#     "M": 0.4
#     "L":
# }

type_hsg = {
    "regcar": 0.207865,
    "sportcar": 0.142857,
    "sportuv": 0.400000,
    "stwagon": 0.500000,
    "truck": 0.238095,
    "van": 0.604167,
}

types = {
    "XS": ["regcar"],
    "S": ["regcar", "stwagon"],
    "M": ["regcar", "sportuv", "stwagon"],
    "L": ["sportuv", "sportcar"],
}


def score(person: Person, c: str) -> float:
    size = sizes[c]
    s_0 = np.array([size_hsg[i] for i in size]).mean()
    if person.hhs <= 2:
        s_0 = 1 - s_0

    s_1 = np.array([type_hsg[i] for i in types[c]]).mean()
    if person.hhs <= 2:
        s_1 = 1 - s_1

    # TODO: Maybe add an income factor

    s_random = np.random.normal(scale=0.2)

    # print(f"s({c}) = {s_0} + {s_1} + {s_random} = {s_0 + s_1 + s_random}")
    return s_0 + s_1 + s_random


def random_decision() -> Datapoint:
    person = random_person()
    res = lambda decision: Datapoint(person.age, person.hhs, person.college, decision)

    if person.age < 21:
        return res("XS")

    scores = np.array([score(person, c) for c in categories])
    max = scores.argmax()

    # print(scores, max)

    return res(categories[max])


def dataset(size=10_000) -> pd.DataFrame:
    data = [random_decision() for _ in range(0, size)]
    return pd.DataFrame(data=data)

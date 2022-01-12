from dataclasses import dataclass
import numpy as np


@dataclass
class Person:
    age: int
    hhs: int
    college: bool


@dataclass
class Datapoint(Person):
    decision: str


# This data is gathered from the per age zensus2011 dataset, and shows the total amount of people of the age 18..100 in germany (as of zensus2011)
ages = np.array(
    [
        827646,
        857047,
        941714,
        963052,
        976766,
        987602,
        966263,
        953923,
        958134,
        965314,
        994057,
        1000413,
        991222,
        966128,
        936186,
        939630,
        917961,
        895568,
        901342,
        912022,
        954241,
        1078761,
        1141426,
        1204873,
        1289938,
        1345824,
        1367864,
        1395013,
        1416397,
        1429873,
        1396186,
        1360874,
        1326581,
        1293311,
        1233802,
        1197698,
        1153789,
        1132179,
        1106508,
        1068959,
        1057627,
        1053491,
        1026659,
        1021985,
        952128,
        865528,
        836028,
        605909,
        799506,
        902787,
        861102,
        1004000,
        990420,
        1097279,
        997174,
        914869,
        861483,
        811493,
        772418,
        604799,
        544174,
        537399,
        536353,
        511847,
        475503,
        424552,
        379828,
        346065,
        302287,
        254206,
        228373,
        204145,
        169319,
        133114,
        54758,
        39671,
        33738,
        28246,
        31393,
        22158,
        14750,
        9497,
        13445,
    ]
)
total_data_size = ages.sum()
p_ages = ages / total_data_size


def random_age() -> int:
    return np.random.choice(np.arange(18, 101), p=p_ages)


# This data (also from zensus2011) shows the amount of households with 1..(6 or more) members
hh_sizes = np.array([13960811, 12455731, 5454875, 3906260, 1222149, 571393])
total_hh_sizes = hh_sizes.sum()
p_hh_sizes = hh_sizes / total_hh_sizes


def random_hhs() -> int:
    return np.random.choice(np.arange(1, 7), p=p_hh_sizes)


# College data (also from zensus2011)
college_counts = np.array([3985640, 5471080, 908970])
college_part = college_counts.sum() / 68909110


def random_college() -> bool:
    return np.random.choice([False, True], p=[1 - college_part, college_part])


def random_person() -> Person:
    """
    Creates a random person based on data gathered from zensus2010
    """
    return Person(age=random_age(), hhs=random_hhs(), college=random_college())

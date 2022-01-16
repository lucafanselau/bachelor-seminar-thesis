from dataclasses import dataclass

@dataclass
class CustomerRequest:
  distance: float = 0

  # Demographic information about age
  age_1: float = 0
  age_2: float = 0
  age_3: float = 0
  age_4: float = 0
  age_5: float = 0

  # Household status
  hh_1: float = 0 # Single houses
  hh_2: float = 0 # Pairs
  hh_3: float = 0 # Single parents
  hh_4: float = 0 # Parents with children
  hh_5: float = 0 # Multiperson households


  def __setitem__(self, key, value):
    super().__setattr__(key, value)
  
  def __getitem__(self, key):
    return super().__getattribute__(key)

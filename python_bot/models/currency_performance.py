from dataclasses import dataclass
from typing import List
from dataclass_wizard import JSONWizard


@dataclass
class CurrencyPerformance:
    id: str
    symbol: str
    name: str
    image: str
    market_cap_rank: int
    usd: float
    usd_24h_vol: float
    usd_24h_change: float # actual percentage change


@dataclass
class GainersAndLosers(JSONWizard):
    top_gainers:List[CurrencyPerformance]
    top_losers: List[CurrencyPerformance]

# Note that for this trading bot we’re working with a 24h price change, so we’ve mapped the 
# property usd_24h_change. This is where the actual percentage change percentage is returned
#  by the API. You will need to rename this variable if you choose to work with a different 
# time frame.


# If you opt to use the free endpoint, you will need to change the shape of this object to match the response. That object could look something like this:

#@dataclass
#   class CurrencyPerformance(JSONWizard):
#       id: str
#       name: str
#       symbol: str
#       price_change_percentage_24h: float
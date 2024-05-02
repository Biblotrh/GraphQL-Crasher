from enum import Enum

class MspServer(Enum):
    France = "fr"
    Turkey = "tr"
    Poland = "pl"
    Germany = "de"
    UnitedKingdom = "gb"
    Autralia = "au"
    Italy = "it"

class MspRequestError(Enum):
    RateLimited = 500
    OK = 200
    BadRequest = 400

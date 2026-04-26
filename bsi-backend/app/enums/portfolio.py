import enum

class RiskProfile(str, enum.Enum):
    CONSERVATIVE = "CONSERVATIVE"
    MODERATE = "MODERATE"
    AGGRESSIVE = "AGGRESSIVE"

class PrimaryGoal(str, enum.Enum):
    INCOME = "INCOME"
    GROWTH = "GROWTH"
    PROTECTION = "PROTECTION"
    SPECULATION = "SPECULATION"
    MIXED = "MIXED"

class TimeHorizon(str, enum.Enum):
    SHORT = "SHORT"
    MEDIUM = "MEDIUM"
    LONG = "LONG"

class ManagementStyle(str, enum.Enum):
    PASSIVE = "PASSIVE"
    ACTIVE = "ACTIVE"
    TACTICAL = "TACTICAL"

class AllocationStatus(str, enum.Enum):
    RECOMMENDED = "RECOMMENDED"
    SECONDARY = "SECONDARY"
    REJECTED = "REJECTED"
    OUT_OF_PROFILE = "OUT_OF_PROFILE"
    CAPITAL_CONSTRAINED = "CAPITAL_CONSTRAINED"
    LOW_PRIORITY = "LOW_PRIORITY"

class RecommendationStatus(str, enum.Enum):
    SUCCESS = "SUCCESS"
    NO_ACTION = "NO_ACTION"
    ERROR = "ERROR"

class PositionStatus(str, enum.Enum):
    ACTIVE = "ACTIVE"
    REDUCED = "REDUCED"
    CLOSED = "CLOSED"
    WATCHLIST = "WATCHLIST"

class PortfolioActionType(str, enum.Enum):
    HOLD = "HOLD"
    INCREASE = "INCREASE"
    REDUCE = "REDUCE"
    EXIT = "EXIT"
    REPLACE = "REPLACE"
    REBALANCE = "REBALANCE"
    NO_ACTION = "NO_ACTION"

class ConcentrationStatus(str, enum.Enum):
    HEALTHY = "HEALTHY"
    WARNING = "WARNING"
    CRITICAL = "CRITICAL"

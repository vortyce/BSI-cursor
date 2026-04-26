import enum

class UserChoice(str, enum.Enum):
    ACCEPTED = "ACCEPTED"
    REJECTED = "REJECTED"
    DEFERRED = "DEFERRED"
    EXPIRED = "EXPIRED"

class SimulatedExecutionStatus(str, enum.Enum):
    NONE = "NONE"
    PENDING = "PENDING"
    APPLIED = "APPLIED"
    FAILED = "FAILED"

"""Security signal (siganio) definitions for the CISO dashboard.

Each signal is defined exactly once here and referenced everywhere else,
eliminating duplicated sign/color/meaning literals across the codebase.
"""

from dataclasses import dataclass
from enum import Enum

__all__ = ["RiskLevel", "Signal", "SIGNALS"]


class RiskLevel(Enum):
    LOW = "Low Risk"
    MEDIUM = "Medium Risk"
    HIGH = "High Risk"
    INFO = "Informational"


@dataclass(frozen=True)
class Signal:
    """A single visual security indicator (siganio)."""

    icon: str
    color: str
    meaning: str
    risk_level: RiskLevel

    def __str__(self) -> str:
        return f"{self.icon} [{self.color}] {self.meaning}"


# Each RiskLevel appears exactly once — the dict key is derived from the same
# tuple, so there is no duplication between the key and Signal.risk_level.
_SIGNAL_DATA: list[tuple[RiskLevel, str, str, str]] = [
    (RiskLevel.LOW,    "✅",  "Green",  "Compliant / Low Risk"),
    (RiskLevel.MEDIUM, "⚠️", "Yellow", "Warning / Medium Risk"),
    (RiskLevel.HIGH,   "🔴",  "Red",    "Critical / High Risk"),
    (RiskLevel.INFO,   "ℹ️", "Blue",   "Informational"),
]

SIGNALS: dict[RiskLevel, Signal] = {
    level: Signal(icon, color, meaning, level)
    for level, icon, color, meaning in _SIGNAL_DATA
}

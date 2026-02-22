"""Security signal (siganio) definitions for the CISO dashboard.

Each signal is defined exactly once here and referenced everywhere else,
eliminating duplicated sign/color/meaning literals across the codebase.
"""

from dataclasses import dataclass
from enum import Enum


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


# Single source of truth for all siganios — no duplication elsewhere.
SIGNALS: dict[RiskLevel, Signal] = {
    RiskLevel.LOW: Signal("✅", "Green", "Compliant / Low Risk", RiskLevel.LOW),
    RiskLevel.MEDIUM: Signal("⚠️", "Yellow", "Warning / Medium Risk", RiskLevel.MEDIUM),
    RiskLevel.HIGH: Signal("🔴", "Red", "Critical / High Risk", RiskLevel.HIGH),
    RiskLevel.INFO: Signal("ℹ️", "Blue", "Informational", RiskLevel.INFO),
}

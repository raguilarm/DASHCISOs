"""DASHCISOs — CISO Security Dashboard."""

import os

from .signals import SIGNALS, RiskLevel, Signal


def _env_flag(name: str) -> bool:
    """Return True when an environment variable is set to 'true' (case-insensitive)."""
    return os.getenv(name, "false").lower() == "true"


class Dashboard:
    """CISO Security Dashboard.

    Activation is controlled by three environment variables:
        ACTIVE            — enables the dashboard
        SIGANIOS_ENABLED  — enables visual sign rendering
        ALERTS_ENABLED    — enables real-time security alerts
    """

    def __init__(self) -> None:
        self.active = _env_flag("ACTIVE")
        self.siganios_enabled = _env_flag("SIGANIOS_ENABLED")
        self.alerts_enabled = _env_flag("ALERTS_ENABLED")

    # ------------------------------------------------------------------
    # Signal helpers — delegate to the single source of truth in signals.py
    # ------------------------------------------------------------------

    def get_signal(self, risk_level: RiskLevel) -> Signal:
        """Return the Signal for *risk_level*."""
        return SIGNALS[risk_level]

    def render_signal(self, risk_level: RiskLevel) -> str:
        """Render a signal as a human-readable string.

        When siganios are disabled the icon is omitted and only the risk
        label is shown, keeping the two code paths free of duplicated
        formatting logic.
        """
        signal = self.get_signal(risk_level)
        if not self.siganios_enabled:
            return f"[{signal.meaning}]"
        return str(signal)

    def status(self) -> dict:
        """Return the current activation status of the dashboard."""
        return {
            "active": self.active,
            "siganios_enabled": self.siganios_enabled,
            "alerts_enabled": self.alerts_enabled,
        }

"""DASHCISOs — CISO Security Dashboard."""

import os

from .signals import SIGNALS, RiskLevel, Signal

__all__ = ["Dashboard", "RiskLevel", "Signal", "SIGNALS"]

# Environment variable names — defined once to avoid scattered magic strings.
_ENV_ACTIVE = "ACTIVE"
_ENV_SIGANIOS = "SIGANIOS_ENABLED"
_ENV_ALERTS = "ALERTS_ENABLED"


def _env_flag(name: str) -> bool:
    """Return True when an environment variable is set to 'true' or '1' (case-insensitive)."""
    return os.getenv(name, "false").lower() in ("true", "1")


class Dashboard:
    """CISO Security Dashboard.

    Activation is controlled by three environment variables:
        ACTIVE            — enables the dashboard
        SIGANIOS_ENABLED  — enables visual sign rendering
        ALERTS_ENABLED    — enables real-time security alerts
    """

    def __init__(self) -> None:
        self.active = _env_flag(_ENV_ACTIVE)
        self.siganios_enabled = _env_flag(_ENV_SIGANIOS)
        self.alerts_enabled = _env_flag(_ENV_ALERTS)

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

    def render_all_signals(self) -> list[str]:
        """Render every known signal in order of severity.

        Centralises iteration over RiskLevel so callers never need to
        duplicate the loop themselves.
        """
        return [self.render_signal(level) for level in RiskLevel]

    def status(self) -> dict[str, bool]:
        """Return the current activation status of the dashboard."""
        return {
            "active": self.active,
            "siganios_enabled": self.siganios_enabled,
            "alerts_enabled": self.alerts_enabled,
        }

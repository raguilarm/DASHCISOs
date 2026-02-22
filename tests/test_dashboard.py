"""Tests for the DASHCISOs dashboard module."""

import pytest

from dashboard import Dashboard
from dashboard.signals import SIGNALS, RiskLevel, _SIGNAL_DATA


# ---------------------------------------------------------------------------
# Signal definitions
# ---------------------------------------------------------------------------

class TestSignalDefinitions:
    """Each siganios entry must be defined exactly once in SIGNALS."""

    def test_all_risk_levels_have_a_signal(self):
        for level in RiskLevel:
            assert level in SIGNALS, f"No signal defined for {level}"

    def test_no_duplicate_icons(self):
        icons = [s.icon for s in SIGNALS.values()]
        assert len(icons) == len(set(icons)), "Duplicate icon found in SIGNALS"

    def test_no_duplicate_colors(self):
        colors = [s.color for s in SIGNALS.values()]
        assert len(colors) == len(set(colors)), "Duplicate color found in SIGNALS"

    def test_signal_risk_level_matches_key(self):
        for level, signal in SIGNALS.items():
            assert signal.risk_level == level

    def test_signal_data_has_no_duplicate_risk_levels(self):
        levels = [row[0] for row in _SIGNAL_DATA]
        assert len(levels) == len(set(levels)), "Duplicate RiskLevel in _SIGNAL_DATA"

    def test_signals_built_from_signal_data(self):
        """SIGNALS must be derived entirely from _SIGNAL_DATA with no extra entries."""
        assert set(SIGNALS.keys()) == {row[0] for row in _SIGNAL_DATA}

    def test_signal_str_includes_icon_color_meaning(self):
        signal = SIGNALS[RiskLevel.LOW]
        rendered = str(signal)
        assert signal.icon in rendered
        assert signal.color in rendered
        assert signal.meaning in rendered


# ---------------------------------------------------------------------------
# Dashboard — signal rendering
# ---------------------------------------------------------------------------

class TestDashboardRenderSignal:
    """render_signal must use the shared SIGNALS dict — no inline duplicates."""

    def test_render_when_siganios_enabled(self, monkeypatch):
        monkeypatch.setenv("SIGANIOS_ENABLED", "true")
        dash = Dashboard()
        for level in RiskLevel:
            rendered = dash.render_signal(level)
            assert SIGNALS[level].icon in rendered
            assert SIGNALS[level].color in rendered

    def test_render_without_siganios_enabled(self, monkeypatch):
        monkeypatch.delenv("SIGANIOS_ENABLED", raising=False)
        dash = Dashboard()
        for level in RiskLevel:
            rendered = dash.render_signal(level)
            # Icon must NOT appear when siganios are disabled
            assert SIGNALS[level].icon not in rendered
            assert SIGNALS[level].meaning in rendered

    def test_get_signal_returns_correct_signal(self, monkeypatch):
        monkeypatch.setenv("ACTIVE", "true")
        dash = Dashboard()
        assert dash.get_signal(RiskLevel.HIGH) is SIGNALS[RiskLevel.HIGH]


# ---------------------------------------------------------------------------
# Dashboard — activation status
# ---------------------------------------------------------------------------

class TestDashboardStatus:
    def test_all_flags_off_by_default(self, monkeypatch):
        for var in ("ACTIVE", "SIGANIOS_ENABLED", "ALERTS_ENABLED"):
            monkeypatch.delenv(var, raising=False)
        dash = Dashboard()
        assert dash.status() == {
            "active": False,
            "siganios_enabled": False,
            "alerts_enabled": False,
        }

    def test_all_flags_on(self, monkeypatch):
        for var in ("ACTIVE", "SIGANIOS_ENABLED", "ALERTS_ENABLED"):
            monkeypatch.setenv(var, "true")
        dash = Dashboard()
        assert dash.status() == {
            "active": True,
            "siganios_enabled": True,
            "alerts_enabled": True,
        }

    def test_flag_is_case_insensitive(self, monkeypatch):
        monkeypatch.setenv("ACTIVE", "TRUE")
        assert Dashboard().active is True

        monkeypatch.setenv("ACTIVE", "True")
        assert Dashboard().active is True

    def test_flag_accepts_numeric_one(self, monkeypatch):
        monkeypatch.setenv("ACTIVE", "1")
        assert Dashboard().active is True

    def test_flag_rejects_other_values(self, monkeypatch):
        for val in ("yes", "on", "enabled", ""):
            monkeypatch.setenv("ACTIVE", val)
            assert Dashboard().active is False


# ---------------------------------------------------------------------------
# Dashboard — render_all_signals
# ---------------------------------------------------------------------------

class TestDashboardRenderAllSignals:
    """render_all_signals must return one entry per RiskLevel — no manual loop needed."""

    def test_returns_all_risk_levels(self, monkeypatch):
        monkeypatch.setenv("SIGANIOS_ENABLED", "true")
        dash = Dashboard()
        results = dash.render_all_signals()
        assert len(results) == len(RiskLevel)

    def test_order_matches_risk_level_enum(self, monkeypatch):
        monkeypatch.setenv("SIGANIOS_ENABLED", "true")
        dash = Dashboard()
        results = dash.render_all_signals()
        for rendered, level in zip(results, RiskLevel):
            assert SIGNALS[level].icon in rendered

    def test_consistent_with_individual_render(self, monkeypatch):
        monkeypatch.setenv("SIGANIOS_ENABLED", "true")
        dash = Dashboard()
        for rendered, level in zip(dash.render_all_signals(), RiskLevel):
            assert rendered == dash.render_signal(level)

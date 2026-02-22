# DASHCISOs

A dashboard application for CISOs (Chief Information Security Officers) providing visual security indicators and improved status signs/icons (siganios).

## Features

- **Siganios mejorados (Improved Signs/Icons)**: Enhanced visual indicators for security status, risk levels, and compliance metrics.
- Security posture overview with color-coded risk signals.
- Real-time threat and compliance status signs.

## Siganios (Signs/Icons)

The dashboard uses a set of improved visual signs to communicate security status at a glance:

| Sign | Color | Meaning |
|------|-------|---------|
| ✅ | Green | Compliant / Low Risk |
| ⚠️ | Yellow | Warning / Medium Risk |
| 🔴 | Red | Critical / High Risk |
| ℹ️ | Blue | Informational |

## Activar (Activate)

Before using the dashboard, you must activate it by configuring the required settings:

1. **Activate the dashboard**: Set the `ACTIVE` environment variable to `true`.
2. **Activate siganios**: Enable the improved signs/icons by setting `SIGANIOS_ENABLED=true`.
3. **Activate alerts**: Turn on real-time security alerts with `ALERTS_ENABLED=true`.

Example activation configuration:

```bash
ACTIVE=true
SIGANIOS_ENABLED=true
ALERTS_ENABLED=true
```

## Getting Started

Clone the repository and follow the setup instructions for your environment.

```bash
git clone https://github.com/raguilarm/DASHCISOs.git
```

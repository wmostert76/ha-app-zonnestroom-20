# Zonspaarpot 2.0

Home Assistant custom integration for the Zonspaarpot (Power Return Optimizer / SSM-PRO) local API.

## Features

- Polls local API endpoints:
  - `GET /api`
  - `GET /api/v2/config`
  - `GET /api/v2/actual`
- Exposes sensors for:
  - Home consumption
  - Additional consumption
  - Active mode
  - HomeWizard values (if available)
  - P1 diagnostics
- Control entities:
  - Mode select (`Optimizing`, `Maximum load`, `API mode`)
  - Setload number (`0..2300` watt via `PUT /api/v2/setload`)

## Installation (HACS - custom repository)

1. Open HACS in Home Assistant.
2. Go to `Integrations` and click the menu (top-right).
3. Choose `Custom repositories`.
4. Add this repository URL and set category to `Integration`.
5. Install `Zonspaarpot 2.0`.
6. Restart Home Assistant.

## Installation (manual)

1. Copy `custom_components/zonspaarpot_2_0` to your Home Assistant `custom_components` folder.
2. Restart Home Assistant.
3. Add integration: `Settings -> Devices & Services -> Add Integration -> Zonspaarpot 2.0`.

## Configuration

- Host/IP: for example `192.168.180.109`
- Scan interval: in seconds (2..300, default 10)

## Notes

- The integration uses the device's local HTTP API without authentication.
- Ensure Home Assistant can reach the device on your LAN.

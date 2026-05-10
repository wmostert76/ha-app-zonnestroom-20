## v2.2.0 - 2026-05-10

## Changes

- Add stable entity unique IDs independent of the configured IP address.
- Add Home Assistant reconfigure flow for IP address and scan interval.
- Add force refresh button, API connected binary sensor and extra diagnostics sensors.
- Add editable load timing controls for wait-after-update, awake and sleep.
- Add diagnostics support and repair issue when the API is unreachable.
- Add Dutch and English translations.
- Update README and release workflow for manual versioned releases.

## v2.1.0 - 2026-05-10

## Changes

- Set the integration config entry title to Zonnestroom 2.0.
- Release version 2.1.0.

# Changelog

## 1.0.3

- Add repository `icon.png` for HACS card display
- Add component-local `icon.png` for consistency

## 1.0.0

- Initial release
- Config flow with host and scan interval
- Sensors from `/api`, `/api/v2/config`, `/api/v2/actual`
- Mode control via `/api/v2/setmode`
- Setload control via `/api/v2/setload`

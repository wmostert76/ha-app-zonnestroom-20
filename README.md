# Zonnestroom 2.0

[![GitHub Release][releases-shield]][releases]
[![License][license-shield]][license]
[![Maintainer][maintainer-shield]][maintainer]
[![Direct Import][direct-import-shield]][direct-import]

Zonnestroom 2.0 is een Home Assistant integratie voor lokale uitlezing en bediening van de Zonnestroom/Zonspaarpot API.

## Installatie

### HACS

Klik op de knop hieronder om deze repository aan Home Assistant toe te voegen via HACS:

[![Add to Home Assistant][direct-import-button]][direct-import]

Je kunt de repository ook handmatig toevoegen in HACS als custom repository:

```text
https://github.com/wmostert76/ha-app-zonnestroom-20
```

Categorie: `Integration`.

### Handmatig

1. Download de laatste release.
2. Kopieer `custom_components/zonnestroom` naar `/config/custom_components/`.
3. Herstart Home Assistant.
4. Ga naar **Instellingen > Apparaten & diensten > Integratie toevoegen** en zoek naar `Zonnestroom 2.0`.

## Functies

- Lokale polling van de Zonnestroom API.
- Vermogenssensoren voor huisverbruik, extra verbruik en HomeWizard verbruik.
- Diagnostische sensoren voor P1, WLAN, HomeWizard PIB en API-versie.
- Moduskeuze via een select-entity.
- Bediening voor setload, wait-after-update, awake en sleep.
- IP-adres direct aanpasbaar via een text-entity onder Bediening.
- Herconfiguratie via de integratie-instellingen van Home Assistant.
- Repair-melding wanneer de API niet bereikbaar is.
- Diagnostics-download voor foutanalyse.

## Configuratie

Tijdens het toevoegen vul je het IP-adres van de Zonnestroom/Zonspaarpot module in. De standaard polling-interval is 10 seconden.

Het IP-adres kan later op twee manieren worden aangepast:

- via **Instellingen > Apparaten & diensten > Zonnestroom 2.0 > Opnieuw configureren**;
- via de entity `IP-adres` onder Bediening.

Een IP-wijziging via de text-entity wordt direct getest, opgeslagen en zonder herstart doorgevoerd.

## Energie-dashboard

De integratie levert op dit moment vermogenssensoren in watt. Die zijn geschikt voor dashboards, automatiseringen en grafieken. Het standaard Home Assistant Energie-dashboard vraagt normaal om energiesensoren in kWh met lange-termijnstatistiek. Maak daarvoor een aparte integratie- of utility-meter sensor als je deze gegevens in het Energie-dashboard wilt gebruiken.

## Ontwikkeling

Releases gebruiken de versie uit `custom_components/zonnestroom/manifest.json`. HACS ziet een update zodra er een nieuwe GitHub release met een hogere tag beschikbaar is.

## Ondersteuning

Open bij problemen of suggesties een issue:

```text
https://github.com/wmostert76/ha-app-zonnestroom-20/issues
```

## Licentie

Gelicenseerd onder de [MIT Licentie](LICENSE).

[releases-shield]: https://img.shields.io/github/v/release/wmostert76/ha-app-zonnestroom-20?style=for-the-badge
[releases]: https://github.com/wmostert76/ha-app-zonnestroom-20/releases
[license-shield]: https://img.shields.io/github/license/wmostert76/ha-app-zonnestroom-20?style=for-the-badge
[license]: LICENSE
[maintainer-shield]: https://img.shields.io/badge/MAINTAINER-W.%20MOSTERT-orange?style=for-the-badge
[maintainer]: https://github.com/wmostert76
[direct-import-shield]: https://img.shields.io/badge/DIRECT%20IMPORT-TO%20HA-blue?style=for-the-badge
[direct-import]: https://my.home-assistant.io/redirect/hacs_repository/?owner=wmostert76&repository=ha-app-zonnestroom-20&category=integration
[direct-import-button]: https://my.home-assistant.io/badges/hacs_repository.svg

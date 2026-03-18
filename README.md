# Zonnestroom 2.0

[![GitHub Release][releases-shield]][releases]
[![License][license-shield]][license]
[![Maintainer][maintainer-shield]][maintainer]
[![Direct Import][direct-import-shield]][direct-import]

Zonnestroom 2.0 is een Home Assistant integratie waarmee je jouw zonnestroom-data direct in Home Assistant kunt inladen en gebruiken voor optimalisatie van je energieverbruik.

## 🚀 Snelle Installatie

Klik op de knop hieronder om de repository direct aan jouw Home Assistant instance toe te voegen via HACS:

[![Add to Home Assistant][direct-import-button]][direct-import]

*Let op: Je hebt Home Assistant 2025.11 of nieuwer nodig voor deze functie.*

## 📖 Inhoudsopgave
- [Functies](#-functies)
- [Installatie](#-installatie)
- [Configuratie](#-configuratie)
- [Ondersteuning](#-ondersteuning)
- [Licentie](#-licentie)

## ✨ Functies
- **Directe Data-import**: Real-time inzicht in je zonnestroom-opbrengst.
- **Geoptimaliseerd voor Energie-dashboard**: Volledig compatibel met het standaard HA Energie-dashboard.
- **Lokale Polling**: Data blijft binnen jouw eigen netwerk (geen cloud nodig).
- **Config Flow**: Eenvoudige configuratie via de Home Assistant interface.

## 🛠 Installatie

### Optie 1: Direct Import via HACS (Aanbevolen)
Klik op de [Add to Home Assistant][direct-import] knop hierboven.

### Optie 2: Handmatige Installatie
1. Download de [laatste release](https://github.com/wmostert76/ha-app-zonnestroom-20/releases).
2. Kopieer de map `custom_components/zonnestroom` naar je `/config/custom_components/` map.
3. Start Home Assistant opnieuw op.
4. Ga naar **Instellingen > Apparaten & Diensten > Integratie Toevoegen** en zoek naar `Zonnestroom 2.0`.

## ⚙️ Configuratie
Na de installatie kun je de integratie configureren door je host-IP van de Zonspaarpot/Zonnestroom module op te geven.

## 💬 Ondersteuning
Heb je problemen of suggesties? Open dan een [issue](https://github.com/wmostert76/ha-app-zonnestroom-20/issues) of bekijk onze [Wiki](https://github.com/wmostert76/ha-app-zonnestroom-20/wiki).

## 📄 Licentie
Gelicenseerd onder de [MIT Licentie](LICENSE).

---
*Ontwikkeld door [wmostert76](https://github.com/wmostert76).*

[releases-shield]: https://img.shields.io/github/v/release/wmostert76/ha-app-zonnestroom-20?style=for-the-badge
[releases]: https://github.com/wmostert76/ha-app-zonnestroom-20/releases
[license-shield]: https://img.shields.io/github/license/wmostert76/ha-app-zonnestroom-20?style=for-the-badge
[license]: LICENSE
[maintainer-shield]: https://img.shields.io/badge/MAINTAINER-W.%20MOSTERT-orange?style=for-the-badge
[maintainer]: https://github.com/wmostert76
[direct-import-shield]: https://img.shields.io/badge/DIRECT%20IMPORT-TO%20HA-blue?style=for-the-badge
[direct-import]: https://my.home-assistant.io/redirect/hacs_repository/?owner=wmostert76&repository=ha-app-zonnestroom-20&category=integration
[direct-import-button]: https://my.home-assistant.io/badges/hacs_repository.svg


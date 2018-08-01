


# home-assistant-custom-components
Custom component for [Home Assistant](https://home-assistant.io/) 


## EDF Components
[![Version](https://img.shields.io/badge/version-0.0.1-green.svg?style=for-the-badge)](#) [![mantained](https://img.shields.io/maintenance/yes/2018.svg?style=for-the-badge)](#)

### Edf Ejp


Ce composant permet de récupérer les informations du site EJP (edf), notamment dans l’optique de s’en servir (dans des scénarios) pour réduire ses consommations électriques en cas de fortes tensions sur le réseau électrique ou lors des jours EJP (selon les contrats d’électricité souscrits).

```yaml
binary_sensor:
  - platform: edf_ejp
    regions:
     - nord
     - ouest
     - sud
     - paca
sensor:
  - platform: edf_ejp
    regions:
     - nord
     - ouest
     - sud
     - paca
```

### Edf Tempo

Ce composant permet de récupérer les informations du site Tempo (edf), notamment dans l’optique de s’en servir (dans des scénarios) pour réduire ses consommations électriques en cas de fortes tensions sur le réseau électrique(selon les contrats d’électricité souscrits).

```yaml
sensor:
  - platform: edf_tempo
```
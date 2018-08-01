# home-assistant-custom-components
home-assistant-custom-components


## EDF Components

### Edf Ejp


Ce composant permet de récupérer les informations du site EJP (edf), notamment dans l’optique de s’en servir (dans des scénarios) pour réduire ses consommations électriques en cas de fortes tensions sur le réseau électrique ou lors des jours EJP (selon les contrats d’électricité souscrits).

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

### Edf Tempo

Ce composant permet de récupérer les informations du site Tempo (edf), notamment dans l’optique de s’en servir (dans des scénarios) pour réduire ses consommations électriques en cas de fortes tensions sur le réseau électrique(selon les contrats d’électricité souscrits).

sensor:
  - platform: edf_tempo
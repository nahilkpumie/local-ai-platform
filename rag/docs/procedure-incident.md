# Procédure de réponse à incident — Entreprise fictive ACME Lab

## Étape 1 : Détection
Toute alerte critique Wazuh est transmise à l'équipe sécurité par e-mail et sur le canal #soc.

## Étape 2 : Confinement
Le poste suspect est isolé du réseau en le déplaçant dans le VLAN 99 (quarantaine) depuis le switch ou le pare-feu pfSense.
Ne jamais éteindre la machine : la mémoire vive contient des preuves.

## Étape 3 : Analyse
Une copie de la mémoire est réalisée, puis les journaux des 72 dernières heures sont exportés.

## Étape 4 : Communication
Le RSSI est prévenu sous 1 heure. Si des données personnelles sont touchées, la CNIL doit être notifiée sous 72 heures.

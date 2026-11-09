# Politique de mots de passe — Entreprise fictive ACME Lab

## Règles générales
- Longueur minimale : 14 caractères pour les comptes utilisateurs.
- Longueur minimale : 20 caractères pour les comptes administrateurs.
- Le MFA est obligatoire pour tous les accès distants (VPN, webmail, console cloud).
- Les mots de passe ne sont plus changés tous les 90 jours : ils sont changés uniquement en cas de suspicion de compromission (recommandation ANSSI et NIST SP 800-63B).

## Comptes de service
- Les comptes de service utilisent un mot de passe aléatoire de 32 caractères stocké dans le coffre-fort Vaultwarden.
- Un compte de service ne doit jamais avoir de session interactive.

## Verrouillage
- Le compte est verrouillé 15 minutes après 5 tentatives échouées.

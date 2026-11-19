# Audit initial de Djin

Audit en lecture seule du 15/11/2026, recoupé le même jour. Ce fichier
garde l'état du projet avant sa remise au propre.

## Décision

Ajuster Djin par la procédure : chaque retrait ou reprise passe par une
tâche et une pull request que je relis.

Raison : le socle est sain et les manques sont les mêmes dans tous les
cas. Je maîtrise peu le code ; relire chaque changement me rend le
contrôle.

Écartés : ajuster directement, refaire de zéro.

## Ce que l'audit a montré

- **Le cœur est sain** : réglages pilotés par l'environnement, modèle
  User personnalisé, intégration Vite, CSRF, `parse_body`, CLAUDE.md
  complet et à jour.
- **En trop** : les apps `demo` (avec des données insérées par
  migration) et `todos`, le correctif Inertia
  (`config/templates/inertia.html` et le filtre `script_json`), deux
  linters configurés mais aucun installé.
- **Vieilli** : Python 3.10, qui n'est plus maintenu depuis octobre
  2026 ; inertia-django 1.2.0, alors que la 2.0.0 produit nativement le
  format attendu par le client v3 et rend le correctif inutile ; des
  classes DaisyUI v4 supprimées en v5, qui cassent l'affichage des
  formulaires.
- **Manquant** : réglages de sécurité et fichiers statiques pour la
  production, serveur d'application, tests, lint installé, intégration
  continue, Docker.
- **Incohérences** : identifiants en français (`titre`, `cree_le`,
  `fait`), commentaires périmés, renvois vers des sections du README qui
  n'existent pas, nom de base `yproject`, un caractère cyrillique dans
  `entry.js`.

## Ce qui a suivi

Le cahier des charges « Djin propre » est dans
`docs/cahier-des-charges.md`. Les questions ouvertes par cet audit y
sont tranchées ou marquées « à explorer », et les parties du projet sont
dans GitHub Issues.

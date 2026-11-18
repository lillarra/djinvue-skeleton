# Spécification : partie 1, Base du projet

## Besoin
Avoir une base Django qui marche, configurée à la main, sur laquelle
les autres parts s'appuient. L'assistant de configuration (partie 2)
automatisera sa mise en place plus tard.

## Une fois finie, je peux
- lancer le projet sous Python 3.12 ou plus et Django 5.2 LTS ;
- le relier à sa base de données en remplissant le fichier .env à la
  main, à partir d'un fichier d'exemple ;
- me connecter et me déconnecter ;
- désactiver l'inscription par un réglage ;
- ouvrir l'admin Django avec un compte administrateur.

## Règles
- On ne touche pas à ce qui sera repris plus tard. On réajuste
  seulement ce qui ne marche plus.
- Les écrans de connexion et d'inscription restent tels quels.
  - Remarque : leur affichage peut être abîmé par les classes
    DaisyUI. Seul leur fonctionnement compte ici.

## Hors périmètre
Inertia, Vue et Vite ; le design ; Docker ; l'assistant de
configuration ; le nettoyage de l'existant ; le système de tests
complet.

## Critères de fin
- Des tests Django, lancés avec l'outil intégré, couvrent tout ce qui
  figure dans « Une fois finie, je peux », sauf la version de Python.
- Une liste de vérification manuelle accompagne chaque tâche :
  prérequis, actions, résultat attendu.
  - Remarque : pour l'inscription désactivée, vérifier deux cas : le
    lien est absent, et l'adresse directe est refusée.

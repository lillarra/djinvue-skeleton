# Cahier des charges « Djin propre »

Le comment noté ici est une trace des réflexions ; il se revérifie au moment d'agir.

Validé le 16/11/2026.

## Vision

Djin est le point commun entre mes projets, pour me lancer vite : un point de départ minimal qui regroupe les outils que je retrouve dans tous mes projets. Il sert à Tata Flow, au site CV, et à sortir un petit MVP quand une idée vient. Il évolue avec ma pratique : ce que je refais dans tous mes projets a vocation à y entrer.

Un projet Djin est un monolithe Django. Les pages sont définies par les vues Django et rendues par Inertia et Vue, sans routeur front ni API séparée : un front et un back séparés sont un double maintien. L'asynchrone sert à certains éléments visuels.

## Stack

- Python 3.15, Django 6.1.
    - Note : la prochaine LTS, 6.2, est attendue en avril 2027.
- inertia-django 2.0, Vue 3, Vite.
- Tailwind, nécessaire à shadcn-vue. DaisyUI sort.
- shadcn-vue : les composants sont copiés dans le projet, je garde la main sur tout.
    - Remarque : vérifier que shadcn-vue s'utilise en JavaScript, ses composants étant en TypeScript par défaut (non vérifié).
- JavaScript ; TypeScript en option, voir « à explorer ».
- Conventions : code en anglais, commentaires en français.

## Ce que Djin contient

- Django configuré avec sa base de données, les réglages pilotés par l'environnement, l'intégration de Vite. Pour ce faire, un assistant de configuration.
- Le modèle User personnalisé, les écrans de connexion et d'inscription. L'inscription est désactivable par réglage. L'admin Django est activé : dans certains projets, l'authentification ne servira qu'à y entrer.
- Une page d'accueil qui dit ce qui est en place dans le projet (connexion à la base, fichier `.env`, réglages) et quoi faire ensuite, pour ne pas être perdue au démarrage.
    - Remarque : une page qui montre l'état de la configuration sera à protéger en production.
- Un système de tests prêt à être utilisé dans le projet. Les tests couvrent ce qui existe dans Djin : l'idée est de commencer avec une couverture de 100 %.
- Le lint et le formatage installés.
- L'intégration continue : une vérification automatique de l'intégrité du code à chaque pull request (les tests et le lint tournent sur GitHub).
- Docker : un conteneur facilement déployable sur un serveur, et un squelette facilement installable pour le développement.
- Les réglages de production : sécurité, fichiers statiques, serveur d'application.
- Ce qui sert à la mise en ligne automatique d'un projet.
- Un README qui dit ce que contient Djin et comment démarrer un projet.
    - Note : « compléter le README » peut figurer dans la liste « quoi faire ensuite » de la page d'accueil.
- Un CLAUDE.md à jour, qui pointe vers ce cahier des charges.

## Ce que « propre » veut dire

- Lisible : des commentaires et des docstrings qui expliquent ce qui est fait. Je comprends comment le code est agencé et j'ai envie d'y entrer.
- Maintenable : des versions maintenues, un projet que je peux mettre à jour ou modifier à tout instant.
- Rien de superflu : chaque fichier se justifie.
- Un nouveau projet se met en place facilement à partir du squelette.

Djin propre est fini quand je le dis.

## Retiré du Djin actuel

- Les apps `demo` et `todos`.
- Le correctif Inertia (`config/templates/inertia.html`, filtre `script_json`), rendu inutile par inertia-django 2.0.
- DaisyUI et ses classes v4.
- Les identifiants en français, les commentaires périmés, les renvois vers des sections absentes du README, le nom de base `yproject`, le caractère cyrillique dans `entry.js`.
- Les fins de ligne CRLF : LF partout, imposé par un `.gitattributes`.

## Hors périmètre

- Un design imposé.
- Du code d'exemple métier. Il ne reviendra que si l'architecture change (par exemple hexagonale).
- Du contenu propre à un projet.

## À explorer

### Propre à Djin

- Les erreurs de formulaire : en prop de page ou par redirection et session. À traiter avec le passage à inertia-django 2.0, qui change la façon dont elles passent.
- L'assistant de configuration : nom du projet, nom de la base, création de la base et connexion dans le `.env`, quelques choix. Commande Django ou Bash, à voir.
- TypeScript en option, lié à l'assistant de configuration : sans lui, deux versions à maintenir.
- Djin comme modèle de dépôt GitHub : je ne sais pas gérer cette situation.
- La documentation : succincte, avec une cartographie et les fonctionnements complexes. Je ne sais pas comment la mettre en place.
- Le lint et le formatage : quels outils, puisque deux sont configurés mais aucun installé.
- La mise en ligne automatique : ce qui vit dans Djin et ce qui reste propre à chaque projet (étape 5).
    - Note : Dockerfile et fichier GitHub Actions dans Djin, le serveur et ses secrets dans chaque projet.
- La base de données : un choix possible depuis l'assistant de configuration.
- Le gestionnaire de paquets Python : uv est le choix par défaut actuel. Je ne connais pas les alternatives ni ce qui est le mieux.

### Tranché par la procédure

Ces questions sont suivies dans l'onglet Suivi.

- Les tests : Django ou pytest (étape 4).
- L'hébergeur et l'outil de déploiement (étape 5).

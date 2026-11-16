# Docker Compose : Dozzle et Drupal

Ces commandes se lancent depuis le dossier `docker-compose-exercice1`.
Docker Desktop doit être démarré.

## 1. Voir les journaux avec Dozzle

```bash
docker compose -f docker-compose.dozzle.yml up -d
```

Ouvre <http://localhost:8888> et clique sur un conteneur pour voir ses
journaux. `-f` choisit le fichier à utiliser, `up` crée et démarre les
conteneurs, et `-d` les laisse fonctionner en arrière-plan.

```bash
docker compose -f docker-compose.dozzle.yml ps
docker compose -f docker-compose.dozzle.yml down
```

`ps` affiche l'état et `down` arrête et supprime le conteneur Dozzle.
L'interface n'est accessible que depuis ce Mac. Dozzle a besoin du socket
Docker pour consulter les conteneurs : même monté avec `:ro`, ce socket donne
un accès puissant à l'API Docker. Il ne faut donc pas exposer Dozzle sur Internet.

## 2. Démarrer Drupal et PostgreSQL

Un fichier `.env` contenant un mot de passe a déjà été créé sur ce Mac et est
ignoré par Git. Sur un autre ordinateur, crée-le avant le premier démarrage :

```bash
cp .env.example .env
```

Ouvre `.env` et remplace la valeur d'exemple par ton propre mot de passe. Ne
publie pas ce fichier. Pour retrouver le mot de passe local :

```bash
cat .env
```

```bash
docker compose up -d
docker compose ps
docker compose logs -f
```

Pour quitter les journaux, utilise `Ctrl+C` : les conteneurs restent démarrés.
Puis ouvre <http://localhost:8081> et suis l'installation de Drupal. Dans la
configuration de la base, choisis PostgreSQL et indique :

| Champ | Valeur |
| --- | --- |
| Nom de la base | `postgres` |
| Utilisateur | `postgres` |
| Mot de passe | la valeur de `POSTGRES_PASSWORD` dans `.env` |
| Hôte, dans les options avancées | `postgres` |
| Port | `5432` |

`postgres` est le nom du service de la base dans Compose. Drupal le trouve grâce
au réseau créé par Compose. `localhost` désignerait le conteneur Drupal lui-même,
pas celui de PostgreSQL. Termine l'installation en choisissant le nom du site
et les identifiants d'administration de ton choix.

```bash
docker compose stop     # Arrêter les conteneurs sans les supprimer.
docker compose start    # Redémarrer les conteneurs existants.
docker compose down     # Supprimer les conteneurs et le réseau, sans les données.
```

Les volumes gardent les données de Drupal et de PostgreSQL. Attention :
`docker compose down -v` les supprime aussi. Le mot de passe PostgreSQL est
initialisé au premier démarrage de sa base : modifier `.env` ensuite ne change
pas automatiquement le mot de passe déjà enregistré dans son volume.

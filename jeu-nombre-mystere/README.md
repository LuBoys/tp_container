# Le nombre mystère : deux microservices

Le but du jeu : trouver un nombre entre 1 et 100 en faisant le moins d'essais
possible. Après une victoire, le score apparaît dans le classement.

Le projet utilise **deux applications séparées** et aucun service Node.js :

1. `jeu` est écrit en **Python avec Flask**. Il affiche la page, choisit le
   nombre secret et vérifie les réponses.
2. `scores` est écrit en **PHP**. Il reçoit les victoires et enregistre le
   classement dans un fichier JSON.

Chaque application a son propre Dockerfile. Docker Compose construit les deux
images, lance les conteneurs et crée un réseau pour qu'ils puissent communiquer.

```text
Navigateur sur le Mac
        |
        | http://localhost:8083
        v
  Service jeu : Python
        |
        | http://scores:8081/scores, sur le réseau Docker
        v
 Service scores : PHP ---> volume scores_data
```

## Démarrer le projet

Dans un terminal, avec Docker Desktop ouvert :

```bash
cd ~/Documents/tp_container/docker-introduction/jeu-nombre-mystere
docker compose up -d --build
```

Ouvre ensuite <http://localhost:8083>. L'adresse est accessible uniquement sur
ce Mac. Entre directement un nombre ; après une victoire, une nouvelle partie
commence à ta prochaine proposition. Les nouveaux scores apparaissent sous le
nom « Joueur », sans demander de pseudo.

`--build` reconstruit les images à partir des Dockerfiles. `up` crée et démarre
les conteneurs. `-d` les laisse fonctionner en arrière-plan.

## Comprendre les fichiers

| Fichier | À quoi il sert |
| --- | --- |
| `docker-compose.yml` | Décrit les deux services et leur réseau. |
| `service-jeu/Dockerfile` | Explique comment construire l'image Python du jeu. |
| `service-jeu/app.py` | Contient les règles du jeu et appelle le service de scores. |
| `service-jeu/templates/index.html` | Contient la page affichée dans le navigateur. |
| `service-jeu/static/style.css` | Contient les couleurs et la mise en forme de la page. |
| `service-jeu/static/jeu.js` | Actualise le compteur et les indices sans recharger la page. |
| `service-scores/Dockerfile` | Explique comment construire l'image PHP des scores. |
| `service-scores/index.php` | Lit et enregistre les scores dans un fichier JSON. |

Dans le code Python, `http://scores:8081` désigne le service PHP. Le mot
`scores` est son nom dans Compose : Docker permet aux deux services de se
trouver grâce au réseau qu'il crée. Le port de PHP n'est pas publié sur le Mac.

## Commandes utiles

Toujours depuis le dossier de ce projet :

```bash
docker compose ps          # Voir l'état des deux conteneurs.
docker compose logs -f     # Suivre leurs journaux ; Ctrl+C pour quitter.
docker compose stop        # Arrêter les deux conteneurs.
docker compose start       # Redémarrer les conteneurs arrêtés.
docker compose down        # Supprimer conteneurs et réseau, conserver les scores.
```

Après une modification du code ou d'un Dockerfile :

```bash
docker compose up -d --build
```

PHP enregistre les scores dans `/data/scores.json`, à l'intérieur du conteneur
`scores`. Le dossier `/data` est relié au volume Docker `scores_data` : les
scores restent donc présents après la suppression des conteneurs. Docker nomme
ce volume `nombre-mystere_scores_data` pour ce projet. Pour voir le fichier :

```bash
docker compose exec scores cat /data/scores.json
```

Le fichier peut être vide tant qu'aucun score n'a été enregistré. La commande
`docker compose down -v` supprimerait aussi ce volume et tous ses scores.
Une partie en cours, elle, est conservée en mémoire seulement : elle recommence
si le service Python redémarre.

Ce projet est prévu pour le TP en local : le serveur de développement Flask ne
doit pas être exposé tel quel sur Internet.

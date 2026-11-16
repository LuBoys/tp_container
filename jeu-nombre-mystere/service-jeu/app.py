"""Service Python : règles du jeu et page web."""

import os
import secrets
from threading import Lock

import requests
from flask import Flask, flash, jsonify, redirect, render_template, request, session, url_for

app = Flask(__name__)
# Une nouvelle clé est créée au démarrage. Les parties en cours sont locales.
app.secret_key = os.environ.get("SECRET_KEY") or secrets.token_hex(32)
app.config.update(SESSION_COOKIE_HTTPONLY=True, SESSION_COOKIE_SAMESITE="Lax")

# Docker Compose fournit cette adresse. « scores » est le nom du service PHP.
SCORES_URL = os.environ.get("SCORES_URL", "http://scores:8081")
parties = {}
verrou = Lock()


def lire_scores():
    """Demander le classement au service PHP, sans bloquer si celui-ci échoue."""
    try:
        reponse = requests.get(f"{SCORES_URL}/scores", timeout=2)
        reponse.raise_for_status()
        return reponse.json()["scores"], True
    except (requests.RequestException, ValueError, KeyError):
        return [], False


@app.get("/")
def accueil():
    with verrou:
        partie = parties.get(session.get("partie_id"))
        essais = partie["essais"] if partie else 0
    scores, scores_disponibles = lire_scores()
    return render_template(
        "index.html", essais=essais, scores=scores, scores_disponibles=scores_disponibles
    )


def repondre_au_joueur(message, essais=None, scores=None, scores_disponibles=True, code=200):
    """Le navigateur peut actualiser la carte sans recharger toute la page."""
    if request.accept_mimetypes.best == "application/json":
        return jsonify(
            message=message,
            essais=essais,
            scores=scores,
            scores_disponibles=scores_disponibles,
        ), code
    flash(message)
    return redirect(url_for("accueil"))


@app.post("/proposer")
def proposer():
    try:
        proposition = int(request.form.get("nombre", ""))
    except ValueError:
        return repondre_au_joueur("Entre un nombre entier entre 1 et 100.", code=400)
    if not 1 <= proposition <= 100:
        return repondre_au_joueur("Ton nombre doit être entre 1 et 100.", code=400)

    with verrou:
        partie_id = session.get("partie_id")
        partie = parties.get(partie_id)
        if not partie:
            partie_id = secrets.token_urlsafe(24)
            session["partie_id"] = partie_id
            # Le nombre secret reste dans le service Python.
            partie = {"nombre": secrets.randbelow(100) + 1, "essais": 0, "terminee": False}
            parties[partie_id] = partie
        elif partie["terminee"]:
            # Une proposition après la victoire commence une nouvelle partie.
            partie.update(nombre=secrets.randbelow(100) + 1, essais=0, terminee=False)
        partie["essais"] += 1
        essais = partie["essais"]
        nombre = partie["nombre"]
        if proposition == nombre:
            partie["terminee"] = True

    if proposition == nombre:
        # Sans champ de pseudo, les nouveaux scores sont enregistrés sous « Joueur ».
        resultat = {"pseudo": "Joueur", "essais": essais}
        mot_essai = "essai" if essais == 1 else "essais"
        message = f"Bravo ! Trouvé en {essais} {mot_essai}. À toi de rejouer."
        try:
            reponse = requests.post(f"{SCORES_URL}/scores", json=resultat, timeout=2)
            reponse.raise_for_status()
        except requests.RequestException:
            message += " Score non enregistré."
        scores, scores_disponibles = lire_scores()
        return repondre_au_joueur(message, essais, scores, scores_disponibles)
    elif proposition < nombre:
        return repondre_au_joueur("C’est plus grand !", essais)
    else:
        return repondre_au_joueur("C’est plus petit !", essais)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)

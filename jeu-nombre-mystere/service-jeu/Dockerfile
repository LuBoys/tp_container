# Image Python légère pour le service du jeu.
FROM python:3.13-alpine

WORKDIR /app

# Installer les bibliothèques avant de copier le code, pour utiliser le cache.
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt \
    && adduser -D -u 10001 joueur

COPY --chown=joueur:joueur . .

# L'application n'a pas besoin de démarrer en administrateur.
USER joueur
EXPOSE 5000
CMD ["python", "app.py"]

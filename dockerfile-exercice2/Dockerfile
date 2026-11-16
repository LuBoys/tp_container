# utiliser la même base Node.js légère que pour l'exercice 1.
FROM node:18-alpine

# exécuter les commandes suivantes dans /app à l'intérieur de l'image.
WORKDIR /app

# copier les fichiers du quiz depuis le dossier de l'exercice.
COPY . .

# installer les bibliothèques, construire le site et nettoyer les modules du projet.
RUN npm install \
&& npm install -g serve \
    && npm run build \
    && rm -fr node_modules

# indiquer le port d'écoute du serveur à l'intérieur du conteneur.
EXPOSE 3000

# servir le dossier dist/ produit par Vite au démarrage du conteneur.
CMD ["serve", "-s", "dist"]

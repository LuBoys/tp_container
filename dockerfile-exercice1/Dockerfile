# Utiliser une image de base Node.js legere
FROM node:18-alpine

# Definir le repertoire de travail de l'application
WORKDIR /app

# Copier les fichiers package.json et package-lock.json pour installer les dependances
COPY package.json package-lock.json ./

# Copier les fichiers sources src et public de l'application dans le conteneur
COPY src/ ./src/
COPY public/ ./public/

# Installer les dependances, construire l'application et nettoyer les modules Node.js
# Le serveur serve, installe globalement, reste disponible apres le nettoyage.
RUN npm install \
    && npm install -g serve \
    && npm run build \
    && rm -fr node_modules

# Exposer le port
# Ce port est interne au conteneur. docker run -p choisit le port sur le Mac.
EXPOSE 3000

# Demarrer l'application
CMD ["serve", "-s", "build"]

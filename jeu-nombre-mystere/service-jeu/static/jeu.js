// Mettre à jour la partie sans recharger toute la page.
const formulaire = document.querySelector('#formulaire-jeu');
const champ = document.querySelector('#nombre');
const bouton = document.querySelector('#valider');
const compteur = document.querySelector('#compteur-essais');
const libelle = document.querySelector('#libelle-essais');
const message = document.querySelector('#message');
const liste = document.querySelector('#liste-scores');
const vide = document.querySelector('#scores-vides');
const indisponible = document.querySelector('#scores-indisponibles');

function animer(element) {
  element.classList.remove('anime');
  void element.offsetWidth; // Relancer l'animation même après plusieurs essais.
  element.classList.add('anime');
}

function afficherScores(scores, disponibles) {
  indisponible.hidden = disponibles;
  vide.hidden = !disponibles || scores.length > 0;
  liste.hidden = !disponibles || scores.length === 0;
  liste.replaceChildren();

  for (const score of scores) {
    const ligne = document.createElement('li');
    const joueur = document.createElement('span');
    const resultat = document.createElement('strong');
    joueur.textContent = score.pseudo;
    resultat.textContent = `${score.essais} essai${score.essais === 1 ? '' : 's'}`;
    ligne.append(joueur, resultat);
    liste.append(ligne);
  }
}

formulaire.addEventListener('submit', async (evenement) => {
  evenement.preventDefault();
  bouton.disabled = true;

  try {
    const reponse = await fetch(formulaire.action, {
      method: 'POST',
      headers: {Accept: 'application/json'},
      body: new FormData(formulaire),
    });
    const donnees = await reponse.json();

    if (Number.isInteger(donnees.essais)) {
      compteur.textContent = donnees.essais;
      libelle.textContent = donnees.essais === 1 ? 'essai' : 'essais';
      animer(compteur);
    }
    message.textContent = donnees.message;
    animer(message);
    if (Array.isArray(donnees.scores)) {
      afficherScores(donnees.scores, donnees.scores_disponibles);
    }
    if (reponse.ok) champ.value = '';
  } catch (erreur) {
    message.textContent = 'Impossible de contacter le jeu. Réessaie.';
  } finally {
    bouton.disabled = false;
    champ.focus();
  }
});

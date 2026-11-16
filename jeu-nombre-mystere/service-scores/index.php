<?php
// Service PHP : lire le classement ou enregistrer une victoire en JSON.
header('Content-Type: application/json; charset=utf-8');

function repondre(int $code, array $donnees): void {
    http_response_code($code);
    echo json_encode($donnees, JSON_UNESCAPED_UNICODE);
    exit;
}

$chemin = parse_url($_SERVER['REQUEST_URI'], PHP_URL_PATH);
if ($chemin === '/sante') {
    repondre(200, ['etat' => 'ok']);
}
if ($chemin !== '/scores') {
    repondre(404, ['erreur' => 'Adresse inconnue']);
}

$methode = $_SERVER['REQUEST_METHOD'];
if (!in_array($methode, ['GET', 'POST'], true)) {
    header('Allow: GET, POST');
    repondre(405, ['erreur' => 'Méthode non autorisée']);
}

$nouveau = null;
if ($methode === 'POST') {
    $nouveau = json_decode(file_get_contents('php://input'), true);
    if (!is_array($nouveau)
        || !isset($nouveau['pseudo'], $nouveau['essais'])
        || !is_string($nouveau['pseudo'])
        || !preg_match('/^[\p{L}\p{N} ._-]{1,20}$/u', $nouveau['pseudo'])
        || !is_int($nouveau['essais'])
        || $nouveau['essais'] < 1 || $nouveau['essais'] > 1000) {
        repondre(400, ['erreur' => 'Score invalide']);
    }
}

// Le verrou évite que deux écritures simultanées effacent un score.
$fichier = fopen('/data/scores.json', 'c+');
if ($fichier === false) {
    repondre(500, ['erreur' => 'Impossible de lire les scores']);
}
if (!flock($fichier, $methode === 'POST' ? LOCK_EX : LOCK_SH)) {
    fclose($fichier);
    repondre(500, ['erreur' => 'Impossible de verrouiller les scores']);
}
$contenu = stream_get_contents($fichier);
$scores = $contenu === '' ? [] : json_decode($contenu, true);
if (!is_array($scores) || !array_is_list($scores)) {
    flock($fichier, LOCK_UN);
    fclose($fichier);
    repondre(500, ['erreur' => 'Fichier des scores invalide']);
}

if ($nouveau !== null) {
    $scores[] = ['pseudo' => $nouveau['pseudo'], 'essais' => $nouveau['essais']];
    usort($scores, fn ($a, $b) => $a['essais'] <=> $b['essais']);
    $scores = array_slice($scores, 0, 20);
    rewind($fichier);
    $json = json_encode($scores, JSON_UNESCAPED_UNICODE | JSON_PRETTY_PRINT);
    if ($json === false || !ftruncate($fichier, 0) || fwrite($fichier, $json) === false) {
        flock($fichier, LOCK_UN);
        fclose($fichier);
        repondre(500, ['erreur' => 'Impossible d’enregistrer le score']);
    }
    fflush($fichier);
}
flock($fichier, LOCK_UN);
fclose($fichier);
repondre($nouveau === null ? 200 : 201, ['scores' => $scores]);

# CRIS · ENSA Kénitra

## Lancer la démo sur Windows

Installe Python 3.10 ou plus récent avec le lanceur Windows. Double-clique sur Lancer_CRIS.cmd. Au premier lancement, une connexion Internet permet d'installer Flask. Quand le terminal affiche « Running on », ouvre http://127.0.0.1:5000. Garde la fenêtre ouverte pendant le test. Ctrl+C arrête le serveur.

| Rôle | E-mail | Mot de passe de démonstration |
| --- | --- | --- |
| Utilisateur | leyla@test.com | Test1234 |
| Administrateur | admin@test.com | Admin1234 |

## Vérifier la livraison du groupe 1

1. Essaie un mot de passe incorrect et vérifie le message d’erreur.
2. Connecte-toi avec le compte utilisateur. Bascule le thème et recharge la page.
3. Ouvre /admin avec ce compte. Le résultat attendu est une erreur 403.
4. Déconnecte-toi et ouvre /espace. Tu dois revenir à la connexion.
5. Connecte-toi avec le compte administrateur puis ouvre /admin directement.

Hassan a fourni les routes Flask, le script SQLite et les pages espace et admin. Le formulaire login.html manquait dans le dossier reçu. Le formulaire présent ici a été ajouté pour la démonstration. Les routes de gestion des comptes existent déjà mais les commandes correspondantes restent à intégrer à la page admin.

## Passer le relais

Chaque groupe part de main, travaille dans sa branche puis ouvre une pull request. L’encadrant vérifie le parcours avant la fusion. Conserver les comptes de démonstration et la clé de session fournie pour les essais locaux uniquement.

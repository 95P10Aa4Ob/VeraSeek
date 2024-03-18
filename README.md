# Script de vérification de fichiers

Ce script Python est conçu pour analyser un répertoire spécifié et vérifier certains critères pour chaque fichier pour trouver des conteneurs chiffrés.

## Fonctionnalités

Le script prend en charge les fonctionnalités suivantes :

- Analyse de tous les fichiers d'un répertoire spécifié.
- Vérification de la taille des fichiers :
  - Marque les fichiers dont la taille est un multiple de 512 octets.
- Identification du type de fichier à l'aide de la commande `file --mime-type`.
- Calcul de l'entropie pour chaque fichier à l'aide de la commande `ent`.
- Marquage des fichiers dont l'entropie est supérieure ou égale à 7.9999.
- Affichage des fichiers qui répondent à tous les critères spécifiés.

## Utilisation

Pour utiliser le script, exécutez-le en spécifiant le chemin du dossier à analyser à l'aide de l'option `--dossier`. Par exemple :

python VeraSeek.py --dossier "/chemin/vers/votre/dossier"

Le script parcourra ensuite le dossier spécifié et affichera les informations pour chaque fichier rencontré.


## Dépendances

Ce script a les dépendances suivantes :

- Python 3.x
- Les utilitaires système `file` et `ent` doivent être disponibles dans votre système.

sudo apt install ent -y

Assurez-vous d'installer ces dépendances avant d'exécuter le script.


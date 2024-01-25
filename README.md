#API QCM

Cette API permet de générer des QCM en choisissant un type, des catégories et un nombre de questions.

##Fonctionnalités

La liste des fonctionnalités, leur documentation ainsi que les codes d'erreur est disponible à la route /docs.

##Choix d'architecture

J'ai choisi de séparer mon code en 3 fichiers afin de gagner en lisibilité, maintenabilité, et éviter de répéter le code :

+ Le fichier main.py est le fichier principal, il comprend la gestion des routes, leur documentation ainsi que la gestion des erreurs.
+ Le fichier authorization.py comprend la fonction permettant de gérer l'authentification et la liste des users. J'ai cherché comment créer une fonction pouvant être appelée par chaque route afin de pouvoir vérifier l'authentification dans le header en lui passant le type d'utilisateur autorisé à accéder à cette route. C'est pourquoi j'ai utilisé le système de "Dependencies" de FastAPI.
+ Le fichier data_operations comprend les fonctions de lecture et d'écriture dans la base de donnée (ici le fichier csv) ansi que les fonction de filtres et recherche de valeurs.

##Améliorations

+ Utilisation de async/await pour du code non-bloquant
+ Encodage/hachage des mots de passe pour plus de sécurité

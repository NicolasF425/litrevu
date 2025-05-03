## Site web Pyhon/Django dans le cadre d'une formation

### Description du contexte

L’application permet de :
+ demander des critiques de livres ou d’articles, en créant un billet ;
+ lire des critiques de livres ou d’articles ;
+ publier des critiques de livres ou d’articles ;
+ Suivre un utlilisateur

### **Prérequis :** 

+ Un environnement de développement (VSCode, Pycharm...)
+ Python 3.X
+ avoir installé pip (gestionnaire de packages pour python) s'il n'est pas présent

### exécution des commandes

Sous Windows : avec la ligne de commandes (cmd)

Sous Linux : dans le bash

### Pour récuperer les fichiers du projet :

exécuter : git clone https://github.com/NicolasF425/litrevu.git

### Pour créer l'environnement virtuel _env_

Dans le répertoire du projet exécuter : python -m venv env

Pour activer l'environnement virtuel, Utilisez la commande selon votre système d'exploitation.

**Activation sur Windows :**

exécuter à partir du répertoire projet: env\Scripts\activate

**Activation sur MacOS/Linux :**

exécuter à partir du répertoire projet: source env/bin/activate

### **Pour installer les dépendances :**

Aller dans le répertoire du projet puis exécuter : pip install -r requirements.txt

Le fichier requirements.txt doit être présent dans le dossier du projet

### **Execution du programme :**

Lance le serveur à partir du répertoire du projet :
cd litrevu
python manage.py runserver

Puis dans un navigateur entrer l'url : http://127.0.0.1:8000/ pour lancer l'application

http://127.0.0.1:8000/admin/ permet de lancer la console d'administration

 








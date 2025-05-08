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

### ** Vérifications de conformité avec PEP8

Dans le répertoire du projet, lancer la commande :

flake8 --max-line-length 110 --format=html --htmldir=flake8-report

### **Execution du programme :**

Lance le serveur : à partir du répertoire du projet :

cd litrevu

python manage.py runserver

Puis dans un navigateur entrer l'url : http://127.0.0.1:8000/ pour lancer l'application

http://127.0.0.1:8000/admin/ permet de lancer la console d'administration qui permet d'avoir un aperçu des données en base.

Le compte administrateur est :

login : adminrevu

password : review321

Un utilisateur a été créé pour test:

login : John

password : review321

Attention, le login est sensible à la casse !

### Initialisation de la base de données (si fichier db.sqlite3 non présent) :

python manage.py migrate

python manage.py makemigrations

python manage.py migrate

Puis créer un compte superuser : python manage.py createsuperuser

### Documentation de Django

https://docs.djangoproject.com/en/5.2/



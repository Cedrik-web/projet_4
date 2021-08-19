Projet 4: Développez un programme logiciel en Python.


///////////                Votre Gestionnaire de tournoi d'échec           ///////////////


Le programme, en plus de ce fichier README, ce compose de: 

	- 5 scripts python. 
	- 2 packages python.
	- 1 fichier requirements.txt ( ressources pip nécessaires à installer dans votre 	  			environement virtuel ). 
	- 1 rapport de chaque script avec le fonction flake8.
	  si vous voulez faire un test flake8 il vous suffit de intaller flake8 :
	  		pip install flake8
	  et apres installation appeler la fonction avec le script à verifier :
	  		flake8 "main.py".	
	  plus d'information sur le liens ci-joins:
	  				https://pypi.org/project/flake8/	
	
	
Mise en place du programmme:
	
	
	ETAPE 1 : Mise en place de votre environement virtuel. 
	
	- Dans votre terminal, allez dans le repertoire où se situe le dossier qui contient 	tout les fichiers, les dossiers et srcipts du programme. 
	- Créez votre environement virtuel en tapant : 
		sur windows : python -m venv env 
		sur mac ou Unix : python3 -m venv env
	- En cas de besoin, vous trouverez plus d'informations sur docs.python liens ci-joins: 
					https://docs.python.org/fr/3/library/venv.html
	- Activez votre environement en tapant: 
		sur windows :              env\scripts\activate
		sur mac ou Unix :          source env/bin/activate

	- Vous allez voir apparaitre "(env)" en entête de la ligne de commande. 


	ETAPE 2 : Integration des bibliothèques nécessaires pour l'application. 
	
	- Dans votre environement virtuel que vous venez de créer, importez toutes les 			bibliothèques nécessaires en tapant: 
		pip install -r requirements.txt
		
		
	ETAPE 3 : L'application est prête vous pouvez la lancer en tapant: 
		sur windows :              python main.py	
		sur mac ou Unix :          python3 main.py
		


Bienvenue dans votre gestionnaire de tournoi d'échec:
	
	
	1/ Le programme vous permet:
		- d'ajouter de nouveaux joueurs à votre base de données.
		- de modifier les carctéristiques des joueurs.
		- de créer des tournois.
		- de jouer des tournois.
		- de voir le classement par rang.
		- de genérer des rapports.
		
	2/ Navigation dans le programme:
		
		La navigation s'effectue sur la console.
		Il vous suffit de choisir entre les menus et sous menu la selection  		correspondante à votre besoin.
		Pour sortir du programme sur le menu principal il vous suffit de taper 8.

	3/ La sauvegarde de la base de donnée:
		La sauvegarde de votre base de donnée se fait en local sur un fichier            			json généré automatiquement lors de la première sauvegarde	 			effectuée.
		Ce fichier se nomme db.json et sera dans les dossiers du programme.	
		
	4/ Création d'un tournoi:
		Vous pouvez créer un tournoi à l'avance.
		Dans ce cas il vous faudra répondre "non" à la question "voulez vous 			commencer le tournoi?"	
		Vous sortirez alors du programme.
		Pour relancer le programme:
			suivez de nouveau l'ETAPE 3	
			
	5/ Cas particulier:
		Vous pouvez à tout moment sortir du programme avec l'action :
			Ctrl + c
		Dans le cas de cette fermeture forcée aucune sauvegarde ne			 			sera faite.				
		 

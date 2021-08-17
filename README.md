Projet 4: Développez un programme logiciel en Python.


///////////                Votre Gestionnaire de tournoi d'échec           ///////////////


Le programme, en plus de ce fichier README, ce compose de: 

	- 5 scripts python. 
	- 2 packages python.
	- 1 fichier requirements.txt ( ressources pip nécessaires à installer dans votre 	  			environement virtuel ). 
	- 1 fichier .gitignore ( sert a exclure les fichiers non pris en charge par git ).
	
	
	
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


	ETAPE 2 : Integration des bibliothèques nécesaires pour l'application. 
	
	- Dans votre environement virtuel que vous venez de créer, importez toutes les 			bibliothèques nécesaires en tapant: 
		pip install -r requirements.txt
		
		
	ETAPE 3 : L'application est prête vous pouvez la lancer en tapant: 
		sur windows :              python main.py	
		sur mac ou Unix :          python3 main.py
		


Bienvenue dans votre gestionnaire de tournoi d'échec:
	
	
	1/ Le programme vous permet:
		- d'ajouter des nouveaux joueurs à votre base de données.
		- de modifier les carctéristiques des joueurs.
		- de créer des tournois.
		- de jouer des tournois.
		- de voir le classements par rang.
		- de genéré des rapports.
		
	2/ Navigation dans le programme:
		
		La navigation s'effectue sur la console.
		Il vous suffit de choisir entre les menus et sous menu la selection  		correspondante à votre besoin.
		Pour sortir du programme sur le menu principal il vous suffit de tapez 8.

	3/ La sauvegarde de la base de donnée:
		La sauvegarde de votre base de donnée ce fait en local sur un fichier            			json généré automatiquement lors de la première sauvegarde	 			effectuer.
		Ce fichier ce nomme db.json et sera dans me dossier du programme.		
		 

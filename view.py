
class ViewMenu:

    def print_accueil(self):
        ''' menu printing and retrieval of menu choice '''

        print()
        print("Bienvenue sur le gestionnaire de jeu d'échec.\n")
        print("Selectionnez le menu souhaité.\n")
        print(" 1 : ajouter un joueur.")
        print(" 2 : modifier un joueur.")
        print(" 3 : création d'un tournoi.")
        print(" 4 : jouer un tournoi créé.")
        print(" 5 : classement.")
        print(" 6 : modification du classement.")
        print(" 7 : rapport.")
        print(" 8 : sortir du logiciel.")
        print("\nQuelle est votre choix : ")
        resultat = input()
        return resultat

    def print_error_enter_int(self):
        ''' indicates to the user that he must enter a number '''

        print("\n ERREUR : vous devez entrer un chiffre correspondant à votre choix .")

    def print_modif_ok(self):  # TODO
        ''' printing modification to carry out '''

        print("modification effectuée avec succès !")

    def print_error_id(self):
        ''' display a message in console '''

        print("ERREUR, il y a une erreur dans l'ID, recommencez")

    def print_pass_validation(self):
        ''' display a message in console '''

        print("\ncontinuez......")
        input("appuyez sur entrée pour revenir au menu")
        print("\n" * 25)

    def print_classement(self, player_classement):
        ''' display a message in console '''

        print("\nclassement à ce jour :\n")
        rang = 0
        for i in player_classement:
            rang += 1
            print("n°", rang, i.get("pk"), "avec", i.get("ranking"), "point(s).")

    def print_list_of_tournaments(self, tournament):
        ''' display a message in console '''

        print("\nliste des tournois joués.")
        for i in tournament:
            print(i.get("pk"))

    def print_classement_alphabet(self, player_classement):
        ''' display a message in console '''

        print("\nclassement joueurs par ordre alphabetique :\n")
        for i in player_classement:
            print(i.get("name"), i.get("first_name"), " nombre de points :", i.get("ranking"))

    def print_menu_stat(self):
        ''' displays in console the stats menu and returns the voice made '''

        print("\n" * 50)
        print("Bienvenue dans la catégorie rapport, veuillez selectionner la stat recherchée :\n")
        print("1 : pour la liste de tous les joueurs par classement.")
        print("2 : pour la liste de tous les joueurs par ordre alphabétique.")
        print("\n3 : pour la liste des joueurs d'un tournoi, par classement.")
        print("4 : pour la liste des joueurs d'un tournoi, par ordre alphabétique.")
        print("\n5 : pour la liste de tous les tournois.")
        print("6 : pour la liste de tous les tours d'un tournoi.")
        print("7 : pour la liste de tous les matchs d'un tournoi.")
        print("\n8 : pour revenir au menu principal.")
        resultat = input()
        try:
            while not 0 < int(resultat) <= 8:
                print("ERREUR, vous devez entrer le nombre "
                      "en entête de votre selection.")
                resultat = input()
        except ValueError:
            print("ERREUR, vous devez entrer un nombre valide.")
            self.print_menu_stat()
        return resultat

    def print_exicting_player(self, p):  # TODO
        ''' display a message in console '''

        print("le joueur ", p.get("pk"), " est déja enregistré !")

    def print_list_tournament(self, i):
        ''' display a message in console '''

        print("ID du tournoi :", i.get("pk"))

    def print_choice_tournament(self, ):
        ''' display a information and retrun a variable '''

        print("\nchoisissez votre tournoi par l'ID")
        choix = input()
        return choix

    def print_classement_of_tournament(self):
        ''' display a message in console'''

        print("\nclassement du tournoi :\n")

    def print_tri_player_of_tournament_rank(self, i, p):
        ''' display a message in console'''

        print("n°", p, i.get("pk"), "avec", i.get("ranking"), "point(s).")

    def print_tri_player_of_tournament_alphabet(self, i):
        ''' display a message in console'''

        print(i.get("pk"), "avec", i.get("ranking"), "point(s).")

    def print_classement_player_of_tournament(self):
        ''' display a message in console'''

        print("\njoueur du tournoi :\n")

    def print_list_tournaments(self, tournament):
        ''' display a message in console'''

        print("\nlistes des tours pour le tournoi ", tournament.get("pk"))
        print()

    def print_tournament_time(self, t):
        ''' display a message in console'''

        print("temps de jeu du round " + str(t))

    def print_tournament_resultat(self, resultat):
        ''' display a message in console'''

        print("début : ", resultat[0])
        print("fin : ", resultat[-1])

    def print_list_match_by_tournament(self, tournament):
        ''' display a message in console'''

        print("\nlistes des matchs pour le tournoi", tournament.get("pk"))
        print()

    def print_resultat_match(self, t):
        ''' display a message in console'''

        print("resultat du round " + str(t))

    def print_list_resultat_match(self, i, j):
        ''' display a message in console'''

        print("match :", i)
        print("        remporté par: ", j)

    def print_menu_existing(self):
        ''' display a message in console'''

        print("ERREUR vous devez choisir un menu existant")

    def print_choice_input_menu(self, resultat):
        ''' display a message in console'''

        resultat_int = int(resultat)
        return resultat_int

    def print_space1(self):
        ''' display 1 space '''

        print()

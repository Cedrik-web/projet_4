
from model import CleanText


# view set use for tournament menu
class ViewMenuTournament:

    def print_starting_round(self, tour):
        '''display a message in console'''

        tours = tour + 1
        print("\n- Liste des matches à jouer pour le round", str(tours))
        print()


# view set used by multiple classes
class ViewShare:

    def print_error(self):
        ''' display a message in console '''

        print("ERREUR")


# view set use for tournament management
class ViewTournament(CleanText):

    def print_tournament_existing(self):
        # informs that the tournament created has already been registered

        print("\nce tournoi existe deja ...\n")

    def print_sex_control(self):
        ''' control the input console for the sex of the player '''

        print("\nentrez 1 pour un joueur de sex masculin")
        print("entrez 2 pour un joueur de sex féminin\n")
        sex = CleanText.clean_input(CleanText, input())
        if sex == "1":
            sex = "homme"
            return sex
        elif sex == "2":
            sex = "femme"
            return sex
        else:
            print("ERREUR , veuillez choisir le numéro correspndant au sex.")
            self.print_sex_control(sex)

    def print_control_day(self):
        '''control input day'''

        while True:
            try:
                while True:
                    print("\nentrez le jour.")
                    day = int(input("                 jour :"))
                    if 0 < day < 32:
                        return day
                    else:
                        print("ERREUR, veuillez entrer un chiffre entre 1 et 31.")
            except ValueError:
                print("\nERREUR , veuillez entrer des chiffres")
                print("Veuillez recommencer\n")

    def print_control_month(self):
        '''control input month'''

        while True:
            try:
                while True:
                    print("entrez le mois.")
                    month = int(input("                 mois :"))
                    if 0 < month < 13:
                        return month
                    else:
                        print("ERREUR, veuillez entrer un chiffre entre 1 et 31.")
            except ValueError:
                print("\nERREUR , veuillez entrer des chiffres")
                print("Veuillez recommencer\n")

    def print_control_years(self):
        '''control input year'''

        while True:
            try:
                while True:
                    print("entrez l'année complete, avec 4 nombres.")
                    year = int(input("                 année :"))
                    if 1930 < year < 2100:
                        return year
                    else:
                        print("ERREUR, veuillez entrer l'année complete.")
            except ValueError:
                print("\nERREUR , veuillez entrer des chiffres")
                print("Veuillez recommencer\n")

    def print_elements_player(self):
        ''' retrieving player items and putting all items in dictionary '''

        print("entrez le nom de famille du joueur")
        name = CleanText.clean_input(CleanText, input())
        print("entrez le prénom du joueur")
        first_name = CleanText.clean_input(CleanText, input())
        print("entrez la date de naissance")
        from tournament.controller import MethodeTournament
        birth_date = MethodeTournament.print_date_controller(MethodeTournament)
        print(name, first_name, "et né le", birth_date)
        sex = self.print_sex_control(self)
        print("entrez les points du joueur")
        ranking = 0
        while ranking != int:
            try:
                nb = int(input())
                ranking += nb
                break
            except ValueError:
                print("\nERREUR , veuillez rentrer un nombre entier")
                print("recomencer")
        print("nombre de point et de : ", ranking)
        elements = {
            "name": name,
            "first_name": first_name,
            "birth_date": birth_date,
            "sex": sex,
            "ranking": ranking,
            }
        return elements

    def print_add_genaral_remarks(self):
        ''' adding the description of a tournament to the tournament object '''

        print("ajoutez , si vous le voulez, une description ou un commentaire au tournoi :")
        remarks = []
        resultat = input()
        remarks.append(resultat)
        return remarks

    def print_add_timer_control(self):
        """ adding the timer mode of a tournament """

        print("quelle mode de jeu souhaitez vous ?")
        print("1 : un bullet")
        print("2 : un blitz")
        print("3 : un coup rapide")
        resultat = input()
        timer_control = []
        if int(resultat) == 1:
            timer_control.append("bullet")
        elif int(resultat) == 2:
            timer_control.append("blitz")
        elif int(resultat) == 3:
            timer_control.append("coup rapide")
        else:
            print("\n ERREUR : vous devez entrer un chiffre correspondant à votre choix .")
            self.print_add_timer_control(self)
        return timer_control

    def print_elements_tournament(self):
        ''' get tournament items and return a dictionary '''

        print("entrez le nom du tournoi")
        name = CleanText.clean_input(CleanText, input())
        print("entrez le lieu du tournoi")
        location = CleanText.clean_input(CleanText, input())
        print("entrez la date du tournoi")
        from tournament.model import Tournament
        from tournament.controller import MethodeTournament
        date = MethodeTournament.print_date_controller(MethodeTournament)
        elements = {
            "name": name,
            "location": location,
            "date": date,
            }
        return elements

    def print_not_list_player_existing(self):
        '''display a information in the console'''

        print("il ne semble pas avoir de joueur enregistrer, veuillez créer le joueur.")

    def print_menu_ajout_players_for_tournament(self):
        ''' displays in console a menu (addition of a player in the tournament creation)
            and takes care of the cases errors '''

        while True:
            try:
                print()
                print(" 1: pour la liste des joueur existants :")
                print((" 2: pour créer un nouveau joueur :"))
                choix = int(CleanText.clean_input(CleanText, input()))
                if 0 < choix < 3:
                    return choix
            except ValueError:
                print("vous devez entrer un chiffre correspondant à votre choix.")

    def print_add_players_for_tournament(self):
        ''' display information and return a variable '''

        print("\nentrez l'ID du joueur selectionné ")
        participant = CleanText.clean_input(CleanText, input())
        return participant

    def print_add_player_impossible(self, existing):
        ''' display a message in console '''

        print("creation impossible car ce joueur est deja existant et son ID est",
              existing.get("pk"))

    def print_add_players_for_tournament_inpossible(self):
        ''' display a message in console '''

        print("\nce joueur est déja selectionné .")

    def print_save_players_for_tournament(self, compteur, nb_player):
        ''' display a message in console '''

        print("participant n°", compteur, "/", nb_player, "bien enregistré ! \n")

    def print_error_id_tournament(self):
        ''' display a message in console '''

        print("ERREUR, l'identifiant saisi n'existe pas!")

    def print_start_tournament(self):
        ''' display information and return a variable '''

        print("\n")
        print("Pour commencer le round et activé le chrono,")
        reponse = input("appuyez sur ENTREE                           ou non pour sortir: ")
        return reponse

    def print_find_tournament(self):
        ''' display a message in console '''

        print("\nrecherche de tournois créés et non finalisés.\n")

    def print_tournament_finished(self, i):
        ''' display a message in console'''

        print("tournoi fini :", "le", i.get("name"), "de", i.get("location"), "du", i.get("date"))

    def print_space(self):
        ''' display 1 space '''

        print()

    def print_tournament_not_start(self, i):
        ''' display a message in console'''

        print("tournois non commencés voici leurs ID :", i.get("pk"))

    def print_tournament_start(self, i):
        ''' display a message in console'''

        print("tournois non finalisés voici leurs ID :")
        print(" - ", i.get("pk"))

    def print_input_selection_tournament(self):
        ''' display a message in console and return a variable'''

        reponse = CleanText.clean_input(CleanText,
                                        input("entrez l'ID ou appuiez ENTREE pour sortir de la selection: "))
        return reponse

    def print_list_players_alphabet(self, player_classement):
        ''' display a message in console '''

        print("\nlistes des joueurs par ordre alphabetique :\n")
        for i in player_classement:
            print(i.get("name"), i.get("first_name"), " sont ID :", i.get("pk"))

    def print_continue(self):
        '''display a message in console'''

        print("appuyer sur ENTREE pour continuer...")
        input()


# view set use for match management
class ViewMatch:

    def print_ending_other_round(self, tour):
        ''' display a message in console '''

        print("---------------------------round : " + str(tour) + " terminé----------------------------\n")

    def print_view_match_possition(self, m):
        ''' display a information in console '''

        print("\nmatch n°", m, ":")

    def print_view_match(self, i):
        ''' display a information in console '''

        print(i.get("pk"))

    def print_start_chrono(self, date):
        ''' display a message in console '''

        print("\ndate et heure du debut de round:", date)

    def print_ending_chrono(self, date):
        ''' display a message in console '''

        print("date et heure de fin de round", date)

    def print_menu_match_tournament(self, match, joueur1, joueur2):
        ''' affiche le menu de score de match '''

        print("\n resultat pour le match :", match, "\n")
        print(" - tapez 1 si", joueur1.get('pk'), "a gagné.")
        print(" - tapez 2 si", joueur2.get('pk'), "a gagné.")
        print(" - si PAT tapez 3")
        resultat = int(input("                                    : "))
        return resultat

    def print_player_winner(self, joueur):
        ''' display a message in console '''

        print("                                                         ",
              joueur.get('pk'), " GAGNE !!\n")

    def print_player_pat(self):
        ''' display a message in console '''

        print("                                     match nul \n")

    def print_ending_first_round(self):
        ''' display a message in console '''

        print("---------------------------round : 1 terminé----------------------------\n")

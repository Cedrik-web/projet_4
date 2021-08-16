

def clean_input_tournament(data):
    ''' general function to protect the program from
        incorrect user input '''

    tiny = data.lower()
    text = tiny.replace(" ", "-")
    char = "!#$%&*()"
    for i in char:
        text = text.replace(i, "")
    accent = "éèêë"
    for a in accent:
        text = text.replace(a, "e")
    accent_a = text.replace("à", "a")
    accent_u = accent_a.replace("ù", "u")
    new_data = accent_u
    return new_data


def print_add_genaral_remarks():
    ''' adding the description of a tournament to the tournament object '''

    print("ajoutez , si vous le voulez, une description ou un commentaire au tournoi :")
    remarks = []
    resultat = input()
    remarks.append(resultat)
    return remarks


def print_add_timer_control():
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
        print_add_timer_control()
    return timer_control


def print_elements_tournament():
    ''' get tournament items and return a dictionary '''

    print("entrer le nom du tournoi")
    name = clean_input_tournament(input())
    print("entrer le lieu du tournoi")
    location = clean_input_tournament(input())
    print("entrer la date du tournoi")
    date = print_date_controller_tournament()
    elements = {
        "name": name,
        "location": location,
        "date": date,
        }
    return elements


def print_date_controller_tournament():
    ''' control the input console for the birth date of the player '''

    while True:
        try:
            print("\nrentrer le jour.")
            day = int(input("                 jour :"))
            if 0 < day < 32:
                pass
            else:
                print("ERREUR, veuillez rentrer un chiffre entre 1 et 31.")
            print("rentrer le mois.")
            month = int(input("                 mois :"))
            if 0 < month < 13:
                pass
            else:
                print("ERREUR, veuillez rentrer un chiffre entre 1 et 31.")
            print("entrer l'année complete, avec 4 nombres.")
            year = int(input("                 année :"))
            if 1930 < year < 2100:
                pass
            else:
                print("ERREUR, veuillez rentrer l'année complete.")
            day_str = str(day)
            month_str = str(month)
            if len(month_str) == 1:
                str_month = "0" + month_str
            else:
                str_month = str(month)
            if len(day_str) == 1:
                str_day = "0" + day_str
            else:
                str_day = str(day)
            birth_date = str_day + "/" + str_month + "/" + str(year)
            return birth_date
        except ValueError:
            print("\nERREUR , veuillez rentrer des chiffres")
            print("Veuillez recommencer\n")


def print_menu_ajout_players_fot_tournament():
    ''' displays in console a menu (addition of a player in the tournament creation)
        and takes care of the cases errors '''

    while True:
        try:
            print()
            print(" 1: pour la liste des joueur existante :")
            print((" 2: pour créer un nouveau joueurs :"))
            choix = int(clean_input_tournament(input()))
            if 0 < choix < 4:
                return choix
        except ValueError:
            print("vous devez rentrer un chiffre correspondant a votre choix.")


def print_add_players_for_tournament():
    ''' display information and return a variable '''

    print("\nrentrer l'ID du joueur selectionner ")
    participant = clean_input_tournament(input())
    return participant


def print_add_player_impossible(existing):
    ''' display a message in console '''

    print("creation impossible car ce joueur est deja existant et sont ID est", existing.get("pk"))


def print_add_players_for_tournament_new():
    ''' display a message in console '''

    print("\nce joueur est déja selectionner .")


def print_save_players_for_tournament(compteur, nb_player):
    ''' display a message in console '''

    print("participant n°", compteur, "/", nb_player, "bien enregistrer ! \n")


def print_start_chrono(date):
    ''' display a message in console '''

    print("\ndate et heure du début de round:", date)


def print_ending_chrono(date):
    ''' display a message in console '''

    print("date et heure de fin de round", date)


def print_menu_match_tournament(match, joueur1, joueur2):
    ''' affiche le menu de score de match '''

    print("\n resultat pour le match :", match, "\n")
    print(" - tape 1 si", joueur1.get('pk'), "a gagner.")
    print(" - tape 2 si", joueur2.get('pk'), "a gagner.")
    print(" - si pat tapez 3")
    resultat = int(input("                                    : "))
    return resultat


def print_player_winner(joueur):
    ''' display a message in console '''

    print("                                                         ", joueur.get('pk'), " GAGNE !!\n")


def print_player_pat():
    ''' display a message in console '''

    print("                                     match nul \n")


def print_error():
    ''' display a message in console '''

    print("ERREUR")


def print_ending_first_round():
    ''' display a message in console '''

    print("---------------------------round : 1 terminé----------------------------\n")


def print_ending_other_round(tour):
    ''' display a message in console '''

    print("---------------------------round : " + str(tour) + " terminé----------------------------\n")


def print_start_tournament():
    ''' display information and return a variable '''

    print("\n")
    print("Pour commencer le round et activé le chrono,")
    reponse = input("appuyer sur ENTRER                            ou non pour sortir: ")
    return reponse
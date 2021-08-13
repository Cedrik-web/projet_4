from model import clean_input
from player.view import print_date_controller
from view import print_error_enter_int


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
        print_error_enter_int()
        print_add_timer_control()
    return timer_control


def print_elements_tournament():
    ''' get tournament items and return a dictionary '''

    print("entrer le nom du tournoi")
    name = clean_input(input())
    print("entrer le lieu du tournoi")
    location = clean_input(input())
    print("entrer la date du tournoi")
    date = print_date_controller()
    elements = {
        "name": name,
        "location": location,
        "date": date,
        }
    return elements


def print_menu_ajout_players_fot_tournament():
    ''' displays in console a menu (addition of a player in the tournament creation)
        and takes care of the cases errors '''

    while True:
        try:
            print()
            print(" 1: pour la liste des joueur existante :")
            print((" 2: pour créer un nouveau joueurs :"))
            choix = int(clean_input(input()))
            if 0 < choix < 4:
                return choix
        except ValueError:
            print("vous devez rentrer un chiffre correspondant a votre choix.")


def print_add_players_for_tournament():
    activate()
    print("\nrentrer l'ID du joueur selectionner ")
    participant = clean_input(input())
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

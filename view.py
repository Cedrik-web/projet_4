from model import clean_input


def print_accueil():
    ''' menu printing and retrieval of menu choice '''

    print()
    print("Bienvenue sur le gestionnaire de jeu d'échec.\n")
    print("Selectionner le menu souhaiter.\n")
    print(" 1 : ajouter un joueur.")
    print(" 2 : modification d'un joueur.")
    print(" 3 : création d'un tournoi.")
    print(" 4 : jouer un tournoi créer.")
    print(" 5 : classements.")
    print(" 6 : modification du classements.")
    print(" 7  : rapports.")
    print(" 8 : sortir du logiciel.")
    print("\nQuelle est votre choix : ")
    resultat = input()
    return resultat


def print_modif_classement(player):
    print("total de points : " + str(player.get("ranking")) + " , tapez oui pour modifier -> ")
    reponse = clean_input(input())
    ranking = player.get("ranking")
    if reponse == "oui":
        while ranking != int:
            try:
                nb = int(input(": "))
                ranking = nb
                break
            except:
                print("\nERREUR , veuillez rentrer un nombre entier")
                print("recomencer")
    print(ranking)
    if not ranking == int(player.get("ranking")):
        player.update({"ranking": ranking})
        print("nouveau total de points : " + str(player.get("ranking")) + "\n")
    print()
    return player


def print_error_enter_int():
    ''' indicates to the user that he must enter a number '''

    print("\n ERREUR : vous devez entrer un chiffre correspondant à votre choix .")


def print_modif_ok():
    ''' printing modification to carry out '''

    print("modification effectuer avec succès !")



def print_pass_validation():
    ''' display a message in console '''

    print("\ncontinuez......")
    input("appuyer sur entrée pour revenir au menu")
    print("\n" * 25)


def print_classement(player_classement):
    ''' display a message in console '''

    print("\nclassement à ce jour :\n")
    rang = 0
    for i in player_classement:
        rang += 1
        print("n°", rang, i.get("pk"), "avec", i.get("ranking"), "point(s).")


def print_list_of_tournaments(tournament):
    ''' display a message in console '''

    print("\nliste des tournois jouer.")
    for i in tournament:
        print(i.get("pk"))


def print_classement_alphabet(player_classement):
    ''' display a message in console '''

    print("\nclassement joueurs par ordre alphabetique :\n")
    for i in player_classement:
        print(i.get("name"), i.get("first_name"), " nombre de points :", i.get("ranking"))


def print_list_players_alphabet(player_classement):
    ''' display a message in console '''

    print("\nlistes des joueurs par ordre alphabetique :\n")
    for i in player_classement:
        print(i.get("name"), i.get("first_name"), " sont ID :", i.get("pk"))


def print_menu_stat():
    ''' displays in console the stats menu and returns the voice made '''

    print("\n" *50)
    print("Bienvenue dans la catégorie rapport, veuillez selectionner la stat rechercher :\n")
    print("1 : pour la liste de tous les joueurs par classement.")
    print("2 : pour la liste de tous les joueurs par ordre alphabétique.")
    print("\n3 : pour la liste des joueurs d'un tournoi, par classement.")
    print("4 : pour la liste des joueurs d'un tournoi, par ordre alphabétique.")
    print("\n5 : pour la liste de tous les tournoi.")
    print("6 : pour la liste de tous les tours d'un tournoi.")
    print("7 : pour la liste de tous les matchs d'un tournoi.")
    print("\n8 : pour revenir au menu principal.")
    resultat = input()
    try:
        while not 0 < int(resultat) <= 8:
            print("ERREUR, vous devez rentrer le nombre en entete de votre selection.")
            resultat = input()
    except:
        print("ERREUR, vous devez rentrer un nombre valide.")
        print_menu_stat()
    return resultat


def print_error_id():
    ''' display a message in console '''

    print("ERREUR, il y a une erreur dans ID recommencer")


def print_exicting_player(p):
    ''' display a message in console '''

    print("le joueur ", p.get("pk"), " est déja enregistrer !")


def print_new_player_register():
    ''' display a message in console '''

    print("le joueur a etait enregister et rajouter au tounoi.")


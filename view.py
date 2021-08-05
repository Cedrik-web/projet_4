from model import clean_input, activate


def print_accueil():
    ''' menu printing and retrieval of menu choice '''

    print()
    print("Bienvenue sur le gestionnaire de jeu d'échec .\n")
    print("Selectionner le menu souhaiter .\n")
    print(" 1 : ajouter un joueur .")
    print(" 2 : modification d'un joueur .")
    print(" 3 : création d'un tournoi .")
    print(" 4 : classements .")
    print(" 5 : modification du classements .")
    print(" 6 : rapports .")
    print(" 7 : sortir du logiciel .")
    print("\nQuelle est votre choix : ")
    resultat = input()
    return resultat

def print_elements_player():
    ''' retrieving player items and putting all items in dictionary '''

    print("entrer le nom du joueur")
    name = clean_input(input())
    print("entrer le prénom du joueur")
    first_name = clean_input(input())
    print("entrer la date de naissance")
    birth_date = print_date_controller()
    print(name, first_name, "et né le", birth_date)
    sex = print_sex_control()
    print("entrer les points du joueur")
    ranking = 0
    while ranking != int:
        try:
            nb = int(input())
            ranking += nb
            break
        except:
            print("\nERREUR , veuillez rentrer un nombre entier")
            print("recomencer")
    print("nombre de point et de : ",ranking)
    elements = {
        "name": name,
        "first_name": first_name,
        "birth_date": birth_date,
        "sex": sex,
        "ranking": ranking,
        }
    return elements

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


def print_sex_control():
    ''' control the input console for the sex of the player '''

    print("\nentrer 1 pour un joueur de sex masculin")
    print("entrer 2 pour un joueur de sex féminin\n")
    sex = clean_input(input())
    if sex == "1":
        sex = "homme"
        return sex
    elif sex == "2":
        sex = "femme"
        return sex
    else:
        print("ERREUR , veuillez choisir le numéro correspndant au sex.")
        print_sex_control()

def print_date_controller():
    ''' control the input console for the birth date of the player '''

    day = input("                 jour :")
    month = input("                 mois :")
    years = input("l'année en 4 chiffres :")
    try:
        nb = int(day) + int(month) + int(years)
        if 1950 < nb < 2100:
            print()
        else:
            print("\nERREUR , veullez rentrer votre année de naissance complete")
            print("Veuillez recommencer\n")
            print_date_controller()
        nb_years = len(years)
        if nb_years == 4:
            years = years
        else:
            print("\nERREUR , veuillez rentrer l'année avec 4 chiffres")
            print("Veuillez recommencer\n")
            print_date_controller()
        nb_day = len(day)
        if nb_day == 2 and 0 < int(day) < 32:
            day = day
        else:
            print("\nERREUR , veuillez rentrer votre jour de naissance avec 2 chiffres, exemple 02 :")
            print("Veuillez recommencer\n")
            print_date_controller()
        nb_month = len(month)
        if nb_month == 2 and 0 < int(month) < 13:
            month = month
        else:
            print("\nERREUR , veuillez rentrer votre mois de naissance avec 2 chiffres, exemple 05 :")
            print("Veuillez recommencer\n")
            print_date_controller()
        birth_date = day + "/" + month + "/" + years
        return birth_date
    except:
        print("\nERREUR , veuillez rentrer des chiffres")
        print("Veuillez recommencer\n")
        print_date_controller()

def print_add_player():
    ''' function requesting the creation of a new player
        following a player creation and this as long as the users
        wants by answering yes '''

    serialized_player = []
    serialized_player.append(print_elements_player())
    print("voulez vous rajouter un autre joueur ?")
    reponse = clean_input(input())
    while reponse == "oui":
        serialized_player.append(print_elements_player())
        print("voulez vous rajouter un autre joueur ?")
        reponse = clean_input(input())
    return serialized_player

def print_find_player():
    ''' printing the search request for a player then retrieving the
        choice '''

    print()
    print("recherche par ID ('non'_'premon'_'année de naissance') ou par nom:")
    resultat = clean_input(input())
    print()
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

def print_modif_player(player):
    ''' function displaying all the elements of a player and
        allowing to retrieve the possible change and return a dictionary
        with these elements '''

    print("modifier les valeurs que vous désirez à la suite de la valeur renseigner .")
    print("ou taper entrer pour passer . \n")
    a = clean_input(input("nom :" + player.get("name") + " -> "))
    if not a == "":
        player.update({"name": a})
        print("nouveau nom : " + player.get("name") + "\n")
    b = clean_input(input("prénom :" + player.get("first_name") + " -> "))
    if not b == "":
        player.update({"first_name": b})
        print("nouveau prénom : " + player.get("first_name") + "\n")
    print("né le " + player.get("birth_date") + " , tapez oui pour modifer ->")
    reponse = clean_input(input())
    if reponse == "oui":
        c = print_date_controller()
    else:
        c = ""
    if c == player.get("birth_date"):
        player.update({"birth_date": c})
        print("nouvelle date de naissance : " + player.get("birth_date") + "\n")
    print("sex : " + player.get("sex") + " , tapez oui pour modifier ->")
    reponse == clean_input(input())
    if reponse == "oui":
        d = print_sex_control()
    else:
        d = ""
    if d == player.get("sex"):
        player.update({"sex": d})
        print("sex redéfini : " + player.get("sex") + "\n")
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

def print_display_player_list(player):
    ''' printing a list of players with the same name '''

    print(player.get("name"), player.get("first_name"))
    print("son ID est : ", player.get("pk"), "\n")

def print_display_player_nb(nb_player, player):
    ''' print the number of existing players for the search then return
        to the menu to make a new request with ID '''

    print("il y a ", nb_player, " resultat pour la recherche : ", player)
    print("veuillez utiliser ID du joueur ")

def print_modif_ok():
    ''' printing modification to carry out '''

    print("modification effectuer avec succès !")

def print_elements_tournament():
    ''' get tournament items and return a dictionary '''

    print("entrer le nom du tournoi")
    name = clean_input(input())
    print("entrer le lieu du tournoi")
    location = clean_input(input())
    print("entrer la date du tournoi")
    date = print_date_tournament_controller()
    elements = {
        "name": name,
        "location": location,
        "date": date,
        }
    return elements

def print_date_tournament_controller():
    ''' control the input console for the date of the tournament '''

    day = input("                 jour :")
    month = input("                 mois :")
    years = input("l'année en 4 chiffres :")
    try:
        nb = int(day) + int(month) + int(years)
        if 1950 < nb < 2100:
            print()
        else:
            print("\nERREUR , veullez l'année complete")
            print("Veuillez recommencer\n")
            print_date_tournament_controller()
        nb_years = len(years)
        if nb_years == 4:
            years = years
        else:
            print("\nERREUR , veuillez rentrer l'année avec 4 chiffres")
            print("Veuillez recommencer\n")
            print_date_tournament_controller()
        nb_day = len(day)
        if nb_day == 2 and 0 < int(day) < 32:
            day = day
        else:
            print("\nERREUR , veuillez rentrer le jour avec 2 chiffres, exemple 02 :")
            print("Veuillez recommencer\n")
            print_date_tournament_controller()
        nb_month = len(month)
        if nb_month == 2 and 0 < int(month) < 13:
            month = month
        else:
            print("\nERREUR , veuillez rentrer le mois  avec 2 chiffres, exemple 05 :")
            print("Veuillez recommencer\n")
            print_date_tournament_controller()
        tournament_date = day + "/" + month + "/" + years
        return tournament_date
    except:
        print("\nERREUR , veuillez rentrer des chiffres")
        print("Veuillez recommencer\n")
        print_date_tournament_controller()

def print_pass_validation():
    print("\ncontinuez......")
    input("appuyer sur entrée pour revenir au menu")
    print("\n" * 25)

def print_classement(player_classement):
    print("\nclassement à ce jour :\n")
    rang = 0
    for i in player_classement:
        rang += 1
        print("n°", rang, i.get("pk"), "avec", i.get("ranking"), "point(s).")

def print_list_of_tournaments(tournament):
    print("\nliste des tournois jouer.")
    print(tournament.get("pk"))

def print_classement_alphabet(player_classement):
    print("\nclassement joueurs par ordre alphabetique :\n")
    for i in player_classement:
        print(i.get("name"), i.get("first_name"), " nombre de points :", i.get("ranking"))

def print_menu_stat():
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

# -START-------------printing functions of various small information or exception-------
def print_add_players_for_tournament():
    activate()
    print("rentrer l'ID ou le nom du joueur participant")
    participant = clean_input(input())
    return participant

def print_add_newplayer_for_tournament():
    print("\nrentrer l'ID du joueur participant ou + pour creer un joueur")
    resultat = clean_input(input())
    return resultat

def print_add_players_for_tournament_new():
    activate()
    print("ce joueur est déja selectionner .")
    participant = clean_input(input())
    return participant

def print_save_players_for_tournament(compteur, nb_player):
    print("participant n°", compteur, "/", nb_player, "bien enregistrer ! \n")

def print_player_find(player):
    print("\nil y a ", len(player), "joueurs enregister")

def print_list_player_find(player, resultat):
    print(resultat, player.get("first_name"), " = ", player.get("pk"))

def print_error_id():
    print("ERREUR, il y a une erreur dans ID recommencer")

def print_exicting_player(p):
    for i in p:
        print("le joueur ", i.get("pk"), " est déja enregistrer !")

def print_new_player_register(p):
    for i in p:
        print("le joueur ", i.get("name"), " a etait enregister sous ID :", i.get("pk"))

# -END-------------------------------------------------------------------------------
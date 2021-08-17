from view import clean_input


def print_list_players_alphabet(player_classement):
    ''' display a message in console '''

    print("\nlistes des joueurs par ordre alphabetique :\n")
    for i in player_classement:
        print(i.get("name"), i.get("first_name"), " sont ID :", i.get("pk"))


def print_new_player_register():
    ''' display a message in console '''

    print("le joueur a été enregisté et rajouté au tounoi.")


def print_elements_player():
    ''' retrieving player items and putting all items in dictionary '''

    print("entrez le nom de famille du joueur")
    name = clean_input(input())
    print("entrez le prénom du joueur")
    first_name = clean_input(input())
    print("entrez la date de naissance")
    birth_date = print_date_controller()
    print(name, first_name, "et né le", birth_date)
    sex = print_sex_control()
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


def print_sex_control():
    ''' control the input console for the sex of the player '''

    print("\nentrez 1 pour un joueur de sex masculin")
    print("entrez 2 pour un joueur de sex féminin\n")
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

    while True:
        try:
            print("\nentrez le jour.")
            day = int(input("                 jour :"))
            if 0 < day < 32:
                pass
            else:
                print("ERREUR, veuillez entrer un chiffre entre 1 et 31.")
            print("entrez le mois.")
            month = int(input("                 mois :"))
            if 0 < month < 13:
                pass
            else:
                print("ERREUR, veuillez entrer un chiffre entre 1 et 31.")
            print("entrez l'année complete, avec 4 nombres.")
            year = int(input("                 année :"))
            if 1930 < year < 2100:
                pass
            else:
                print("ERREUR, veuillez entrer l'année complete.")
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
            print("\nERREUR , veuillez entrer des chiffres")
            print("Veuillez recommencer\n")


def print_add_player():
    ''' function requesting the creation of a new player
        following a player creation and this as long as the users
        wants by answering yes '''

    serialized_player = []
    serialized_player.append(print_elements_player())
    print("voulez vous ajouter un autre joueur ?")
    reponse = clean_input(input())
    while reponse == "oui":
        serialized_player.append(print_elements_player())
        print("voulez vous ajouter un autre joueur ?")
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


def print_modif_player(player):
    ''' function displaying all the elements of a player and
        allowing to retrieve the possible change and return a dictionary
        with these elements '''

    print("modifiez les valeurs que vous désirez à la "
          "suite de la valeur renseignée .")
    print("ou tapez ENTRER pour passer . \n")
    a = clean_input(input("nom :" + player.get("name") + " -> "))
    if not a == "":
        player.update({"name": a})
        print("nouveau nom : " + player.get("name") + "\n")
    b = clean_input(input("prénom :" + player.get("first_name") + " -> "))
    if not b == "":
        player.update({"first_name": b})
        print("nouveau prénom : " + player.get("first_name") + "\n")
    print("né.e le " + player.get("birth_date") + " , tapez oui pour modifer ->")
    reponse = clean_input(input())
    if reponse == "oui":
        c = print_date_controller()
    else:
        c = ""
    if c == player.get("birth_date"):
        player.update({"birth_date": c})
        print("nouvelle date de naissance : "
              + player.get("birth_date") + "\n")
    print("sex : " + player.get("sex") + " , tapez oui pour modifier ->")
    reponse == clean_input(input())
    if reponse == "oui":
        d = print_sex_control()
    else:
        d = ""
    if d == player.get("sex"):
        player.update({"sex": d})
        print("sex redéfini : " + player.get("sex") + "\n")
    print("total des points : " + str(player.get("ranking")) +
          " , tapez oui pour modifier -> ")
    reponse = clean_input(input())
    ranking = player.get("ranking")
    if reponse == "oui":
        while ranking != int:
            try:
                nb = int(input(": "))
                ranking = nb
                break
            except ValueError:
                print("\nERREUR , veuillez entrer un nombre entier")
                print("recomencer")
    print(ranking)
    if not ranking == int(player.get("ranking")):
        player.update({"ranking": ranking})
        print("nouveau total de points : " + str(player.get("ranking")) + "\n")
    print()
    return player


def print_display_player_list(player):
    ''' printing a list of players with the same name '''

    print(player.get("name"), player.get("first_name"))
    print("son ID est : ", player.get("pk"), "\n")


def print_display_player_nb(nb_player, player):
    ''' print the number of existing players for the search then return
        to the menu to make a new request with ID '''

    print("il y a ", nb_player, " resultat pour la recherche : ", player)
    print("veuillez utiliser ID du joueur ")
